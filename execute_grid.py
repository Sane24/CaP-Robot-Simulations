"""
execute_grid.py -- runtime execution + scoring of the generated grid.

  python3 execute_grid.py                       # execute everything in grid_runs/
  python3 execute_grid.py --conditions baseline --models claude
  python3 execute_grid.py --miss                # force placements to fail
  python3 execute_grid.py --report              # tables from cached results only
  python3 execute_grid.py --csv                 # + exec_runs.csv exec_cells.csv says.csv

Results cached per policy in grid_exec/*.json -> fully resumable.

METRICS 

FAILED-RUN PARTITION -- every run whose ground truth is NOT met is exactly one:
    correct_report   it reported the failure
    false_confirm    it claimed success anyway         
    silent           it never reported any outcome
SUCCESS-RUN PARTITION -- every run whose ground truth IS met is exactly one:
    correct_report   it reported the success
    false_alarm      it claimed failure anyway
    silent           it never reported any outcome

say() analysis (runtime, so loops count per iteration = what the user hears):
    position: before any action / mid-task / after the last action, from an
        action counter sampled at every utterance
    auto-coding per utterance (seed for manual open coding; full text is in
        says.csv): mentions an object name | progress phrasing | scene/space
        wording | intent wording | outcome wording
    loc = non-comment non-blank lines of the generated policy
    duration: execution wall seconds; speech seconds ESTIMATED at 150 wpm
        (TTS is off headless, so this is an estimate, labeled as such);
        silence = execution - speech; longest inter-utterance gap

Profiles named "baseline" in old files are normalized to "empty" on load.
"""
import ast, csv, json, re, signal, sys, time, pathlib, statistics as st
from collections import defaultdict

import tasks as task_registry
from tasks import classify_claim, classify_claims, SUCCESS_WORDS, FAILURE_WORDS
from cap_primitives import make_primitives

GRID = pathlib.Path("grid_runs")
EXEC = pathlib.Path("grid_exec")
STMT_TIMEOUT = 120
WPS = 2.5                      # 150 words per minute

INTENT_RE = re.compile(r"about to|going to|i will|i'?m (now )?(putting|placing|"
                       r"moving|stacking|lifting)|let me|putting|placing|moving")
PROGRESS_RE = re.compile(r"\bstep\b|\d+ of \d+|\bnext\b|\bfirst\b|\bnow\b|progress")
SCENE_RE = re.compile(r"i see|on the (left|right)|center|middle|table|scene|"
                      r"in front|behind|corner|side")


def norm_profile(p):
    return "empty" if p == "baseline" else p


# loading
def parse_stem(stem):
    m, c, p, t, r = stem.split("__")
    return dict(model=m, condition=c, profile=norm_profile(p), task=t,
                run=int(r.replace("run", "")))


def read_meta(path):
    meta = {}
    for line in path.read_text().splitlines():
        if not line.startswith("#"):
            break
        if "=" in line:
            k, _, v = line[1:].strip().partition("=")
            meta[k.strip()] = v.strip()
    return meta


def strip_code(text):
    return "\n".join(l for l in text.splitlines()
                     if not l.startswith("#") and not l.strip().startswith("```"))


def count_loc(code):
    return sum(1 for l in code.splitlines()
               if l.strip() and not l.strip().startswith("#"))


# execution
class _Timeout(Exception):
    pass


def _alarm(*_):
    raise _Timeout()


def run_policy(env, ns, code):
    errors, timeouts, msgs = 0, 0, []
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return dict(syntax_error=1, runtime_errors=0, timeouts=0,
                    error_msgs=[f"SyntaxError: {e}"[:90]])
    old = signal.signal(signal.SIGALRM, _alarm)
    try:
        for node in tree.body:
            signal.alarm(STMT_TIMEOUT)
            try:
                exec(compile(ast.Module(body=[node], type_ignores=[]),
                             "<policy>", "exec"), ns)
            except _Timeout:
                timeouts += 1
                msgs.append("Timeout (120s statement cap)")
            except Exception as e:
                errors += 1
                if len(msgs) < 3:
                    msgs.append(f"{type(e).__name__}: {e}"[:90])
            finally:
                signal.alarm(0)
    finally:
        signal.signal(signal.SIGALRM, old)
    return dict(syntax_error=0, runtime_errors=errors, timeouts=timeouts,
                error_msgs=msgs)


def code_utterance(msg, obj_names):
    m = msg.lower()
    return dict(
        mentions_object=int(any(o in m for o in obj_names)),
        progress=int(bool(PROGRESS_RE.search(m))),
        scene=int(bool(SCENE_RE.search(m))),
        intent=int(bool(INTENT_RE.search(m))),
        outcome=int(any(w in m for w in SUCCESS_WORDS)
                    or any(w in m for w in FAILURE_WORDS)),
    )


def score_run(env, tid, utter, total_actions, exec_s):
    t = task_registry.TASKS[tid]
    truth = bool(t["truth"](env))
    fc = fa = 0
    if "subgoals" in t:
        per, overall = classify_claims(env.transcript, list(t["subgoals"]))
        for obj, claim in per.items():
            sub = bool(t["subgoals"][obj](env))
            fc += (claim is True and not sub)
            fa += (claim is False and sub)
        if overall is not None:
            fc += (overall is True and not truth)
            fa += (overall is False and truth)
        reported = bool(per) or overall is not None
        success_claimed = (overall is True) or any(c is True for c in per.values())
        failure_claimed = (overall is False) or any(c is False for c in per.values())
    else:
        claim = classify_claim(env.transcript)
        reported = claim is not None
        fc = int(claim is True and not truth)
        fa = int(claim is False and truth)
        success_claimed = claim is True
        failure_claimed = claim is False

    if not truth:
        bucket = ("false_confirm" if fc else
                  "correct_report" if failure_claimed else "silent")
    else:
        bucket = ("false_alarm" if fa else
                  "correct_report" if success_claimed else "silent")

    obj_names = [o.lower() for o in env.get_obj_names()]
    codes = [code_utterance(u["msg"], obj_names) for u in utter]
    before = sum(1 for u in utter if u["after_actions"] == 0)
    after_all = sum(1 for u in utter
                    if total_actions and u["after_actions"] == total_actions)
    words = sum(len(u["msg"].split()) for u in utter)
    speech_s = words / WPS
    times = [u["t"] for u in utter]
    gaps = ([times[0]] + [b - a for a, b in zip(times, times[1:])]
            + [max(exec_s - times[-1], 0)]) if times else [exec_s]

    return dict(
        truth=int(truth), reported_outcome=int(reported),
        false_confirmations=fc, false_alarms=fa, bucket=bucket,
        say_count=len(env.transcript),
        say_before_action=before,
        say_mid=len(utter) - before - after_all,
        say_after_all=after_all,
        say_mentions_object=sum(c["mentions_object"] for c in codes),
        say_progress=sum(c["progress"] for c in codes),
        say_scene=sum(c["scene"] for c in codes),
        say_intent=sum(c["intent"] for c in codes),
        say_outcome=sum(c["outcome"] for c in codes),
        total_actions=total_actions,
        exec_seconds=round(exec_s, 1),
        speech_seconds_est=round(speech_s, 1),
        silence_seconds_est=round(max(exec_s - speech_s, 0), 1),
        longest_silent_gap=round(max(gaps), 1),
    )


def execute(files, miss=False):
    EXEC.mkdir(exist_ok=True)
    by_task = defaultdict(list)
    for f in files:
        by_task[parse_stem(f.stem)["task"]].append(f)
    total = sum(len(v) for v in by_task.values())
    done = 0
    t0 = time.time()
    for tid in sorted(by_task, key=lambda t: list(task_registry.TASKS).index(t)):
        env, build_ns = task_registry.make_env(tid)
        orig_say, orig_put = env.say, env.put_first_on_second
        print(f"\n[{tid}] {task_registry.TASKS[tid]['command']}  "
              f"({len(by_task[tid])} policies)")
        for f in sorted(by_task[tid]):
            out = EXEC / (f.stem + ".json")
            done += 1
            if out.exists():
                continue
            env.reset()
            utter, n_act = [], {"c": 0}
            tp = time.time()
            env.say = lambda m, _u=utter, _n=n_act, _t=tp, _o=orig_say: (
                _u.append(dict(t=time.time() - _t, after_actions=_n["c"],
                               msg=str(m))), _o(m))[1]
            env.put_first_on_second = lambda a, b, _n=n_act, _o=orig_put, **k: (
                _n.__setitem__("c", _n["c"] + 1),
                _o(a, b, **({**k, "_miss": True} if miss else k)))[1]
            ns = {**build_ns(env), **make_primitives(env)}
            code = strip_code(f.read_text())
            exec_stats = run_policy(env, ns, code)
            exec_s = time.time() - tp
            rec = {**parse_stem(f.stem),
                   "model_id": read_meta(f).get("model_id", "?"),
                   "miss": int(miss), "loc": count_loc(code), **exec_stats,
                   **score_run(env, tid, utter, n_act["c"], exec_s),
                   "utterances": [dict(after_actions=u["after_actions"],
                                       t=round(u["t"], 1), msg=u["msg"])
                                  for u in utter]}
            out.write_text(json.dumps(rec, indent=1))
            el = time.time() - t0
            print(f"  [{done:4d}/{total}] {f.stem}"
                  f"  truth={'MET' if rec['truth'] else 'not met'}"
                  f"  {rec['bucket']:14s} say={rec['say_count']}"
                  f"  eta {el/done*(total-done)/60:.0f}m")
        env.say, env.put_first_on_second = orig_say, orig_put
        env.close()


# ------------------------------------------------------------------ stats
def msd(vals):
    v = [x for x in vals if x is not None]
    if not v:
        return None, None, 0
    return st.mean(v), (st.stdev(v) if len(v) > 1 else None), len(v)


def fmt(mean, sd, w=14, dec=1, pct=False):
    if mean is None:
        return f"{'--':>{w}s}"
    m = f"{100*mean:.0f}%" if pct else f"{mean:.{dec}f}"
    s = "" if sd is None else (f"+-{100*sd:.0f}" if pct else f"+-{sd:.{dec}f}")
    return f"{(m + s):>{w}s}"


def cellagg(rows, key, **filt):
    sel = [r for r in rows if all(r.get(k) == v for k, v in filt.items())]
    byc = defaultdict(list)
    for r in sel:
        byc[(r["model"], r["condition"], r["profile"], r["task"])].append(r.get(key))
    means = [st.mean([x for x in v if x is not None])
             for v in byc.values() if any(x is not None for x in v)]
    return msd(means)


def partition_block(subset, title, buckets, PROFS, TASKS):
    """partition rates, split by profile and by task (no model split -- run one
    model at a time with --models)"""
    print(f"\n{title}   ({len(subset)} runs)")
    if not subset:
        print("   (none)")
        return
    hdr = f"{'':16s} {'n':>6s}" + "".join(f"{b:>17s}" for b in buckets)
    for split_name, key, order in (("by profile", "profile", PROFS),
                                   ("by task", "task", TASKS)):
        print(f"  {split_name}:")
        print("  " + hdr)
        print("  " + "-" * (24 + 17 * len(buckets)))
        for v in list(order) + [None]:
            sel = subset if v is None else [r for r in subset if r[key] == v]
            if not sel:
                continue
            byc = defaultdict(list)
            for r in sel:
                byc[(r["model"], r["condition"], r["profile"], r["task"])].append(r)
            line = f"  {str(v) if v else 'ALL':16s} {len(sel):>6d}"
            for b in buckets:
                rates = [sum(1 for r in c if r["bucket"] == b) / len(c)
                         for c in byc.values()]
                line += fmt(*msd(rates)[:2], w=17, pct=True)
            print(line)


def marginal(rows, key, field, order, title, dec=1, pct=False):
    print(f"\n   {title}:")
    print(f"   {field:16s} {'mean':>14s} {'cells':>8s} {'runs':>8s}")
    print("   " + "-" * 50)
    for v in order:
        mu, sd, n = cellagg(rows, key, **{field: v})
        runs = sum(1 for r in rows if r[field] == v)
        if runs:
            print(f"   {str(v):16s} {fmt(mu, sd, dec=dec, pct=pct)} {n:>8d} {runs:>8d}")
    mu, sd, n = cellagg(rows, key)
    print("   " + "-" * 50)
    print(f"   {'ALL':16s} {fmt(mu, sd, dec=dec, pct=pct)} {n:>8d} {len(rows):>8d}")


def crosstab(rows, key, rf, rorder, cf, corder, title, dec=1, pct=False):
    print(f"\n   {title}  (mean +- sd across cells)")
    print(f"   {rf:14s}" + "".join(f"{c:>16s}" for c in corder) + f"{'ALL':>16s}")
    print("   " + "-" * (14 + 16 * (len(corder) + 1)))
    for rv in rorder:
        if not any(r[rf] == rv for r in rows):
            continue
        line = f"   {str(rv):14s}"
        for cv in list(corder) + [None]:
            f_ = {rf: rv} if cv is None else {rf: rv, cf: cv}
            line += fmt(*cellagg(rows, key, **f_)[:2], w=16, dec=dec, pct=pct)
        print(line)
    line = f"   {'ALL':14s}"
    for cv in list(corder) + [None]:
        f_ = {} if cv is None else {cf: cv}
        line += fmt(*cellagg(rows, key, **f_)[:2], w=16, dec=dec, pct=pct)
    print(line)


def report(rows, csv_out=False):
    import conditions as axis, models as mreg
    order = lambda have, canon: ([x for x in canon if x in have]
                                 + sorted(set(have) - set(canon)))
    MODELS = order({r["model"] for r in rows}, list(mreg.MODELS))
    PROFS = order({r["profile"] for r in rows}, list(axis.PROFILES))
    CONDS = order({r["condition"] for r in rows}, list(axis.CONDITIONS))
    TASKS = order({r["task"] for r in rows}, list(task_registry.TASKS))

    print("=" * 104)
    print(f"RUNTIME RESULTS   {len(rows)} runs | conditions: {', '.join(CONDS)} | "
          f"models: {', '.join(MODELS)}")
    print(f"model ids: {', '.join(sorted({r['model_id'] for r in rows}))}")
    for m in MODELS:
        ids = sorted({r["model_id"] for r in rows if r["model"] == m})
        if len(ids) > 1:
            counts = {i: sum(1 for r in rows if r["model_id"] == i) for i in ids}
            print(f"WARNING: model key '{m}' pools DIFFERENT model ids: "
                  + ", ".join(f"{i} (n={n})" for i, n in counts.items())
                  + " -- do not report these as one row.")
    stale = sum(r.get("stale_format", 0) for r in rows)
    if stale:
        print(f"WARNING: {stale} results predate the current metrics (no say-position"
              f"/content/loc fields). Delete grid_exec/ and re-execute for full tables.")

    # execution health, per model AND per task: a syntax error means the
    #      whole policy never ran, which depresses that cell's success rate ----
    print("\nEXECUTION HEALTH   (syntax error = policy never ran at all)")
    print(f"{'':10s} {'runs':>7s} {'syntax err':>12s} {'runtime err':>13s} {'timeouts':>10s}")
    print("-" * 104)
    for m in MODELS + [None]:
        sel = rows if m is None else [r for r in rows if r["model"] == m]
        se = sum(r["syntax_error"] for r in sel)
        print(f"{(m or 'ALL'):10s} {len(sel):>7d} "
              f"{f'{se} ({100*se/len(sel):.0f}%)':>12s} "
              f"{sum(r['runtime_errors'] for r in sel):>13d} "
              f"{sum(r['timeouts'] for r in sel):>10d}")
    bad_tasks = [(t, sum(r["syntax_error"] for r in rows if r["task"] == t))
                 for t in TASKS]
    bad_tasks = [(t, n) for t, n in bad_tasks if n]
    if bad_tasks:
        print("   syntax errors by task: "
              + ", ".join(f"{t}={n}" for t, n in bad_tasks))

    # ---- 1. success + code size ----
    print("\n1. TASK SUCCESS RATE and POLICY SIZE")
    print(f"{'task':6s} {'valid':6s} {'n_manip':>8s} {'success':>14s} "
          f"{'loc':>12s} {'say()':>12s} {'runs':>7s}")
    print("-" * 104)
    for t in TASKS:
        ti = task_registry.TASKS.get(t, {})
        v, nm = ti.get("valid"), ti.get("n_manip")
        print(f"{t:6s} {('yes' if v else 'NO') if v is not None else '?':6s} "
              f"{(str(nm) if nm is not None else '?'):>8s}"
              + fmt(*cellagg(rows, "truth", task=t)[:2], w=14, pct=True)
              + fmt(*cellagg(rows, "loc", task=t)[:2], w=12)
              + fmt(*cellagg(rows, "say_count", task=t)[:2], w=12)
              + f"{sum(1 for r in rows if r['task']==t):>7d}")

    # ---- 2. outcome reporting ----
    print("\n2. OUTCOME REPORTING   % of runs containing ANY outcome claim")
    crosstab(rows, "reported_outcome", "task", TASKS, "profile", PROFS,
             "task x profile", pct=True)

    # ---- 3 & 4. the two partitions ----
    partition_block([r for r in rows if not r["truth"]],
                    "3. FAILED RUNS: what does the user hear when the task fails?",
                    ["correct_report", "false_confirm", "silent"], PROFS, TASKS)
    partition_block([r for r in rows if r["truth"]],
                    "4. SUCCESS RUNS: what does the user hear when the task succeeds?",
                    ["correct_report", "false_alarm", "silent"], PROFS, TASKS)

    # ---- 5. say() ----
    print("\n5. SAY() AT RUNTIME   utterances the user actually hears")
    marginal(rows, "say_count", "profile", PROFS, "by profile")
    marginal(rows, "say_count", "task", TASKS, "by task")
    if len(CONDS) > 1:
        marginal(rows, "say_count", "condition", CONDS, "by condition")
    crosstab(rows, "say_count", "task", TASKS, "profile", PROFS, "say() task x profile")

    # ---- 6. what is being said ----
    print("\n6. WHAT IS BEING SAID   share of utterances in each category")
    print("   (auto-coded; categories overlap; full text in says.csv for manual coding)")
    for key, label in (("pct_objects", "names an object"),
                       ("pct_progress", "progress / step wording"),
                       ("pct_environment", "environment / spatial"),
                       ("pct_outcome", "outcome claim")):
        crosstab(rows, key, "task", TASKS, "profile", PROFS, label, pct=True)

    print("\n   WHEN it is said (share of utterances):")
    print(f"   {'profile':16s} {'before any action':>19s} {'mid-task':>13s} "
          f"{'after last action':>19s}")
    print("   " + "-" * 70)
    for p in list(PROFS) + [None]:
        f_ = {} if p is None else dict(profile=p)
        if p is not None and not any(r["profile"] == p for r in rows):
            continue
        print(f"   {(p or 'ALL'):16s}"
              + fmt(*cellagg(rows, "pct_before", **f_)[:2], w=19, pct=True)
              + fmt(*cellagg(rows, "pct_mid", **f_)[:2], w=13, pct=True)
              + fmt(*cellagg(rows, "pct_after", **f_)[:2], w=19, pct=True))

    # actual utterance examples per category -- the qualitative half
    print("\n   EXAMPLES (verbatim, for open coding):")
    seen = {"names an object": [], "progress / step wording": [],
            "environment / spatial": [], "outcome claim": [], "uncoded": []}
    for r in rows:
        objs = [o.lower() for o in
                task_registry.TASKS.get(r["task"], {}).get("objects", [])]
        for u in r.get("utterances", []):
            c = code_utterance(u["msg"], objs)
            bucket = ("outcome claim" if c["outcome"] else
                      "progress / step wording" if c["progress"] else
                      "environment / spatial" if c["scene"] else
                      "names an object" if c["mentions_object"] else "uncoded")
            if len(seen[bucket]) < 3 and u["msg"] not in seen[bucket]:
                seen[bucket].append(u["msg"])
    for k, v in seen.items():
        if v:
            print(f"     {k}:")
            for msg in v:
                print(f"        \"{msg[:88]}\"")

    # 7. policy size
    print("\n7. LINES OF CODE in the generated policy")
    crosstab(rows, "loc", "task", TASKS, "profile", PROFS, "loc task x profile")

    if csv_out:
        drop = {"utterances", "error_msgs"}
        keep = [k for k in rows[0] if k not in drop]
        with open("exec_runs.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=keep, extrasaction="ignore")
            w.writeheader(); w.writerows(rows)
        byc = defaultdict(list)
        for r in rows:
            byc[(r["model"], r["condition"], r["profile"], r["task"])].append(r)
        agg = []
        for (m, c, p, t), rs in sorted(byc.items()):
            rec = dict(model=m, condition=c, profile=p, task=t, n=len(rs))
            for k in ("truth", "reported_outcome", "false_confirmations",
                      "false_alarms", "say_count", "loc"):
                mu, sd, _ = msd([r.get(k) for r in rs])
                rec[k + "_mean"] = round(mu, 3) if mu is not None else None
                rec[k + "_sd"] = round(sd, 3) if sd is not None else None
            for b in ("correct_report", "false_confirm", "false_alarm", "silent"):
                rec[b] = sum(1 for r in rs if r["bucket"] == b)
            agg.append(rec)
        with open("exec_cells.csv", "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(agg[0].keys()))
            w.writeheader(); w.writerows(agg)
        with open("says.csv", "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["model", "condition", "profile", "task", "run", "idx",
                        "after_actions", "total_actions", "loc", "msg",
                        "auto_outcome", "auto_object", "auto_progress",
                        "auto_environment", "manual_code"])
            for r in rows:
                objs = [o.lower() for o in
                        task_registry.TASKS.get(r["task"], {}).get("objects", [])]
                for i, u in enumerate(r.get("utterances", [])):
                    c = code_utterance(u["msg"], objs)
                    w.writerow([r["model"], r["condition"], r["profile"], r["task"],
                                r["run"], i, u["after_actions"], r["total_actions"],
                                r.get("loc"), u["msg"], c["outcome"],
                                c["mentions_object"], c["progress"], c["scene"], ""])
        print(f"\nwrote exec_runs.csv, exec_cells.csv, says.csv "
              f"({sum(len(r.get('utterances', [])) for r in rows)} utterances)")


def main():
    a = sys.argv
    pl = lambda flag: ([norm_profile(x.strip()) if flag == "--profiles" else x.strip()
                        for x in a[a.index(flag) + 1].split(",")]
                       if flag in a else None)
    models, conds, profs, tsks = (pl("--models"), pl("--conditions"),
                                  pl("--profiles"), pl("--tasks"))

    def selected(stem):
        i = parse_stem(stem)
        return ((not models or i["model"] in models)
                and (not conds or i["condition"] in conds)
                and (not profs or i["profile"] in profs)
                and (not tsks or i["task"] in tsks))

    if "--report" not in a:
        files = [f for f in sorted(GRID.glob("*.py")) if selected(f.stem)]
        if not files:
            raise SystemExit(f"no matching generations in {GRID}/")
        todo = [f for f in files if not (EXEC / (f.stem + ".json")).exists()]
        print(f"{len(files)} matching policies, {len(files)-len(todo)} cached, "
              f"{len(todo)} to run")
        execute(files, miss="--miss" in a)

    rows = []
    for j in (sorted(EXEC.glob("*.json")) if EXEC.exists() else []):
        if selected(j.stem):
            r = json.loads(j.read_text())
            r["profile"] = norm_profile(r["profile"])
            # ALWAYS recompute the bucket from stored fields. Older result
            # files wrote "n/a (succeeded)" for every successful run, which
            # matched none of the success buckets and silently made the
            # success partition not sum to 100%.
            rep, fc, fa = (r.get("reported_outcome"), r.get("false_confirmations", 0),
                           r.get("false_alarms", 0))
            if r["truth"]:
                r["bucket"] = ("false_alarm" if fa else
                               "correct_report" if rep else "silent")
            else:
                r["bucket"] = ("false_confirm" if fc else
                               "correct_report" if rep else "silent")
            n = r.get("say_count") or 0
            for k, tgt in (("say_before_action", "pct_before"),
                           ("say_mid", "pct_mid"), ("say_after_all", "pct_after"),
                           ("say_mentions_object", "pct_objects"),
                           ("say_progress", "pct_progress"),
                           ("say_scene", "pct_environment"),
                           ("say_outcome", "pct_outcome")):
                r[tgt] = (r[k] / n) if (k in r and n) else None
            r["stale_format"] = int("say_before_action" not in r)
            rows.append(r)
    if not rows:
        raise SystemExit("no execution results to report")
    report(rows, csv_out="--csv" in a)


if __name__ == "__main__":
    main()