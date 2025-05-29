import streamlit as st
from sqlmodel import select
from app.db import init_db, get_session
from app.models import Lead

init_db()                              # ensure table exists
st.title("Chat CRM – Slice 1")

if "history" not in st.session_state:
    st.session_state.history = []

def handle(prompt: str) -> str:
    prompt = prompt.lower().strip()

    # ---- add lead ----
    if prompt.startswith("add lead"):
        email = prompt.split()[-1]
        with get_session() as s:
            s.add(Lead(email=email))
            s.commit()
        return f"✅ Lead {email} added."

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
