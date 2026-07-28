"""
narration_demo.py -- Goal 3. Runs a policy ONE STATEMENT AT A TIME and shows:
  >>> the currently executing line
  [robot] everything said so far
Works on the fast custom sim (instant) or the robosuite arm (real motion).

Run:  python narration_demo.py                       demo policy, fast sim
      python narration_demo.py robosuite             demo policy, Panda arm
      python narration_demo.py <policy.py>           your generated file, fast sim
      python narration_demo.py <policy.py> robosuite your file, Panda arm

For a video: run with robosuite + render (see note at bottom) and screen-record
with QuickTime; the terminal shows line + narration in sync with the arm.
"""
import ast, sys, time, pathlib

DEMO = """
confirm_before('put the blue block on the green block')
put_first_on_second('blue block', 'green block')
say_progress(1, 1, 'placement finished, checking')
say_verified(lambda: is_placed('blue block', 'green block'),
             'Done. Verified the placement.',
             'The placement failed.')
pause_for_verification(1)
describe_scene()
"""

def load_policy(path):
    txt = pathlib.Path(path).read_text()
    return "\n".join(l for l in txt.splitlines() if not l.startswith("#"))

def run_narrated(env, ns, code, delay=0.4):
    said = 0
    tree = ast.parse(code)
    for node in tree.body:
        src = ast.get_source_segment(code, node)
        print(f"\n>>> {src}")
        try:
            exec(compile(ast.Module(body=[node], type_ignores=[]), "<policy>", "exec"), ns)
        except Exception as e:
            print(f"    [runtime failure] {type(e).__name__}: {e}")
        for msg in env.transcript[said:]:
            print(f"    [robot] {msg}")
        said = len(env.transcript)
        time.sleep(delay)
    print("\n--- end state ---")
    for n in env.get_obj_names():
        p = env.get_obj_pos(n)
        print(f"  {n}: ({p[0]:.2f}, {p[1]:.2f}, {p[2]:.2f})")

if __name__ == "__main__":
    args = sys.argv[1:]
    use_rs = "robosuite" in args
    files = [a for a in args if a.endswith(".py")]
    if use_rs:
        from robosuite_shim import RoboSuiteTabletop, build_namespace
        env = RoboSuiteTabletop()          # render=True for a live window on Mac
    else:
        from cap_sim import TabletopSim, build_namespace
        env = TabletopSim()
    from cap_primitives import make_primitives
    ns = {**build_namespace(env), **make_primitives(env)}
    code = load_policy(files[0]) if files else (
        DEMO if use_rs else DEMO.replace("'green block')", "'yellow bowl')"))
    run_narrated(env, ns, code)

# Live-view note (Mac): RoboSuiteTabletop(render=True) opens a mujoco viewer window,
# and each env.step renders. Screen-record window + terminal side by side.
