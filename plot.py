"""
plot.py -- figures from exec_runs.csv.

    python3 plot.py                                  # everything in the csv
    python3 plot.py --model claude45                 # one model only
    python3 plot.py --model claude45 --out figs_45   # write into a folder
    python3 plot.py --condition baseline --model claude --out figs_48
    python3 plot.py --csv other_run.csv --label "Opus 4.5"

Filters (--model / --condition / --profile / --task) select rows; --out sets
the output folder (created if needed); --label goes into figure titles so two
model runs are distinguishable side by side.

All error bars are sd over CELL means (cell = profile x task), matching the
tables: runs are averaged within a cell first, so a 5-run cell is not counted
five times and the sd is not artificially shrunk.
"""
import csv, collections, os, sys, statistics as st
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

A = sys.argv
arg = lambda f, d=None: A[A.index(f) + 1] if f in A else d
CSV = arg("--csv", "exec_runs.csv")
OUT = arg("--out", ".")
LABEL = arg("--label")
FILTERS = {k: arg("--" + k) for k in ("model", "condition", "profile", "task")}
FILTERS = {k: v for k, v in FILTERS.items() if v}
os.makedirs(OUT, exist_ok=True)
p = lambda name: os.path.join(OUT, name)

PROF = ["empty", "blind", "sighted", "blind_assist", "sighted_assist"]
PLBL = ["empty\n(no prompt)", "blind", "sighted", "blind\n+assist", "sighted\n+assist"]
CODES = ["objects", "progress", "environment", "intent",
         "confirming", "verb", "robot_action", "error"]
GREEN, RED, AMBER, DARK, MID = "#2E7D32", "#C62828", "#F9A825", "#37474F", "#78909C"

rows = [r for r in csv.DictReader(open(CSV))
        if all(r.get(k) == v for k, v in FILTERS.items())]
if not rows:
    raise SystemExit(f"no rows in {CSV} matching {FILTERS or 'any filter'}")
MODELS = sorted({r["model"] for r in rows})
IDS = sorted({r.get("model_id", "?") for r in rows})
SUB = LABEL or (", ".join(IDS) if len(IDS) <= 2 else f"{len(rows)} runs")
print(f"{len(rows)} runs | models: {', '.join(MODELS)} | ids: {', '.join(IDS)}")
if len(IDS) > 1 and not LABEL:
    print("WARNING: this csv mixes model ids -- filter with --model or --csv")
NUM = ("truth reported_outcome false_confirmations false_alarms say_count loc "
       "say_before_action say_mid say_after_all total_actions primitive_calls"
       ).split() + [f"say_{c}" for c in CODES]
for r in rows:
    for k in NUM:
        v = r.get(k, "")
        r[k] = float(v) if v not in ("", "None", None) else 0.0
    r["bucket"] = (("false_confirm" if r["false_confirmations"] else
                    "correct_report" if r["reported_outcome"] else "silent")
                   if not r["truth"] else
                   ("false_alarm" if r["false_alarms"] else
                    "correct_report" if r["reported_outcome"] else "silent"))
    r["failure_type"] = (None if r["truth"] else
                         ("no_attempt" if not r["total_actions"] else "attempted"))

# task order: shorts then longs, as in the registry
TASKS = sorted({r["task"] for r in rows},
               key=lambda t: (t[0] != "S", int(t[1:])))


def cellstat(sel, key):
    c = collections.defaultdict(list)
    for r in sel:
        c[(r["profile"], r["task"])].append(r[key])
    m = [st.mean(v) for v in c.values()]
    return (st.mean(m), st.stdev(m) if len(m) > 1 else 0.0) if m else (0.0, 0.0)


def style(ax, ylab, title, pct=False):
    ax.set_ylabel(ylab, fontsize=9)
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)
    ax.yaxis.grid(True, color="#E0E0E0", lw=0.7)
    ax.set_axisbelow(True)
    if pct:
        ax.set_ylim(0, 104)


def stack(ax, subset, field, order, buckets, minw=0.62):
    """100% stacked partition; n printed under each label"""
    order = [v for v in order if any(r[field] == v for r in subset)]
    if not order:
        ax.axis("off"); return
    bot = np.zeros(len(order))
    for b, lbl, col in buckets:
        vals = [100 * sum(1 for r in subset if r[field] == v and r["bucket"] == b)
                / max(sum(1 for r in subset if r[field] == v), 1) for v in order]
        ax.bar(np.arange(len(order)), vals, minw, bottom=bot, label=lbl,
               color=col, edgecolor="white", lw=0.7)
        bot += np.array(vals)
    ns = [sum(1 for r in subset if r[field] == v) for v in order]
    ax.set_xticks(np.arange(len(order)))
    rot = 30 if field == "profile" else 0
    ax.set_xticklabels([f"{v}\nn={n}" for v, n in zip(order, ns)], fontsize=7,
                       rotation=rot, ha="right" if rot else "center")


# ---------- 1 + 2: say() by profile, by task ----------
fig, ax = plt.subplots(1, 2, figsize=(13, 4.2),
                       gridspec_kw={"width_ratios": [1, 2.4]})
m, s = zip(*[cellstat([r for r in rows if r["profile"] == p], "say_count")
             for p in PROF])
ax[0].bar(np.arange(5), m, 0.6, yerr=s, capsize=3, color=DARK,
          error_kw=dict(lw=0.9, alpha=0.6))
ax[0].set_xticks(np.arange(5)); ax[0].set_xticklabels(PLBL, fontsize=7.5)
style(ax[0], "utterances per run", f"say() by profile\n{SUB}")

m, s = zip(*[cellstat([r for r in rows if r["task"] == t], "say_count")
             for t in TASKS])
cols = [RED if v > 1.05 else DARK for v in m]
ax[1].bar(np.arange(len(TASKS)), m, 0.6, yerr=s, capsize=2, color=cols,
          error_kw=dict(lw=0.8, alpha=0.6))
ax[1].set_xticks(np.arange(len(TASKS))); ax[1].set_xticklabels(TASKS, fontsize=8)
style(ax[1], "", "say() by task   (red = more than one utterance)")
fig.tight_layout(); fig.savefig(p("fig1_say_by_profile_and_task.png"), dpi=200,
                                bbox_inches="tight")

# ---------- 3: say() task x profile heatmap ----------
M = np.array([[cellstat([r for r in rows if r["task"] == t and r["profile"] == p],
                        "say_count")[0] for p in PROF] for t in TASKS])
fig, ax = plt.subplots(figsize=(6.4, 0.42 * len(TASKS) + 1.6))
im = ax.imshow(M, cmap="YlOrRd", aspect="auto", vmin=0)
ax.set_xticks(np.arange(5)); ax.set_xticklabels(PROF, rotation=30, ha="right", fontsize=8)
ax.set_yticks(np.arange(len(TASKS))); ax.set_yticklabels(TASKS, fontsize=8)
for i in range(len(TASKS)):
    for j in range(5):
        ax.text(j, i, f"{M[i, j]:.1f}", ha="center", va="center", fontsize=7.5,
                color="white" if M[i, j] > M.max() * 0.6 else "#212121")
ax.set_title(f"say() count: task x profile\n{SUB}", fontsize=10, fontweight="bold")
fig.colorbar(im, ax=ax, shrink=0.6, label="utterances per run")
fig.tight_layout(); fig.savefig(p("fig2_say_task_x_profile.png"), dpi=200,
                                bbox_inches="tight")

# ---------- 4: when say() is used + actions/primitives ----------
fig, ax = plt.subplots(1, 2, figsize=(12, 6.2),
                       gridspec_kw={"width_ratios": [1, 1.15]})
bot = np.zeros(len(PROF))
for k, lbl, col in (("say_before_action", "before any action", DARK),
                    ("say_mid", "between actions\n(mid-task)", MID),
                    ("say_after_all", "after last action", RED)):
    vals = [100 * sum(r[k] for r in rows if r["profile"] == p)
            / max(sum(r["say_count"] for r in rows if r["profile"] == p), 1)
            for p in PROF]
    ax[0].bar(np.arange(5), vals, 0.6, bottom=bot, label=lbl, color=col,
              edgecolor="white", lw=0.7)
    bot += np.array(vals)
ax[0].set_xticks(np.arange(5)); ax[0].set_xticklabels(PLBL, fontsize=7.5)
style(ax[0], "% of utterances", f"WHEN say() is used, by profile\n{SUB}", pct=True)
ax[0].legend(frameon=False, fontsize=8, ncol=3, loc="upper center",
             bbox_to_anchor=(0.5, -0.16))

# right panel: physical work vs speech, as a diverging pair per task.
# A grouped bar chart mixes quantities on different scales (up to 8 actions vs
# ~1 utterance) and hides the thing that matters -- the GAP between them. A
# back-to-back layout makes "8 actions, 2 utterances" readable at a glance.
order = sorted(TASKS, key=lambda t: -cellstat([r for r in rows if r["task"] == t],
                                              "total_actions")[0])
acts = [cellstat([r for r in rows if r["task"] == t], "total_actions")[0] for t in order]
says = [cellstat([r for r in rows if r["task"] == t], "say_count")[0] for t in order]
prims = [cellstat([r for r in rows if r["task"] == t], "primitive_calls")[0] for t in order]
y = np.arange(len(order))
ax[1].barh(y, [-a for a in acts], 0.66, color=MID, label="physical actions")
ax[1].barh(y, says, 0.66, color=DARK, label="utterances heard")
if any(prims):
    ax[1].barh(y, prims, 0.66, left=says, color=GREEN, label="verified primitives")
for i, (a, sy) in enumerate(zip(acts, says)):
    if a: ax[1].text(-a - 0.18, i, f"{a:.0f}", va="center", ha="right", fontsize=7.5)
    ax[1].text(sy + 0.18, i, f"{sy:.1f}", va="center", fontsize=7.5, fontweight="bold")
ax[1].axvline(0, color="#455A64", lw=1)
ax[1].set_yticks(y); ax[1].set_yticklabels(order, fontsize=7.5)
ax[1].invert_yaxis()
lo = min(acts + [0]); hi = max(says + [1])
ax[1].set_xlim(-max(acts) - 1.4, hi + 1.4)
ax[1].set_xticks(np.arange(-int(max(acts)), int(hi) + 1, 2))
ax[1].set_xticklabels([str(abs(v)) for v in
                       np.arange(-int(max(acts)), int(hi) + 1, 2)], fontsize=8)
ax[1].set_xlabel("<-- actions taken        utterances -->", fontsize=8.5)
ax[1].set_title("Physical work vs speech, per task", fontsize=11, fontweight="bold")
ax[1].spines[["top", "right", "left"]].set_visible(False)
ax[1].xaxis.grid(True, color="#E0E0E0", lw=0.7); ax[1].set_axisbelow(True)
ax[1].legend(frameon=False, fontsize=8, ncol=3, loc="upper center",
             bbox_to_anchor=(0.5, -0.12))
fig.tight_layout(); fig.savefig(p("fig3_when_and_actions.png"), dpi=200,
                                bbox_inches="tight")

# ---------- 5: FAILED runs, split by failure type ----------
FB = [("correct_report", "reported the failure", GREEN),
      ("false_confirm", "claimed success anyway", RED),
      ("silent", "said nothing", AMBER)]
no_att = [r for r in rows if r["failure_type"] == "no_attempt"]
att = [r for r in rows if r["failure_type"] == "attempted"]
fig, axes = plt.subplots(2, 2, figsize=(13, 8),
                         gridspec_kw={"width_ratios": [1, 2.2]})
for row, (sub, name) in enumerate(((no_att, "NO ATTEMPT (never moved)"),
                                   (att, "ATTEMPTED (acted, then failed)"))):
    stack(axes[row][0], sub, "profile", PROF, FB)
    style(axes[row][0], "% of failed runs", f"{name}\nby profile", pct=True)
    stack(axes[row][1], sub, "task", TASKS, FB)
    style(axes[row][1], "", f"{name}  (n={len(sub)})\nby task", pct=True)
axes[0][1].legend(frameon=False, fontsize=8, ncol=3, loc="upper center",
                  bbox_to_anchor=(0.5, 1.30))
fig.suptitle(f"What the user hears when the task FAILS   [{SUB}]", fontsize=13,
             fontweight="bold", y=1.0)
fig.tight_layout(); fig.savefig(p("fig4_failed_runs.png"), dpi=200, bbox_inches="tight")

# ---------- 6: SUCCESS runs ----------
SB = [("correct_report", "reported the success", GREEN),
      ("false_alarm", "claimed failure anyway", RED),
      ("silent", "said nothing", AMBER)]
succ = [r for r in rows if r["truth"]]
fig, ax = plt.subplots(1, 2, figsize=(13, 4.4),
                       gridspec_kw={"width_ratios": [1, 2.2]})
stack(ax[0], succ, "profile", PROF, SB)
style(ax[0], "% of successful runs", "by profile", pct=True)
stack(ax[1], succ, "task", TASKS, SB)
style(ax[1], "", "by task", pct=True)
ax[1].legend(frameon=False, fontsize=8, ncol=3, loc="upper center",
             bbox_to_anchor=(0.5, 1.16))
fig.suptitle(f"What the user hears when the task SUCCEEDS  (n={len(succ)})   [{SUB}]",
             fontsize=13, fontweight="bold", y=1.02)
fig.tight_layout(); fig.savefig(p("fig5_success_runs.png"), dpi=200, bbox_inches="tight")

# ---------- 7: what is being said ----------
fig, ax = plt.subplots(1, 2, figsize=(13, 4.6),
                       gridspec_kw={"width_ratios": [1, 1.5]})
tot_say = sum(r["say_count"] for r in rows) or 1
share = [100 * sum(r[f"say_{c}"] for r in rows) / tot_say for c in CODES]
o = np.argsort(share)[::-1]
ax[0].barh([CODES[i] for i in o][::-1], [share[i] for i in o][::-1],
           color=DARK, height=0.6)
for i, v in enumerate([share[i] for i in o][::-1]):
    ax[0].text(v + 1.2, i, f"{v:.0f}%", va="center", fontsize=9, fontweight="bold")
ax[0].set_xlim(0, 105)
ax[0].set_xlabel("% of all utterances", fontsize=9)
ax[0].set_title(f"What is being said\n{SUB}", fontsize=10, fontweight="bold")
ax[0].spines[["top", "right"]].set_visible(False)
ax[0].xaxis.grid(True, color="#E0E0E0", lw=0.7); ax[0].set_axisbelow(True)

H = np.array([[100 * sum(r[f"say_{c}"] for r in rows if r["task"] == t)
               / max(sum(r["say_count"] for r in rows if r["task"] == t), 1)
               for c in CODES] for t in TASKS])
im = ax[1].imshow(H, cmap="Blues", aspect="auto", vmin=0, vmax=100)
ax[1].set_xticks(np.arange(len(CODES)))
ax[1].set_xticklabels(CODES, rotation=35, ha="right", fontsize=8)
ax[1].set_yticks(np.arange(len(TASKS))); ax[1].set_yticklabels(TASKS, fontsize=7.5)
ax[1].set_title("category share, by task", fontsize=11, fontweight="bold")
fig.colorbar(im, ax=ax[1], shrink=0.7, label="% of that task's utterances")
fig.tight_layout(); fig.savefig(p("fig6_say_content.png"), dpi=200, bbox_inches="tight")

print(f"wrote 6 figures to {OUT}/  ({SUB})")