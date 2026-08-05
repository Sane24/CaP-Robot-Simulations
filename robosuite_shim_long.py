"""
robosuite_shim_long.py -- shim for MultiBlock (N blocks + Panda arm).

  - N blocks instead of 2
  - put_first_on_second(block, [x, y])   place at a POSITION, not just on an object
  - workspace geometry: get_workspace_bounds, get_corner_pos, get_side_pos
  - is_at(block, [x, y])                 GROUND-TRUTH position check for say_verified

Top-down convention (matches parse_question in the T1-T5 shim):
  top = +x (far from the robot)   bottom = -x
  left = -y                       right = +y
"""
import numpy as np, subprocess, shutil
import robosuite as suite
from robosuite.controllers import load_composite_controller_config
import multiblock_env                     # registers env_name="MultiBlock"

_SAY_BIN = shutil.which("say")
HALF = 0.021
TABLE_Z = 0.80
WS = {"x": (-0.13, 0.19), "y": (-0.23, 0.23)}     # reachable region


class MultiBlockTabletop:
    def __init__(self, blocks=None, robot="Panda", render=False, verbose=True,
                 speak=False, voice="Samantha", blocking_speech=True,
                 render_every=1, env_name="MultiBlock"):
        cfg = load_composite_controller_config(controller="BASIC")
        self.env = suite.make(env_name=env_name, robots=robot,
                              controller_configs=cfg, block_names=blocks,
                              has_renderer=render, has_offscreen_renderer=False,
                              use_camera_obs=False, horizon=100000, ignore_done=True)
        self.env.reset()
        self.render, self.verbose = render, verbose
        self.render_every = max(1, int(render_every))
        self.speak, self.voice, self.blocking_speech = speak, voice, blocking_speech
        self.blocks = list(self.env.block_names)
        self.bowls = []
        self.transcript = []
        self.last_failure_reason = None
        self.history = []                   # post-action pose snapshots: L9-style
                                            # sequential truths need intermediates
        _snap_initial(self)                 # initial poses, for relative tasks

    # ---- low level ----
    def _pos(self, n):
        if n not in self.env.obj_body_id:
            return np.zeros(3)
        return self.env.sim.data.body_xpos[self.env.obj_body_id[n]].copy()

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

    # ---- geometry the LLM may call ----
    def get_workspace_bounds(self):
        """(x_min, x_max, y_min, y_max). top = +x, left = -y."""
        return (WS["x"][0], WS["x"][1], WS["y"][0], WS["y"][1])

    def get_corner_pos(self, corner):
        c = corner.lower()
        return np.array([WS["x"][1] if "top" in c else WS["x"][0],
                         WS["y"][0] if "left" in c else WS["y"][1]])

    def get_side_pos(self, side):
        s = side.lower()
        if "top" in s:    return np.array([WS["x"][1], 0.0])
        if "bottom" in s: return np.array([WS["x"][0], 0.0])
        if "left" in s:   return np.array([0.0, WS["y"][0]])
        if "right" in s:  return np.array([0.0, WS["y"][1]])
        return np.array([0.0, 0.0])

    def get_corner_name(self, pos):
        return ("top " if pos[0] > 0 else "bottom ") + \
               ("left" if pos[1] < 0 else "right") + " corner"

    def get_side_name(self, pos):
        return ("top side" if pos[0] > 0.08 else "bottom side" if pos[0] < -0.08
                else "left side" if pos[1] < 0 else "right side")

    # ---- CaP vocabulary ----
    def get_obj_names(self): return list(self.blocks)
    def get_obj_pos(self, n): return self._pos(n)

    def say(self, msg):
        self.transcript.append(msg)
        print(f"robot says: {msg}")
        if self.speak and _SAY_BIN:
            cmd = [_SAY_BIN, "-v", self.voice, msg]
            subprocess.run(cmd) if self.blocking_speech else subprocess.Popen(cmd)

    def put_first_on_second(self, a, b, _miss=False):
        """b = OBJECT NAME (stack on it) or POSITION [x, y] (place there)."""
        self.last_failure_reason = None
        if a not in self.blocks or (isinstance(b, str) and b not in self.blocks):
            self.last_failure_reason = "unknown_object"
            return False
        pa = self._pos(a)
        self._osc_goto(pa + [0, 0, 0.10], -1)
        self._osc_goto(pa + [0, 0, 0.004], -1, tol=0.005)
        self._squeeze(1, n=30)
        z0 = self._pos(a)[2]
        self._osc_goto(pa + [0, 0, 0.22], 1, tol=0.012)
        if self._pos(a)[2] - z0 < 0.05:
            self.last_failure_reason = "grasp_failed"
            if self.verbose: print("  [detected] grasp failed")
            self._squeeze(-1, n=15)
            return False

        if isinstance(b, str):
            pb = self._pos(b)
            rel = np.array([pb[0], pb[1], pb[2] + 2 * HALF + 0.012])
        else:
            b = np.asarray(b, dtype=float).ravel()
            rel = np.array([b[0], b[1], TABLE_Z + HALF + 0.012])
        if _miss:
            rel = rel + np.array([0.11, 0, 0.05])

        self._osc_goto(rel + [0, 0, 0.10], 1, tol=0.012)
        self._osc_goto(rel, 1, tol=0.009)
        self._squeeze(-1, n=25)
        self._osc_goto(rel + [0, 0, 0.13], -1, tol=0.02)
        for _ in range(50):
            self._step(np.concatenate([np.zeros(6), [-1]]))
        self.history.append({n: tuple(float(v) for v in self.get_obj_pos(n))
                             for n in self.blocks})
        return True

    def stack_objects_in_order(self, object_names):
        for lower, upper in zip(object_names[:-1], object_names[1:]):
            self.put_first_on_second(upper, lower)

    def hold(self, seconds):
        for _ in range(min(int(seconds * 50), 500)):
            self._step(np.concatenate([np.zeros(6), [0]]))

    def reset(self):
        self.env.reset(); self.transcript = []
        self.last_failure_reason = None; self._scene_snap = {}
        self.history = []
        _snap_initial(self)                 # initial poses, for relative tasks

    def close(self): self.env.close()

    # ---- checks ----
    def is_obj_visible(self, name):
        if name not in self.blocks: return False
        p = self._pos(name)
        for o in self.blocks:
            if o == name: continue
            q = self._pos(o)
            if abs(q[0]-p[0]) < 0.03 and abs(q[1]-p[1]) < 0.03 and q[2] > p[2]:
                return False
        return True

    def is_placed(self, a, b):
        """GROUND TRUTH: a stacked on b (b an object), or a at b (b a position)."""
        if a not in self.blocks: return False
        pa = self._pos(a)
        if isinstance(b, str):
            if b not in self.blocks: return False
            pb = self._pos(b)
            return bool(abs(pa[0]-pb[0]) < 0.035 and abs(pa[1]-pb[1]) < 0.035
                        and pa[2] > pb[2] + 0.015)
        return self.is_at(a, b)

    def is_at(self, a, pos, tol=0.06):
        """GROUND TRUTH: block a is within tol of position [x, y]."""
        if a not in self.blocks: return False
        p = self._pos(a); q = np.asarray(pos, dtype=float).ravel()
        return bool(np.linalg.norm(p[:2] - q[:2]) < tol)

    # ---- planning stubs ----
    def parse_obj_name(self, desc, ctx=None):
        """Resolve a description to object name(s) present in the scene.

        Plural forms return a LIST, singular a string. Groups are derived from
        the scene's own name suffixes ("bowl", "plate", "bin", ...), not a
        hardcoded block list: returning "" for 'the bowls' made a correct policy
        iterate over nothing, so it placed nothing and raised nothing -- a
        SILENT no-op that scored as a normal failed run and was invisible in the
        error counts. An unresolvable description still returns "" (the CaP
        behaviour a policy can test), but every group the scene actually
        contains now resolves."""
        d = str(desc).lower()
        scene = self.get_obj_names()

        # plural group words, longest first so "blocks" wins over "block"
        groups = {}
        for n in scene:
            head = n.split()[-1]                 # block / bowl / plate / bin
            groups.setdefault(head, []).append(n)
        for head, members in sorted(groups.items(), key=lambda kv: -len(kv[0])):
            if head + "s" in d or (head in d and "all" in d):
                return list(members)

        # exact name match ("the red bowl")
        for n in sorted(scene, key=len, reverse=True):
            if n in d:
                return n
        # colour + group ("the red one" style is out of scope, but "red bowl"
        # written as "red  bowl" or "bowl that is red" is not worth guessing)
        return ""

    def parse_question(self, q, ctx=None):
        names = [n for n in self.blocks if n in q.lower()]
        if "left of" in q.lower() and len(names) >= 2:
            return self._pos(names[0])[1] < self._pos(names[1])[1]
        return False



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


class BowlsTabletop(MultiBlockTabletop):
    """BlockBowls scene: 3 colored blocks + 3 colored bowls (fixed spots).
    Blocks match the bowl colors 1:1 so 'non-matching colors' (CaP B+B #4) has
    a clean derangement; a 4th block would make 'every block in a bowl'
    unsatisfiable with 3 bowls. Bowls are TARGETS only (never grasped).
    Placement into a bowl releases above the rim and lets the block drop in."""

    def __init__(self, **kw):
        kw.setdefault("env_name", "BlockBowls")
        kw.setdefault("blocks", ["red block", "green block", "blue block"])
        super().__init__(**kw)

    def get_obj_names(self):
        return list(self.blocks) + [n for n in self.env.obj_body_id
                                    if n.endswith(" bowl")]

    def is_bowl(self, name):
        return isinstance(name, str) and name.endswith(" bowl")

    def put_first_on_second(self, a, b, _miss=False):
        import multiblock_env as ME
        if not self.is_bowl(b):
            return super().put_first_on_second(a, b, _miss=_miss)
        if a not in self.blocks:
            self.last_failure_reason = "unknown_object"
            return False
        bp = self._pos(b)
        rim = bp[2] + ME.BOWL_H
        pa = self._pos(a)
        self._osc_goto(pa + [0, 0, 0.10], -1)
        self._osc_goto(pa + [0, 0, 0.002], -1, tol=0.005)
        self._squeeze(1, 35)
        z0 = self._pos(a)[2]
        self._osc_goto(pa + [0, 0, 0.22], 1, tol=0.02)
        if self._pos(a)[2] - z0 < 0.05:
            self.last_failure_reason = "grasp_failed"
            self._squeeze(-1, 15)
            return False
        tgt = bp + (np.array([0.12, 0, 0]) if _miss else 0)
        self._osc_goto([tgt[0], tgt[1], rim + 0.12], 1, tol=0.015)
        self._osc_goto([tgt[0], tgt[1], rim + 0.055], 1, tol=0.012)
        self._squeeze(-1, 30)                        # drop into the cavity
        self._osc_goto([tgt[0], tgt[1], rim + 0.20], -1, tol=0.03)
        for _ in range(40):
            self._step(np.concatenate([np.zeros(6), [-1]]))
        return True

    def is_in_bowl(self, block, bowl=None):
        """GROUND TRUTH: block inside a bowl cavity -- xy within the inner
        radius, z below rim + one block height (a cube resting on another
        cube inside still counts)."""
        import multiblock_env as ME
        if block not in self.blocks:
            return False
        p = self._pos(block)
        bowls = [bowl] if bowl else [n for n in self.get_obj_names()
                                     if self.is_bowl(n)]
        for bn in bowls:
            bp = self._pos(bn)
            if (np.linalg.norm(p[:2] - bp[:2]) < ME.BOWL_R_IN - 0.006
                    and p[2] < bp[2] + ME.BOWL_H + 0.07):
                return bn
        return False

    def is_placed(self, a, b=None):
        if self.is_bowl(b):
            return bool(self.is_in_bowl(a, b))
        return super().is_placed(a, b)


def build_namespace(env):
    from spatial import make_parse_position, transform_shape_pts
    ns0 = {"get_initial_pos": (lambda n, _e=env: _get_initial_pos(_e, n)),
           "transform_shape_pts": transform_shape_pts}
    if hasattr(env, "is_in_bowl"):
        ns0["is_in_bowl"] = env.is_in_bowl
    if hasattr(env, "is_on_plate"):
        ns0["is_on_plate"] = env.is_on_plate
    return {**ns0, "parse_position": make_parse_position(env),
            "get_obj_names": env.get_obj_names, "get_obj_pos": env.get_obj_pos,
            "say": env.say, "put_first_on_second": env.put_first_on_second,
            "stack_objects_in_order": env.stack_objects_in_order,
            "is_obj_visible": env.is_obj_visible, "is_placed": env.is_placed,
            "is_at": env.is_at, "parse_obj_name": env.parse_obj_name,
            "parse_question": env.parse_question,
            "get_corner_pos": env.get_corner_pos, "get_side_pos": env.get_side_pos,
            "get_corner_name": env.get_corner_name, "get_side_name": env.get_side_name,
            "get_workspace_bounds": env.get_workspace_bounds, "np": np}


FRUIT_GRASP_DZ = {"lemon": 0.000, "bottle": 0.035}   # tuned: 0.000 grasps the settled center; higher misses
CATEGORIES = {"fruit": ["lemon"], "fruits": ["lemon"],
              "bottle": ["bottle"], "bottles": ["bottle"]}


class FruitPlatesTabletop(MultiBlockTabletop):
    """CaP Fruits #4 scene, adapted (see FruitPlates env docstring). Graspables:
    lemon (low grasp: squat ellipsoid, top +0.02) and bottle (grasp HIGH on the
    neck: tall, top +0.075). Plates are shallow dish targets, never grasped."""

    SETTLE = 30        # ellipsoids bounce/roll after the spawn drop; blocks
                       # settle instantly but a lemon read too early is ~2.5cm
                       # high, which aims the grasp above the fruit entirely

    def __init__(self, **kw):
        kw.setdefault("env_name", "FruitPlates")
        super().__init__(**kw)
        self._settle()

    def _settle(self):
        for _ in range(self.SETTLE):
            self._step(np.concatenate([np.zeros(6), [-1]]))

    def reset(self):
        super().reset()
        self._settle()

    def get_obj_names(self):
        return list(self.blocks) + [n for n in self.env.obj_body_id
                                    if n.endswith(" plate")]

    def parse_obj_name(self, desc, ctx=None):
        d = str(desc).lower()
        for cat, members in CATEGORIES.items():
            if cat in d:
                return [m for m in members if m in self.blocks]
        return super().parse_obj_name(desc, ctx)

    def put_first_on_second(self, a, b, _miss=False):
        """blocks routine adapted: per-object grasp height; plate targets
        release low above the dish."""
        self.last_failure_reason = None
        if a not in self.blocks:
            self.last_failure_reason = "unknown_object"
            return False
        pa = self._pos(a)
        if isinstance(b, str):
            if b.endswith(" plate"):
                q = self._pos(b)
                rel = np.array([q[0], q[1], q[2] + 0.075])
            elif b in self.blocks:
                q = self._pos(b)
                rel = np.array([q[0], q[1], q[2] + 0.06])
            else:
                self.last_failure_reason = "unknown_object"
                return False
        else:
            bq = np.asarray(b, dtype=float).ravel()
            rel = np.array([bq[0], bq[1], TABLE_Z + 0.05])
        if _miss:
            rel = rel + np.array([0.11, 0, 0.05])

        dz = FRUIT_GRASP_DZ.get(a, 0.0)
        self._osc_goto(pa + [0, 0, 0.18], -1)
        self._osc_goto([pa[0], pa[1], pa[2] + dz], -1, tol=0.005)
        self._squeeze(1, n=45)
        z0 = self._pos(a)[2]
        self._osc_goto([pa[0], pa[1], pa[2] + 0.30], 1, tol=0.03)
        if self._pos(a)[2] - z0 < 0.05:
            self.last_failure_reason = "grasp_failed"
            if self.verbose: print("  [detected] grasp failed")
            self._squeeze(-1, n=15)
            return False
        self._osc_goto([rel[0], rel[1], rel[2] + 0.12], 1, tol=0.03)
        self._osc_goto(rel, 1, tol=0.02)
        self._squeeze(-1, n=30)
        self._osc_goto([rel[0], rel[1], rel[2] + 0.15], -1, tol=0.04)
        for _ in range(40):
            self._step(np.concatenate([np.zeros(6), [-1]]))
        self.history.append({n: tuple(float(v) for v in self.get_obj_pos(n))
                             for n in self.blocks})
        return True

    def is_on_plate(self, obj, plate=None):
        """GROUND TRUTH: obj within the dish radius, resting at dish height."""
        if obj not in self.blocks:
            return False
        p = self._pos(obj)
        plates = [plate] if plate else [n for n in self.env.obj_body_id
                                        if n.endswith(" plate")]
        for pl in plates:
            q = self._pos(pl)
            if (np.linalg.norm(p[:2] - q[:2]) < 0.062 and p[2] < q[2] + 0.09):
                return pl
        return False

    def is_placed(self, a, b=None):
        if isinstance(b, str) and b.endswith(" plate"):
            return bool(self.is_on_plate(a, b))
        return super().is_placed(a, b)