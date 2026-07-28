"""
diag.py -- just for diagnosis to find WHERE the time goes.

  python3 diag.py # times each stage separately
  python3 diag.py --sim # also times a headless S1 execution
"""
import sys, time, os

print("=" * 60)
print("1. CaP prompt fetch")
print("=" * 60)
import pathlib, requests
URL = "https://code-as-policies.github.io/prompts/tabletop_ui.txt"
cache = pathlib.Path("cap_tabletop_ui.txt")
if cache.exists():
    print(f"   cached already: {len(cache.read_text())} chars, 0.0s")
else:
    t = time.time()
    try:
        r = requests.get(URL, timeout=20)
        print(f"   HTTP {r.status_code}, {len(r.text)} chars, {time.time()-t:.1f}s")
        if r.ok:
            cache.write_text(r.text); print(f"   cached -> {cache}")
    except Exception as e:
        print(f"   FAILED after {time.time()-t:.1f}s: {type(e).__name__}: {e}")
        print("   ^ this was hanging your runs (no timeout before)")

print()
print("=" * 60)
print("2. LLM call")
print("=" * 60)
for name, key in (("claude", "ANTHROPIC_API_KEY"), ("openai", "OPENAI_API_KEY")):
    if not os.environ.get(key):
        print(f"   {name}: {key} not set, skipping"); continue
    t = time.time()
    try:
        if name == "claude":
            from anthropic import Anthropic
            r = Anthropic(timeout=120.0).messages.create(
                model="claude-opus-4-5", max_tokens=50,
                messages=[{"role": "user", "content": "reply with the word ok"}])
            txt = r.content[0].text
        else:
            from openai import OpenAI
            r = OpenAI(timeout=120.0).chat.completions.create(
                model="gpt-5.2",
                messages=[{"role": "user", "content": "reply with the word ok"}])
            txt = r.choices[0].message.content
        print(f"   {name}: {time.time()-t:.1f}s -> {txt.strip()[:30]!r}")
    except Exception as e:
        print(f"   {name}: FAILED after {time.time()-t:.1f}s: {type(e).__name__}: {e}")

print()
print("=" * 60)
print("3. env creation (headless)")
print("=" * 60)
import tasks
for tid in ("S1", "S4"):
    t = time.time()
    env, _ = tasks.make_env(tid)
    print(f"   {tid}: {time.time()-t:.1f}s   scene={env.get_obj_names()}")
    env.close()

if "--sim" in sys.argv:
    print()
    print("=" * 60)
    print("4. sim execution, headless (no LLM)")
    print("=" * 60)
    from cap_primitives import make_primitives
    env, bn = tasks.make_env("S1")
    ns = {**bn(env), **make_primitives(env)}
    t = time.time()
    exec("put_first_on_second('red block', 'green block')", ns)
    print(f"   S1 motion: {time.time()-t:.1f}s   truth={tasks.TASKS['S1']['truth'](env)}")
    env.close()

print()
print("  stage 1 huge -> network/host problem (now cached + 20s timeout)")
print("  stage 2 huge -> API latency or a bad model name")
print("  stage 3/4 huge -> sim (use --render-every, or drop --render)")
