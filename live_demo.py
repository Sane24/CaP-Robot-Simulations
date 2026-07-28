"""
live_demo.py -- generate a policy with the LLM, then IMMEDIATELY run it on the
rendered RoboSuite arm, statement by statement, with narration.

The scene sent to the LLM is read FROM THE SIM, so the generated code references
objects that actually exist. No name translation, no fake bowls.

  export ANTHROPIC_API_KEY=...   OPENAI_API_KEY=...

  mjpython live_demo.py --condition baseline --task S1 --render
  mjpython live_demo.py --condition baseline --task L1 --render
  mjpython live_demo.py --condition baseline --task S3 --render
  mjpython live_demo.py --condition baseline --task S4 --render
  mjpython live_demo.py --condition baseline --task S5 --render

  mjpython live_demo.py --condition promptbook --task S1 --render --miss
  python3  live_demo.py --condition baseline  --task T5            (headless)

  --condition  baseline | instructions | predefined_primitives   (see conditions.py)
  --profile    baseline | blind | sighted | blind_assist | sighted_assist
  --task       S1..S5 | L1..L5   (see tasks.py for the full registry + provenance)
  --model      claude | openai
  --miss       force the placement to fail (tests honest failure reporting)
  --render     open the MuJoCo window (requires mjpython on macOS)
  --render-every N   redraw only every Nth sim step (default 1). robosuite syncs
               the viewer inside EVERY env.step and on macOS that sync dominates
               wall time; N=4 is ~4x faster and still looks continuous.

CONDITION and PROFILE are independent axes and COMPOSE. The prompt is built as
    profile text + condition text + CaP flashcards + scene + command
so you can run e.g. primitives + blind (verified reporting, rich narration) vs
primitives + busy (verified reporting, minimal narration). That is the
personalization experiment: honesty and verbosity are separate knobs.
"""
import ast, sys, time, pathlib, requests
import tasks as task_registry
import conditions as axis                    # profiles + conditions, single source

TASKS = {tid: t["command"] for tid, t in task_registry.TASKS.items()}

SYSTEM = (
    "You write Python robot policy code in the Code-as-Policies style. "
    "You will see many example pairs: an English command as a # comment, then the code that does it. "
    "For the FINAL command, write ONLY the code that should follow it. "
    "No explanations, no markdown fences, match the style and only call functions shown in the examples."
)

PROFILES = axis.PROFILES
CONDITIONS = axis.CONDITIONS
get_profile = axis.get_profile
get_condition = axis.get_condition
PROMPTBOOK = axis.INSTRUCTIONS_TEXT          # back-compat alias


def generate(model, profile_text, condition_text, command, scene):
    cap_prompt = requests.get(
        "https://code-as-policies.github.io/prompts/tabletop_ui.txt").text
    user = (profile_text + condition_text + "\n" + cap_prompt
            + f"\nobjects = {scene}\n# {command}\n")
    if model == "claude":
        from anthropic import Anthropic
        r = Anthropic().messages.create(model="claude-opus-4-5", max_tokens=1000,
            system=SYSTEM, messages=[{"role": "user", "content": user}])
        return r.content[0].text
    from openai import OpenAI
    r = OpenAI().chat.completions.create(model="gpt-5.2",
        messages=[{"role": "system", "content": SYSTEM},
                  {"role": "user", "content": user}])
    return r.choices[0].message.content


def run_narrated(env, ns, code, pause=0.6):
    """execute one statement at a time, printing the live line + what the robot says"""
    said = 0
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        print(f"[the LLM emitted invalid python] {e}")
        return
    for node in tree.body:
        src = ast.get_source_segment(code, node)
        print(f"\n\033[36m>>> {src}\033[0m")
        try:
            exec(compile(ast.Module(body=[node], type_ignores=[]), "<policy>", "exec"), ns)
        except Exception as e:
            print(f"    \033[31m[runtime error] {type(e).__name__}: {e}\033[0m")
        for msg in env.transcript[said:]:
            print(f"    \033[33m[robot] {msg}\033[0m")
        said = len(env.transcript)
        time.sleep(pause)


def main():
    # NOTE: everything here must be a LOCAL, not a module global.
    # mjpython's UI dispatcher writes a variable named `task` into __main__'s
    # globals when the viewer launches (mujoco/viewer.py: launch_on_ui_thread),
    # which silently clobbers any module-level `task`. Locals are safe.
    a = sys.argv
    cond = a[a.index("--condition") + 1] if "--condition" in a else "predefined_primitives"
    prof = a[a.index("--profile") + 1] if "--profile" in a else "baseline"
    task = a[a.index("--task") + 1] if "--task" in a else "T1"
    model = a[a.index("--model") + 1] if "--model" in a else "claude"
    render = "--render" in a
    miss = "--miss" in a
    rev = int(a[a.index("--render-every") + 1]) if "--render-every" in a else 1

    from cap_primitives import make_primitives

    env, build_namespace = task_registry.make_env(task, render=render, render_every=rev)
    scene = env.get_obj_names()                 # ask the SIM what exists
    command = TASKS[task]

    print(f"\n{'='*70}\ncondition : {cond}\nprofile   : {prof}\nmodel     : {model}\n"
          f"scene     : {scene}   <- read from the sim\ncommand   : {command}\n"
          f"forced miss: {miss}\n{'='*70}")

    print("\ngenerating policy...")
    code = generate(model, get_profile(prof), get_condition(cond), command, scene)
    print(f"\n\033[32m--- LLM-generated policy ---\033[0m\n{code}\n"
          f"\033[32m--- executing on the arm ---\033[0m")

    ns = {**build_namespace(env), **make_primitives(env)}
    if miss:
        real = env.put_first_on_second
        ns["put_first_on_second"] = lambda x, y, **k: real(x, y, _miss=True)

    run_narrated(env, ns, code)

    task_registry.verdict(env, task)


if __name__ == "__main__":
    main()
