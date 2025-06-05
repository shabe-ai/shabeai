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
from app.utils import to_json_safe, to_uuid
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
                                 user_id=to_uuid(st.session_state["current_user"]["id"]))
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
                          user_id=to_uuid(st.session_state["current_user"]["id"]))
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
        from app import handle
        answer = handle(prompt, user)
        st.session_state.history.append((prompt, answer))

for q, resp in st.session_state.history:
    st.chat_message("user").write(q)
    if isinstance(resp, str):
        st.chat_message("assistant").write(resp)
    else:
        # assume Plotly figure
        st.chat_message("assistant").plotly_chart(resp, use_container_width=True)

if __name__ == "__main__":
    # Your original Streamlit bootstrap
    pass 