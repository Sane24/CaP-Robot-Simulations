"""
robosuite_shim.py -- CaP vocabulary on a RoboSuite Panda arm (Stack env, 2 cubes).

RoboSuite Stack: cubeA is RED, cubeB is GREEN.

  mjpython robosuite_shim.py --render          watch a pick-place
  mjpython robosuite_shim.py --render --fail   watch it deliberately miss
  python3  robosuite_shim.py                   headless
"""
import numpy as np
import subprocess, shutil
import robosuite as suite
from robosuite.controllers import load_composite_controller_config

_SAY_BIN = shutil.which("say")        # macOS built-in TTS; None elsewhere

NAME_MAP = {"red block": "cubeA_main", "green block": "cubeB_main",
            "cubeA": "cubeA_main", "cubeB": "cubeB_main"}


class RoboSuiteTabletop:
    def __init__(self, env_name="Stack", robot="Panda", render=False, verbose=True,
                 speak=False, voice="Samantha", blocking_speech=True,
                 render_every=1):
        cfg = load_composite_controller_config(controller="BASIC")
        self.env = suite.make(env_name=env_name, robots=robot, controller_configs=cfg,
                              has_renderer=render, has_offscreen_renderer=False,
                              use_camera_obs=False, horizon=100000, ignore_done=True)
        self.env.reset()
        self.render = render
        self.render_every = max(1, int(render_every))
        self.verbose = verbose
        self.speak = speak
        self.voice = voice
        self.blocking_speech = blocking_speech
        self.transcript = []
        self.blocks = ["red block", "green block"]
        self.bowls = []
        self.last_failure_reason = None

    # ---- low level ----
    def _body(self, name):
        return NAME_MAP.get(name, name)

    def _known(self, name):
        return isinstance(name, str) and self._body(name) in ("cubeA_main", "cubeB_main")

    def _pos(self, name):
        if not self._known(name):
            return np.zeros(3)                 # unknown object: no position
        bid = self.env.sim.model.body_name2id(self._body(name))
        return self.env.sim.data.body_xpos[bid].copy()

    def _eef(self):
        sid = self.env.sim.model.site_name2id("gripper0_right_grip_site")
        return self.env.sim.data.site_xpos[sid].copy()

    def _step(self, action):
        """render_every>1 skips the viewer sync on intermediate steps (robosuite
        calls viewer.update() inside every env.step; on macOS that dominates)."""
        self._k = getattr(self, "_k", 0) + 1
        if self.render and getattr(self, "render_every", 1) > 1 and (self._k % self.render_every):
            keep = self.env.renderer
            self.env.renderer = "mujoco"
            try:
                self.env.step(action)
            finally:
                self.env.renderer = keep
        else:
            self.env.step(action)

    def _osc_goto(self, target, grip, tol=0.006, max_steps=250, gain=8.0, patience=40):
        """CLOSED-LOOP: drive until within tol, budget exhausted, or progress stalls."""
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
                    return False
            err = target - self._eef()
            self._step(np.concatenate([np.clip(err * gain, -1, 1), [0, 0, 0], [grip]]))
        return False

    def _squeeze(self, grip, n=25):
        for _ in range(n):
            self._step(np.concatenate([np.zeros(6), [grip]]))

    # ---- CaP vocabulary ----
    def get_obj_names(self):
        return list(self.blocks)

    def get_obj_pos(self, name):
        return self._pos(name)

    def say(self, msg):
        """A blind user HEARS this. Speaks aloud when speak=True (macOS `say`)."""
        self.transcript.append(msg)
        print(f"robot says: {msg}")
        if self.speak and _SAY_BIN:
            cmd = [_SAY_BIN, "-v", self.voice, msg]
            subprocess.run(cmd) if self.blocking_speech else subprocess.Popen(cmd)

    def put_first_on_second(self, a, b, _miss=False):
        """Scripted pick-place with convergence + grasp verification.
        _miss=True releases 12cm off-target (controlled failure injection).
        b may be an OBJECT NAME (stack on it) or a POSITION [x, y] (place there).
        Unknown a or b -> fail gracefully (last_failure_reason='unknown_object'),
        never crash: a policy that references a nonexistent object gets a failed
        action, which is the realistic outcome and lets the rest of the policy
        keep executing (so its final claim can be scored)."""
        self.last_failure_reason = None
        to_position = not isinstance(b, str)          # b is [x, y] coordinates
        if not self._known(a) or (not to_position and not self._known(b)):
            self.last_failure_reason = "unknown_object"
            if self.verbose:
                print(f"  [no-op] unknown object in put_first_on_second({a!r}, {b!r})")
            return False
        pa = self._pos(a)

        reached = self._osc_goto(pa + [0, 0, 0.10], -1)          # above, open
        if not reached and self.verbose:
            print("  [warn] approach did not converge")
        self._osc_goto(pa + [0, 0, 0.005], -1, tol=0.005)        # descend to cube
        self._squeeze(1, n=30)                                   # CLOSE gripper

        z_before = self._pos(a)[2]
        self._osc_goto(pa + [0, 0, 0.20], 1, tol=0.01)           # lift
        if self._pos(a)[2] - z_before < 0.05:                    # cube did not lift
            self.last_failure_reason = "grasp_failed"
            if self.verbose:
                print("  [detected] grasp failed, cube did not lift")
            self._squeeze(-1, n=15)
            return False

        if to_position:
            bq = np.asarray(b, dtype=float).ravel()
            rel = np.array([bq[0], bq[1], self.TABLE_Z + 0.032])
        else:
            pb = self._pos(b)
            rel = pb + (np.array([0.12, 0, 0.06]) if _miss else np.array([0, 0, 0.055]))
        if to_position and _miss:
            rel = rel + np.array([0.12, 0, 0.06])
        self._osc_goto(rel + [0, 0, 0.10], 1, tol=0.01)          # over target
        self._osc_goto(rel, 1, tol=0.008)                        # descend
        self._squeeze(-1, n=25)                                  # RELEASE
        self._osc_goto(rel + [0, 0, 0.12], -1, tol=0.02)         # retreat
        for _ in range(60):                                      # settle
            self._step(np.concatenate([np.zeros(6), [-1]]))
        return True

    def stack_objects_in_order(self, object_names):
        for lower, upper in zip(object_names[:-1], object_names[1:]):
            self.put_first_on_second(upper, lower)

    def hold(self, seconds):
        """for pause_for_verification: hold still, gripper unchanged."""
        for _ in range(min(int(seconds * 50), 500)):
            self._step(np.concatenate([np.zeros(6), [0]]))

    def reset(self):
        """Re-randomize the scene WITHOUT tearing down the window."""
        self.env.reset()
        self.transcript = []
        _snap_initial(self)
        self.last_failure_reason = None
        self._scene_snap = {}

    # ---- checks ----
    def is_obj_visible(self, name):
        """FRAGILE check: 'occluded' only if another block sits on top of it.
        Cannot tell 'placed correctly' from 'on the table nearby'."""
        if name not in self.blocks:
            return False
        p = self._pos(name)
        for other in self.blocks:
            if other == name:
                continue
            q = self._pos(other)
            if abs(q[0] - p[0]) < 0.03 and abs(q[1] - p[1]) < 0.03 and q[2] > p[2]:
                return False
        return True

    # ---- workspace geometry (same convention as the MultiBlock shim:
    #      top = +x far from the robot, left = -y) ----
    WS = {"x": (-0.13, 0.19), "y": (-0.23, 0.23)}
    TABLE_Z = 0.80

    def get_workspace_bounds(self):
        return (self.WS["x"][0], self.WS["x"][1], self.WS["y"][0], self.WS["y"][1])

    def get_corner_pos(self, corner):
        c = str(corner).lower()
        return np.array([self.WS["x"][1] if "top" in c else self.WS["x"][0],
                         self.WS["y"][0] if "left" in c else self.WS["y"][1]])

    def get_side_pos(self, side):
        sd = str(side).lower()
        if "top" in sd:    return np.array([self.WS["x"][1], 0.0])
        if "bottom" in sd: return np.array([self.WS["x"][0], 0.0])
        if "left" in sd:   return np.array([0.0, self.WS["y"][0]])
        if "right" in sd:  return np.array([0.0, self.WS["y"][1]])
        return np.array([0.0, 0.0])

    def is_at(self, a, pos, tol=0.06):
        """GROUND TRUTH: block a within tol of position [x, y]."""
        if not self._known(a): return False
        p = self._pos(a)
        q = np.asarray(pos, dtype=float).ravel()
        return bool(np.linalg.norm(p[:2] - q[:2]) < tol)

    def is_placed(self, a, b):
        """GROUND TRUTH from real MuJoCo poses. Unknown names -> False, never
        crash. b as a position [x, y] delegates to is_at."""
        if not isinstance(b, str):
            return self.is_at(a, b)
        if not self._known(a) or not self._known(b):
            return False
        if a not in self.blocks:
            return False
        pa, pb = self._pos(a), self._pos(b)
        return bool(abs(pa[0] - pb[0]) < 0.035 and abs(pa[1] - pb[1]) < 0.035
                    and pa[2] > pb[2] + 0.015)

    def check_success(self):
        return bool(self.env._check_success())

    def close(self):
        self.env.close()

    # ---- planning stubs ----
    def parse_obj_name(self, desc, ctx=None):
        d = desc.lower()
        if "blocks" in d:
            return list(self.blocks)
        if "bowls" in d:
            return list(self.bowls)
        for n in self.blocks + self.bowls:
            if n in d:
                return n
        return ""

    def parse_question(self, q, ctx=None):
        names = [n for n in self.get_obj_names() if n in q.lower()]
        if "left of" in q.lower() and len(names) >= 2:
            return self._pos(names[0])[1] < self._pos(names[1])[1]
        return False

    def get_corner_name(self, pos):
        return "middle"

    def get_side_name(self, pos):
        return "middle"



def _snap_initial(env):
    env._initial_pos = {n: tuple(float(v) for v in env.get_obj_pos(n))
                        for n in env.get_obj_names()}


def _get_initial_pos(env, name):
    """Position of `name` at the START of the run (after the last reset).
    Needed for relative commands: 'move the red block 5cm to the bottom' is
    scored against where the block WAS, which the final state alone cannot give.
    Lazy: snapshots on first access if reset() hasn't stamped one yet."""
    import numpy as np
    if not hasattr(env, "_initial_pos"):
        _snap_initial(env)
    return np.array(env._initial_pos.get(name, (0.0, 0.0, 0.0)))


def build_namespace(env):
    ns0 = {"get_initial_pos": (lambda n, _e=env: _get_initial_pos(_e, n))}
    from spatial import make_parse_position
    return {**ns0, "parse_position": make_parse_position(env),
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


if __name__ == "__main__":
    import sys
    render = "--render" in sys.argv
    fail = "--fail" in sys.argv
    env = RoboSuiteTabletop(render=render)
    print("objects:", env.get_obj_names())
    print("before: is_placed(red on green):", env.is_placed("red block", "green block"))
    env.put_first_on_second("red block", "green block", _miss=fail)
    print("after : is_placed(red on green):", env.is_placed("red block", "green block"))
    print("robosuite _check_success():", env.check_success())
    if env.last_failure_reason:
        print("failure reason:", env.last_failure_reason)