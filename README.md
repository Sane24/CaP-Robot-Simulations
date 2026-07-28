# Communication-Aware Robot Policies

Generate robot policies with LLMs, run them on a simulated Panda arm, and score what the robot **said** against what actually **happened**.

Three conditions compared: `baseline` (nothing), `instructions` (plain-language rules), `predefined_primitives` (communication primitives with the check built in).

## Run

```bash
pip install "mujoco==3.2.3" robosuite numpy requests anthropic openai google-genai
export ANTHROPIC_API_KEY=...  OPENAI_API_KEY=...  GEMINI_API_KEY=...
```

## Experiment axes

- **`tasks.py`** — the 10 tasks (`S1`-`S5` short, `L1`-`L5` long): command, environment, ground-truth check. Also `verdict()`, the shared claim-vs-reality scorer.
- **`conditions.py`** — 5 control profiles (`baseline`/`blind`/`sighted`/`blind_assist`/`sighted_assist`) and the 3 policy conditions, including their teaching-block text.

## Pipeline

```
run_grid.py → grid_runs/*.py → execute_grid.py → grid_exec/*.json
                    └────────→ score_grid.py (reads code, never runs it)
```

- **`run_grid.py`** — generation. Loops models × conditions × profiles × tasks × runs, writes one `.py` per cell. 
- **`execute_grid.py`** — runs each policy in sim and scores claims against ground truth. Reports the failed-run partition (honest / false confirmation / silent), reporting rate, false confirmations, runtime `say()` counts. [Under Construction - might not work]

## Shims

RoboSuite gives physics and a controller but no pick-and-place, so that simulation movement layer is here.

- **`robosuite_shim.py`** — `Stack` (red + green cube). Closed-loop OSC, waypoint `put_first_on_second`, grasp verification, ground-truth `is_placed`, fragile `is_obj_visible`, `_miss` failure injection, macOS TTS.
- **`multiblock_env.py`** + **`robosuite_shim_long.py`** — N colored blocks; placement at coordinates, `is_at`, workspace geometry.
- **`household_shim.py`** — `PickPlace` family (milk/bread/cereal/can into bins, RoboSuite's `objects_in_bins` as ground truth) and `Lift`.
- **`spatial.py`** — deterministic `parse_position`. CaP's flashcards demonstrate it, so policies call it; without it they crash and the scorer records artifact false confirmations.
- **`cap_primitives.py`** — the five primitives: `say_verified`, `confirm_before`, `describe_scene`, `say_progress`, `pause_for_verification`. The check lives inside, so the model decides *to* verify, not *how*.

Convention: top = +x (away from the robot), left = −y.

## Demos 

- **`live_demo.py`** — one task live: generate, execute on the rendered arm line by line, print the verdict.
- **`live_session.py`** — persistent window. `run <condition> <profile> <task> [miss]`, `reset`, `scene`, `quit`. Speaks aloud.

- **`diag.py`** — only or speed diagnosis: times prompt fetch / LLM call / env creation separately to localize a slowdown.

`--render` needs `mjpython` on macOS. 

## Output

- `grid_runs/*.py` — generated policies, `<model>__<condition>__<profile>__<task>__run<N>.py`, model id and tokens in the header. Plus `manifest.json`.
- `grid_exec/*.json` — per-policy execution results.
- `exec_runs.csv`, `exec_cells.csv`, `grid_policies.csv`, `grid_cells.csv`.
- `cap_tabletop_ui.txt` — cached CaP flashcards (cached so the prompt can't drift mid-experiment).

