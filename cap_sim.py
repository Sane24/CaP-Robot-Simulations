"""
cap_sim.py  -- no-GPU MuJoCo tabletop sim + Code-as-Policies primitive shims.

Purpose: actually EXECUTE a generated CaP policy against ground truth,
so "the model wrote a check" becomes "the check is correct / wrong at runtime."

Two checks are deliberately distinguished:
  - is_obj_visible(name)  : OCCLUSION-FRAGILE. Models a top-down camera + segmenter.
                            An object resting inside a bowl (top below the rim) is
                            reported NOT visible. This is the prompted-verification
                            predicate from Run 4 that false-alarms after in-bowl placement.
  - is_placed(a, b)       : GROUND TRUTH. Reads real body poses from the sim. This is
                            the correct check you put *inside* a primitive.

To swap in your own robosuite prototype instead of this sim: implement the same
five methods (get_obj_names, get_obj_pos, put_first_on_second, is_obj_visible,
is_placed) against your env's mujoco data, and build_namespace() works unchanged.
"""
import mujoco, numpy as np

# default scene = your Run 3 scene
DEFAULT_SCENE = {
    "blocks": {  # name: (x, y)
        "blue block":  (0.00, -0.10),
        "green block": (0.00,  0.10),
    },
    "bowls": {   # name: (x, y)
        "yellow bowl": (0.30, -0.15),
        "green bowl":  (0.30,  0.00),
        "red bowl":    (0.30,  0.15),
    },
}
COLORS = {"blue": "0.1 0.1 0.9", "green": "0.1 0.8 0.1", "yellow": "0.9 0.9 0.1",
          "red": "0.9 0.1 0.1", "orange": "0.9 0.5 0.1", "purple": "0.6 0.1 0.8"}
BLOCK_HALF = 0.02      # 4 cm cubes
BOWL_HW    = 0.05      # 10 cm bowl footprint
BOWL_RIM   = 0.05      # 5 cm rim -> a 4 cm cube inside sits below the rim


def _col(name):
    return COLORS.get(name.split()[0], "0.5 0.5 0.5")


def make_scene(n_blocks=2, n_bowls=3):
    """Build a bigger tabletop. Up to 4 blocks and 4 bowls.
    Use this when long multi-step tasks need more objects:
        TabletopSim(make_scene(n_blocks=4, n_bowls=4))
    """
    bnames = ["blue block", "green block", "red block", "yellow block"][:n_blocks]
    wnames = ["yellow bowl", "green bowl", "red bowl", "blue bowl"][:n_bowls]
    blocks = {n: (0.00, -0.18 + 0.12 * i) for i, n in enumerate(bnames)}
    bowls = {n: (0.32, -0.18 + 0.12 * i) for i, n in enumerate(wnames)}
    return {"blocks": blocks, "bowls": bowls}


class TabletopSim:
    def __init__(self, scene=DEFAULT_SCENE):
        self.scene = scene
        self.blocks = dict(scene["blocks"])
        self.bowls = dict(scene["bowls"])
        self.transcript = []
        self._build()

    def _build(self):
        wall_t = 0.006
        parts = ['<geom name="floor" type="plane" size="2 2 0.1" rgba="0.85 0.85 0.85 1"/>']
        for name, (x, y) in self.bowls.items():
            c = _col(name)
            b = f'<body name="{name}" pos="{x} {y} 0">'
            b += f'<geom type="box" size="{BOWL_HW} {BOWL_HW} 0.004" pos="0 0 0.004" rgba="{c} 1"/>'
            for sx, sy, ex, ey in [(BOWL_HW, 0, wall_t, BOWL_HW), (-BOWL_HW, 0, wall_t, BOWL_HW),
                                   (0, BOWL_HW, BOWL_HW, wall_t), (0, -BOWL_HW, BOWL_HW, wall_t)]:
                b += (f'<geom type="box" size="{ex} {ey} {BOWL_RIM/2}" '
                      f'pos="{sx} {sy} {BOWL_RIM/2}" rgba="{c} 0.55"/>')
            parts.append(b + "</body>")
        for name, (x, y) in self.blocks.items():
            parts.append(f'<body name="{name}" pos="{x} {y} {BLOCK_HALF}"><freejoint/>'
                         f'<geom name="{name}_g" type="box" size="{BLOCK_HALF} {BLOCK_HALF} {BLOCK_HALF}" '
                         f'rgba="{_col(name)} 1" mass="0.05"/></body>')
        xml = (f'<mujoco><option gravity="0 0 -9.81" timestep="0.002"/>'
               f'<worldbody>{"".join(parts)}</worldbody></mujoco>')
        self.m = mujoco.MjModel.from_xml_string(xml)
        self.d = mujoco.MjData(self.m)
        mujoco.mj_forward(self.m, self.d)

    # ---- low level ----
    def _bid(self, n): return mujoco.mj_name2id(self.m, mujoco.mjtObj.mjOBJ_BODY, n)
    def pos(self, n):  return self.d.xpos[self._bid(n)].copy()

    def _settle(self, n=600):
        for _ in range(n):
            mujoco.mj_step(self.m, self.d)

    def _set_block(self, name, xyz):
        j = self.m.body_jntadr[self._bid(name)]
        q = self.m.jnt_qposadr[j]
        self.d.qpos[q:q+3] = xyz
        self.d.qpos[q+3:q+7] = [1, 0, 0, 0]
        self.d.qvel[self.m.body_dofadr[self._bid(name)]:
                    self.m.body_dofadr[self._bid(name)]+6] = 0
        mujoco.mj_forward(self.m, self.d)

    # ---- CaP primitives (the robot's vocabulary) ----
    def get_obj_names(self):
        return list(self.blocks) + list(self.bowls)

    def get_obj_pos(self, name):
        return self.pos(name)

    def say(self, msg):
        self.transcript.append(msg)
        print(f"robot says: {msg}")

    def put_first_on_second(self, a, b, _miss=False):
        """Drop block a into/onto target b and let physics settle.
        _miss=True offsets the drop so it lands beside the bowl (simulated missed grasp)."""
        if a not in self.blocks:
            return
        t = self.pos(b)
        off = np.array([0.09, 0.0, 0.0]) if _miss else np.array([0.0, 0.0, 0.0])
        drop = t + off + np.array([0.0, 0.0, 0.14])
        self._set_block(a, drop)
        self._settle()

    def stack_objects_in_order(self, object_names):
        for lower, upper in zip(object_names[:-1], object_names[1:]):
            self.put_first_on_second(upper, lower)

    def is_obj_visible(self, name):
        """OCCLUSION-FRAGILE top-down visibility. False if inside a bowl below its rim,
        or if the object is not in the scene at all."""
        if name not in self.get_obj_names():
            return False
        p = self.pos(name)
        for bowl in self.bowls:
            bp = self.pos(bowl)
            if abs(p[0]-bp[0]) < BOWL_HW and abs(p[1]-bp[1]) < BOWL_HW:
                if p[2] + BLOCK_HALF < BOWL_RIM:       # top below rim -> occluded
                    return False
        return True

    # ---- GROUND TRUTH (correct check, lives inside primitives in TODO 3) ----
    def is_placed(self, a, b):
        if a not in self.blocks:
            return False
        p, bp = self.pos(a), self.pos(b)
        if b in self.bowls:                            # contained in bowl
            return (abs(p[0]-bp[0]) < BOWL_HW and abs(p[1]-bp[1]) < BOWL_HW
                    and 0 < p[2] < BOWL_RIM)
        return (abs(p[0]-bp[0]) < 0.03 and abs(p[1]-bp[1]) < 0.03   # stacked on block
                and p[2] > bp[2] + BLOCK_HALF)

    # ---- planning-helper stubs (deterministic, no 2nd LLM call) ----
    def parse_obj_name(self, desc, ctx=None):
        d = desc.lower()
        if "block" in d and ("blocks" in d or d.strip() in ("the blocks", "blocks")):
            return list(self.blocks)
        if "bowl" in d and ("bowls" in d or d.strip() in ("the bowls", "bowls")):
            return list(self.bowls)
        for n in self.get_obj_names():                 # specific object
            if n in d:
                return n
        return ""                                      # absent -> falsy

    def parse_question(self, q, ctx=None):
        names = [n for n in self.get_obj_names() if n in q.lower()]
        if "left of" in q.lower() and len(names) >= 2:
            return self.pos(names[0])[1] < self.pos(names[1])[1]
        return False

    def get_corner_name(self, pos): return "middle"
    def get_side_name(self, pos):   return "middle"


def build_namespace(env):
    """Expose env methods as the free functions a CaP policy expects to call."""
    return {
        "get_obj_names": env.get_obj_names,
        "get_obj_pos": env.get_obj_pos,
        "say": env.say,
        "put_first_on_second": env.put_first_on_second,
        "stack_objects_in_order": env.stack_objects_in_order,
        "is_obj_visible": env.is_obj_visible,
        "is_placed": env.is_placed,             # ground-truth, for say_verified
        "parse_obj_name": env.parse_obj_name,
        "parse_question": env.parse_question,
        "get_corner_name": env.get_corner_name,
        "get_side_name": env.get_side_name,
        "np": np,
    }
