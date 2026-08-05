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

        # NOTE: no material. A material OVERRIDES rgba on the visual geom, so
        # with material=wood every "colored" block rendered the same gray --
        # 'the red block' and 'the green block' were visually identical in the
        # viewer (semantics still worked headless because names carry them).
        self.blocks = [
            BoxObject(name=f"blk{i}", size_min=[HALF]*3, size_max=[HALF]*3,
                      rgba=PALETTE.get(n, [0.5, 0.5, 0.5, 1]))
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


BOWLS = {                       # fixed spots: top row (x=+0.16), spaced >= bowl diameter
    "red bowl":   ([0.16, -0.20], [1.00, 0.15, 0.15, 1]),
    "green bowl": ([0.16, -0.02], [0.15, 0.80, 0.15, 1]),
    "blue bowl":  ([0.16,  0.16], [0.20, 0.35, 0.95, 1]),
}
BOWL_R_OUT, BOWL_R_IN, BOWL_H = 0.080, 0.062, 0.040


class BlockBowls(MultiBlock):
    """MultiBlock + three colored bowls (HollowCylinderObject -- robosuite ships
    no bowl asset, so the bowl is a procedural open cylinder). Bowls sit at
    FIXED positions; blocks spawn in the lower-left region so the CaP
    blocks-and-bowls commands are never trivially satisfied at reset
    (e.g. "left of the rightmost bowl" starts FALSE by construction).
    Bowls are dense (2000) so a dropped cube does not tip them."""

    def _load_model(self):
        super()._load_model()
        from robosuite.models.objects import HollowCylinderObject
        from robosuite.utils.placement_samplers import (
            SequentialCompositeSampler, UniformRandomSampler)
        self.bowls = {}
        for bname, (pos, rgba) in BOWLS.items():
            self.bowls[bname] = HollowCylinderObject(
                name=bname.replace(" ", "_"), outer_radius=BOWL_R_OUT,
                inner_radius=BOWL_R_IN, height=BOWL_H, ngeoms=12,
                rgba=rgba, density=2000.0)

        sampler = SequentialCompositeSampler(name="ObjectSampler")
        sampler.append_sampler(UniformRandomSampler(
            name="BlockSampler", mujoco_objects=self.blocks,
            x_range=[-0.12, 0.04], y_range=[0.08, 0.21],
            rotation=None, rotation_axis="z",
            ensure_object_boundary_in_range=False, ensure_valid_placement=True,
            reference_pos=self.table_offset, z_offset=0.01))
        for bname, (pos, rgba) in BOWLS.items():
            sampler.append_sampler(UniformRandomSampler(
                name=f"S_{bname.replace(' ', '_')}",
                mujoco_objects=self.bowls[bname],
                x_range=[pos[0], pos[0]], y_range=[pos[1], pos[1]],
                rotation=0.0, rotation_axis="z",
                ensure_object_boundary_in_range=False, ensure_valid_placement=False,
                reference_pos=self.table_offset, z_offset=0.001))
        self.placement_initializer = sampler

        self.model = ManipulationTask(
            mujoco_arena=self.model.mujoco_arena,
            mujoco_robots=[r.robot_model for r in self.robots],
            mujoco_objects=self.blocks + list(self.bowls.values()))

    def _setup_references(self):
        super()._setup_references()
        for bname, obj in self.bowls.items():
            self.obj_body_id[bname] = self.sim.model.body_name2id(obj.root_body)


suite.environments.base.REGISTERED_ENVS["BlockBowls"] = BlockBowls


# ---------------------------------------------------------------- FruitPlates
from robosuite.models.objects import LemonObject, BottleObject

PLATE_R = 0.075          # shallow dish: wide, low walls
PLATE_H = 0.014
PLATE_COLORS = {"green plate": [0.10, 0.80, 0.10, 1],
                "blue plate":  [0.15, 0.30, 0.95, 1]}
PLATE_POS = {"green plate": (0.15, -0.14), "blue plate": (0.15, 0.14)}


class FruitPlates(MultiBlock):
    """CaP 'Fruits, Bottles, and Plates' adapted to what RoboSuite ships:
    exactly one fruit asset (Lemon) and one Bottle. Plates are shallow
    HollowCylinder dishes at fixed spots (colored, so 'the green plate' is a
    real referent). DOCUMENTED LIMITATION: 'all fruits' = [lemon]."""

    def __init__(self, **kwargs):
        kwargs["block_names"] = []            # no blocks in this scene
        super().__init__(**kwargs)

    def _load_model(self):
        super(Stack, self)._load_model()
        xpos = self.robots[0].robot_model.base_xpos_offset["table"](self.table_full_size[0])
        self.robots[0].robot_model.set_base_xpos(xpos)
        arena = TableArena(table_full_size=self.table_full_size,
                           table_friction=self.table_friction,
                           table_offset=self.table_offset)
        arena.set_origin([0, 0, 0])

        from robosuite.models.objects import HollowCylinderObject
        from robosuite.utils.placement_samplers import SequentialCompositeSampler
        self.lemon = LemonObject(name="lemon")
        self.bottle = BottleObject(name="bottle")
        self.plates = [HollowCylinderObject(
                           name=n.replace(" ", "_"), outer_radius=PLATE_R,
                           inner_radius=PLATE_R - 0.012, height=PLATE_H,
                           rgba=c, ngeoms=12, density=3000.0)
                       for n, c in PLATE_COLORS.items()]
        movables = [self.lemon, self.bottle]
        self.blocks = movables                 # what the shim treats as graspable
        self.cubeA, self.cubeB = movables[0], movables[1]   # Stack expects these

        self.placement_initializer = SequentialCompositeSampler(name="ObjectSampler")
        self.placement_initializer.append_sampler(UniformRandomSampler(
            name="movables", mujoco_objects=movables,
            x_range=[-0.12, 0.02], y_range=[-0.10, 0.10],
            rotation=None, rotation_axis="z",
            ensure_object_boundary_in_range=False, ensure_valid_placement=True,
            reference_pos=self.table_offset, z_offset=0.01))
        for plate, (n, _) in zip(self.plates, PLATE_COLORS.items()):
            px, py = PLATE_POS[n]
            self.placement_initializer.append_sampler(UniformRandomSampler(
                name=n.replace(" ", "_") + "_s", mujoco_objects=[plate],
                x_range=[px, px], y_range=[py, py], rotation=0, rotation_axis="z",
                ensure_object_boundary_in_range=False, ensure_valid_placement=False,
                reference_pos=self.table_offset, z_offset=0.001))

        self.model = ManipulationTask(
            mujoco_arena=arena,
            mujoco_robots=[r.robot_model for r in self.robots],
            mujoco_objects=movables + self.plates)

    def _setup_references(self):
        super(Stack, self)._setup_references()
        self.obj_body_id = {
            "lemon": self.sim.model.body_name2id(self.lemon.root_body),
            "bottle": self.sim.model.body_name2id(self.bottle.root_body),
        }
        for plate, n in zip(self.plates, PLATE_COLORS):
            self.obj_body_id[n] = self.sim.model.body_name2id(plate.root_body)
        self.cubeA_body_id = self.obj_body_id["lemon"]
        self.cubeB_body_id = self.obj_body_id["bottle"]
        self.block_names = ["lemon", "bottle"]


suite.environments.base.REGISTERED_ENVS["FruitPlates"] = FruitPlates