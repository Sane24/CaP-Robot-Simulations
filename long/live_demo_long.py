"""
live_demo_long.py -- LLM generates a LONG-task policy from the sim's real scene,
then it executes immediately on the rendered Panda arm with narration.
Same pipeline as live_demo.py, but the MultiBlock env (4 blocks) and tasks L1-L5.

  export ANTHROPIC_API_KEY=...  OPENAI_API_KEY=...
  mjpython live_demo_long.py --task L1 --condition primitives --profile blind --render --speak
  python3  live_demo_long.py --task L1 --condition promptbook --miss

  --task L1..L5   --condition baseline|promptbook|primitives
  --profile none|blind_bare|sighted|distracted|blind|busy
  --model claude|openai   --miss   --render   --speak
  --blocks "red block,green block,blue block,yellow block,orange block"
"""
import sys, pathlib, requests
import live_demo                      # SYSTEM, PROMPTBOOK, PROFILES, run_narrated
import long_tasks as LT


def get_condition(name):
    if name == "promptbook":
        return live_demo.PROMPTBOOK
    if name == "primitives":
        return pathlib.Path("cap_prompt_long.txt").read_text()
    return ""


def generate(model, profile_text, condition_text, command, scene):
    cap = requests.get("https://code-as-policies.github.io/prompts/tabletop_ui.txt").text
    user = profile_text + condition_text + "\n" + cap + f"\nobjects = {scene}\n# {command}\n"
    if model == "claude":
        from anthropic import Anthropic
        r = Anthropic().messages.create(model="claude-opus-4-5", max_tokens=1600,
            system=live_demo.SYSTEM, messages=[{"role": "user", "content": user}])
        return r.content[0].text
    from openai import OpenAI
    r = OpenAI().chat.completions.create(model="gpt-5.2",
        messages=[{"role": "system", "content": live_demo.SYSTEM},
                  {"role": "user", "content": user}])
    return r.choices[0].message.content


def main():
    # locals, not globals: mjpython clobbers a global named `task` when the viewer opens
    a = sys.argv
    g = lambda f, d: a[a.index(f) + 1] if f in a else d
    task, cond, prof, model = (g("--task", "L1"), g("--condition", "primitives"),
                               g("--profile", "none"), g("--model", "claude"))
    blocks = g("--blocks", "").split(",") if "--blocks" in a else None

    from robosuite_shim_long import MultiBlockTabletop, build_namespace
    from cap_primitives import make_primitives

    env = MultiBlockTabletop(blocks=blocks, render="--render" in a, verbose=False,
                             speak="--speak" in a)
    scene, command = env.get_obj_names(), LT.TASKS[task]
    print(f"\n{'='*72}\ntask: {task}   condition: {cond}   profile: {prof}   "
          f"miss: {'--miss' in a}\nscene: {scene}   <- read from the sim\n"
          f"command: {command}\n{'='*72}\ngenerating...")

    code = generate(model, live_demo.get_profile(prof), get_condition(cond), command, scene)
    print(f"\n\033[32m--- generated policy ---\033[0m\n{code}\n\033[32m--- executing ---\033[0m")

    ns = {**build_namespace(env), **make_primitives(env)}
    if "--miss" in a:
        real = env.put_first_on_second
        ns["put_first_on_second"] = lambda x, y, **k: real(x, y, _miss=True)

    live_demo.run_narrated(env, ns, code, pause=0.3)
    LT.verdict(env, task)


if __name__ == "__main__":
    main()
