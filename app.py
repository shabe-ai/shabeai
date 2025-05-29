import streamlit as st
from app.db import init_db, get_session
from app.models import Lead, Account
from sqlmodel import select

init_db()                              # ensure table exists
st.title("Chat CRM – Slice 1")

if "history" not in st.session_state:
    st.session_state.history = []

def handle(prompt: str) -> str:
    prompt = prompt.lower().strip()

    # ---- add account ----
    if prompt.startswith("add account"):
        name = prompt.replace("add account", "").strip()
        with get_session() as s:
            s.add(Account(name=name))
            s.commit()
        return f"🏢 Account '{name}' created."

    # ---- add lead ----
    if prompt.startswith("add lead"):
        email = prompt.split()[-1]
        with get_session() as s:
            s.add(Lead(email=email))
            s.commit()
        return f"✅ Lead {email} added."

    # ---- attach lead to account ----
    if prompt.startswith("attach lead"):
        # naive parse: "attach lead email to accountname"
        parts = prompt.split()
        email = parts[2]
        acct_name = parts[-1]
        with get_session() as s:
            acct = s.exec(select(Account).where(Account.name == acct_name)).first()
            if not acct:
                return f"Account '{acct_name}' not found."
            lead = s.exec(select(Lead).where(Lead.email == email)).first()
            if not lead:
                return f"Lead '{email}' not found."
            lead.account_id = acct.id
            s.add(lead)
            s.commit()
        return f"🔗 Attached {email} → {acct_name}."

    # ---- show leads for account ----
    if prompt.startswith("show leads for"):
        acct_name = prompt.replace("show leads for", "").strip()
        with get_session() as s:
            acct = s.exec(select(Account).where(Account.name == acct_name)).first()
            if not acct:
                return f"Account '{acct_name}' not found."
            rows = s.exec(select(Lead).where(Lead.account_id == acct.id)).all()
        if not rows:
            return f"No leads for {acct_name}."
        return "\n".join(f"• {l.email}" for l in rows)

    # ---- list leads ----
    if prompt.startswith("list leads"):
        with get_session() as s:
            rows = s.exec(select(Lead)).all()
        if not rows:
            return "No leads yet."
        return "\n".join(f"• {l.email}" for l in rows)

    return "Sorry, I don't understand yet."

prompt = st.chat_input("Say something…")
if prompt:
    answer = handle(prompt)
    st.session_state.history.append((prompt, answer))

for q, a in st.session_state.history:
    st.chat_message("user").write(q)
    st.chat_message("assistant").write(a)
