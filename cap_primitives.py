"""
cap_primitives.py -- Goal 2. The five communication primitives as real functions.
Backing-agnostic: works on cap_sim.TabletopSim or robosuite_shim.RoboSuiteTabletop,
anything with say / get_obj_names / get_obj_pos / is_placed (+ optional hold).

Design principle: the correct check lives INSIDE (is_placed = ground truth).
The LLM decides *to* verify, never *how*.

Run:  python cap_primitives.py           (demo on the fast custom sim)
      python cap_primitives.py robosuite (demo on the Panda arm, ~1 min)
"""

def make_primitives(env):

    def say_verified(claim_check, success_msg, fail_msg):
        ok = bool(claim_check())
        env.last_verified_claim = ok        # machine-readable claim, no text parsing
        env.say(success_msg if ok else fail_msg)
        return ok

    def confirm_before(action_desc):
        env.say(f"About to {action_desc}.")

    def describe_scene(only_changed=False):
        snap = getattr(env, "_scene_snap", {})
        lines, new = [], {}
        for n in env.get_obj_names():
            p = env.get_obj_pos(n)
            new[n] = tuple(round(float(v), 3) for v in p)
            side = "left" if p[1] < -0.05 else "right" if p[1] > 0.05 else "center"
            if (not only_changed) or snap.get(n) != new[n]:
                lines.append(f"{n} on the {side}")
        env._scene_snap = new
        env.say((("Now changed: " if only_changed else "I see: ") + ", ".join(lines) + ".")
                if lines else "Nothing has changed.")

    def say_progress(step, total, desc=""):
        env.say(f"Step {step} of {total}" + (f": {desc}" if desc else "") + ".")

    def pause_for_verification(seconds=2.0):
        env.say(f"Pausing {seconds:g}s so you can check by touch. Holding still.")
        if hasattr(env, "hold"):
            env.hold(seconds)
        env.say("Resuming.")

    ns = {"say_verified": say_verified, "confirm_before": confirm_before,
          "describe_scene": describe_scene, "say_progress": say_progress,
          "pause_for_verification": pause_for_verification,
          "is_placed": env.is_placed}
    # spatial-arrangement checkers. Without these, say_verified has nothing to
    # check for line/position tasks and the policy falls back to unverified say().
    for chk in ("is_in_line", "is_near_top"):
        if hasattr(env, chk):
            ns[chk] = getattr(env, chk)
    return ns


if __name__ == "__main__":
    import sys
    demo = """
confirm_before('put the blue block on the green block')
put_first_on_second('blue block', 'green block')
pause_for_verification(1)
say_verified(lambda: is_placed('blue block', 'green block'),
             'Done. Verified the blue block is on the green block.',
             'The blue block did not end up on the green block.')
describe_scene()
"""
    if len(sys.argv) > 1 and sys.argv[1] == "robosuite":
        from robosuite_shim import RoboSuiteTabletop, build_namespace
        env = RoboSuiteTabletop()
    else:
        from cap_sim import TabletopSim, build_namespace
        env = TabletopSim()
        demo = demo.replace("'green block')", "'yellow bowl')").replace(
                            "on the green block", "in the yellow bowl")
    ns = {**build_namespace(env), **make_primitives(env)}
    exec(demo, ns)
    print("--- transcript ---")
    for line in env.transcript: print(" ", line)
