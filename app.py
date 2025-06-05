import os
import uuid

from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from app.db import init_db, get_session
from app.models import Lead, Account, Stage, AuditLog, User
from sqlmodel import select, col, func
import pandas as pd
from io import StringIO
import re
import plotly.express as px
from app.audit import audit
from app.utils import to_json_safe
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTStrategy, AuthenticationBackend
from fastapi import Depends
from app.auth import fastapi_users
from app.reports import funnel_counts, win_rate
from app.nl_router import dispatch
import requests

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
st.title("Chat CRM – Slice 1")

# ---------- Sidebar CSV import ----------
st.sidebar.header("📥 CSV import")

# Clean previous state *before* creating the widget
if "csv_uploader" in st.session_state and st.session_state.get("csv_uploaded"):
    st.session_state.pop("csv_uploader")
    st.session_state.pop("csv_uploaded")

csv_file = st.sidebar.file_uploader(
    "Upload a CSV with columns: email, account, tags (optional)",
    type=["csv"],
    key="csv_uploader",
)

if csv_file is not None:
    bytes_data = csv_file.getvalue()
    df = read_csv_any_encoding(bytes_data)

    required_cols = {"email", "account"}
    if not required_cols.issubset(df.columns):
        st.sidebar.error("CSV must include at least 'email' and 'account' columns.")
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

                # --- ensure account exists ---
                acct = s.exec(select(Account).where(Account.name == acct_name)).first()
                if not acct:
                    acct = Account(name=acct_name,
                                 user_id=uuid.UUID(st.session_state["current_user"]["id"]))
                    s.add(acct)
                    s.commit()  # needed so acct.id is generated

                # --- check duplicate lead ---
                existing = s.exec(select(Lead).where(Lead.email == email)).first()
                if existing:
                    skipped += 1
                    continue

                lead = Lead(email=email,
                          account_id=acct.id,
                          tags=tags,
                          user_id=uuid.UUID(st.session_state["current_user"]["id"]))
                s.add(lead)
                new_rows += 1
            s.commit()

        st.sidebar.success(
            f"Imported {new_rows} rows (skipped {skipped} duplicates)."
        )
        st.session_state["csv_uploaded"] = True      # flag so we know to clear next run

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

prompt = st.chat_input("Say something…")
if prompt:
    user = st.session_state.get("current_user")
    if not user:
        st.chat_message("assistant").write("Please log in first.")
    else:
        answer = handle(prompt, user)
        st.session_state.history.append((prompt, answer))

for q, resp in st.session_state.history:
    st.chat_message("user").write(q)
    if isinstance(resp, str):
        st.chat_message("assistant").write(resp)
    else:
        # assume Plotly figure
        st.chat_message("assistant").plotly_chart(resp, use_container_width=True)
