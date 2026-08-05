"""
household_shim.py -- shims for RoboSuite's PickPlace family + Lift (Panda arm).

HouseholdTabletop: PickPlace / PickPlaceCan / PickPlaceMilk / PickPlaceCereal etc.
  Real household objects (milk, bread, cereal, can) picked from a source bin and
  placed into their target bin slot. Ground truth = robosuite's own
  env.objects_in_bins flags (object must sit DOWN INSIDE the walled bin --
  native occlusion). Single-object variants park unused objects at (10,10,~10);
  get_obj_names() filters those out so policies only see what's on the table.

LiftTabletop: the Lift env (one cube). CaP's vocabulary has no hold-in-air
  primitive, so ground truth is "the cube's peak height during execution
  exceeded table + 4cm" (robosuite Lift's own threshold), tracked every step.
  DECISION: peak-based rather than end-state, because put_first_on_second
  necessarily sets the object down at the end; documented in DECISIONS.md.

Grasp heights are per-object (validated 7/19): tall objects must be grasped
HIGH because the source bin's walls block a deep reach.
"""
import numpy as np, subprocess, shutil
import robosuite as suite
from robosuite.controllers import load_composite_controller_config

_SAY_BIN = shutil.which("say")

# validated per-object grasp z-offsets relative to the object's body origin
GRASP_DZ = {"milk": 0.020, "bread": 0.000, "cereal": 0.020, "can": -0.015}
REAL = {"milk": "Milk", "bread": "Bread", "cereal": "Cereal", "can": "Can"}


class _ArmBase:
    """shared closed-loop OSC + speech + transcript machinery"""

    def _eef(self):
        sid = self.env.sim.model.site_name2id("gripper0_right_grip_site")
        return self.env.sim.data.site_xpos[sid].copy()

    def _step(self, a):
        """One control step. render_every>1 skips the viewer sync on
        intermediate steps: robosuite calls viewer.update() inside EVERY
        env.step, and on macOS/mjpython that sync dominates wall time.
        Temporarily setting renderer to "mujoco" makes both render branches
        in MujocoEnv.step fall through without touching the viewer object."""
        self._k = getattr(self, "_k", 0) + 1
        if self.render and self.render_every > 1 and (self._k % self.render_every):
            keep = self.env.renderer
            self.env.renderer = "mujoco"          # skip this frame
            try:
                self.env.step(a)
            finally:
                self.env.renderer = keep
        else:
            self.env.step(a)
        self._after_step()

    def _after_step(self):
        pass

    def _osc_goto(self, target, grip, tol=0.007, max_steps=350, gain=8.0, patience=40):
        """CLOSED-LOOP: drive until within tol, budget exhausted, OR progress
        stalls. Stall detection matters: reaching into a bin, the fingers
        contact the object/wall and the eef physically cannot close the last
        few mm, which otherwise burns the whole budget (measured: 350 wasted
        steps of 675 on a single pick-place)."""
        target = np.asarray(target, dtype=float)
        best, since = np.inf, 0
        for _ in range(max_steps):
            d = float(np.linalg.norm(target - self._eef()))
            if d < tol:
                return True
            if d < best - 1e-4:
                best, since = d, 0
            else:
                since += 1
                if since >= patience:
                    return False                  # stuck: stop wasting steps
            err = target - self._eef()
            self._step(np.concatenate([np.clip(err * gain, -1, 1), [0, 0, 0], [grip]]))
        return False

    def _squeeze(self, grip, n=40):
        for _ in range(n):
            self._step(np.concatenate([np.zeros(6), [grip]]))

    def say(self, msg):
        self.transcript.append(msg)
        print(f"robot says: {msg}")
        if self.speak and _SAY_BIN:
            cmd = [_SAY_BIN, "-v", self.voice, msg]
            subprocess.run(cmd) if self.blocking_speech else subprocess.Popen(cmd)

    def hold(self, seconds):
        for _ in range(min(int(seconds * 50), 500)):
            self._step(np.concatenate([np.zeros(6), [0]]))

    def close(self):
        self.env.close()

    # ---- shared workspace geometry (top = +x, left = -y) ----
    def get_workspace_bounds(self):
        return (self._WS[0], self._WS[1], self._WS[2], self._WS[3])

    def get_corner_pos(self, corner):
        c = str(corner).lower()
        x_min, x_max, y_min, y_max = self.get_workspace_bounds()
        return np.array([x_max if "top" in c else x_min,
                         y_min if "left" in c else y_max])

    def get_side_pos(self, side):
        sd = str(side).lower()
        x_min, x_max, y_min, y_max = self.get_workspace_bounds()
        if "top" in sd:    return np.array([x_max, (y_min + y_max) / 2])
        if "bottom" in sd: return np.array([x_min, (y_min + y_max) / 2])
        if "left" in sd:   return np.array([(x_min + x_max) / 2, y_min])
        if "right" in sd:  return np.array([(x_min + x_max) / 2, y_max])
        return np.array([(x_min + x_max) / 2, (y_min + y_max) / 2])

    def is_at(self, a, pos, tol=0.07):
        p = self.get_obj_pos(a)
        q = np.asarray(pos, dtype=float).ravel()
        return bool(np.linalg.norm(np.asarray(p[:2]) - q[:2]) < tol)

    # planning stubs shared
    def parse_question(self, q, ctx=None):
        names = [n for n in self.get_obj_names() if n in q.lower()]
        if "left of" in q.lower() and len(names) >= 2:
            return self.get_obj_pos(names[0])[1] < self.get_obj_pos(names[1])[1]
        return False

    def get_corner_name(self, pos): return "middle"
    def get_side_name(self, pos): return "middle"


class HouseholdTabletop(_ArmBase):
    def __init__(self, env_name="PickPlace", robot="Panda", render=False,
                 verbose=True, speak=False, voice="Samantha", blocking_speech=True,
                 render_every=1):
        cfg = load_composite_controller_config(controller="BASIC")
        self.env = suite.make(env_name=env_name, robots=robot, controller_configs=cfg,
                              has_renderer=render, has_offscreen_renderer=False,
                              use_camera_obs=False, horizon=100000, ignore_done=True)
        self.env.reset()
        self.render, self.verbose = render, verbose
        self.render_every = max(1, int(render_every))
        self.speak, self.voice, self.blocking_speech = speak, voice, blocking_speech
        self.transcript = []
        self.last_failure_reason = None
        self._WS = (-0.10, 0.30, -0.50, 0.55)      # spans both bins

    def _pos_real(self, real_name):
        return self.env.sim.data.body_xpos[self.env.obj_body_id[real_name]].copy()

    def _present(self, real_name):
        """Near the table region. NOT just z<2: single-object variants park
        unused objects at (10,10,~10) with no support, so they FREE-FALL all
        episode and eventually pass z=2 going down -- a duration-dependent
        presence bug (an object 'reappeared' after ~6 sim seconds)."""
        p = self._pos_real(real_name)
        return abs(p[0]) < 1.0 and abs(p[1]) < 1.0 and 0.3 < p[2] < 2.0

    def get_obj_names(self):
        """only objects actually ON THE TABLE; '<name> bin' targets for each."""
        present = [f for f, r in REAL.items() if self._present(r)]
        return present + [f"{f} bin" for f in present]

    def get_obj_pos(self, name):
        n = name.replace(" bin", "")
        real = REAL.get(n)
        if real is None:
            return np.zeros(3)
        if name.endswith(" bin"):
            return self._pos_real("Visual" + real)     # the object's target slot
        return self._pos_real(real)

    def put_first_on_second(self, a, b, _miss=False):
        """a = object; b = '<obj> bin' / 'bin' / 'its bin' / position.
        Carries the object into ITS target bin slot (robosuite's per-object slot)."""
        self.last_failure_reason = None
        a = a.replace(" bin", "")
        real = REAL.get(a)
        if real is None or not self._present(real):
            return False
        p = self._pos_real(real)
        tgt = self._pos_real("Visual" + real)          # its assigned slot in bin2
        if isinstance(b, (list, tuple, np.ndarray)):
            tgt = np.array([b[0], b[1], 0.90])

        self._osc_goto(p + [0, 0, 0.17], -1)
        self._osc_goto(p + [0, 0, GRASP_DZ.get(a, 0.0)], -1, tol=0.005)
        self._squeeze(1, 45)
        z0 = self._pos_real(real)[2]
        self._osc_goto(p + [0, 0, 0.30], 1, tol=0.025)
        if self._pos_real(real)[2] - z0 < 0.05:
            self.last_failure_reason = "grasp_failed"
            if self.verbose: print(f"  [detected] grasp failed on {a}")
            self._squeeze(-1, 15)
            return False
        rel = tgt + (np.array([0.30, 0, 0.06]) if _miss else 0)
        self._osc_goto([rel[0], rel[1], tgt[2] + 0.24], 1, tol=0.025)
        self._osc_goto([rel[0], rel[1], tgt[2] + 0.08], 1, tol=0.025)
        self._squeeze(-1, 30)
        self._osc_goto([rel[0], rel[1], tgt[2] + 0.26], -1, tol=0.035)
        for _ in range(40):                       # settle (was 90; 40 is enough
            self._step(np.concatenate([np.zeros(6), [-1]]))   # for the object to come to rest)
        return True

    def stack_objects_in_order(self, object_names):
        for n in object_names:
            self.put_first_on_second(n, "bin")

    # ---- checks ----
    def is_placed(self, a, b=None):
        """GROUND TRUTH: robosuite's own objects_in_bins flag for object a."""
        a = a.replace(" bin", "")
        real = REAL.get(a)
        if real is None:
            return False
        self.env._check_success()                      # refreshes objects_in_bins
        return bool(self.env.objects_in_bins[self.env.object_to_id[a]])

    def is_in_bin(self, a):
        return self.is_placed(a)

    def is_obj_visible(self, name):
        """FRAGILE: an object down inside the walled bin is occluded from above."""
        n = name.replace(" bin", "")
        real = REAL.get(n)
        if real is None or not self._present(real):
            return False
        p = self._pos_real(real)
        bx, by = self.env.bin2_pos[0], self.env.bin2_pos[1]
        inside_bin2 = (abs(p[0]-bx) < 0.30 and abs(p[1]-by) < 0.30
                       and p[2] < self.env.bin2_pos[2] + 0.10)
        return not inside_bin2

    def check_success(self):
        return bool(self.env._check_success())

    def parse_obj_name(self, desc, ctx=None):
        d = desc.lower()
        objs = [n for n in self.get_obj_names() if not n.endswith(" bin")]
        if "object" in d or "everything" in d or ("all" in d and "bin" not in d):
            return objs
        for n in objs:
            if n in d:
                return n
        return ""

    def reset(self):
        self.env.reset(); self.transcript = []
        self.last_failure_reason = None
        _snap_initial(self)


class LiftTabletop(_ArmBase):
    def __init__(self, robot="Panda", render=False, verbose=True,
                 speak=False, voice="Samantha", blocking_speech=True,
                 render_every=1):
        cfg = load_composite_controller_config(controller="BASIC")
        self.env = suite.make(env_name="Lift", robots=robot, controller_configs=cfg,
                              has_renderer=render, has_offscreen_renderer=False,
                              use_camera_obs=False, horizon=100000, ignore_done=True)
        self.env.reset()
        self.render, self.verbose = render, verbose
        self.render_every = max(1, int(render_every))
        self.speak, self.voice, self.blocking_speech = speak, voice, blocking_speech
        self.transcript = []
        self.last_failure_reason = None
        self._WS = (-0.13, 0.19, -0.23, 0.23)      # the table
        self._bid = self.env.sim.model.body_name2id("cube_main")
        self.table_top = float(self.env.model.mujoco_arena.table_offset[2])
        self.peak_z = self._cube()[2]

    def _cube(self):
        return self.env.sim.data.body_xpos[self._bid].copy()

    def _after_step(self):
        z = self._cube()[2]
        if z > self.peak_z:
            self.peak_z = z

    def get_obj_names(self): return ["cube"]

    def get_obj_pos(self, name):
        return self._cube() if name == "cube" else np.zeros(3)

    def put_first_on_second(self, a, b, _miss=False):
        """pick the cube, LIFT it high, then set it down (at b if a position)."""
        if a != "cube":
            return False
        p = self._cube()
        self._osc_goto(p + [0, 0, 0.10], -1)
        self._osc_goto(p + [0, 0, 0.003], -1, tol=0.005)
        self._squeeze(1, 35)
        z0 = self._cube()[2]
        self._osc_goto(p + [0, 0, 0.25], 1, tol=0.02)   # the lift
        if self._cube()[2] - z0 < 0.05:
            self.last_failure_reason = "grasp_failed"
            self._squeeze(-1, 15)
            return False
        tgt = (np.array([b[0], b[1], self.table_top + 0.03])
               if isinstance(b, (list, tuple, np.ndarray)) else p)
        self._osc_goto([tgt[0], tgt[1], self.table_top + 0.05], 1, tol=0.01)
        self._squeeze(-1, 25)
        self._osc_goto([tgt[0], tgt[1], self.table_top + 0.20], -1, tol=0.03)
        return True

    def stack_objects_in_order(self, object_names): pass

    # ---- checks ----
    def was_lifted(self, name="cube"):
        """GROUND TRUTH: peak cube height exceeded table + 4cm at some point
        (robosuite Lift's own success threshold, applied to the peak)."""
        return bool(self.peak_z > self.table_top + 0.04)

    def is_placed(self, a, b=None):
        return self.was_lifted(a)

    def is_obj_visible(self, name): return name == "cube"

    def check_success(self):
        return bool(self.env._check_success())          # end-state version

    def parse_obj_name(self, desc, ctx=None):
        return "cube" if "cube" in desc.lower() or "block" in desc.lower() else ""

    def reset(self):
        self.env.reset(); self.transcript = []
        self.peak_z = self._cube()[2]
        _snap_initial(self)



def _snap_initial(env):
    env._initial_pos = {n: tuple(float(v) for v in env.get_obj_pos(n))
                        for n in env.get_obj_names()}


def _get_initial_pos(env, name):
    """Position at the START of the run. Lazy: snapshots on first access if
    reset() hasn't stamped one. Needed for relative commands ('move 5cm to the
    bottom'), which the final state alone cannot score."""
    import numpy as np
    if not hasattr(env, "_initial_pos"):
        _snap_initial(env)
    return np.array(env._initial_pos.get(name, (0.0, 0.0, 0.0)))

def build_namespace(env):
    from spatial import make_parse_position
    ns = {"get_initial_pos": (lambda n, _e=env: _get_initial_pos(_e, n)),
          "parse_position": make_parse_position(env),
          "get_workspace_bounds": env.get_workspace_bounds,
          "get_corner_pos": env.get_corner_pos, "get_side_pos": env.get_side_pos,
          "is_at": env.is_at,
          "get_obj_names": env.get_obj_names, "get_obj_pos": env.get_obj_pos,
          "say": env.say, "put_first_on_second": env.put_first_on_second,
          "stack_objects_in_order": env.stack_objects_in_order,
          "is_obj_visible": env.is_obj_visible, "is_placed": env.is_placed,
          "parse_obj_name": env.parse_obj_name, "parse_question": env.parse_question,
          "get_corner_name": env.get_corner_name, "get_side_name": env.get_side_name,
          "np": np}
    if hasattr(env, "is_in_bin"): ns["is_in_bin"] = env.is_in_bin
    if hasattr(env, "was_lifted"): ns["was_lifted"] = env.was_lifted
    return ns