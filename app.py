import os
import re
import uuid
from io import StringIO

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from dotenv import load_dotenv
from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTStrategy, AuthenticationBackend
from sqlmodel import select, func

from app.audit import audit
from app.auth import fastapi_users
from app.db import init_db, get_session
from app.models import Lead, Account, Stage, AuditLog
from app.nl_router import dispatch
from app.reports import funnel_counts, win_rate
from app.text import h1, h2, h3, body, primary_btn, card
from app.utils import to_json_safe, to_uuid

# Inject the glassmorphic feel (must be at the very top)
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
  background: radial-gradient(circle at 60% 40%, #FFFBE6 0%, #F7F7F7 25%, #2E3740 100%) !important;
}
section[data-testid="stSidebar"] > div:first-child {
  background: rgba(17,23,28,0.85) !important;
  backdrop-filter: blur(16px);
  border-radius: 1.5rem 0 0 1.5rem;
  box-shadow: 0 0 32px 0 #3343;
  min-width: 320px;
}
section[data-testid="stSidebar"] img {
  margin: 0 auto;
  display: block;
}
section.main > div, [data-testid="stVerticalBlock"] > div:first-child {
  background: rgba(255,255,255,0.06);
  backdrop-filter: blur(16px);
  border-radius: 1rem;
  border:1px solid rgba(255,255,255,0.08);
}
button[kind="primary"], .stButton>button {
  background:#F9C941 !important;
  border-radius:.5rem !important;
  box-shadow:0 0 12px #F9C94188 !important;
  font-weight: 600;
  font-family: 'Figtree', sans-serif;
}
button[kind="primary"]:hover, .stButton>button:hover{
  background:#FFE875 !important;
}
input, textarea, .stTextInput>div>div>input {
  background:rgba(255,255,255,0.06) !important;
  backdrop-filter:blur(8px) !important;
  border:1px solid rgba(255,255,255,0.12) !important;
  border-radius:2rem !important;
  color:#1E2429 !important;
}
</style>
""", unsafe_allow_html=True)

load_dotenv()

# Set default Plotly colors
px.defaults.color_discrete_sequence = ["#F9C941", "#FFE875", "#D9D2C7", "#1E2429"]

def read_csv_any_encoding(raw: bytes) -> pd.DataFrame:
    """Try common encodings to read CSV data."""
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return pd.read_csv(StringIO(raw.decode(enc)))
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("Could not decode CSV with common encodings.")

# auto-fetch current user if token already stored
if "access_token" in st.session_state and "current_user" not in st.session_state:
    r = requests.get(
        "http://localhost:8000/users/me",
        cookies={"crm-auth": st.session_state.access_token},
        timeout=5,
    )
    if r.status_code == 200:
        st.session_state.current_user = r.json()
    else:
        st.session_state.pop("access_token")   # token expired → force re-login

init_db()                              # ensure table exists

# Ensure chat history is initialized before any access
if "history" not in st.session_state:
    st.session_state.history = []

# --- Custom Layout: Sidebar and Main ---
sidebar_col, main_col = st.columns([0.32, 0.68], gap="large")

with sidebar_col:
    st.markdown(
        '''
        <div class="glass-tile">
            <img src="assets/shabe_logo_centered_white.png" alt="Shabe AI logo" />
        </div>
        <div class="shabe-logo" style="justify-content:center; margin-bottom:2rem;">
            <span style="font-family:'Bricolage Grotesque',sans-serif;font-size:2rem;color:var(--clr-gold);font-weight:700;">shabe ai</span>
        </div>
        <div class="sidebar-menu">
            <div class="menu-item active"><span class="menu-icon">📄</span> CSV import</div>
            <div class="menu-item"><span class="menu-icon">💬</span> Chat</div>
            <div class="menu-item"><span class="menu-icon">ℹ️</span> Audit</div>
            <div class="menu-item"><span class="menu-icon">⚙️</span> Settings</div>
        </div>
        ''', unsafe_allow_html=True
    )

    # ---------- CSV Import ----------
    st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
    st.markdown("**Upload a CSV with columns: email, account, tags (optional)**")
    csv_file = st.file_uploader(
        "Upload CSV",
        type=["csv"],
        key="csv_uploader",
    )
    if csv_file is not None:
        bytes_data = csv_file.getvalue()
        df = read_csv_any_encoding(bytes_data)
        required_cols = {"email", "account"}
        if not required_cols.issubset(df.columns):
            st.error("CSV must include at least 'email' and 'account' columns.")
        else:
            new_rows = 0
            skipped = 0
            with get_session() as s:
                for _, row in df.iterrows():
                    email = str(row["email"]).lower().strip()
                    acct_name = str(row["account"]).strip()
                    tags = (
                        str(row.get("tags", "")).lower().replace(";", ",").replace("|", ",")
                    )
                    acct = s.exec(select(Account).where(Account.name == acct_name)).first()
                    if not acct:
                        acct = Account(name=acct_name, user_id=uuid.UUID(st.session_state["current_user"]["id"]))
                        s.add(acct)
                        s.commit()
                    existing = s.exec(select(Lead).where(Lead.email == email)).first()
                    if existing:
                        skipped += 1
                        continue
                    lead = Lead(email=email, account_id=acct.id, tags=tags, user_id=uuid.UUID(st.session_state["current_user"]["id"]))
                    s.add(lead)
                    new_rows += 1
                s.commit()
            st.success(f"Imported {new_rows} rows (skipped {skipped} duplicates).")
            st.session_state["csv_uploaded"] = True

    # ---------- Login (example placeholder) ----------
    st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
    st.markdown("<b>🔒 Sign in</b>", unsafe_allow_html=True)
    st.text_input("Email")
    st.text_input("Password", type="password")
    st.button("Login")

    # ---------- Audit (example placeholder) ----------
    st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
    st.markdown("<b>🔎 Audit</b>", unsafe_allow_html=True)
    st.selectbox("Pick a lead e-mail:", options=["t"])
    st.info("No audit events yet.")

with main_col:
    h1("Chat CRM – Slice 1")
    # Chat history
    chat_container = st.container()
    with chat_container:
        card(chat_container)
        for msg in st.session_state.history:
            if msg["role"] == "user":
                body(f"👤 You: {msg['content']}")
            else:
                body(f"🤖 Assistant: {msg['content']}")
    # Floating chat input bar
    st.markdown(
        '''
        <div class="chat-input-card" style="position:fixed;left:calc(32vw + 2rem);right:2rem;bottom:2rem;z-index:100;">
            <form method="post" style="display:flex;align-items:center;gap:1rem;width:100%;">
                <input type="text" name="prompt" placeholder="Ask me anything!" style="flex:1;padding:0.75rem 1.5rem;font-size:1.1rem;border:none;background:rgba(255,255,255,0.06);backdrop-filter:blur(8px);border-radius:2rem;color:#1E2429;outline:none;" autocomplete="off" />
                <button type="submit" style="background:var(--clr-gold);border:none;border-radius:50%;width:44px;height:44px;display:flex;align-items:center;justify-content:center;box-shadow:0 0 12px #F9C94188;cursor:pointer;transition:background 0.2s;">
                    <span class="send-arrow" style="font-size:1.5rem;color:var(--clr-charcoal);font-weight:bold;">&#9654;</span>
                </button>
            </form>
        </div>
        ''', unsafe_allow_html=True)

    if "history" not in st.session_state:
        st.session_state.history = []

    def secure_select_leads(session, user_uuid):
        return session.exec(select(Lead).where(Lead.user_id == user_uuid))

    def handle(prompt: str, current_user) -> str:
        if "access_token" not in st.session_state:
            return "Please log in first."

        prompt = prompt.lower().strip()

        # 🔑  consistently use a UUID object from here on
        user_uuid = uuid.UUID(str(current_user["id"]))

        # ---- reports ----
        if prompt == "reports funnel":
            with get_session() as s:
                counts = funnel_counts(s, user_uuid)
            if not counts:
                return "No leads yet."
            # ordered by pipeline flow
            order = ["new", "qualified", "proposal", "won", "lost"]
            stages = [st for st in order if st in counts]
            vals = [counts[st] for st in stages]
            fig = px.funnel(y=stages, x=vals, title="Lead Funnel")
            return fig

        if prompt == "reports winrate":
            with get_session() as s:
                rate, won, total = win_rate(s, user_uuid)
            return f"🏆 Win-rate (last 30 d): **{rate:.1f}%**  ({won}/{total})"

        # ---- add account ----
        if prompt.startswith("add account"):
            name = prompt.replace("add account", "").strip()
            with get_session() as s:
                # case-folded lookup
                existing = s.exec(select(Account).where(Account.name == name.lower())).first()
                if existing:
                    return f"🤔 Account '{name}' already exists."
                s.add(Account(name=name.lower(), user_id=user_uuid))
                s.commit()
            return f"🏢 Account '{name}' created."

        # ---- add lead ----
        if prompt.startswith("add lead"):
            email = prompt.split()[-1]
            with get_session() as s:
                lead = Lead(email=email, user_id=user_uuid)
                s.add(lead)
                s.commit()
            return f"✅ Lead {email} added."

        # ---- attach lead ----
        if prompt.startswith("attach lead"):
            parts = prompt.split()
            email = parts[2]
            acct_name = parts[-1]
            with get_session() as s:
                acct = s.exec(select(Account).where(Account.name == acct_name)).first()
                if not acct:
                    return f"Account '{acct_name}' not found."
                lead = s.exec(select(Lead).where(Lead.email == email, Lead.user_id == user_uuid)).first()
                if not lead:
                    return f"Lead '{email}' not found."
                lead.account_id = acct.id
                s.commit()
            return f"🔗 Attached {email} → {acct_name}."

        # ===== NEW TAG COMMAND =====
        if prompt.startswith("tag lead"):
            # "tag lead email vip" (single tag for now)
            parts = prompt.split()
            email, tag = parts[2], parts[3]
            with get_session() as s:
                lead = s.exec(select(Lead).where(Lead.email == email, Lead.user_id == user_uuid)).first()
                if not lead:
                    return f"Lead '{email}' not found."
                tags_set = set(filter(None, map(str.strip, lead.tags.split(","))))
                tags_set.add(tag)
                lead.tags = ",".join(sorted(tags_set))
                s.commit()
            return f"🏷️  Tag '{tag}' added to {email}."

        # ===== NEW GLOBAL FIND =====
        if prompt.startswith("find"):
            term = prompt.replace("find", "").replace("leads", "").strip()
            with get_session() as s:
                # 1️⃣  leads matched on tags or email
                q1 = select(Lead).where(
                    (Lead.tags.like(f"%{term}%")) | (Lead.email.like(f"%{term}%"))
                )
                rows = s.exec(q1).all()
                # 2️⃣  leads matched via their account name
                if not rows:
                    q2 = (
                        select(Lead)
                        .join(Account, Lead.account_id == Account.id)
                        .where(Account.name.like(f"%{term}%"))
                    )
                    rows = s.exec(q2).all()
        if not rows:
            return f"No leads match '{term}'."
        return "\n".join(f"• {l.email}  ({l.tags})" for l in rows)

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

        # ---- list all leads ----
        if prompt.startswith("list leads"):
            with get_session() as s:
                rows = list(secure_select_leads(s, user_uuid))
            if not rows:
                return "No leads yet."
            return "\n".join(f"• {l.email}" for l in rows)

        # ---- set stage of lead ----
        if prompt.startswith("set stage of"):
            parts = prompt.split()
            email = parts[3]
            try:
                new_stage = Stage(parts[-1])
            except ValueError:
                return "Unknown stage. Use: new, qualified, proposal, won, lost."

            with get_session() as s:
                lead = s.exec(select(Lead).where(Lead.email == email, Lead.user_id == user_uuid)).first()
                if not lead:
                    return f"Lead '{email}' not found."

                before = to_json_safe(lead.dict())

                lead.stage = new_stage
                s.commit()
                after = to_json_safe(lead.dict())

                s.add(
                    AuditLog(
                        email=email,
                        action="update_stage",
                        before=before,
                        after=after,
                    )
                )
                s.commit()

            return f"🎯 Stage of {email} set to {new_stage.value}."

        # ---- rename lead ----
        # syntax:  "rename lead OLD@email.com to NEW@email.com"
        if prompt.startswith("rename lead"):
            parts = prompt.split(maxsplit=5)
            if len(parts) != 5 or parts[3] != "to":
                return "Usage: rename lead <old-email> to <new-email>"

            old_email, new_email = parts[2].lower(), parts[4].lower()

            with get_session() as s:
                lead = s.exec(
                    select(Lead).where(Lead.email == old_email, Lead.user_id == user_uuid)
                ).first()
                if not lead:
                    return f"Lead '{old_email}' not found."

                dup = s.exec(
                    select(Lead).where(Lead.email == new_email, Lead.user_id == user_uuid)
                ).first()
                if dup:
                    return f"Lead '{new_email}' already exists."

                # audit snapshot
                before = to_json_safe(lead.dict())

                lead.email = new_email
                s.commit()

                s.add(AuditLog(
                    email=new_email,
                    action="rename_lead",
                    before=before,
                    after=to_json_safe(lead.dict()),
                ))
                s.commit()

            return f"✏️  Lead e-mail updated to **{new_email}**."

        # ---- show pipeline kanban ----
        if prompt.startswith("show pipeline kanban"):
            with get_session() as s:
                rows = (
                    s.exec(
                        select(Lead.stage, func.count())
                        .group_by(Lead.stage)
                        .order_by(Lead.stage)
                    )
                    .all()
                )
            if not rows:
                return "No leads to graph yet."
            stages, counts = zip(*rows)
            fig = px.bar(
                x=counts,
                y=[s.value for s in stages],
                orientation="h",
                title="Pipeline by Stage",
                labels=dict(x="Leads", y="Stage"),
            )
            return fig  # return the figure object, no st.plotly_chart here

        # ---- show audit for lead ----
        if prompt.startswith("show audit for"):
            email = prompt.replace("show audit for", "").strip()
            with get_session() as s:
                logs = (
                    s.exec(
                        select(AuditLog)
                        .where(AuditLog.email == email)
                        .order_by(AuditLog.ts)
                    )
                    .all()
                )
            if not logs:
                return f"No audit records for {email}."
            lines = []
            for log in logs:
                ts = log.ts.strftime("%Y-%m-%d %H:%M")
                lines.append(f"- {ts} | {log.action}")
            return "\n".join(lines)

        # ---- delete lead ----
        if prompt.startswith(("delete lead", "remove lead")):
            email = prompt.split()[-1]
            with get_session() as s:
                lead = s.exec(
                    select(Lead).where(Lead.email == email, Lead.user_id == user_uuid)
                ).first()
                if not lead:
                    return f"Lead '{email}' not found."
                s.delete(lead)
                s.add(
                    AuditLog(
                        email=email,
                        action="delete_lead",
                        before={}, after={},    # keep minimal
                    )
                )
                s.commit()
            return f"🗑️ Lead {email} deleted."

        # ---- delete account ----
        if prompt.startswith(("delete account", "remove account")):
            acct_name = (
                prompt.replace("delete account", "")
                      .replace("remove account", "")
                      .strip()
                      .lower()
            )

            with get_session() as s:
                # fetch by name only, then check ownership
                acct = s.exec(select(Account).where(Account.name == acct_name)).first()
                if not acct:
                    return f"Account '{acct_name}' not found."

                if to_uuid(acct.user_id) != user_uuid:        # works for str or UUID
                    return "⛔ You don't own that account."

                leads_cnt = (
                    s.exec(select(func.count()).where(Lead.account_id == acct.id))
                     .one()[0]
                )
                if leads_cnt:
                    return f"⚠️ Account has {leads_cnt} lead(s). Delete them first."

                s.delete(acct)
                s.commit()

            return f"🗑️ Account '{acct_name}' deleted."

        # ---- rename account ----
        if prompt.startswith("rename account"):
            # expected syntax:  "rename account OLD to NEW"
            #                       0     1      2  3  4
            parts = prompt.split(maxsplit=4)
            if len(parts) != 5 or parts[3] != "to":
                return "Usage: rename account <old> to <new>"

            old_name, new_name = parts[2].lower(), parts[4].lower()

            with get_session() as s:
                acct = s.exec(
                    select(Account)
                    .where(Account.name == old_name, Account.user_id == user_uuid)
                ).first()
                if not acct:
                    return f"Account '{old_name}' not found."

                exists = s.exec(
                    select(Account)
                    .where(Account.name == new_name, Account.user_id == user_uuid)
                ).first()
                if exists:
                    return f"Account name '{new_name}' already exists."

                acct.name = new_name
                s.commit()

            return f"✏️  Account renamed to **{new_name}**."

        # ---- NLP fallback ----
        result = dispatch(prompt, ctx={"handle": handle, "user": current_user})
        if result is not None:
            return result

        return "Sorry, I don't understand yet."

    # ---- Streamlit sidebar login ----
    if "access_token" not in st.session_state:
        st.sidebar.subheader("🔐 Sign in")
        email = st.sidebar.text_input("Email")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            COOKIE_NAME = "crm-auth"
            resp = requests.post(
                "http://localhost:8000/auth/jwt/login",
                data={"username": email, "password": password},   # exact keys
                timeout=5,
            )
            print("LOGIN RESPONSE:", resp.status_code)
            print("RESPONSE HEADERS:", dict(resp.headers))
            print("RESPONSE COOKIES:", dict(resp.cookies))
            print("RESPONSE CONTENT:", resp.text)  # Add this line to see error details
            if resp.status_code in (200, 204):
                token = resp.cookies.get(COOKIE_NAME)
                if token:
                    st.session_state.access_token = token        # 👍 saved
                    # fetch profile immediately
                    prof = requests.get(
                        "http://localhost:8000/users/me",
                        cookies={"crm-auth": token},
                        timeout=5,
                    )
                    print("PROFILE RESPONSE:", prof.status_code)
                    print("PROFILE HEADERS:", dict(prof.headers))
                    if prof.status_code == 200:
                        st.session_state.current_user = prof.json()
                    st.rerun()
                else:
                    st.sidebar.error("Login cookie missing!")
            else:
                st.sidebar.error("Bad credentials")
    else:
        st.sidebar.success("Logged in!")
        # Update headers to use cookies instead of Authorization
        headers = {"Cookie": f"crm-auth={st.session_state.access_token}"}
        # pass headers into every request / session wrapper

    # 🔎─--- Audit inspector -------------------------------------------------
    st.sidebar.header("🔎 Audit")

    # collect every email that has at least one audit record
    with get_session() as s:
        audited_leads = (
            s.exec(select(AuditLog.email).group_by(AuditLog.email).order_by(AuditLog.email))
            .all()
        )
    emails = [row[0] for row in audited_leads]

    if emails:
        chosen_email = st.sidebar.selectbox("Pick a lead e-mail:", emails, key="audit_email")
        if chosen_email:
            # fetch logs for the chosen lead
            with get_session() as s:
                logs = (
                    s.exec(
                        select(AuditLog)
                        .where(AuditLog.email == chosen_email)
                        .order_by(AuditLog.ts.desc())
                    )
                    .all()
                )

            # ↪ instantly render a bullet list (newest first)
            if logs:
                lines = [
                    f"- {log.ts:%Y-%m-%d %H:%M} | {log.action.replace('_', ' ')}"
                    for log in logs
                ]
                st.sidebar.markdown("\n".join(lines))
            else:
                st.sidebar.info("No audit events yet.")
    else:
        st.sidebar.info("No audited leads found.")

    # Chat interface
    chat_container = st.container()
    with chat_container:
        card(chat_container)
        for msg in st.session_state.history:
            if msg["role"] == "user":
                body(f"👤 You: {msg['content']}")
            else:
                body(f"🤖 Assistant: {msg['content']}")

    # Input area (fixed at bottom, custom HTML)
    st.markdown(
        '''
        <form class="chat-input-card" autocomplete="off">
            <input type="text" name="prompt" id="chat-prompt" placeholder="Ask me anything!" autocomplete="off" />
            <button type="submit"><span class="send-arrow">&#9654;</span></button>
        </form>
        <script>
        const form = window.parent.document.querySelector('.chat-input-card');
        if (form) {
            form.onsubmit = function(e) {
                e.preventDefault();
                const input = form.querySelector('input[name="prompt"]');
                if (input && input.value.trim()) {
                    window.parent.postMessage({type: 'streamlit:setComponentValue', value: input.value}, '*');
                    input.value = '';
                }
            };
        }
        </script>
        ''', unsafe_allow_html=True)
