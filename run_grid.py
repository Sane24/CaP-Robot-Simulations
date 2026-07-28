"""
run_grid.py -- STEP 5. Generate the full experiment grid.

    conditions x profiles x tasks x models x runs

Every generation is cached to disk, so the run is resumable: rerun after a
crash, a rate limit, or a laptop closing, and it picks up where it stopped.
Nothing is re-billed.

  python3 run_grid.py --dry-run                     # counts + cost, no API calls
  python3 run_grid.py                               # the full grid
  python3 run_grid.py --models claude                # one model at a time
  python3 run_grid.py --tasks S1,S3 --runs 1        # a quick pilot
  python3 run_grid.py --conditions baseline,instructions
  python3 run_grid.py --profiles baseline,blind
  python3 run_grid.py --status                       # what's done, what's left

DESIGN NOTES (DECISIONS.md material)

runs>=3 per cell: the 7/14 feedback requires a stdev with every average, and a
    stdev needs n>=2; 3 is the smallest n that makes an outlier visible. Runs
    differ ONLY in sampling (same prompt, same temperature default), so the
    spread measures model nondeterminism, which is exactly the quantity the
    "prompting is a lottery" claim rests on.

Prompt assembly is FIXED and identical everywhere:
    profile + condition + CaP flashcards + scene + command
The CaP flashcards are read from the local cache (cap_tabletop_ui.txt) so the
prompt bytes cannot drift mid-grid.

The scene string comes from the TASK's real environment, not a hardcoded list,
so the model is only ever shown objects that exist. Scenes are read once per
task and reused for every cell of that task (identical prompts across cells).

One process for the whole grid: robosuite/MuJoCo import and JIT are paid once.
"""
import sys, json, time, pathlib, datetime
import conditions as axis
import tasks as task_registry
import models as model_registry

OUT = pathlib.Path("grid_runs")
CAP_CACHE = pathlib.Path("cap_tabletop_ui.txt")

SYSTEM = (
    "You write Python robot policy code in the Code-as-Policies style. "
    "You will see many example pairs: an English command as a # comment, then "
    "the code that does it. For the FINAL command, write ONLY the code that "
    "should follow it. No explanations, no markdown fences, match the style and "
    "only call functions shown in the examples."
)

# published list prices per 1M tokens, USD. VERIFY on the provider dashboards --
# these are only for the --dry-run estimate, never for a reported number.
PRICING = {
    "claude": (5.00, 25.00),
    "openai": (1.25, 10.00),
    "gemini": (1.25, 10.00),
}
EST_OUTPUT_TOKENS = 300


def cap_prompt():
    if CAP_CACHE.exists():
        return CAP_CACHE.read_text()
    import requests
    url = "https://code-as-policies.github.io/prompts/tabletop_ui.txt"
    print(f"fetching CaP flashcards once -> {CAP_CACHE}")
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    CAP_CACHE.write_text(r.text)
    return r.text


def scenes_for(task_ids):
    """Open each task's env ONCE to read its real object list. Kept fixed for
    every cell of that task so prompts are identical across conditions."""
    out = {}
    for tid in task_ids:
        env, _ = task_registry.make_env(tid)
        out[tid] = env.get_obj_names()
        env.close()
    return out


def build_prompt(cap, profile, condition, command, scene):
    return (axis.get_profile(profile) + axis.get_condition(condition) + "\n"
            + cap + f"\nobjects = {scene}\n# {command}\n")


def cell_path(model, cond, prof, task, run):
    return OUT / f"{model}__{cond}__{prof}__{task}__run{run}.py"


def parse_list(argv, flag, default):
    if flag not in argv:
        return list(default)
    return [x.strip() for x in argv[argv.index(flag) + 1].split(",") if x.strip()]


def main():
    a = sys.argv
    models = parse_list(a, "--models", model_registry.DEFAULT_MODELS)
    conds = parse_list(a, "--conditions", axis.CONDITIONS)
    profs = parse_list(a, "--profiles", axis.PROFILES)
    tsks = parse_list(a, "--tasks", task_registry.TASKS)
    runs = int(a[a.index("--runs") + 1]) if "--runs" in a else 3
    dry = "--dry-run" in a
    status_only = "--status" in a

    for m in models: model_registry.model_id(m)          # validate early
    for c in conds: axis.get_condition(c)
    for p in profs: axis.get_profile(p)
    for t in tsks:
        if t not in task_registry.TASKS:
            raise SystemExit(f"unknown task '{t}'. options: {', '.join(task_registry.TASKS)}")

    OUT.mkdir(exist_ok=True)
    cells = [(m, c, p, t, r) for m in models for c in conds
             for p in profs for t in tsks for r in range(1, runs + 1)]
    done = [x for x in cells if cell_path(*x).exists()]
    todo = [x for x in cells if not cell_path(*x).exists()]

    print("=" * 74)
    print("EXPERIMENT GRID")
    print("=" * 74)
    print(f"  models     ({len(models)}): " +
          ", ".join(f"{m} [{model_registry.model_id(m)}]" for m in models))
    print(f"  conditions ({len(conds)}): {', '.join(conds)}")
    print(f"  profiles   ({len(profs)}): {', '.join(profs)}")
    print(f"  tasks      ({len(tsks)}): {', '.join(tsks)}")
    print(f"  runs/cell     : {runs}")
    print(f"  TOTAL CELLS   : {len(cells)}")
    print(f"  already cached: {len(done)}")
    print(f"  TO GENERATE   : {len(todo)}")

    if status_only:
        missing_by_model = {}
        for m, c, p, t, r in todo:
            missing_by_model[m] = missing_by_model.get(m, 0) + 1
        for m in models:
            print(f"    {m}: {missing_by_model.get(m, 0)} remaining")
        return

    cap = cap_prompt()
    print(f"\n  CaP flashcards: {len(cap)} chars (cached, identical every cell)")

    # ---- cost estimate from REAL prompt sizes ----
    worst = len(cap) + max(len(axis.get_condition(c)) for c in conds) \
            + max(len(axis.get_profile(p)) for p in profs) + 200
    in_tok = worst // 4
    print(f"  prompt (worst case): {worst} chars ~= {in_tok} input tokens")
    print(f"\n{'model':10s} {'calls':>7s} {'in Mtok':>9s} {'out Mtok':>9s} {'est $':>9s}")
    print("-" * 74)
    total = 0.0
    for m in models:
        n = sum(1 for x in todo if x[0] == m)
        mi, mo = n * in_tok / 1e6, n * EST_OUTPUT_TOKENS / 1e6
        pin, pout = PRICING.get(m, (0, 0))
        cost = mi * pin + mo * pout
        total += cost
        print(f"{m:10s} {n:>7d} {mi:>9.2f} {mo:>9.2f} {cost:>9.2f}")
    print("-" * 74)
    print(f"{'TOTAL':10s} {len(todo):>7d} {'':>9s} {'':>9s} {total:>9.2f}")
    print("  ^ estimate only, from published list prices. VERIFY on the dashboards.")
    print(f"  rough wall time at ~8s/call: {len(todo)*8/60:.0f} min "
          f"({len(todo)*8/3600:.1f} h)")

    if dry:
        print("\n--dry-run: nothing generated.")
        return
    if not todo:
        print("\nnothing to do, every cell is cached.")
        return

    missing = [m for m in models if not model_registry.have_key(m)]
    if missing:
        raise SystemExit(f"\nmissing API keys for: {', '.join(missing)}")

    print("\nreading scenes from the real environments...")
    scene_of = scenes_for(sorted({x[3] for x in todo}))
    for t, s in scene_of.items():
        print(f"  {t}: {s}")

    print(f"\ngenerating {len(todo)} cells...\n")
    t_start = time.time()
    ok = fail = 0
    usage_by_model = {m: [0, 0] for m in models}

    for i, (m, c, p, t, r) in enumerate(todo, 1):
        f = cell_path(m, c, p, t, r)
        command = task_registry.TASKS[t]["command"]
        user = build_prompt(cap, p, c, command, scene_of[t])
        try:
            text, meta = model_registry.generate(m, SYSTEM, user)
        except Exception as e:
            fail += 1
            print(f"[{i:4d}/{len(todo)}] FAIL {f.stem}: {type(e).__name__}: "
                  f"{str(e)[:70]}")
            time.sleep(3)
            continue
        usage_by_model[m][0] += meta.get("input", 0)
        usage_by_model[m][1] += meta.get("output", 0)
        header = (
            f"# model_key={m}\n# model_id={meta['model_id']}\n"
            f"# provider={meta['provider']}\n# condition={c}\n# profile={p}\n"
            f"# task={t}\n# run={r}\n# scene={scene_of[t]}\n# command={command}\n"
            f"# generated={datetime.datetime.now().isoformat(timespec='seconds')}\n"
            f"# prompt_chars={len(user)}\n"
            f"# tokens_in={meta.get('input','?')} tokens_out={meta.get('output','?')}\n"
            f"# seconds={meta['seconds']}\n\n")
        f.write_text(header + text + "\n")
        ok += 1
        el = time.time() - t_start
        eta = el / i * (len(todo) - i)
        print(f"[{i:4d}/{len(todo)}] ok   {f.stem}  {meta['seconds']:.1f}s  "
              f"eta {eta/60:.0f}m")

    print(f"\n{'='*74}\ndone: {ok} generated, {fail} failed, "
          f"{(time.time()-t_start)/60:.1f} min")
    manifest = dict(
        finished=datetime.datetime.now().isoformat(timespec="seconds"),
        models={m: model_registry.MODELS[m] for m in models},
        conditions=conds, profiles=profs, tasks=tsks, runs=runs,
        cells=len(cells), generated=ok, failed=fail,
        tokens={m: dict(input=u[0], output=u[1]) for m, u in usage_by_model.items()},
        cap_prompt_chars=len(cap), system_prompt=SYSTEM,
    )
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"wrote {OUT}/manifest.json  (exact model ids + token totals)")
    if fail:
        print(f"\n{fail} failed. Rerun the same command to retry ONLY those.")


if __name__ == "__main__":
    main()
