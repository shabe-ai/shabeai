"""
Pure helper functions for business logic.

These functions don't touch I/O (no DB, no network) so they're easy to test.
"""
from collections import Counter
from app.models import Stage, Lead, Account

def stage_counts(leads: list[Lead]) -> dict[str, int]:
    """Return {stage: n} ordered by workflow."""
    counter = Counter(l.stage.value for l in leads)
    order = ["new", "qualified", "proposal", "won", "lost"]
    return {s: counter[s] for s in order if counter[s]}

def win_rate(leads: list[Lead]) -> float:
    """Calculate win rate from leads."""
    if not leads:
        return 0.0
    won = sum(1 for l in leads if l.stage.value.lower() == "won")
    total = sum(1 for l in leads if l.stage.value.lower() in
                {"won", "lost", "proposal", "qualified", "new"})
    return won / total if total else 0.0

def find_account_by_name(accounts: list[Account], name: str) -> Account | None:
    """Find account by case-insensitive name match."""
    name = name.lower()
    return next((a for a in accounts if a.name.lower() == name), None)

def find_lead_by_email(leads: list[Lead], email: str) -> Lead | None:
    """Find lead by case-insensitive email match."""
    email = email.lower()
    return next((l for l in leads if l.email.lower() == email), None) 