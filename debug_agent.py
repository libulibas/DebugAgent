import os, sys
from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv()
MODEL = "claude-sonnet-4-20250514"

def claude(prompt, system="", max_tokens=2000):
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("Set ANTHROPIC_API_KEY (copy .env.example to .env).")
    c = Anthropic(api_key=key)
    kw = dict(model=MODEL, max_tokens=max_tokens,
              messages=[{"role": "user", "content": prompt}])
    if system:
        kw["system"] = system
    r = c.messages.create(**kw)
    return "".join(b.text for b in r.content if b.type == "text")



def debug(error: str, code: str) -> str:
    sys_p = ("You are a debugging expert. Output: ## Likely Root Cause, "
             "## Why It Happens, ## Step-by-step Fix, ## Corrected Code.")
    return claude(f"Error:\n{error}\n\nCode:\n```\n{code}\n```",
                  system=sys_p, max_tokens=2500)

if __name__ == "__main__":
    err = input("Paste error message: ")
    print("Paste code, end with Ctrl-D/Ctrl-Z:")
    code = sys.stdin.read()
    print(debug(err, code))
