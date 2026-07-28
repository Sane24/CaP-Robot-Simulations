"""
score_grid.py -- STEP 6. Static scoring of the generated grid, with mean +- sd
on every number.

  python3 score_grid.py                  # all cached generations
  python3 score_grid.py --models claude
  python3 score_grid.py --tasks S1,S3
  python3 score_grid.py --csv            # also write per-policy + per-cell CSVs

WHICH STANDARD DEVIATION (DECISIONS.md -- this is the "explain your small
choices" item that matters most here). The grid has TWO independent sources of
spread and they answer different questions, so this script never mixes them:

  WITHIN-CELL sd  = spread across the >=3 runs of ONE (model, condition,
      profile, task). Same prompt every time, so this is pure model
      nondeterminism. This is the number the "prompting makes verification a
      lottery" claim rests on.

  BETWEEN-CELL sd = spread across the cell MEANS inside a reported group
      (e.g. all tasks x profiles for one condition). This is how much behavior
      varies across situations.

Every aggregate table reports mean +- BETWEEN-cell sd over cell means, because
averaging runs first stops a noisy cell from being counted 3 times (which would
understate the sd and overstate significance). WITHIN-cell sd gets its own
table. n is printed everywhere; sd is shown as "--" when n<2, never as 0.

COUNTING is AST-based, not regex: it counts call SITES, so a call inside a loop
counts once statically (the comm_in_loop flag marks policies whose runtime
counts would multiply).
"""
import ast, csv, sys, pathlib, statistics as st
from collections import defaultdict, Counter

GRID = pathlib.Path("grid_runs")

COMM = ["say", "say_verified", "say_progress", "confirm_before",
        "pause_for_verification", "describe_scene"]
ACT = ["put_first_on_second", "stack_objects_in_order"]

# ground-truth checks our primitives expose vs. everything else a model might
# reach for. The DISTINCTION is the finding, so keep the categories explicit.
GROUND_TRUTH_CHECKS = {"is_placed", "is_at", "is_in_bin", "was_lifted"}
WEAK_CHECKS = {"is_obj_visible", "parse_question", "get_obj_pos", "norm",
               "get_obj_names"}


# ------------------------------------------------------------------ loading
def parse_header(text):
    meta = {}
    for line in text.splitlines():
        if not line.startswith("#"):
            break
        if "=" in line:
            k, _, v = line[1:].strip().partition("=")
            meta[k.strip()] = v.strip()
    return meta


def strip_code(text):
    lines = [l for l in text.splitlines()
             if not l.startswith("#") and not l.strip().startswith("```")]
    return "\n".join(lines)


def score_policy(code):
    """AST call-site counts + which verification check the policy chose."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None
    calls = Counter()
    in_loop = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.While)):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name):
                    in_loop.add(sub.func.id)
        if isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Name):
                calls[f.id] += 1
            elif isinstance(f, ast.Attribute):
                calls[f.attr] += 1                 # np.linalg.norm -> "norm"

    say, ver = calls["say"], calls["say_verified"]
    comm = sum(calls[k] for k in COMM)
    acts = sum(calls[a] for a in ACT)

    gt = sorted(c for c in GROUND_TRUTH_CHECKS if calls[c])
    weak = sorted(c for c in WEAK_CHECKS if calls[c])
    has_branch = any(isinstance(n, ast.If) for n in ast.walk(tree))

    # what did this policy use to decide what to report?
    if ver:
        kind = "primitive(" + "+".join(gt) + ")" if gt else "primitive(unspecified)"
    elif gt and has_branch:
        kind = "manual(" + "+".join(gt) + ")"
    elif weak and has_branch:
        kind = "manual(" + "+".join(weak) + ")"
    elif say:
        kind = "none(unchecked say)"
    else:
        kind = "no report"

    return dict(
        say=say, say_verified=ver, say_progress=calls["say_progress"],
        confirm_before=calls["confirm_before"],
        pause=calls["pause_for_verification"], describe_scene=calls["describe_scene"],
        total_comm=comm, actions=acts,
        comm_per_action=(comm / acts) if acts else None,
        verified_share=(ver / (ver + say)) if (ver + say) else None,
        comm_in_loop=int(bool(set(COMM) & in_loop)),
        reports_outcome=int(bool(ver) or bool(say and has_branch and (gt or weak))),
        check_kind=kind,
    )


def load(models=None, conds=None, profs=None, tsks=None):
    rows, bad = [], []
    for f in sorted(GRID.glob("*.py")):
        text = f.read_text()
        meta = parse_header(text)
        try:
            m, c, p, t, r = f.stem.split("__")
            run = int(r.replace("run", ""))
        except ValueError:
            bad.append((f.name, "unparseable filename")); continue
        if models and m not in models: continue
        if conds and c not in conds: continue
        if profs and p not in profs: continue
        if tsks and t not in tsks: continue
        s = score_policy(strip_code(text))
        if s is None:
            bad.append((f.name, "invalid python emitted by the model")); continue
        rows.append(dict(model=m, model_id=meta.get("model_id", "?"),
                         condition=c, profile=p, task=t, run=run, **s))
    return rows, bad


# ------------------------------------------------------- stats helpers
def msd(values):
    """(mean, sd, n). sd is None when n<2 -- never silently 0."""
    v = [x for x in values if x is not None]
    if not v:
        return None, None, 0
    return st.mean(v), (st.stdev(v) if len(v) > 1 else None), len(v)


def fmt(mean, sd, n=None, w=14, dec=1, pct=False):
    if mean is None:
        return f"{'--':>{w}s}"
    m = f"{100*mean:.0f}%" if pct else f"{mean:.{dec}f}"
    s = "" if sd is None else (f"+-{100*sd:.0f}" if pct else f"+-{sd:.{dec}f}")
    return f"{(m + s):>{w}s}"


def cell_means(rows, key):
    """Collapse runs -> one mean per (model, condition, profile, task) cell.
    Aggregates are computed over CELL MEANS so a 3-run cell is not counted
    three times."""
    byc = defaultdict(list)
    for r in rows:
        byc[(r["model"], r["condition"], r["profile"], r["task"])].append(r[key])
    return {k: st.mean([x for x in v if x is not None])
            for k, v in byc.items() if any(x is not None for x in v)}


def agg(rows, key, **filt):
    sel = [r for r in rows if all(r[k] == v for k, v in filt.items())]
    cm = cell_means(sel, key)
    return msd(list(cm.values()))


# ------------------------------------------------------------------ tables
def tables(rows, bad, CONDS, PROFS, TASKS, MODELS):
    print("=" * 100)
    print("COVERAGE")
    print("=" * 100)
    cells = defaultdict(int)
    for r in rows:
        cells[(r["model"], r["condition"], r["profile"], r["task"])] += 1
    ns = sorted(cells.values())
    print(f"  policies scored : {len(rows)}")
    print(f"  cells populated : {len(cells)}")
    print(f"  runs per cell   : min {ns[0] if ns else 0}, "
          f"median {st.median(ns) if ns else 0}, max {ns[-1] if ns else 0}")
    if ns and ns[0] < 2:
        print(f"  WARNING: {sum(1 for n in ns if n < 2)} cell(s) have n<2, "
              f"so no within-cell sd is computable there")
    if bad:
        print(f"  unparseable     : {len(bad)}")
        for name, why in bad[:5]:
            print(f"      {name}: {why}")
    for m in MODELS:
        ids = {r["model_id"] for r in rows if r["model"] == m}
        if ids:
            print(f"  model '{m}' -> {', '.join(sorted(ids))}")

    # ---- A. narration volume, condition x profile ----
    print(f"\n{'='*100}")
    print("A. TOTAL COMMUNICATION CALLS   mean +- sd across cells (tasks x models)")
    print("=" * 100)
    print(f"{'condition':24s}" + "".join(f"{p:>15s}" for p in PROFS))
    print("-" * 100)
    for c in CONDS:
        line = f"{c:24s}"
        for p in PROFS:
            line += fmt(*agg(rows, "total_comm", condition=c, profile=p)[:2], w=15)
        print(line)

    # ---- B. profile effect ----
    print(f"\n{'='*100}")
    print("B. PROFILE EFFECT   cell-mean delta vs the baseline profile, +- sd of the deltas")
    print("   (paired per cell: same condition, task and model, profile swapped)")
    print("=" * 100)
    print(f"{'condition':24s}" + "".join(f"{p:>15s}" for p in PROFS))
    print("-" * 100)
    for c in CONDS:
        base = cell_means([r for r in rows if r["condition"] == c
                           and r["profile"] == "baseline"], "total_comm")
        line = f"{c:24s}"
        for p in PROFS:
            other = cell_means([r for r in rows if r["condition"] == c
                                and r["profile"] == p], "total_comm")
            deltas = [other[k] - base[(k[0], k[1], "baseline", k[3])]
                      for k in other
                      if (k[0], k[1], "baseline", k[3]) in base]
            m, s, n = msd(deltas)
            line += (f"{'--':>15s}" if m is None else
                     f"{(f'{m:+.1f}' + ('' if s is None else f'+-{s:.1f}')):>15s}")
        print(line)

    # ---- C. verification behaviour ----
    print(f"\n{'='*100}")
    print("C. VERIFICATION BEHAVIOUR   mean +- sd across cells")
    print("=" * 100)
    hdr = ["say", "say_verified", "confirm", "progress", "pause", "reports outcome"]
    keys = ["say", "say_verified", "confirm_before", "say_progress", "pause",
            "reports_outcome"]
    print(f"{'condition':24s}" + "".join(f"{h:>15s}" for h in hdr))
    print("-" * 100)
    for c in CONDS:
        line = f"{c:24s}"
        for k in keys:
            m, s, n = agg(rows, k, condition=c)
            line += fmt(m, s, w=15, pct=(k == "reports_outcome"))
        print(line)

    # ---- D. THE LOTTERY TABLE ----
    print(f"\n{'='*100}")
    print("D. WHICH CHECK DID THE POLICY USE?   (the 'lottery vs invariant' measure)")
    print("=" * 100)
    for c in CONDS:
        sel = [r for r in rows if r["condition"] == c]
        if not sel:
            continue
        kinds = Counter(r["check_kind"] for r in sel)
        print(f"\n  {c}  (n={len(sel)} policies, {len(kinds)} distinct strategies)")
        for k, v in kinds.most_common():
            print(f"      {100*v/len(sel):5.1f}%  {v:4d}x  {k}")

    print(f"\n{'-'*100}")
    print("  WITHIN-CELL AGREEMENT: of cells with >=2 runs, the share where every")
    print("  run picked the SAME check. Same prompt, so disagreement is the model")
    print("  choosing differently run to run.")
    print(f"{'-'*100}")
    print(f"{'condition':24s} {'cells>=2 runs':>14s} {'all runs agree':>16s} "
          f"{'distinct checks':>17s}")
    print("-" * 100)
    for c in CONDS:
        byc = defaultdict(list)
        for r in rows:
            if r["condition"] == c:
                byc[(r["model"], r["profile"], r["task"])].append(r["check_kind"])
        multi = {k: v for k, v in byc.items() if len(v) >= 2}
        if not multi:
            print(f"{c:24s} {0:>14d} {'--':>16s} {'--':>17s}")
            continue
        agree = sum(1 for v in multi.values() if len(set(v)) == 1)
        distinct = len({k for v in byc.values() for k in v})
        print(f"{c:24s} {len(multi):>14d} {f'{100*agree/len(multi):.0f}%':>16s} "
              f"{distinct:>17d}")

    # ---- E. within-cell (run-to-run) variability ----
    print(f"\n{'='*100}")
    print("E. RUN-TO-RUN VARIABILITY   mean WITHIN-cell sd (same prompt, resampled)")
    print("   higher = the model's behaviour is less reproducible")
    print("=" * 100)
    print(f"{'condition':24s}" + "".join(f"{m:>15s}" for m in MODELS) + f"{'all':>15s}")
    print("-" * 100)
    for c in CONDS:
        line = f"{c:24s}"
        for m in list(MODELS) + [None]:
            byc = defaultdict(list)
            for r in rows:
                if r["condition"] == c and (m is None or r["model"] == m):
                    byc[(r["model"], r["profile"], r["task"])].append(r["total_comm"])
            sds = [st.stdev(v) for v in byc.values() if len(v) > 1]
            line += (f"{'--':>15s}" if not sds
                     else f"{f'{st.mean(sds):.2f} (n={len(sds)})':>15s}")
        print(line)

    # ---- F. model comparison ----
    print(f"\n{'='*100}")
    print("F. MODEL COMPARISON   mean +- sd across cells")
    print("=" * 100)
    print(f"{'model':10s} {'condition':24s}" +
          "".join(f"{h:>15s}" for h in ["comm", "say", "say_verified", "pause"]))
    print("-" * 100)
    for m in MODELS:
        for c in CONDS:
            if not any(r["model"] == m and r["condition"] == c for r in rows):
                continue
            line = f"{m:10s} {c:24s}"
            for k in ["total_comm", "say", "say_verified", "pause"]:
                line += fmt(*agg(rows, k, model=m, condition=c)[:2], w=15)
            print(line)

    # ---- G. by task ----
    print(f"\n{'='*100}")
    print("G. BY TASK   total communication calls, mean +- sd across cells")
    print("=" * 100)
    present = [t for t in TASKS if any(r["task"] == t for r in rows)]
    half = (len(present) + 1) // 2
    for chunk in (present[:half], present[half:]):
        if not chunk: continue
        print(f"{'condition':24s}" + "".join(f"{t:>15s}" for t in chunk))
        print("-" * 100)
        for c in CONDS:
            line = f"{c:24s}"
            for t in chunk:
                line += fmt(*agg(rows, "total_comm", condition=c, task=t)[:2], w=15)
            print(line)
        print()


def write_csvs(rows):
    with open("grid_policies.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    agg_rows = []
    byc = defaultdict(list)
    for r in rows:
        byc[(r["model"], r["condition"], r["profile"], r["task"])].append(r)
    for (m, c, p, t), rs in sorted(byc.items()):
        rec = dict(model=m, condition=c, profile=p, task=t, n_runs=len(rs))
        for k in ["total_comm", "say", "say_verified", "confirm_before",
                  "say_progress", "pause", "reports_outcome"]:
            mean, sd, n = msd([x[k] for x in rs])
            rec[f"{k}_mean"] = None if mean is None else round(mean, 3)
            rec[f"{k}_sd"] = None if sd is None else round(sd, 3)
        rec["checks_used"] = "|".join(sorted({x["check_kind"] for x in rs}))
        rec["all_runs_agree"] = int(len({x["check_kind"] for x in rs}) == 1)
        agg_rows.append(rec)
    with open("grid_cells.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(agg_rows[0].keys()))
        w.writeheader(); w.writerows(agg_rows)
    print(f"\nwrote grid_policies.csv ({len(rows)} policies) "
          f"and grid_cells.csv ({len(agg_rows)} cells)")


def main():
    a = sys.argv
    pl = lambda flag: ([x.strip() for x in a[a.index(flag) + 1].split(",")]
                       if flag in a else None)
    if not GRID.exists():
        raise SystemExit(f"no {GRID}/ folder. Run run_grid.py first.")
    rows, bad = load(pl("--models"), pl("--conditions"), pl("--profiles"), pl("--tasks"))
    if not rows:
        raise SystemExit(f"no generations found in {GRID}/")

    import conditions as axis, tasks as treg, models as mreg
    order = lambda have, canon: ([x for x in canon if x in have]
                                 + sorted(have - set(canon)))
    CONDS = order({r["condition"] for r in rows}, list(axis.CONDITIONS))
    PROFS = order({r["profile"] for r in rows}, list(axis.PROFILES))
    TASKS = order({r["task"] for r in rows}, list(treg.TASKS))
    MODELS = order({r["model"] for r in rows}, list(mreg.MODELS))

    tables(rows, bad, CONDS, PROFS, TASKS, MODELS)
    if "--csv" in a:
        write_csvs(rows)


if __name__ == "__main__":
    main()
