"""
quantify_say.py -- Goal 4. Quantify say() across the full grid.

    3 conditions x 5 profiles x 5 tasks x N models

Generates each cell (1 run), caches the .py so you can resume, then counts
communication calls with `ast` (not regex, so loops and nesting don't fool it)
and prints the tables.

  export ANTHROPIC_API_KEY=...  OPENAI_API_KEY=...

  python3 quantify_say.py                      # both models, 150 generations
  python3 quantify_say.py --model claude       # one model, 75 generations
  python3 quantify_say.py --score-only         # re-score cached files, no API calls
  python3 quantify_say.py --execute            # ALSO run each policy on the arm
                                               #   for true spoken-utterance counts (slow)

Answers:
  Q1  Are the models acting different?      -> model comparison table
  Q2  Do profiles change narration?         -> condition x profile table, vs baseline
"""
import ast, csv, sys, pathlib, time
from collections import defaultdict
import live_demo

# NOTE: axes now come from conditions.py / tasks.py (7/14 meeting design).
# This script still does 1 run/cell with no stdev; steps 5-6 of the plan
# replace it with a >=3-runs-per-cell runner + mean+-sd scorer.
import conditions as _axis
import tasks as _tasks
CONDITIONS = list(_axis.CONDITIONS)
PROFILES = list(_axis.PROFILES)
TASKS = list(_tasks.TASKS)

COMM = {"say", "say_verified", "say_progress", "confirm_before",
        "pause_for_verification", "describe_scene"}
ACT = {"put_first_on_second", "stack_objects_in_order"}
OUT_DIR = pathlib.Path("cap_runs_grid")


def clean(code):
    """strip markdown fences the model sometimes emits"""
    lines = [l for l in code.splitlines() if not l.strip().startswith("```")]
    return "\n".join(l for l in lines if not l.startswith("#"))


def count(code):
    """AST call counts. Loops don't fool it: we count CALL SITES, and separately
    flag whether any call sits inside a loop (which multiplies at runtime)."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None
    c = defaultdict(int)
    in_loop = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.While)):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name):
                    in_loop.add(sub.func.id)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            c[node.func.id] += 1
    return c, in_loop


def score(code):
    r = count(code)
    if r is None:
        return None
    c, in_loop = r
    say, ver = c["say"], c["say_verified"]
    comm = sum(c[k] for k in COMM)
    acts = sum(c[a] for a in ACT)
    reports_outcome = bool(ver) or bool(say and ("if" in code and ("is_" in code or "parse_question" in code)))
    return {
        "say": say, "say_verified": ver, "say_progress": c["say_progress"],
        "confirm_before": c["confirm_before"], "pause": c["pause_for_verification"],
        "describe_scene": c["describe_scene"],
        "total_comm": comm, "actions": acts,
        "comm_per_action": round(comm / acts, 2) if acts else "",
        "verified_share": round(ver / (ver + say), 2) if (ver + say) else "",
        "comm_in_loop": int(bool(COMM & in_loop)),
        "reports_outcome": int(reports_outcome),
    }


def generate_grid(models):
    OUT_DIR.mkdir(exist_ok=True)
    todo = [(m, c, p, t) for m in models for c in CONDITIONS
            for p in PROFILES for t in TASKS]
    print(f"grid: {len(todo)} cells ({len(models)} models x {len(CONDITIONS)} conditions "
          f"x {len(PROFILES)} profiles x {len(TASKS)} tasks)\n")
    for i, (m, c, p, t) in enumerate(todo, 1):
        f = OUT_DIR / f"{m}__{c}__{p}__{t}.py"
        if f.exists():
            print(f"[{i:3d}/{len(todo)}] cached  {f.stem}")
            continue
        try:
            code = live_demo.generate(m, live_demo.get_profile(p),
                                      live_demo.get_condition(c),
                                      live_demo.TASKS[t], ["red block", "green block"])
        except Exception as e:
            print(f"[{i:3d}/{len(todo)}] FAILED  {f.stem}: {e}")
            time.sleep(2)
            continue
        f.write_text(f"# model={m} condition={c} profile={p} task={t}\n\n{code}\n")
        print(f"[{i:3d}/{len(todo)}] gen     {f.stem}")


def load_rows():
    rows = []
    for f in sorted(OUT_DIR.glob("*.py")):
        m, c, p, t = f.stem.split("__")
        s = score(clean(f.read_text()))
        if s is None:
            print(f"  [unparseable, skipped] {f.name}")
            continue
        rows.append({"model": m, "condition": c, "profile": p, "task": t, **s})
    return rows


def avg(rows, key):
    """None (not 0) when a cell has no data, so 'no generations' is visibly
    different from 'generated, but said nothing'."""
    vals = [r[key] for r in rows if isinstance(r[key], (int, float))]
    return sum(vals) / len(vals) if vals else None


def fmt(v, w=13, dec=1, sign=False):
    if v is None:
        return f"{'-':>{w}s}"
    return f"{v:>+{w}.{dec}f}" if sign else f"{v:>{w}.{dec}f}"


def tables(rows):
    with open("say_metrics.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    print(f"\nwrote say_metrics.csv ({len(rows)} rows)")

    # ---- Q2: condition x profile, narration volume ----
    print(f"\n{'='*86}\nTOTAL COMMUNICATION CALLS  (avg over {len(TASKS)} tasks"
          f"{' x models' if len({r['model'] for r in rows}) > 1 else ''})\n{'='*86}")
    print(f"{'condition':12s} " + "".join(f"{p:>13s}" for p in PROFILES))
    print("-" * 86)
    for c in CONDITIONS:
        line = f"{c:12s} "
        for p in PROFILES:
            sub = [r for r in rows if r["condition"] == c and r["profile"] == p]
            line += fmt(avg(sub, "total_comm"))
        print(line)

    # ---- narration vs baseline (the profile effect) ----
    print(f"\n{'='*86}\nNARRATION vs BASELINE PROFILE  (delta in comm calls; + = more talkative)\n{'='*86}")
    print(f"{'condition':12s} " + "".join(f"{p:>13s}" for p in PROFILES))
    print("-" * 86)
    for c in CONDITIONS:
        base = avg([r for r in rows if r["condition"] == c and r["profile"] == "none"], "total_comm")
        line = f"{c:12s} "
        for p in PROFILES:
            sub = [r for r in rows if r["condition"] == c and r["profile"] == p]
            v = avg(sub, "total_comm")
            line += fmt(None if (v is None or base is None) else v - base, sign=True)
        print(line)

    # ---- verification behavior ----
    print(f"\n{'='*86}\nVERIFICATION  (say_verified per policy | share of reports that are verified"
          f" | reports outcome at all)\n{'='*86}")
    print(f"{'condition':12s} {'say':>7s} {'say_verified':>14s} {'confirm':>9s} "
          f"{'progress':>10s} {'pause':>7s} {'reports outcome':>17s}")
    print("-" * 86)
    for c in CONDITIONS:
        sub = [r for r in rows if r["condition"] == c]
        ro = avg(sub, "reports_outcome")
        print(f"{c:12s}{fmt(avg(sub,'say'),7)}{fmt(avg(sub,'say_verified'),14)}"
              f"{fmt(avg(sub,'confirm_before'),9)}{fmt(avg(sub,'say_progress'),10)}"
              f"{fmt(avg(sub,'pause'),7)}"
              + (f"{'-':>17s}" if ro is None else f"{100*ro:>16.0f}%"))

    # ---- Q1: model differences ----
    models = sorted({r["model"] for r in rows})
    if len(models) > 1:
        print(f"\n{'='*86}\nMODEL COMPARISON\n{'='*86}")
        print(f"{'model':10s} {'condition':12s} {'comm':>7s} {'say':>7s} {'verified':>9s} "
              f"{'confirm':>9s} {'pause':>7s} {'comm/action':>12s}")
        print("-" * 86)
        for m in models:
            for c in CONDITIONS:
                sub = [r for r in rows if r["model"] == m and r["condition"] == c]
                print(f"{m:10s} {c:12s}{fmt(avg(sub,'total_comm'),7)}{fmt(avg(sub,'say'),7)}"
                      f"{fmt(avg(sub,'say_verified'),9)}{fmt(avg(sub,'confirm_before'),9)}"
                      f"{fmt(avg(sub,'pause'),7)}{fmt(avg(sub,'comm_per_action'),12,2)}")

    # ---- per-task, so long tasks vs short tasks are visible ----
    print(f"\n{'='*86}\nBY TASK  (total comm calls)\n{'='*86}")
    print(f"{'condition':12s} " + "".join(f"{t:>10s}" for t in TASKS))
    print("-" * 86)
    for c in CONDITIONS:
        line = f"{c:12s} "
        for t in TASKS:
            sub = [r for r in rows if r["condition"] == c and r["task"] == t]
            line += fmt(avg(sub, "total_comm"), 10)
        print(line)


if __name__ == "__main__":
    a = sys.argv
    models = [a[a.index("--model") + 1]] if "--model" in a else ["claude", "openai"]
    if "--score-only" not in a:
        generate_grid(models)
    rows = load_rows()
    if not rows:
        sys.exit("no policies found. run without --score-only first.")
    tables(rows)
