# Task sources: every task in CaP, CaP-X, and RoboSuite

Horizon uses our criterion (long = ≥2 sequential manipulations).

## 1. Code-as-Policies (CaP) demo commands

Source for ALL of these: https://code-as-policies.github.io/ (each domain section lists its commands; the tabletop prompt they all share is https://code-as-policies.github.io/prompts/tabletop_ui.txt)

### Tabletop: Blocks

| # | command | horizon | current? |
|---|---|---|---|
| 1 | Put the blocks in a horizontal line near the top | long | **yes — L3** |
| 2 | Move the sky-colored block in between the red block and the second block from the left | short | yes (MultiBlock, needs a truth check) |
| 3 | Why did you move the green block? | n/a (question) | needs dialogue support |
| 4 | Which block did you move? | n/a (question) | needs dialogue support |
| 5 | Arrange the blocks in a square around the middle | long | yes (MultiBlock + geometric check) |
| 6 | Make the square bigger | long | needs multi-turn state |
| 7 | Undo that | long | needs multi-turn state |
| 8 | Rotate the square by 45 degrees | long | needs multi-turn state |
| 9 | Can you throw blocks? | n/a (question) | needs dialogue support |
| 10 | Move the red block 5cm to the bottom | short | yes (is_at check) |
| 11 | Do the same with the other blocks | long | needs multi-turn state |
| 12 | Put the blocks on different corners clockwise starting at the top right corner | long | **yes — L5** |

### Tabletop: Blocks and Bowls

RoboSuite ships no bowls; adaptation = bowls→bins (household shim) where marked.

| # | command | horizon | current? |
|---|---|---|---|
| 1 | Put the red block to the left of the rightmost bowl | short | adaptable (bins) |
| 2 | Now move it to the side farthest away from it | short | needs multi-turn |
| 3 | How many bowls are to the left of the red block? | n/a (question) | needs dialogue |
| 4 | Place the blocks in bowls with non matching colors | long | adaptable (bins) |
| 5 | Put the blocks in a vertical line 20 cm long and 10 cm below the blue bowl | long | adaptable |
| 6–9 | volcano/forest/ocean pretend-play sequence | long | no (open-ended roleplay) |

### Tabletop: Fruits, Bottles, and Plates

| # | command | horizon | current? |
|---|---|---|---|
| 1 | How many fruits are there? | n/a (question) | needs dialogue |
| 2 | Tell me their names | n/a (question) | needs dialogue |
| 3 | Are there any fruits on the green plate? | n/a (question) | needs dialogue |
| 4 | Move all fruits to the green plate and bottles to the blue plate | long | adaptable (household objects→bins) |
| 5 | Move the smallest fruit back to the yellow plate | short | no (no fruit assets) |
| 6 | Wait until you see an egg and put it on the green plate | short | no (perception trigger) |
| 7 | Put the darkest object in the plate that has the apple | short | no (no fruit assets) |

### Whiteboard Drawing — different effector (pen), not runnable on robosuite shims

Commands 1–10 (hexagon, bisecting line, sun/ground/pyramid scene, circles around blocks, square around the sweeter fruit). Same source page, "Whiteboard Drawing" section.

### Mobile Robot: Navigation + Manipulation — different embodiment, not runnable

Navigation 1–5 (rectangles, convex hull, back-and-forth) and Manipulation 1–3 (coke can + apple to bins, coke amid fruits, how many fruits). Same source page, mobile robot sections.

---

## 2. CaP-X (CaP-Gym / CaP-Bench)

Paper: https://arxiv.org/abs/2603.22435 · Repo: https://github.com/capgym/cap-x · Site: https://capgym.github.io/

The paper's primary analysis uses **7 core tasks** (100 trials each, tiered by primitive abstraction):

| task | base env | horizon | ours? |
|---|---|---|---|
| Cube Lift | RoboSuite Lift | short | **yes — our S2** |
| Cube Stack | RoboSuite Stack | short | **yes — our S1** |
| Spill Wipe | RoboSuite Wipe | long (surface coverage) | no shim yet |
| Peg Insertion | RoboSuite (peg-in-hole) | short | no shim yet |
| Cube Re-stack | RoboSuite Stack variant | long | yes (MultiBlock, needs truth check) |
| Two-Arm Lift | RoboSuite TwoArmLift | short | no (single Panda) |
| Two-Arm Handover | RoboSuite TwoArmHandover | long | no (single Panda) |

Full CaP-Gym: **187 tasks = 7 RoboSuite + 130 LIBERO-PRO + 50 BEHAVIOR** (paper §Simulation Task Suite; the repo currently ships 39 interactive tasks per its release notes — cite the paper for 187, the repo for what's downloadable). LIBERO-PRO and BEHAVIOR task lists live in those benchmarks' own repos.

---

## 3. RoboSuite environments (the authoritative registry)

Task descriptions + success criteria: https://robosuite.ai/docs/modules/environments.html
Per-class API docs: https://robosuite.ai/docs/source/robosuite.environments.manipulation.html
The registry itself is `robosuite.ALL_ENVIRONMENTS`.

| env | task | horizon | ours? |
|---|---|---|---|
| Lift | lift the cube above the table | short | **yes — S2** (https://robosuite.ai/docs/modules/environments.html#block-lifting) |
| Stack | stack cubeA on cubeB | short | **yes — S1/S3** (https://robosuite.ai/docs/modules/environments.html#block-stacking) |
| PickPlace | all 4 objects → their bins | long | **yes — L1** (https://robosuite.ai/docs/modules/environments.html#pick-and-place) |
| PickPlaceSingle | one random object → bin | short | yes (shim supports env name) |
| PickPlaceMilk | milk → bin | short | yes |
| PickPlaceBread | bread → bin | short | yes (flakiest grasp) |
| PickPlaceCereal | cereal → bin | short | **yes — S5** |
| PickPlaceCan | can → bin | short | **yes — S4** |
| NutAssembly | both nuts → their pegs | long | no shim (peg insertion) |
| NutAssemblySingle / Square / Round | one nut → peg | short | no shim |
| Door | open the door | short | no shim (articulated object) |
| Wipe | wipe the dirt off the table | long | no shim (surface contact) |
| ToolHang | insert frame, hang tool | long | no shim (1.5 docs list it under manipulation) |
| TwoArmLift | two arms lift the pot | short | no (single Panda) |
| TwoArmPegInHole | peg into hole, two arms | short | no |
| TwoArmHandover | hand object between arms | long | no |

---

## Current 10 tasks

S1 (Stack), S2 (Lift), S4 (PickPlaceCan), S5 (PickPlaceCereal), L1 (PickPlace) — RoboSuite, links above. L3, L5 — CaP Blocks commands 1 and 12. L2 (tower), L4 (2-object narrated subset) — RoboSuite-derived extensions. S3 — ours by design (counterfactual absent referent; justification in tasks.py).


# Numbered list: every task that can run in RoboSuite

Excluding questions, mobile-robot commands (different embodiment), and the volcano/forest roleplay sequence. Only physical action task whose objects exist in RoboSuite.

Status key: **[ready]** runs on an existing shim, needs only a ground-truth check · **[shim]** RoboSuite env exists, no shim written · **[2-arm]** needs a second robot · **[multi-turn]** needs conversation state from the previous command · **[asset-limited]** only an approximation of the original scene is possible

| # | task / command | source | env | horizon | status |
|---|---|---|---|---|---|
| 1 | put the red block on the green block | RoboSuite Stack / CaP-X Cube Stack | Stack | short | **[S1]** |
| 2 | lift the cube above the table | RoboSuite Lift / CaP-X Cube Lift | Lift | short | **[S2]** |
| 3 | put the red block on the purple block (absent referent) | ours | Stack | short | **[S3]** |
| 4 | put the can in its bin | RoboSuite PickPlaceCan | PickPlaceCan | short | **[S4]** |
| 5 | put the cereal box in its bin | RoboSuite PickPlaceCereal | PickPlaceCereal | short | **[S5]** |
| 6 | put every object in its matching bin, one at a time | RoboSuite PickPlace | PickPlace | long | **[L1]** |
| 7 | stack all the blocks into one tower | RoboSuite Stack ext. / CaP-X Cube Re-stack | MultiBlock | long | **[L2]** |
| 8 | put the blocks in a horizontal line near the top | CaP Blocks #1 | MultiBlock | long | **[L3]** |
| 9 | put the milk and the cereal each in its bin, telling me as you go | RoboSuite PickPlace subset | PickPlace | long | **[L4]** |
| 10 | put the blocks on different corners clockwise starting at the top right corner | CaP Blocks #12 | MultiBlock | long | **[L5]** |
| 11 | arrange the blocks in a square around the middle | CaP Blocks #5 | MultiBlock | long | [ready] |
| 12 | move the red block 5cm to the bottom | CaP Blocks #10 | MultiBlock | short | [ready] |
| 13 | move the sky-colored block in between the red block and the second block from the left | CaP Blocks #2 | MultiBlock | short | [ready] |
| 14 | put the milk in its bin | RoboSuite PickPlaceMilk | PickPlaceMilk | short | [ready] |
| 15 | put the bread in its bin | RoboSuite PickPlaceBread | PickPlaceBread | short | [ready] |
| 16 | put the object in its bin (random single object) | RoboSuite PickPlaceSingle | PickPlaceSingle | short | [ready] |
| 17 | put the red block to the left of the rightmost bin | CaP Blocks+Bowls #1 (bowls→bins) | PickPlace | short | [ready] |
| 18 | put the blocks in a vertical line 20cm long and 10cm below the blue bin | CaP Blocks+Bowls #5 (bowls→bins) | MultiBlock | long | [ready] |
| 19 | make the square bigger | CaP Blocks #6 | MultiBlock | long | [multi-turn] |
| 20 | rotate the square by 45 degrees | CaP Blocks #8 | MultiBlock | long | [multi-turn] |
| 21 | undo that | CaP Blocks #7 | MultiBlock | long | [multi-turn] |
| 22 | do the same with the other blocks | CaP Blocks #11 | MultiBlock | long | [multi-turn] |
| 23 | now move it to the side farthest away from it | CaP Blocks+Bowls #2 | MultiBlock | short | [multi-turn] |
| 24 | place the blocks in bins with non-matching colors | CaP Blocks+Bowls #4 | MultiBlock+bins | long | [asset-limited] (bins are not colored) |
| 25 | move all fruits to one bin and bottles to another | CaP Fruits #4 | custom | long | [asset-limited] (one fruit: lemon) |
| 26 | put the square nut on its peg | RoboSuite NutAssemblySquare | NutAssemblySquare | short | [shim] |
| 27 | put the round nut on its peg | RoboSuite NutAssemblyRound | NutAssemblyRound | short | [shim] |
| 28 | put one nut on its peg (random) | RoboSuite NutAssemblySingle | NutAssemblySingle | short | [shim] |
| 29 | put both nuts on their pegs | RoboSuite NutAssembly / CaP-X Peg Insertion | NutAssembly | long | [shim] |
| 30 | open the door | RoboSuite Door | Door | short | [shim] |
| 31 | wipe the dirt off the table | RoboSuite Wipe / CaP-X Spill Wipe | Wipe | long | [shim] |
| 32 | insert the frame into the base, then hang the tool on it | RoboSuite ToolHang | ToolHang | long | [shim] |
| 33 | lift the pot with both arms | RoboSuite TwoArmLift / CaP-X Two-Arm Lift | TwoArmLift | short | [2-arm] |
| 34 | insert the peg into the hole with both arms | RoboSuite TwoArmPegInHole | TwoArmPegInHole | short | [2-arm] |
| 35 | hand the object from one arm to the other | RoboSuite TwoArmHandover / CaP-X Two-Arm Handover | TwoArmHandover | long | [2-arm] |

**Counts:** 10 in the current set,8 more ready on existing shims (11–18)
5 needing multi-turn support (19–23), 2 asset-limited (24–25), 7 need a new shim (26–32), 3 need a second arm (33–35).

