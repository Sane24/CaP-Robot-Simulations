"""
live_session_long.py -- persistent session for the LONG tasks (L1-L5).
Window opens ONCE and stays open. Robot speaks its narration out loud.

  mjpython live_session_long.py                    # window + voice
  mjpython live_session_long.py --quiet            # window, no voice
  python3  live_session_long.py --no-render        # headless
  --blocks "red block,green block,blue block,yellow block,orange block"

At the prompt:
  run primitives blind L1          generate + execute
  run promptbook blind L1 miss     force placements to fail
  reset | scene | say <text> | quit

tasks      : L1 line near top | L2 tower red on top | L3 two corners + describe
             L4 3-block stack with checks | L5 warm left / cool right
conditions : baseline | promptbook | primitives
profiles   : none | blind_bare | sighted | distracted | blind | busy
"""
import sys, select, time
import numpy as np
import live_demo, live_demo_long as LD
import long_tasks as LT
from robosuite_shim_long import MultiBlockTabletop, build_namespace, _SAY_BIN
from cap_primitives import make_primitives

HOLD = np.concatenate([np.zeros(6), [-1]])


def prompt_while_stepping(env, ps="\033[1;36mrobot>\033[0m "):
    """Poll stdin while stepping the sim, so the window stays alive while you type."""
    sys.stdout.write(ps); sys.stdout.flush()
    while True:
        if select.select([sys.stdin], [], [], 0.0)[0]:
            return sys.stdin.readline().strip()
        if env.render:
            env._step(HOLD)
        else:
            time.sleep(0.05)


def do_run(env, parts, model):
    cond = parts[0] if len(parts) > 0 else "primitives"
    prof = parts[1] if len(parts) > 1 else "none"
    task = parts[2] if len(parts) > 2 else "L1"
    miss = "miss" in parts
    if task not in LT.TASKS:
        print(f"unknown task '{task}'. options: {', '.join(LT.TASKS)}\n"); return

    env.reset()
    scene, command = env.get_obj_names(), LT.TASKS[task]
    print(f"\n{'='*70}\ncondition: {cond}   profile: {prof}   task: {task}   miss: {miss}\n"
          f"scene: {scene}   <- read from the sim\ncommand: {command}\n{'='*70}\ngenerating...")

    code = LD.generate(model, live_demo.get_profile(prof), LD.get_condition(cond),
                       command, scene)
    print(f"\n\033[32m--- generated policy ---\033[0m\n{code}\n\033[32m--- executing ---\033[0m")

    ns = {**build_namespace(env), **make_primitives(env)}
    if miss:
        real = env.put_first_on_second
        ns["put_first_on_second"] = lambda x, y, **k: real(x, y, _miss=True)

    live_demo.run_narrated(env, ns, code, pause=0.3)
    LT.verdict(env, task)
    print()


def main():
    a = sys.argv
    g = lambda f, d: a[a.index(f) + 1] if f in a else d
    render = "--no-render" not in a
    speak = "--quiet" not in a
    model = g("--model", "claude")
    blocks = g("--blocks", "").split(",") if "--blocks" in a else None

    env = MultiBlockTabletop(blocks=blocks, render=render, verbose=False, speak=speak)
    print(f"\nlong-task session. blocks={env.get_obj_names()}")
    print(f"window={render}  voice={'on' if speak and _SAY_BIN else 'off'}")
    print("commands: run <condition> <profile> <task> [miss] | reset | scene | say <text> | quit")
    for k, v in LT.TASKS.items():
        print(f"  {k}: {v}")
    print()

    while True:
        try:
            line = prompt_while_stepping(env)
        except (EOFError, KeyboardInterrupt):
            break
        if not line: continue
        p = line.split(); cmd = p[0].lower()
        if cmd in ("quit", "exit", "q"): break
        elif cmd == "reset": env.reset(); print("scene re-randomized\n")
        elif cmd == "scene": print(LT.scene_report(env) + "\n")
        elif cmd == "say": env.say(" ".join(p[1:]))
        elif cmd == "run":
            try: do_run(env, p[1:], model)
            except Exception as e: print(f"\033[31m[error] {type(e).__name__}: {e}\033[0m\n")
        else: print("try: run primitives blind L1 miss | reset | scene | quit\n")

    env.close(); print("session ended.")


if __name__ == "__main__":
    main()
