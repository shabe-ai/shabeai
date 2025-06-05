import openai, os, json
from typing import Callable, Any, Dict
import uuid

# --- map handler names -> (callable, schema) -------------------------------

# pick a model that supports tools
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")      # <- full model

SYSTEM_PROMPT = (
    "You are an assistant for a chat-only CRM. "
    "Always respond with a function call that matches the user's intent; "
    "never answer with plain text."
)

def _schema(name, desc, params):
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": desc,
            "parameters": {
                "type": "object",
                "properties": params,
                "required": list(params),
            },
        },
    }

REGISTRY: dict[str, tuple[Callable, dict]] = {}

def register(name: str, schema: dict):
    def decorator(fn: Callable):
        REGISTRY[name] = (fn, schema)
        return fn
    return decorator

# -- register wrappers around your existing handle() logic ------------------

@register(
    "add_account",
    _schema("add_account", "Create a CRM account", {"name": {"type": "string"}}),
)
def add_account_nl(ctx, name: str):
    return ctx["handle"](f"add account {name}", ctx["user"])

@register(
    "add_lead",
    _schema("add_lead", "Create a lead under current user", {"email": {"type": "string"}}),
)
def add_lead_nl(ctx, email: str):
    return ctx["handle"](f"add lead {email}", ctx["user"])

@register(
    "attach_lead",
    _schema(
        "attach_lead",
        "Attach an existing lead to an account",
        {"email": {"type": "string"}, "account": {"type": "string"}},
    ),
)
def attach_lead_nl(ctx, email: str, account: str):
    return ctx["handle"](f"attach lead {email} to {account}", ctx["user"])

@register(
    "report_funnel",
    _schema("report_funnel", "Show funnel chart", {}),
)
def funnel_nl(ctx):
    return ctx["handle"]("reports funnel", ctx["user"])

@register(
    "report_winrate",
    _schema("report_winrate", "Show win-rate text", {}),
)
def winrate_nl(ctx):
    return ctx["handle"]("reports winrate", ctx["user"])

# ---------- NEW TOOL REGISTRATIONS -----------------------------------------

@register(
    "find_leads",
    _schema(
        "find_leads",
        "Search leads by tag, email or account name",
        {"term": {"type": "string"}},
    ),
)
def find_leads_nl(ctx, term: str):
    return ctx["handle"](f"find {term}", ctx["user"])

@register(
    "list_leads",
    _schema("list_leads", "List all leads for the current user", {}),
)
def list_leads_nl(ctx):
    return ctx["handle"]("list leads", ctx["user"])

@register(
    "tag_lead",
    _schema(
        "tag_lead",
        "Add a tag to a lead",
        {"email": {"type": "string"}, "tag": {"type": "string"}},
    ),
)
def tag_lead_nl(ctx, email: str, tag: str):
    return ctx["handle"](f"tag lead {email} {tag}", ctx["user"])

@register(
    "update_stage",
    _schema(
        "update_stage",
        "Change the pipeline stage of a lead",
        {
            "email": {"type": "string"},
            "stage": {
                "type": "string",
                "enum": ["new", "qualified", "proposal", "won", "lost"],
            },
        },
    ),
)
def update_stage_nl(ctx, email: str, stage: str):
    return ctx["handle"](f"set stage of {email} to {stage}", ctx["user"])

# ---------------------------------------------------------------------------

def call_openai(prompt: str) -> Dict[str, Any] | None:
    """Return a tool call dict (name + arguments) or None."""
    tool_defs = [schema for _, schema in REGISTRY.values()]  # schemas are already wrapped

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": prompt},
    ]

    resp = openai.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        tools=tool_defs,
        tool_choice="auto",
        temperature=0.0,
    )

    msg = resp.choices[0].message
    if msg.tool_calls:
        return msg.tool_calls[0]   # name + arguments
    return None

def dispatch(prompt: str, ctx) -> str | Any:
    tc = call_openai(prompt)
    if not tc:
        return None  # let fallback say "sorry"
    name = tc.function.name
    args = json.loads(tc.function.arguments or "{}")
    fn, _ = REGISTRY[name]
    return fn(ctx, **args) 