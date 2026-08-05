# Task sources: every task in CaP, CaP-X, and RoboSuite

Long/Short Horizon uses criterion (long = ≥2 sequential manipulations). "Ours" = runs on our RoboSuite shims today; adaptations noted.


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
| 12 | Put the blocks on different corners clockwise starting at the top right corner | long | **yes — our L5** |

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

### Whiteboard Drawing — different effector (pen), not runnable on our shims

Commands 1–10 (hexagon, bisecting line, sun/ground/pyramid scene, circles around blocks, square around the sweeter fruit). Same source page, "Whiteboard Drawing" section.

### Mobile Robot: Navigation + Manipulation — different embodiment, not runnable

Navigation 1–5 (rectangles, convex hull, back-and-forth) and Manipulation 1–3 (coke can + apple to bins, coke amid fruits, how many fruits). Same source page, mobile robot sections.

---

## 2. CaP-X (CaP-Gym / CaP-Bench)

Paper: https://arxiv.org/abs/2603.22435 · Repo: https://github.com/capgym/cap-x · Site: https://capgym.github.io/

The paper's primary analysis uses **7 core tasks** (100 trials each, tiered by primitive abstraction):

| task | base env | horizon | current? |
|---|---|---|---|
| Cube Lift | RoboSuite Lift | short | **yes — S2** |
| Cube Stack | RoboSuite Stack | short | **yes — S1** |
| Spill Wipe | RoboSuite Wipe | long (surface coverage) | no shim yet |
| Peg Insertion | RoboSuite (peg-in-hole) | short | no shim yet |
| Cube Re-stack | RoboSuite Stack variant | long | yes (MultiBlock, needs truth check) |
| Two-Arm Lift | RoboSuite TwoArmLift | short | no (single Panda) |
| Two-Arm Handover | RoboSuite TwoArmHandover | long | no (single Panda) |

Full CaP-Gym release: **187 tasks = 7 RoboSuite + 130 LIBERO-PRO + 50 BEHAVIOR** (paper §Simulation Task Suite; the repo currently ships 39 interactive tasks per its release notes — cite the paper for 187, the repo for what's downloadable). LIBERO-PRO and BEHAVIOR task lists live in those benchmarks' own repos.

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

## Where our current 19 sit

S1 (Stack), S2 (Lift), S4 (PickPlaceCan), S5 (PickPlaceCereal), L1 (PickPlace) — RoboSuite, links above. L3, L5 — CaP Blocks commands 1 and 12. L2 (tower), L4 (2-object narrated subset) — RoboSuite-derived extensions. S3 — ours by design (counterfactual absent referent; justification in tasks.py). Group A+C additions: S6/S7/L6 (CaP Blocks #10/#2/#5, MultiBlock), S8/S9/S10 (PickPlace singles), S11/L7/L8 (CaP Blocks+Bowls #1/#5/#4 on the BlockBowls env).

## Nearest expansion candidates, if more tasks are wanted

1. CaP Blocks #5 "square around the middle" — MultiBlock runs it today; only a geometric truth check is needed. Adds a second CaP-verbatim long task.
2. CaP Blocks #10 "move the red block 5cm to the bottom" — short, precise, `is_at` already exists. Adds a CaP-verbatim short task.
3. PickPlaceMilk / PickPlaceBread — registered single-object envs the household shim already handles; one line each in tasks.py.
4. CaP question tasks (#3/#4/Blocks-and-Bowls #3) — natural fit for `describe_scene`/`parse_question`, but need answer-checking support first.

---

# Numbered list: every task that can run in RoboSuite

Excludes pure questions ("how many bowls…", "why did you move…"), whiteboard drawing (no pen effector), mobile-robot commands (different embodiment), and the volcano/forest roleplay sequence. Everything below is a physical action task whose objects exist in RoboSuite.

Status key: **[ours]** in our current 10 · **[ready]** runs on an existing shim, needs only a ground-truth check · **[shim]** RoboSuite env exists, no shim written · **[2-arm]** needs a second robot · **[multi-turn]** needs conversation state from the previous command · **[asset-limited]** only an approximation of the original scene is possible

| # | task / command | source | env | horizon | status |
|---|---|---|---|---|---|
| 1 | put the red block on the green block | RoboSuite Stack / CaP-X Cube Stack | Stack | short | **[ours S1]** |
| 2 | lift the cube above the table | RoboSuite Lift / CaP-X Cube Lift | Lift | short | **[ours S2]** |
| 3 | put the red block on the purple block (absent referent) | ours | Stack | short | **[ours S3]** |
| 4 | put the can in its bin | RoboSuite PickPlaceCan | PickPlaceCan | short | **[ours S4]** |
| 5 | put the cereal box in its bin | RoboSuite PickPlaceCereal | PickPlaceCereal | short | **[ours S5]** |
| 6 | put every object in its matching bin, one at a time | RoboSuite PickPlace | PickPlace | long | **[ours L1]** |
| 7 | stack all the blocks into one tower | RoboSuite Stack ext. / CaP-X Cube Re-stack | MultiBlock | long | **[ours L2]** |
| 8 | put the blocks in a horizontal line near the top | CaP Blocks #1 | MultiBlock | long | **[ours L3]** |
| 9 | put the milk and the cereal each in its bin, telling me as you go | RoboSuite PickPlace subset | PickPlace | long | **[ours L4]** |
| 10 | put the blocks on different corners clockwise starting at the top right corner | CaP Blocks #12 | MultiBlock | long | **[ours L5]** |
| 11 | arrange the blocks in a square around the middle | CaP Blocks #5 | MultiBlock | long | **[ours L6]** |
| 12 | move the red block 5cm to the bottom | CaP Blocks #10 | MultiBlock | short | **[ours S6]** |
| 13 | move the sky-colored block in between the red block and the second block from the left | CaP Blocks #2 | MultiBlock | short | **[ours S7]** |
| 14 | put the milk in its bin | RoboSuite PickPlaceMilk | PickPlaceMilk | short | [ready] (was S8; removed to balance 10 short + 10 long) |
| 15 | put the bread in its bin | RoboSuite PickPlaceBread | PickPlaceBread | short | **[ours S9]** |
| 16 | put the object in its bin (random single object) | RoboSuite PickPlaceSingle | PickPlaceSingle | short | **[ours S10]** |
| 17 | put the red block to the left of the rightmost bowl | CaP Blocks+Bowls #1 | BlockBowls (new env: colored HollowCylinder bowls) | short | **[ours S11]** |
| 18 | put the blocks in a vertical line 20cm long and 10cm below the blue bowl | CaP Blocks+Bowls #5 | BlockBowls | long | **[ours L7]** |
| 19 | arrange the blocks in a square around the middle. then, make the square bigger | CaP Blocks #5+#6 composed | MultiBlock | long | **[ours L9]** (sequential command, history-verified — no multi-turn needed) |
| 20 | rotate the square by 45 degrees | CaP Blocks #8 | MultiBlock | long | [multi-turn] |
| 21 | undo that | CaP Blocks #7 | MultiBlock | long | [multi-turn] |
| 22 | do the same with the other blocks | CaP Blocks #11 | MultiBlock | long | [multi-turn] |
| 23 | now move it to the side farthest away from it | CaP Blocks+Bowls #2 | MultiBlock | short | [multi-turn] |
| 24 | place the blocks in bowls with non-matching colors | CaP Blocks+Bowls #4 | BlockBowls | long | **[ours L8]** |
| 25 | move all fruits to the green plate and bottles to the blue plate | CaP Fruits #4 | **FruitPlates (new env)** | long | **[ours L10]** (adapted: robosuite ships one fruit — lemon — and one bottle; plates = shallow HollowCylinder dishes) |
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

**Counts:** 20 in the current set (10 short + 10 long) · 4 needing multi-turn support (20–23) · 1 ready but benched (14, milk — removed to balance the set) · 7 needing a new shim (26–32) · 3 needing a second arm (33–35). BlockBowls unlocked 17/18/24 with real bowls; FruitPlates unlocked 25; composing CaP Blocks #5+#6 into one sequential command unlocked 19 without multi-turn support.

**Note on 17/18/24:** originally listed as bins-approximations; now run verbatim on our BlockBowls env (3 colored `HollowCylinderObject` bowls + matching blocks), so the CaP bowl wording is used as written.