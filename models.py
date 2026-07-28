"""
models.py -- the model axis. ONE place where model identifiers live, so every
generation is attributable to an exact, recorded model string.

  python3 models.py --list     ask each provider what YOUR key can actually use
  python3 models.py --ping     send a 5-token call to each configured model
  python3 models.py --show     print the pinned registry

"""
import os, sys, time

MODELS = {
    "claude": dict(provider="anthropic", model_id="claude-opus-4-8",
                   label="Claude Opus 4.8"),
    "openai": dict(provider="openai", model_id="gpt-5.2",
                   label="GPT-5.2"),
    "gemini": dict(provider="google", model_id="gemini-3.1-pro-preview",
                   label="Gemini 3.1 Pro"),
}
DEFAULT_MODELS = ["claude", "openai", "gemini"]

ENV_KEY = {"anthropic": "ANTHROPIC_API_KEY",
           "openai": "OPENAI_API_KEY",
           "google": "GEMINI_API_KEY"}

MAX_TOKENS = 1000          # same ceiling for every model: one less variable
TIMEOUT = 120.0
RETRIES = 2


def model_id(key):
    if key not in MODELS:
        raise SystemExit(f"unknown model '{key}'. options: {', '.join(MODELS)}")
    return MODELS[key]["model_id"]


def have_key(key):
    return bool(os.environ.get(ENV_KEY[MODELS[key]["provider"]]))


# generation
def generate(model_key, system, user):
    """Returns (text, meta). meta records the EXACT model id and token usage,
    which gets written into every cached generation's header."""
    m = MODELS[model_key]
    mid, prov = m["model_id"], m["provider"]
    t0 = time.time()

    if prov == "anthropic":
        from anthropic import Anthropic
        r = Anthropic(timeout=TIMEOUT, max_retries=RETRIES).messages.create(
            model=mid, max_tokens=MAX_TOKENS, system=system,
            messages=[{"role": "user", "content": user}])
        text = "".join(b.text for b in r.content if getattr(b, "type", "") == "text")
        usage = dict(input=r.usage.input_tokens, output=r.usage.output_tokens)

    elif prov == "openai":
        from openai import OpenAI
        r = OpenAI(timeout=TIMEOUT, max_retries=RETRIES).chat.completions.create(
            model=mid, messages=[{"role": "system", "content": system},
                                 {"role": "user", "content": user}])
        text = r.choices[0].message.content or ""
        u = getattr(r, "usage", None)
        usage = dict(input=getattr(u, "prompt_tokens", 0),
                     output=getattr(u, "completion_tokens", 0)) if u else {}

    elif prov == "google":
        from google import genai
        from google.genai import types
        client = genai.Client()                       # reads GEMINI_API_KEY
        r = client.models.generate_content(
            model=mid, contents=user,
            config=types.GenerateContentConfig(
                system_instruction=system, max_output_tokens=MAX_TOKENS))
        text = r.text or ""
        u = getattr(r, "usage_metadata", None)
        usage = dict(input=getattr(u, "prompt_token_count", 0),
                     output=getattr(u, "candidates_token_count", 0)) if u else {}
    else:
        raise SystemExit(f"unknown provider '{prov}'")

    return text, dict(model_key=model_key, model_id=mid, provider=prov,
                      seconds=round(time.time() - t0, 1), **usage)


# utilities
def list_available():
    """Ask each provider what this key can actually use. Pin from THIS list."""
    print("=" * 70)
    print("MODELS AVAILABLE TO YOUR KEYS  (pin exact ids from here)")
    print("=" * 70)

    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            from anthropic import Anthropic
            print("\nanthropic:")
            for m in Anthropic().models.list(limit=20).data:
                print(f"   {m.id}")
        except Exception as e:
            print(f"   anthropic list failed: {type(e).__name__}: {e}")
    else:
        print("\nanthropic: ANTHROPIC_API_KEY not set")

    if os.environ.get("OPENAI_API_KEY"):
        try:
            from openai import OpenAI
            ids = sorted(m.id for m in OpenAI().models.list().data)
            print("\nopenai (gpt* only):")
            for i in ids:
                if i.startswith("gpt"):
                    print(f"   {i}")
        except Exception as e:
            print(f"   openai list failed: {type(e).__name__}: {e}")
    else:
        print("\nopenai: OPENAI_API_KEY not set")

    if os.environ.get("GEMINI_API_KEY"):
        try:
            from google import genai
            print("\ngoogle (generateContent-capable):")
            for m in genai.Client().models.list():
                acts = getattr(m, "supported_actions", None) or []
                if (not acts) or ("generateContent" in acts):
                    print(f"   {m.name}")
        except Exception as e:
            print(f"   google list failed: {type(e).__name__}: {e}")
    else:
        print("\ngoogle: GEMINI_API_KEY not set")


def ping():
    print(f"{'key':8s} {'model_id':22s} {'status':10s} {'sec':>6s}  reply")
    print("-" * 70)
    for k in MODELS:
        if not have_key(k):
            print(f"{k:8s} {MODELS[k]['model_id']:22s} {'NO KEY':10s} "
                  f"{'-':>6s}  set {ENV_KEY[MODELS[k]['provider']]}")
            continue
        try:
            txt, meta = generate(k, "Reply with exactly: ok", "say ok")
            print(f"{k:8s} {meta['model_id']:22s} {'OK':10s} "
                  f"{meta['seconds']:>6.1f}  {txt.strip()[:24]!r}")
        except Exception as e:
            print(f"{k:8s} {MODELS[k]['model_id']:22s} {'FAILED':10s} "
                  f"{'-':>6s}  {type(e).__name__}: {str(e)[:60]}")


def show():
    print(f"{'key':8s} {'provider':10s} {'model_id':24s} {'key set':8s} label")
    print("-" * 76)
    for k, m in MODELS.items():
        print(f"{k:8s} {m['provider']:10s} {m['model_id']:24s} "
              f"{'yes' if have_key(k) else 'NO':8s} {m['label']}")
    print(f"\nmax_tokens={MAX_TOKENS}  timeout={TIMEOUT}s  retries={RETRIES}")


if __name__ == "__main__":
    a = sys.argv
    if "--list" in a:
        list_available()
    elif "--ping" in a:
        ping()
    else:
        show()
