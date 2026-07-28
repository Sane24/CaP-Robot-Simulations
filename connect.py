from robosuite_shim import RoboSuiteTabletop
from run_policy import run_policy
code = "\n".join(l for l in open("cap_runs_primitives_XXXX/primitives_T1_simple_claude_run1.py").read().splitlines() if not l.startswith("#"))
run_policy(RoboSuiteTabletop(), code.replace("yellow bowl", "green block"), "T1_on_arm", primitives=True)
