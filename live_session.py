"""
live_session.py -- persistent robot session. The MuJoCo window opens ONCE and
stays open. You type commands, the LLM generates a policy, the arm executes it,
and the robot SPEAKS its narration out loud (macOS `say`).

  export ANTHROPIC_API_KEY=...  OPENAI_API_KEY=...
  mjpython live_session.py                    # window + voice
  mjpython live_session.py --quiet            # window, no voice
  python3  live_session.py --no-render        # voice only, no window

At the prompt:
  run primitives blind T1            generate + execute (condition, profile, task)
  run promptbook blind T1 miss       same, but force the placement to fail
  run baseline sighted T5
  say hello there                    make the robot speak a line (test the voice)
  reset                              re-randomize the cubes, window stays open
  scene                              print what the robot can see
  quit

conditions : baseline | instructions | predefined_primitives
profiles   : baseline | blind | sighted | blind_assist | sighted_assist
tasks      : S1-S5 (short) | L1-L5 (long) -- see tasks.py

The window stays responsive between commands because the sim idles (holding the
arm still) while waiting for you to type.
"""
import sys, select, time
import numpy as np
import live_demo
import tasks as task_registry
from robosuite_shim import _SAY_BIN
from cap_primitives import make_primitives

HOLD = np.concatenate([np.zeros(6), [-1]])


def prompt_while_stepping(env, ps="\033[1;36mrobot>\033[0m "):
    """Read a line of input WITHOUT freezing the viewer: keep stepping the sim
    (arm holds still) and poll stdin until a line arrives."""
    sys.stdout.write(ps)
    sys.stdout.flush()
    while True:
        if select.select([sys.stdin], [], [], 0.0)[0]:
            return sys.stdin.readline().strip()
        if env.render:
            env._step(HOLD)          # keeps the MuJoCo window alive + responsive
        else:
            time.sleep(0.05)


def do_run(state, parts, model, render, speak, render_every=1):
    cond = parts[0] if len(parts) > 0 else "predefined_primitives"
    prof = parts[1] if len(parts) > 1 else "baseline"
    task = parts[2] if len(parts) > 2 else "S1"
    miss = "miss" in parts
    if task not in task_registry.TASKS:
        print(f"unknown task '{task}'. options: {', '.join(task_registry.TASKS)}\n")
        return
    fam = task_registry.TASKS[task]["family"]
    if state["family"] != fam:                  # task lives in a different scene
        print(f"[scene change: {state['family']} -> {fam}; reopening the environment]")
        if state["env"] is not None:
            state["env"].close()
        state["env"], state["build_ns"] = task_registry.make_env(
            task, render=render, speak=speak, render_every=render_every)
        state["family"] = fam
    env, build_namespace = state["env"], state["build_ns"]

    env.reset()
    scene = env.get_obj_names()
    command = live_demo.TASKS[task]
    print(f"\n{'='*68}\ncondition: {cond}   profile: {prof}   task: {task}"
          f"   forced miss: {miss}\nscene: {scene}   <- read from the sim\n"
          f"command: {command}\n{'='*68}\ngenerating...")

    code = live_demo.generate(model, live_demo.get_profile(prof),
                              live_demo.get_condition(cond), command, scene)
    print(f"\n\033[32m--- generated policy ---\033[0m\n{code}\n"
          f"\033[32m--- executing ---\033[0m")

    ns = {**build_namespace(env), **make_primitives(env)}
    if miss:
        real = env.put_first_on_second
        ns["put_first_on_second"] = lambda x, y, **k: real(x, y, _miss=True)

    live_demo.run_narrated(env, ns, code, pause=0.3)

    task_registry.verdict(env, task)
    print()


def main():
    # locals, not globals: mjpython clobbers a global named `task` when the
    # viewer launches. see live_demo.main() for the full explanation.
    a = sys.argv
    render = "--no-render" not in a
    speak = "--quiet" not in a
    model = a[a.index("--model") + 1] if "--model" in a else "claude"
    rev = int(a[a.index("--render-every") + 1]) if "--render-every" in a else 1

    env, build_ns = task_registry.make_env("S1", render=render, speak=speak,
                                           render_every=rev)
    state = {"env": env, "build_ns": build_ns, "family": "stack"}
    print(f"\nrobot session ready. window={render}  voice={'on' if speak and _SAY_BIN else 'off'}")
    print("tasks: " + ", ".join(task_registry.TASKS))
    if speak and not _SAY_BIN:
        print("  (no `say` binary found, narration will be text only)")
    print("commands: run <condition> <profile> <task> [miss] | say <text> | reset | scene | quit\n")

    while True:
        try:
            line = prompt_while_stepping(state["env"])
        except (EOFError, KeyboardInterrupt):
            break
        if not line:
            continue
        parts = line.split()
        cmd = parts[0].lower()

        if cmd in ("quit", "exit", "q"):
            break
        elif cmd == "reset":
            state["env"].reset(); print("scene re-randomized, window still open\n")
        elif cmd == "scene":
            for n in state["env"].get_obj_names():
                p = state["env"].get_obj_pos(n)
                print(f"  {n}: ({p[0]:.3f}, {p[1]:.3f}, {p[2]:.3f})")
            print()
        elif cmd == "say":
            state["env"].say(" ".join(parts[1:]))
        elif cmd == "run":
            try:
                do_run(state, parts[1:], model, render, speak, rev)
            except Exception as e:
                print(f"\033[31m[error] {type(e).__name__}: {e}\033[0m\n")
        else:
            print("unknown. try: run primitives blind T1 miss | say hi | reset | scene | quit\n")

    state["env"].close()
    print("session ended.")


if __name__ == "__main__":
    main()
