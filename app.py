import streamlit as st
from app.db import init_db, get_session
from app.models import Lead, Account, Stage
from sqlmodel import select, col, func
import pandas as pd
from io import StringIO
import re
import plotly.express as px

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
    df = pd.read_csv(StringIO(bytes_data.decode("utf-8")))

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
                    acct = Account(name=acct_name)
                    s.add(acct)
                    s.commit()  # needed so acct.id is generated

                # --- check duplicate lead ---
                existing = s.exec(select(Lead).where(Lead.email == email)).first()
                if existing:
                    skipped += 1
                    continue

                lead = Lead(email=email, account_id=acct.id, tags=tags)
                s.add(lead)
                new_rows += 1
            s.commit()

        st.sidebar.success(
            f"Imported {new_rows} rows (skipped {skipped} duplicates)."
        )
        st.session_state["csv_uploaded"] = True      # flag so we know to clear next run

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

    # ---- attach lead ----
    if prompt.startswith("attach lead"):
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
            s.commit()
        return f"🔗 Attached {email} → {acct_name}."

    # ===== NEW TAG COMMAND =====
    if prompt.startswith("tag lead"):
        # "tag lead email vip" (single tag for now)
        parts = prompt.split()
        email, tag = parts[2], parts[3]
        with get_session() as s:
            lead = s.exec(select(Lead).where(Lead.email == email)).first()
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
            rows = s.exec(select(Lead)).all()
        if not rows:
            return "No leads yet."
        return "\n".join(f"• {l.email}" for l in rows)

    # ---- set stage of lead ----
    if prompt.startswith("set stage of"):
        # format: set stage of email to <stage>
        parts = prompt.split()
        email = parts[3]
        try:
            new_stage = Stage(parts[-1])
        except ValueError:
            return "Unknown stage. Use: new, qualified, proposal, won, lost."
        with get_session() as s:
            lead = s.exec(select(Lead).where(Lead.email == email)).first()
            if not lead:
                return f"Lead '{email}' not found."
            lead.stage = new_stage
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

    return "Sorry, I don't understand yet."

prompt = st.chat_input("Say something…")
if prompt:
    answer = handle(prompt)
    st.session_state.history.append((prompt, answer))

for q, resp in st.session_state.history:
    st.chat_message("user").write(q)
    if isinstance(resp, str):
        st.chat_message("assistant").write(resp)
    else:
        # assume Plotly figure
        st.chat_message("assistant").plotly_chart(resp, use_container_width=True)
