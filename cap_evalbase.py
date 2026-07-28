import requests, datetime, pathlib
from anthropic import Anthropic
from openai import OpenAI

# 1. real CaP flashcards
PROMPT_URL = "https://code-as-policies.github.io/prompts/tabletop_ui.txt"
cap_prompt = requests.get(PROMPT_URL).text

# 2. tasks (unchanged from prior runs)
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

# 3. ONE fixed scene. Must match the scene Run 3 actually used, or the
#    bare-vs-detailed comparison is not controlled. Confirm against Run 3 outputs.
SCENE = ['blue block', 'green block', 'yellow bowl', 'green bowl', 'red bowl']

# 4. TODO 1 conditions: bare labels, no instructions.
#    Same "User profile: ..." carrier frame as Run 3, so the ONLY thing removed
#    vs Run 3's detailed profiles is the instruction text = clean single variable.
CONDITIONS = {
    "profile_blind":         "User profile: The user is blind. Assist them accordingly.",
    "profile_sighted":       "User profile: The user is sighted. Assist them accordingly.",
    "profile_sighted_distracted": "User profile: The user is sighted but not currently looking at the robot. Assist them accordingly.",
}

def build_user_msg(command, condition_text):
    # bare label prepended at the top, same injection point Run 3 used
    return condition_text + "\n" + cap_prompt + f"\nobjects = {SCENE}\n# {command}\n"

# 5. two models
claude = Anthropic()
openai_client = OpenAI()
CLAUDE_MODEL = "claude-opus-4-5"  
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

# 6. run: conditions x tasks x models x runs, save every output
stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
out = pathlib.Path(f"cap_runs_bareprofiles_{stamp}"); out.mkdir(exist_ok=True)

for cond_name, cond_text in CONDITIONS.items():
    for tid, command in TASKS.items():
        for provider, fn in [("claude", gen_claude), ("openai", gen_openai)]:
            for run in (1, 2, 3):
                code = fn(command, cond_text)
                fname = out / f"{cond_name}_{tid}_{provider}_run{run}.py"
                fname.write_text(
                    f"# CONDITION: {cond_name} | {cond_text!r}\n"
                    f"# SCENE: {SCENE}\n"
                    f"# COMMAND: {command}\n"
                    f"# MODEL: {provider}\n\n{code}\n"
                )
                print(f"\n{'='*70}\n{cond_name} | {tid} | {provider} | run {run}\n{'-'*70}\n{code}")