"""
run_policy.py -- execute a generated CaP policy against a sim env.
Works with cap_sim.TabletopSim or robosuite_shim.RoboSuiteTabletop.

  from cap_sim import TabletopSim
  from run_policy import run_policy
  run_policy(TabletopSim(), code, "label", primitives=True)
"""

def run_policy(env, code, label="", primitives=False):
    if hasattr(env, "bowls") and isinstance(getattr(env, "blocks", None), dict):
        from cap_sim import build_namespace          # custom sim
    else:
        from robosuite_shim import build_namespace   # robosuite
    ns = build_namespace(env)
    if primitives:
        from cap_primitives import make_primitives
        ns.update(make_primitives(env))
    env.transcript = []
    print(f"\n{'='*68}\nPOLICY: {label}\n{'-'*68}\n{code.strip()}\n{'-'*68}  execution:")
    err = None
    try:
        exec(code, ns)
    except Exception as e:
        err = f"{type(e).__name__}: {e}"
        print(f"  [runtime failure] {err}")
    print(f"{'-'*68}  end state:")
    for n in env.get_obj_names():
        p = env.get_obj_pos(n)
        print(f"  {n}: ({p[0]:.2f}, {p[1]:.2f}, {p[2]:.2f})")
    return {"label": label, "transcript": list(env.transcript), "error": err}
