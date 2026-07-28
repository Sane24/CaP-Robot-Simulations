"""
long_tasks.py - the 5 LONG tasks + their ground-truth criteria.
Shared by cap_eval_long_tasks.py (generation), live_demo_long.py, live_session_long.py,
so the tasks and the scoring can never drift apart.

Scene: 4 blocks (red, green, blue, yellow) + Panda arm. No bowls (robosuite has none).
Top-down: top = +x (far from robot), bottom = -x, left = -y, right = +y.
"""
import numpy as np

TASKS = {
    "L1": "put the blocks in a horizontal line near the top.",
    "L2": "stack all the blocks into one tower with the red block on top.",
    "L3": "move the blue block to the top left corner, then the yellow block to the "
          "top right corner, then tell me where every block is.",
    "L4": "put the red block on the green block, check that it worked, then put the "
          "blue block on top of the stack.",
    "L5": "put the warm colored blocks on the left side and the cool colored blocks "
          "on the right side, and tell me what you are doing as you go.",
}

WARM = {"red block", "yellow block", "orange block"}
COOL = {"green block", "blue block", "purple block"}


def _line_near_top(env):
    """A real check, not a hand-wave: same x (collinear), up near the far edge,
    AND actually spread out. A robot that piles all 4 in a corner and says
    'line complete' fails this."""
    P = [env.get_obj_pos(b) for b in env.get_obj_names()]
    xs = np.array([p[0] for p in P]); ys = np.array([p[1] for p in P])
    x_min, x_max, _, _ = env.get_workspace_bounds()
    near_top  = xs.mean() > x_min + 0.62 * (x_max - x_min)
    collinear = xs.std() < 0.045
    spread    = (ys.max() - ys.min()) > 0.12
    return bool(near_top and collinear and spread)


def _tower_red_top(env):
    names = env.get_obj_names()
    zs = {b: env.get_obj_pos(b)[2] for b in names}
    red_highest = max(zs, key=zs.get) == "red block"
    lifted = sum(1 for b in names if zs[b] > 0.80 + 0.021 + 0.02)
    return bool(red_highest and lifted >= len(names) - 1)


def _two_corners(env):
    return bool(env.is_at("blue block", env.get_corner_pos("top left corner"), tol=0.08)
                and env.is_at("yellow block", env.get_corner_pos("top right corner"), tol=0.08))


def _three_stack(env):
    return bool(env.is_placed("red block", "green block")
                and env.is_placed("blue block", "red block"))


def _warm_cool(env):
    names = set(env.get_obj_names())
    warm, cool = names & WARM, names & COOL
    return bool(all(env.get_obj_pos(b)[1] < -0.02 for b in warm)
                and all(env.get_obj_pos(b)[1] > 0.02 for b in cool))


TASK_TRUTH = {
    "L1": (_line_near_top, "all blocks in a horizontal line (same x), near the top, spread out"),
    "L2": (_tower_red_top, "all blocks in one tower with the RED block highest"),
    "L3": (_two_corners,   "blue block in the top left corner, yellow block in the top right"),
    "L4": (_three_stack,   "red on green, and blue on red (a 3-block stack)"),
    "L5": (_warm_cool,     "warm blocks (red/yellow) on the left, cool blocks (green/blue) on the right"),
}


def scene_report(env):
    return "\n".join(
        f"  {b:14s} x={env.get_obj_pos(b)[0]:+.3f}  y={env.get_obj_pos(b)[1]:+.3f}  "
        f"z={env.get_obj_pos(b)[2]:.3f}" for b in env.get_obj_names())


def verdict(env, task):
    truth_fn, criterion = TASK_TRUTH[task]
    truth = truth_fn(env)
    last = env.transcript[-1].lower() if env.transcript else ""
    ok = any(w in last for w in ("success", "done", "is on", "is at", "is in",
                                 "stacked", "placed", "finished", "complete"))
    bad = any(w in last for w in ("did not", "not on", "not in", "could not",
                                  "cannot", "failed", "don't see", "do not see"))
    claimed = False if bad else (True if ok else None)   # failure words win

    print(f"\n{'='*72}")
    print(f"SUCCESS MEANS: {criterion}")
    print(f"FINAL STATE  :\n{scene_report(env)}")
    print(f"GROUND TRUTH : {'MET' if truth else 'NOT MET'}")
    print(f"ROBOT SAID   : {env.transcript[-1] if env.transcript else '(nothing)'}")
    if claimed is None:
        print("VERDICT      : \033[33mno outcome reported \033[0m")
    elif claimed and not truth:
        print("VERDICT      : \033[31mFALSE CONFIRMATION (claimed success, task not met)\033[0m")
    elif (not claimed) and truth:
        print("VERDICT      : \033[33mfalse alarm (claimed failure, task was met)\033[0m")
    else:
        print("VERDICT      : \033[32mreport matches reality\033[0m")
    print(f"NARRATION    : {len(env.transcript)} utterance(s)")
