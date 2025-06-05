from sqlmodel import select, func
from app.models import Lead, Stage
from datetime import datetime, timedelta

def funnel_counts(session, user_id):
    rows = (
        session.exec(
            select(Lead.stage, func.count())
            .where(Lead.user_id == user_id)
            .group_by(Lead.stage)
        ).all()
    )
    return {stage.value: count for stage, count in rows}

def win_rate(session, user_id, days=30):
    since = datetime.utcnow() - timedelta(days=days)
    won = session.exec(
        select(func.count()).where(
            Lead.user_id == user_id,
            Lead.stage == Stage.WON,
            Lead.created_at >= since,
        )
    ).one()
    lost = session.exec(
        select(func.count()).where(
            Lead.user_id == user_id,
            Lead.stage == Stage.LOST,
            Lead.created_at >= since,
        )
    ).one()
    total = won + lost
    rate = (won / total) * 100 if total else 0
    return rate, won, total 