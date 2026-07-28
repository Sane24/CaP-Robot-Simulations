"""
capx_env.py -- custom RoboSuite env with N colored cubes (not just 2).

RoboSuite's Stack env ships exactly two cubes and no bowls. This subclasses it
and swaps in an arbitrary set of colored cubes so longer multi-step tasks have
enough objects to be interesting.

    register_capx_env()                  # call once, before suite.make
    suite.make(env_name="CaPTabletop", ...)

Colors/sizes are declared in BLOCKS. Bowls are NOT here: RoboSuite has no bowl
primitive. Use cap_sim (custom MuJoCo) when you need bowls + occlusion.
"""
import numpy as np
from robosuite.environments.manipulation.stack import Stack
from robosuite.models.objects import BoxObject
from robosuite.models.arenas import TableArena
from robosuite.models.tasks import ManipulationTask
from robosuite.utils.mjcf_utils import CustomMaterial
from robosuite.utils.placement_samplers import UniformRandomSampler
import robosuite as suite
from robosuite.environments.base import register_env

# name -> (rgba, half-size, wood texture)
BLOCKS = {
    "cubeA": ([1, 0, 0, 1],   0.020, "WoodRed"),      # red
    "cubeB": ([0, 1, 0, 1],   0.025, "WoodGreen"),    # green
    "cubeC": ([0, 0, 1, 1],   0.020, "WoodBlue"),     # blue
    "cubeD": ([1, 0.9, 0, 1], 0.020, "WoodLight"),    # yellow
}
# CaP-facing names the LLM will see
CAP_NAMES = {"cubeA": "red block", "cubeB": "green block",
             "cubeC": "blue block", "cubeD": "yellow block"}


class CaPTabletop(Stack):
    """Stack env with a configurable number of colored cubes."""

    def __init__(self, n_blocks=4, **kwargs):
        self.n_blocks = n_blocks
        super().__init__(**kwargs)

    def _load_model(self):
        # skip Stack._load_model, rebuild from ManipulationEnv level
        super(Stack, self)._load_model()

        xpos = self.robots[0].robot_model.base_xpos_offset["table"](self.table_full_size[0])
        self.robots[0].robot_model.set_base_xpos(xpos)

        arena = TableArena(table_full_size=self.table_full_size,
                           table_friction=self.table_friction,
                           table_offset=self.table_offset)
        arena.set_origin([0, 0, 0])

        tex_attrib = {"type": "cube"}
        mat_attrib = {"texrepeat": "1 1", "specular": "0.4", "shininess": "0.1"}

        names = list(BLOCKS)[: self.n_blocks]
        cubes = []
        for i, nm in enumerate(names):
            rgba, half, tex = BLOCKS[nm]
            mat = CustomMaterial(texture=tex, tex_name=f"{nm}_tex",
                                 mat_name=f"{nm}_mat",
                                 tex_attrib=tex_attrib, mat_attrib=mat_attrib)
            obj = BoxObject(name=nm, size_min=[half]*3, size_max=[half]*3,
                            rgba=rgba, material=mat)
            setattr(self, nm, obj)
            cubes.append(obj)
        # Stack's own code references cubeA/cubeB for reward + success
        self.cubeA, self.cubeB = cubes[0], cubes[1]
        self.cubes = cubes

        if self.placement_initializer is not None:
            self.placement_initializer.reset()
            self.placement_initializer.add_objects(cubes)
        else:
            self.placement_initializer = UniformRandomSampler(
                name="ObjectSampler", mujoco_objects=cubes,
                x_range=[-0.12, 0.12], y_range=[-0.14, 0.14],
                rotation=None, ensure_object_boundary_in_range=False,
                ensure_valid_placement=True, reference_pos=self.table_offset,
                z_offset=0.01)

        self.model = ManipulationTask(
            mujoco_arena=arena,
            mujoco_robots=[r.robot_model for r in self.robots],
            mujoco_objects=cubes)

    def _setup_references(self):
        super(Stack, self)._setup_references()
        self.obj_body_id = {c.name: self.sim.model.body_name2id(c.root_body)
                            for c in self.cubes}
        self.cubeA_body_id = self.obj_body_id["cubeA"]
        self.cubeB_body_id = self.obj_body_id["cubeB"]


_REGISTERED = False


def register_capx_env():
    global _REGISTERED
    if not _REGISTERED:
        register_env(CaPTabletop)
        _REGISTERED = True


if __name__ == "__main__":
    register_capx_env()
    from robosuite.controllers import load_composite_controller_config
    cfg = load_composite_controller_config(controller="BASIC")
    env = suite.make(env_name="CaPTabletop", robots="Panda", controller_configs=cfg,
                     has_renderer=False, has_offscreen_renderer=False,
                     use_camera_obs=False, n_blocks=4, ignore_done=True, horizon=100000)
    env.reset()
    for nm in list(BLOCKS)[:4]:
        bid = env.sim.model.body_name2id(f"{nm}_main")
        print(f"{CAP_NAMES[nm]:14s} ({nm}) pos:", np.round(env.sim.data.body_xpos[bid], 3))
    print("\n4-block env OK")
