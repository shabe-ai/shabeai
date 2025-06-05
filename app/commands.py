from __future__ import annotations
import uuid
import re
import plotly.express as px
from app.db import get_session
from app.models import Lead, Account, Stage, AuditLog
from sqlmodel import select, col, func
from app.utils import to_json_safe, to_uuid
from app.nl_router import dispatch
from app.reports import funnel_counts, win_rate

def handle(prompt: str, current_user) -> str:
    if not current_user:
        return "Please log in first."

    prompt = prompt.lower().strip()

    # 🔑  consistently use a UUID object from here on
    user_uuid = to_uuid(current_user["id"])

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
        name = prompt.replace("add account", "").strip().lower()
        with get_session() as s:
            if s.exec(select(Account).where(Account.name == name)).first():
                return f"🏢 Account '{name}' already **created**."
            s.add(Account(name=name, user_id=user_uuid))
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
    m = re.match(r"attach lead\s+(\S+)\s+to\s+(.+)", prompt)
    if m:
        email, acct_name = m.groups()
        with get_session() as s:
            acct = s.exec(
                select(Account).where(Account.name == acct_name.lower(),
                                       Account.user_id == user_uuid)
            ).first()
            if not acct:
                return f"Account '{acct_name}' not found."
            lead = s.exec(
                select(Lead).where(Lead.email == email, Lead.user_id == user_uuid)
            ).first()
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

            before = to_json_safe(lead.model_dump())

            lead.stage = new_stage
            s.commit()
            after = to_json_safe(lead.model_dump())

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
            before = to_json_safe(lead.model_dump())

            lead.email = new_email
            s.commit()

            s.add(AuditLog(
                email=new_email,
                action="rename_lead",
                before=before,
                after=to_json_safe(lead.model_dump()),
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
        acct_name = prompt.replace("delete account", "").replace("remove account","").strip().lower()
        with get_session() as s:
            acct = s.exec(
                select(Account).where(Account.name == acct_name, Account.user_id == user_uuid)
            ).first()
            if not acct:
                return f"Account '{acct_name}' not found."
            # how many leads point at this account?
            cnt = s.exec(
                select(func.count()).where(Lead.account_id == acct.id)
            ).one()          # <- returns an int

            if cnt:          # non-zero means still attached
                return f"⚠️ Account has {cnt} lead(s). Delete them first."
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