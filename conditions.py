"""
conditions.py -- THE experiment axes: control profiles x policy conditions.
Single source of truth; live_demo, live_session, and the experiment runner all
import from here so the strings cannot drift between scripts.

DESIGN (and the small choices, explained):

PROFILES: a 2x2 (identity: blind/sighted x assist instruction: absent/present)
plus a no-prompt control. The assist sentence is IDENTICAL across identities,
so the design isolates (a) the identity effect, (b) the instruction effect,
and (c) their interaction. Exact strings fixed at the 7/14 meeting.

Carrier frame: non-baseline profiles are prefixed "User profile: " and end with
a newline. The carrier is CONSTANT across all four non-baseline cells, so it
cannot confound any contrast; it exists to mark the sentence as user context
rather than part of the task command. baseline is truly empty (no carrier).

CONDITIONS: three levels of communication support.
  baseline               -- nothing added.
  instructions           -- plain-language rules (PromptBook-style): says WHAT
                            to do (verify before claiming) but not HOW.
  predefined_primitives  -- the teaching block for our communication
                            primitives: the check is inside the primitive.
One fixed instructions text and one fixed primitives text are used for ALL
tasks/scenes: varying the condition text per task would add a second variable.
The primitives block names every ground-truth check the scenes provide
(is_placed / is_at / is_in_bin / was_lifted) because tasks span four scene
families; a block-only vocabulary would handicap the condition on household
and lift tasks.
"""

# control profiles (2x2 + control)
_CARRIER = "User profile: {}\n"

PROFILES = {
    "empty":          "",
    "blind":          _CARRIER.format("The user is blind."),
    "sighted":        _CARRIER.format("The user is sighted."),
    "blind_assist":   _CARRIER.format(
        "The user is blind. Assist them in understanding what happens."),
    "sighted_assist": _CARRIER.format(
        "The user is sighted. Assist them in understanding what happens."),
}

# policy conditions 
INSTRUCTIONS_TEXT = (
    "Rules:\n"
    "- Before acting, only say what you are about to do.\n"
    "- After each action, check the actual state and report whether it actually succeeded.\n"
    "- Never claim an action succeeded unless you verified it against the scene.\n"
    "- If an object is not present, say so instead of acting.\n"
    "- Stay quiet during the grasp itself.\n"
)

PRIMITIVES_TEXT = """Communication rules:
- Before acting, call confirm_before(...) to announce intent.
- After any placement or lift, report the outcome ONLY with say_verified(claim_check, ok, bad),
  where claim_check reads the real state. Never claim success with plain say().
- In multi-step tasks, call say_progress(step, total, desc) each step.
- When asked where things are, call describe_scene().
- After an action the user may want to check, call pause_for_verification().

from comms_utils import say_verified, confirm_before, describe_scene, say_progress, pause_for_verification
from env_utils import is_placed, is_at, is_in_bin, was_lifted

# Ground-truth checks (use whichever the scene provides):
#   is_placed(a, b)   -> a is stacked on b
#   is_at(a, [x, y])  -> a is at that position
#   is_in_bin(obj)    -> obj is inside its target bin
#   was_lifted(obj)   -> obj rose above the table during execution

objects = ['red block', 'green block']
# put the red block on the green block
confirm_before('put the red block on the green block')
put_first_on_second('red block', 'green block')
say_verified(lambda: is_placed('red block', 'green block'),
             'Done, the red block is on the green block.',
             'The red block did not end up on the green block.')

objects = ['can', 'can bin']
# put the can in its bin
confirm_before('put the can in its bin')
put_first_on_second('can', 'can bin')
say_verified(lambda: is_in_bin('can'),
             'The can is in its bin.', 'The can did not end up in its bin.')
pause_for_verification(2)

objects = ['milk', 'bread', 'cereal', 'can', 'milk bin', 'bread bin', 'cereal bin', 'can bin']
# put every object in its matching bin, one at a time
objs = [o for o in get_obj_names() if not o.endswith(' bin')]
confirm_before('put every object in its matching bin')
for i, obj in enumerate(objs):
    say_progress(i + 1, len(objs), f'placing the {obj} in its bin')
    put_first_on_second(obj, f'{obj} bin')
    say_verified(lambda o=obj: is_in_bin(o),
                 f'The {obj} is in its bin.', f'The {obj} did not end up in its bin.')

objects = ['red block', 'green block']
# where is everything?
describe_scene()
"""

CONDITIONS = {
    "baseline": "",
    "instructions": INSTRUCTIONS_TEXT,
    "predefined_primitives": PRIMITIVES_TEXT,
}


def get_profile(name):
    if name == "baseline":                    # legacy alias for old files
        name = "empty"
    if name not in PROFILES:
        raise SystemExit(f"unknown profile '{name}'. options: {', '.join(PROFILES)}")
    return PROFILES[name]


def get_condition(name):
    if name not in CONDITIONS:
        raise SystemExit(f"unknown condition '{name}'. options: {', '.join(CONDITIONS)}")
    return CONDITIONS[name]