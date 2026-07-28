"""
cap_eval_long_tasks.py -- GENERATION ONLY, for the 5 LONG tasks.
Same shape as cap_eval.py / cap_evalbase.py / cap_eval_primitives.py:
build the prompt, call both models, save every .py, print it. NO simulation.

  export ANTHROPIC_API_KEY=...  OPENAI_API_KEY=...
  python3 cap_eval_long_tasks.py                    # 3 cond x 5 tasks x 2 models x 3 runs = 90
  python3 cap_eval_long_tasks.py --profile blind    # add a user profile to every prompt
  python3 cap_eval_long_tasks.py --runs 1           # 30 generations

Outputs to cap_runs_long_<timestamp>/, one .py per generation.
Feed them to run_generated.py later, or just read/code them like the earlier runs.
"""
import requests, datetime, pathlib, sys
from anthropic import Anthropic
from openai import OpenAI
import live_demo                    # reuse SYSTEM, PROMPTBOOK, PROFILES
from long_tasks import TASKS

PROMPT_URL = "https://code-as-policies.github.io/prompts/tabletop_ui.txt"
cap_prompt = requests.get(PROMPT_URL).text

# the REAL MultiBlock scene: 4 blocks, no bowls (robosuite ships no bowl)
SCENE = ['red block', 'green block', 'blue block', 'yellow block']

CONDITIONS = {
    "baseline":   "",
    "promptbook": live_demo.PROMPTBOOK,
    "primitives": pathlib.Path("cap_prompt_long.txt").read_text(),
}

a = sys.argv
profile = a[a.index("--profile") + 1] if "--profile" in a else "none"
RUNS = int(a[a.index("--runs") + 1]) if "--runs" in a else 3
profile_text = live_demo.get_profile(profile)


def build_user_msg(command, condition_text):
    return (profile_text + condition_text + "\n" + cap_prompt
            + f"\nobjects = {SCENE}\n# {command}\n")


claude = Anthropic()
openai_client = OpenAI()
CLAUDE_MODEL = "claude-opus-4-5"      # confirm exact strings with Mina
OPENAI_MODEL = "gpt-5.2"


def gen_claude(command, cond):
    r = claude.messages.create(model=CLAUDE_MODEL, max_tokens=1600,
        system=live_demo.SYSTEM,
        messages=[{"role": "user", "content": build_user_msg(command, cond)}])
    return r.content[0].text


def gen_openai(command, cond):
    r = openai_client.chat.completions.create(model=OPENAI_MODEL,
        messages=[{"role": "system", "content": live_demo.SYSTEM},
                  {"role": "user", "content": build_user_msg(command, cond)}])
    return r.choices[0].message.content


stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
out = pathlib.Path(f"cap_runs_long_{stamp}"); out.mkdir(exist_ok=True)
total = len(CONDITIONS) * len(TASKS) * 2 * RUNS
print(f"{total} generations -> {out}/  (profile={profile}, scene={SCENE})\n")

for cond_name, cond_text in CONDITIONS.items():
    for tid, command in TASKS.items():
        for provider, fn in [("claude", gen_claude), ("openai", gen_openai)]:
            for run in range(1, RUNS + 1):
                code = fn(command, cond_text)
                f = out / f"{cond_name}_{tid}_{provider}_run{run}.py"
                f.write_text(f"# CONDITION: {cond_name}\n# PROFILE: {profile}\n"
                             f"# SCENE: {SCENE}\n# COMMAND: {command}\n"
                             f"# MODEL: {provider}\n\n{code}\n")
                print(f"\n{'='*70}\n{cond_name} | {tid} | {provider} | run {run}\n"
                      f"{'-'*70}\n{code}")
