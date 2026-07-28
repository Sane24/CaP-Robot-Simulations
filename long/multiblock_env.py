"""
multiblock_env.py -- a RoboSuite env with N colored blocks on a table (Panda arm).

RoboSuite's Stack env is hardcoded to exactly 2 cubes, which is not enough for
longer multi-step tasks (lines, sorting, 3-block towers). This subclasses Stack
and swaps in an arbitrary set of colored blocks.

BoxObject is procedural (no mesh asset needed), which is why adding blocks is cheap.
Registered as env_name="MultiBlock". Stack is untouched, so T1-T5 keep working.
"""
import numpy as np
from robosuite.environments.manipulation.stack import Stack
from robosuite.models.objects import BoxObject
from robosuite.models.tasks import ManipulationTask
from robosuite.models.arenas import TableArena
from robosuite.utils.mjcf_utils import CustomMaterial
from robosuite.utils.placement_samplers import UniformRandomSampler
import robosuite as suite

PALETTE = {
    "red block":    [1.00, 0.10, 0.10, 1],
    "green block":  [0.10, 0.80, 0.10, 1],
    "blue block":   [0.15, 0.30, 0.95, 1],
    "yellow block": [0.95, 0.85, 0.10, 1],
    "orange block": [1.00, 0.55, 0.05, 1],
    "purple block": [0.60, 0.10, 0.80, 1],
}
HALF = 0.021                          # 4.2 cm cube


class MultiBlock(Stack):
    def __init__(self, block_names=None, **kwargs):
        self.block_names = block_names or ["red block", "green block",
                                           "blue block", "yellow block"]
        super().__init__(**kwargs)

    def _load_model(self):
        super(Stack, self)._load_model()               # skip Stack's 2-cube setup
        xpos = self.robots[0].robot_model.base_xpos_offset["table"](self.table_full_size[0])
        self.robots[0].robot_model.set_base_xpos(xpos)

        arena = TableArena(table_full_size=self.table_full_size,
                           table_friction=self.table_friction,
                           table_offset=self.table_offset)
        arena.set_origin([0, 0, 0])

        wood = CustomMaterial(texture="WoodLight", tex_name="lightwood",
                              mat_name="lightwood_mat",
                              tex_attrib={"type": "cube"},
                              mat_attrib={"texrepeat": "1 1", "specular": "0.4",
                                          "shininess": "0.1"})

        self.blocks = [
            BoxObject(name=f"blk{i}", size_min=[HALF]*3, size_max=[HALF]*3,
                      rgba=PALETTE.get(n, [0.5, 0.5, 0.5, 1]), material=wood)
            for i, n in enumerate(self.block_names)
        ]
        self.cubeA, self.cubeB = self.blocks[0], self.blocks[1]   # Stack expects these

        self.placement_initializer = UniformRandomSampler(
            name="ObjectSampler", mujoco_objects=self.blocks,
            x_range=[-0.13, 0.13], y_range=[-0.21, 0.21],
            rotation=None, rotation_axis="z",
            ensure_object_boundary_in_range=False, ensure_valid_placement=True,
            reference_pos=self.table_offset, z_offset=0.01)

        self.model = ManipulationTask(
            mujoco_arena=arena,
            mujoco_robots=[r.robot_model for r in self.robots],
            mujoco_objects=self.blocks)

    def _setup_references(self):
        super(Stack, self)._setup_references()
        self.obj_body_id = {n: self.sim.model.body_name2id(o.root_body)
                            for n, o in zip(self.block_names, self.blocks)}
        self.cubeA_body_id = self.obj_body_id[self.block_names[0]]
        self.cubeB_body_id = self.obj_body_id[self.block_names[1]]

    def _setup_observables(self):
        return super(Stack, self)._setup_observables()

    def reward(self, action=None):
        return 0.0

    def _check_success(self):
        return False                  # task-specific success lives in the eval


suite.environments.base.REGISTERED_ENVS["MultiBlock"] = MultiBlock
