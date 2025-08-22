from datetime import datetime
from llama_index.core.tools import FunctionTool

def compute_laytime(arrival_str: str, completion_str: str, allowed_days: float) -> dict:
    """
    Computes laytime details based on vessel arrival, completion of cargo operations,
    and the allowed time in days.

    Args:
        arrival_str (str): Vessel arrival datetime in 'YYYY-MM-DD HH:MM' format.
        completion_str (str): Cargo operations completion datetime in 'YYYY-MM-DD HH:MM' format.
        allowed_days (float): The number of days allowed for cargo operations as per the charter party.
    """
    try:
        arrival = datetime.strptime(arrival_str, "%Y-%m-%d %H:%M")
        completion = datetime.strptime(completion_str, "%Y-%m-%d %H:%M")
    except ValueError:
        return {"error": "Invalid date format. Use 'YYYY-MM-DD HH:MM'."}

    gross_duration = completion - arrival
    gross_hours = gross_duration.total_seconds() / 3600
    allowed_hours = allowed_days * 24

    # This is a simplification; a real laytime calculation would have many more rules
    # for excluding periods like weekends, bad weather, etc.
    excluded_hours = 0
    used_hours = gross_hours - excluded_hours
    balance_hours = allowed_hours - used_hours

    status = "despatch" if balance_hours > 0 else "demurrage"

    return {
        "gross_hours": round(gross_hours, 2),
        "allowed_hours": round(allowed_hours, 2),
        "excluded_hours": round(excluded_hours, 2),
        "used_hours": round(used_hours, 2),
        "balance_hours": round(balance_hours, 2),
        "status": status,
    }

laytime_tool = FunctionTool.from_defaults(
    fn=compute_laytime,
    name="laytime_calculator",
    description="Calculates laytime, demurrage, or despatch based on arrival and completion times, and allowed duration.",
)
