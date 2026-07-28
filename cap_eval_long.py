import requests, datetime, pathlib
from anthropic import Anthropic
from openai import OpenAI

PROMPT_URL = "https://code-as-policies.github.io/prompts/tabletop_ui.txt"
cap_prompt = requests.get(PROMPT_URL).text

# LONGER tasks = more actions and more narration opportunities,
# so density differences between conditions can actually show up.
TASKS = {
    "T6_long":     "put every block in a bowl, then move them all onto the red bowl, then tell me the final arrangement.",
    "T7_sort":     "sort the blocks into the bowl of the matching color and report each one as you go.",
    "T8_sequence": "move the blue block to the red bowl, then move the green block to where the blue block was, then confirm everything is where it should be.",
}

SYSTEM = (
    "You write Python robot policy code in the Code-as-Policies style. "
    "You will see many example pairs: an English command as a # comment, then the code that does it. "
    "For the FINAL command, write ONLY the code that should follow it. "
    "No explanations, no markdown fences, match the style and only call functions shown in the examples."
)

# third block so long tasks aren't degenerate
SCENE = ['blue block', 'green block', 'red block', 'yellow bowl', 'green bowl', 'red bowl']

PROFILE_BLIND = ("User profile: The user is blind and monitors you only by sound and touch. "
                 "Tell them what they cannot see. Be specific about what you are doing and whether it worked.\n")
PROFILE_BUSY  = ("User profile: The user is sighted and busy. "
                 "Only speak if something goes wrong or needs their attention.\n")
PRIMITIVES = pathlib.Path("cap_prompt_primitives.txt").read_text()

CONDITIONS = {
    "baseline":      "",
    "profile_blind": PROFILE_BLIND,
    "profile_busy":  PROFILE_BUSY,
    "primitives":    PRIMITIVES,
}

def build_user_msg(command, condition_text):
    return condition_text + "\n" + cap_prompt + f"\nobjects = {SCENE}\n# {command}\n"

claude = Anthropic(); openai_client = OpenAI()
CLAUDE_MODEL = "claude-opus-4-5"; OPENAI_MODEL = "gpt-5.2"

def gen_claude(command, cond):
    r = claude.messages.create(model=CLAUDE_MODEL, max_tokens=1500, system=SYSTEM,
        messages=[{"role":"user","content":build_user_msg(command, cond)}])
    return r.content[0].text

def gen_openai(command, cond):
    r = openai_client.chat.completions.create(model=OPENAI_MODEL,
        messages=[{"role":"system","content":SYSTEM},
                  {"role":"user","content":build_user_msg(command, cond)}])
    return r.choices[0].message.content

stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
out = pathlib.Path(f"cap_runs_long_{stamp}"); out.mkdir(exist_ok=True)

for cond_name, cond_text in CONDITIONS.items():
    for tid, command in TASKS.items():
        for provider, fn in [("claude", gen_claude), ("openai", gen_openai)]:
            for run in (1, 2, 3):
                code = fn(command, cond_text)
                f = out / f"{cond_name}_{tid}_{provider}_run{run}.py"
                f.write_text(f"# CONDITION: {cond_name}\n# SCENE: {SCENE}\n"
                             f"# COMMAND: {command}\n# MODEL: {provider}\n\n{code}\n")
                print(f"\n{'='*70}\n{cond_name} | {tid} | {provider} | run {run}\n{'-'*70}\n{code}")
