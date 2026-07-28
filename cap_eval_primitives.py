import requests, datetime, pathlib
from anthropic import Anthropic
from openai import OpenAI

# 1. real CaP flashcards
PROMPT_URL = "https://code-as-policies.github.io/prompts/tabletop_ui.txt"
cap_prompt = requests.get(PROMPT_URL).text

# 2. tasks (unchanged)
TASKS = {
    "T1_simple":       "put the blue block on the yellow bowl.",
    "T2_multistep":    "stack all the blocks with the green block on top.",
    "T3_failureprone": "put the purple block on the red bowl.",
    "T4_question":     "is the blue block to the left of the green bowl?",
    "T5_comms":        "put the blocks in the bowls and tell me what you're doing.",
}

SYSTEM = (
    "You write Python robot policy code in the Code-as-Policies style. "
    "You will see many example pairs: an English command as a # comment, then the code that does it. "
    "For the FINAL command, write ONLY the code that should follow it. "
    "No explanations, no markdown fences, match the style and only call functions shown in the examples."
)

# one fixed scene (Run 3 scene) so this is comparable to prior code-level runs
SCENE = ['blue block', 'green block', 'yellow bowl', 'green bowl', 'red bowl']

PROMPTBOOK = (
    "Rules:\n"
    "- Before acting, only say what you are about to do.\n"
    "- After each action, check the actual state and report whether it actually succeeded.\n"
    "- Never claim an action succeeded unless you verified it against the scene.\n"
    "- If an object is not present, say so instead of acting.\n"
    "- Stay quiet during the grasp itself.\n"
)

# the primitives teaching block: import line + flashcards + rules (see cap_prompt_primitives.txt)
PRIMITIVES = pathlib.Path("cap_prompt_primitives.txt").read_text()

# 3 conditions, held on the same scene/tasks/models so the ONLY variable is the prompt
CONDITIONS = {
    "baseline":   "",
    "promptbook": PROMPTBOOK,
    "primitives": PRIMITIVES,
}

def build_user_msg(command, condition_text):
    return condition_text + "\n" + cap_prompt + f"\nobjects = {SCENE}\n# {command}\n"

# 3. two models
claude = Anthropic()
openai_client = OpenAI()
CLAUDE_MODEL = "claude-opus-4-5"   # confirm strings with Mina
OPENAI_MODEL = "gpt-5.2"

def gen_claude(command, condition_text):
    r = claude.messages.create(model=CLAUDE_MODEL, max_tokens=1000,
        system=SYSTEM, messages=[{"role":"user","content":build_user_msg(command, condition_text)}])
    return r.content[0].text

def gen_openai(command, condition_text):
    r = openai_client.chat.completions.create(model=OPENAI_MODEL,
        messages=[{"role":"system","content":SYSTEM},
                  {"role":"user","content":build_user_msg(command, condition_text)}])
    return r.choices[0].message.content

# 4. generate + save every output (NO execution -- code-level analysis, like TODO 1)
stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
out = pathlib.Path(f"cap_runs_primitives_{stamp}"); out.mkdir(exist_ok=True)

for cond_name, cond_text in CONDITIONS.items():
    for tid, command in TASKS.items():
        for provider, fn in [("claude", gen_claude), ("openai", gen_openai)]:
            for run in (1, 2, 3):
                code = fn(command, cond_text)
                fname = out / f"{cond_name}_{tid}_{provider}_run{run}.py"
                fname.write_text(
                    f"# CONDITION: {cond_name}\n# SCENE: {SCENE}\n"
                    f"# COMMAND: {command}\n# MODEL: {provider}\n\n{code}\n"
                )
                print(f"\n{'='*70}\n{cond_name} | {tid} | {provider} | run {run}\n{'-'*70}\n{code}")
