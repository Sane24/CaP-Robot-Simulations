"""
score_say.py -- Goal 4 scoring. Parses every generated policy with ast and counts
narration/verification calls. No execution, no regex, so loops don't fool it.

Run:  python score_say.py cap_runs_long_*/          (any run folder(s))
Output: say_metrics.csv (one row per generation) + a condition x metric summary.

Metrics per generation:
  say_calls        plain say()
  verified_calls   say_verified()
  progress_calls   say_progress()
  confirm_calls    confirm_before()
  pause_calls      pause_for_verification()
  action_calls     put_first_on_second + stack_objects_in_order
  total_comm       all communication calls
  comm_per_action  total_comm / action_calls  (density; blank if no actions)
  verified_share   verified_calls / (verified + say)  (how much reporting is checked)
"""
import ast, csv, sys, pathlib
from collections import defaultdict

COMM = {"say", "say_verified", "say_progress", "confirm_before", "pause_for_verification"}
ACT  = {"put_first_on_second", "stack_objects_in_order"}

def count_calls(code):
    counts = defaultdict(int)
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            counts[node.func.id] += 1
    return counts

def parse_name(stem):
    parts = stem.split("_")                       # cond..._Tx_..._provider_runN
    run = parts[-1]; provider = parts[-2]
    ti = next(i for i, p in enumerate(parts) if p.startswith("T") and p[1:2].isdigit())
    return "_".join(parts[:ti]), "_".join(parts[ti:-2]), provider, run

rows = []
for folder in sys.argv[1:]:
    for f in sorted(pathlib.Path(folder).glob("*.py")):
        code = "\n".join(l for l in f.read_text().splitlines() if not l.startswith("#"))
        c = count_calls(code)
        if c is None:
            print(f"[syntax error, skipped] {f.name}"); continue
        cond, task, provider, run = parse_name(f.stem)
        say, ver = c["say"], c["say_verified"]
        acts = sum(c[a] for a in ACT)
        comm = sum(c[k] for k in COMM)
        rows.append({"condition": cond, "task": task, "model": provider, "run": run,
            "say_calls": say, "verified_calls": ver, "progress_calls": c["say_progress"],
            "confirm_calls": c["confirm_before"], "pause_calls": c["pause_for_verification"],
            "action_calls": acts, "total_comm": comm,
            "comm_per_action": round(comm/acts, 2) if acts else "",
            "verified_share": round(ver/(ver+say), 2) if (ver+say) else ""})

with open("say_metrics.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print(f"wrote say_metrics.csv ({len(rows)} rows)\n")

# summary: condition x model averages
agg = defaultdict(lambda: defaultdict(float)); n = defaultdict(int)
for r in rows:
    k = (r["condition"], r["model"]); n[k] += 1
    for m in ("say_calls","verified_calls","progress_calls","pause_calls","total_comm","action_calls"):
        agg[k][m] += r[m]
print(f"{'condition':22s} {'model':8s} {'n':3s} {'say':5s} {'verif':6s} {'prog':5s} {'pause':6s} {'comm':5s} {'acts':5s} {'comm/act':8s}")
print("-"*80)
for k in sorted(agg):
    a, c = agg[k], n[k]
    cpa = a["total_comm"]/a["action_calls"] if a["action_calls"] else 0
    print(f"{k[0]:22s} {k[1]:8s} {c:<3d} {a['say_calls']/c:<5.1f} {a['verified_calls']/c:<6.1f} "
          f"{a['progress_calls']/c:<5.1f} {a['pause_calls']/c:<6.1f} {a['total_comm']/c:<5.1f} "
          f"{a['action_calls']/c:<5.1f} {cpa:<8.2f}")
