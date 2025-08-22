from datetime import datetime
from typing import List, Tuple, Dict, Optional

# Very simplified laytime engine for hackathon:
# - Assumes SHINC (Saturdays, Sundays, Holidays Included) by default
# - Accepts exclusion windows (e.g., weather delays, strikes)
# - Extend with SHEX/WWD and notice/turntime as needed

def parse_dt(s: str) -> datetime:
    # Accepts "2025-08-10 12:00" (local/UTC; you can standardize)
    return datetime.strptime(s, "%Y-%m-%d %H:%M")

def hours_between(a: datetime, b: datetime) -> float:
    return (b - a).total_seconds() / 3600.0

def compute_laytime(
    arrived: str,
    completed: str,
    allowed_days: float,
    exclusions: Optional[List[Tuple[str, str]]] = None,
) -> Dict:
    start = parse_dt(arrived)
    end = parse_dt(completed)
    gross_hours = hours_between(start, end)

    excluded = 0.0
    for ex in (exclusions or []):
        exs, exe = parse_dt(ex[0]), parse_dt(ex[1])
        # overlap window
        s, e = max(start, exs), min(end, exe)
        if s < e:
            excluded += hours_between(s, e)

    used_hours = max(0.0, gross_hours - excluded)
    allowed_hours = allowed_days * 24.0
    balance = allowed_hours - used_hours

    return {
        "gross_hours": round(gross_hours, 2),
        "excluded_hours": round(excluded, 2),
        "used_hours": round(used_hours, 2),
        "allowed_hours": round(allowed_hours, 2),
        "balance_hours": round(balance, 2),
        "status": "despatch" if balance > 0 else ("on_time" if balance == 0 else "demurrage"),
    }
