# Communication-Aware Robot Policies - RoboSuite Simulations

Does a Code-as-Policies robot tell a blind user what actually happened?
Generate robot policies with LLMs, execute them on a simulated arm, and score
every spoken claim against simulator ground truth.

## Setup

```bash
pip install "mujoco==3.2.3" robosuite numpy requests matplotlib anthropic openai google-genai
export ANTHROPIC_API_KEY=...  OPENAI_API_KEY=...  GEMINI_API_KEY=...
```

The mujoco pin is needed because robosuite calls a function signature that mujoco 3.3
removed. Ignore pip's dependency-conflict warning.

Smoke test (headless, no API key needed for the env itself):

```bash
python3 -c "import tasks; e,_ = tasks.make_env('S1'); print(e.get_obj_names()); e.close()"
```

## Experiment axes

Single source of truth for every axis. Nothing else hardcodes an axis value.

- **`tasks.py`** - the 20 tasks (10 short `S1-S11`, 10 long `L1-L10`; S8
  removed to balance). Each entry: command, env factory, ground-truth check,
  success criterion, provenance (`source`), `valid` flag, `n_manip`,
  `objects`, `horizon`. Also `verdict()` and the claim classifiers shared by
  every scorer. 16 of 20 commands are verbatim from RoboSuite envs or CaP's
  demo command list; the 4 authored ones (S2, S3, L4, L9) exist to make
  failure observable and are documented in their `source` fields.
- **`conditions.py`** - 5 user profiles (`empty` / `blind` / `sighted` /
  `blind_assist` / `sighted_assist`) x 3 policy conditions:
  `baseline` (nothing), `instructions` (plain-language verify-and-report
  rules), `predefined_primitives` (communication primitives with the check
  built in; the prompt text lists every check the scenes support, including
  `is_in_bowl` and `is_on_plate`).
- **`models.py`** - pinned model ids behind short keys (`claude`, `openai`,
  `gemini`). `python3 models.py --list` shows ids, `--ping` round-trips each
  provider. To compare model versions, add a second key (e.g. `claude45`) so
  cached filenames differ; never repoint an existing key at a new id, the
  cache will silently mix versions.

## Pipeline

```
run_grid.py  ->  grid_runs/*.py  ->  execute_grid.py  ->  grid_exec/*.json + report + csvs
                      \->  score_grid.py (static AST scoring, never executes)
```

`run_grid.py` generates one policy file per cell and never regenerates an
existing file. That makes runs resumable and cheap to extend, and it also
means: if you change a prompt, a condition, or a model id, delete the affected
`grid_runs` files first or you will analyze stale generations.

`execute_grid.py` executes each policy statement by statement on the simulated
arm, records every `say()` with its timing relative to actions, counts every
primitive call by category (perception / verification / action /
communication), and scores claims against ground truth. Results cache in
`grid_exec/`; re-running only executes what is missing.

## Reproducing the experiments

**1. Baseline grid (1 model, 5 profiles, 20 tasks, 5 runs = 500 generations):**

```bash
python3 run_grid.py --conditions baseline --models claude --runs 5 --dry-run
python3 run_grid.py --conditions baseline --models claude --runs 5
python3 execute_grid.py --conditions baseline --models claude --report --csv
```

The report prints: task legend, success rates, outcome-reporting rates, the
failed-run partition split by failure type (3a no-attempt vs 3b attempted),
the success-run partition, volunteered outcome claims, say() marginals and
crosstabs, actions vs communication primitives, and 8-category content coding
of every utterance. `--miss` forces placements to fail for testing response under failure only.

**2. Figures:**

```bash
python3 plot.py # plots for everything in exec_runs.csv
python3 plot.py --model claude --out figs_48 --label "Opus 4.8"
```

Seven figures for a single condition; three condition-comparison figures
(cc1-cc3) appear automatically when the csv contains more than one condition.
fig7 needs the primitive-category fields, which only exist in freshly executed
results; if it prints SKIPPED, `rm -rf grid_exec` and re-execute (free).

**3. Open coding of what the robot said:**

```bash
python3 opencode.py says.csv --out open_coding
```

Codes every utterance with a mutually exclusive 4-act scheme
(announce_intent / claim_completion / report_absence / refusal_capability),
a verifiability dimension (can this sentence be wrong?), and surface features.
Writes `says_coded.csv`, a 115-row `says_distinct.csv` worksheet for manual
recoding, `codebook.md`, and 4 figures.

**4. The three-condition comparison:**

```bash
python3 run_grid.py --conditions instructions,predefined_primitives --models claude --runs 5
rm -rf grid_exec        # older results predate current fields
python3 execute_grid.py --models claude --report --csv
python3 plot.py --model claude
```

Pre-registered prediction: instructions raise reporting and introduce false
confirmations; primitives raise reporting without them.

**5. Model/version comparison**

```bash
# add "claude45" to models.py first
python3 run_grid.py --conditions baseline --models claude45 --runs 5
python3 execute_grid.py --models claude45 --report --csv
python3 plot.py --model claude45 --out figs_45 --label "Opus 4.5"
```

## Shims

RoboSuite gives physics and a controller but no pick-and-place; the movement
layer and the CaP vocabulary live here.

- **`robosuite_shim.py`** - `Stack` (red + green cube). Closed-loop OSC,
  waypoint `put_first_on_second`, grasp verification, ground-truth
  `is_placed`, deliberately fragile `is_obj_visible`, `_miss` failure
  injection, macOS TTS.
- **`multiblock_env.py`** - registers three environments: `MultiBlock`
  (N colored blocks), `BlockBowls` (3 blocks + 3 colored bowls, procedural
  HollowCylinder; RoboSuite ships no bowl asset), `FruitPlates` (lemon +
  bottle + 2 shallow plates; RoboSuite ships exactly one fruit).
- **`robosuite_shim_long.py`** - `MultiBlockTabletop` plus `BowlsTabletop`
  and `FruitPlatesTabletop` subclasses. Placement at coordinates, `is_at`,
  `is_in_bowl`, `is_on_plate`, workspace geometry, eager initial-pose capture
  on reset (relative-move tasks), post-action history snapshots (L9's
  sequential ground truth), settle steps for rolling objects, per-object
  grasp heights, generic `parse_obj_name` that resolves any group the scene
  contains ("the bowls", "the plates", "all fruits").
- **`household_shim.py`** - `PickPlace` family (milk/bread/cereal/can into
  bins, RoboSuite's `objects_in_bins` as ground truth) and `Lift`. Presence
  filter tests near-the-table, not z-height (parked objects free-fall).
- **`spatial.py`** - deterministic `parse_position` (points, offsets, lines,
  corners, squares) and `transform_shape_pts` (scale / rotate / shift).
  Both are demonstrated CaP vocabulary: without them, correct policies crash
  and the scorer records artifact false confirmations.
- **`cap_primitives.py`** - the five communication primitives:
  `say_verified`, `confirm_before`, `describe_scene`, `say_progress`,
  `pause_for_verification`. The check lives inside the primitive, so the
  model decides *when* to communicate, never *how* to verify.

Convention: top = +x (away from the robot), left = -y.

## Demos

Collect experiment data only through `run_grid.py`. The demo tools share the
same prompt assembly, model registry, and cached flashcards as the grid, but
their convenience defaults are exactly how uncontrolled variables slip in.

- **`live_demo.py`** - one task live: generate, execute on the rendered arm
  line by line, print the verdict. Prints the resolved model id every run.
- **`live_session.py`** - persistent window.
  `run <condition> <profile> <task> [miss]`, `reset`, `scene`, `quit`.
  Handles all 20 tasks; reopens the env when a task lives in a different
  scene family. Speaks aloud.
- **`diff_prompt.py`** - proves the live path and the grid path send the same
  bytes: builds the prompt exactly as run_grid does, hashes it, diffs against
  a cached cell's recorded header (model id, prompt chars, scene).
- **`diag.py`** - times prompt fetch / LLM call / env creation separately to
  localize a slowdown.

`--render` needs `mjpython` on macOS; wrap script bodies in `main()` because
the mjpython viewer writes a global named `task` into `__main__`.
`--render-every 4` makes rendering ~4x faster.

## Output

- `grid_runs/*.py` - generated policies,
  `<model>__<condition>__<profile>__<task>__run<N>.py`, model id, prompt size
  and tokens in the header. Plus `manifest.json`.
- `grid_exec/*.json` - per-run execution results: success, claims, buckets,
  failure type, say timings, per-category primitive counts, full
  `prim_breakdown`.
- `exec_runs.csv` / `exec_cells.csv` - per-run and per-cell tables for
  analysis and `plot.py`.
- `says.csv` - one row per utterance with timing and 8 auto-code columns plus
  an empty `manual_code` column for hand coding.
- `cap_tabletop_ui.txt` - cached CaP flashcards (cached so the prompt cannot
  drift mid-experiment; delete to refetch).

## Additional Notes:

- Silence robosuite's console spam once per environment:
  copy `macros.py` to `macros_private.py` inside the robosuite install and set
  `CONSOLE_LOGGING_LEVEL = "ERROR"`.
- `run_grid` caches by filename; changing a model id or prompt without
  deleting the affected cells analyzes stale generations.
- Old `grid_exec` results may predate newer per-run fields; re-execution is
  free and always safe (`rm -rf grid_exec`).
- Household grasps succeed ~50-70%, blocks ~90%, lemon ~75%. That spread is
  intentional: natural execution failures are the data.