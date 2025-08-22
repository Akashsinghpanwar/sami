# app/agent.py
from typing import Dict, Any

SYSTEM_PROMPT = """You are a Maritime Virtual Assistant.
- Use tools for calculations (laytime, distance).
- For clauses & SOF, use RAG and include short citations (filenames).
- Be precise with dates, ports, units (nm, kts, USD/day).
- If key inputs are missing, ask one concise follow-up question.
- Keep answers structured and brief, with a final one-line conclusion."""

def route_intent(message: str) -> str:
    m = message.lower()
    if any(k in m for k in ["laytime", "demurrage", "despatch"]):
        return "laytime"
    if any(k in m for k in ["distance", "nm", "route"]):
        return "distance"
    if any(k in m for k in ["stage", "pre-fixture", "post-fixture", "loading", "discharge"]):
        return "stage"
    return "rag"

def run_agent(message: str) -> Dict[str, Any]:
    intent = route_intent(message)

    if intent == "laytime":
        import re
        from app.tools.laytime import compute_laytime
        a = re.search(r"arrived ([0-9\-: ]+)", message)
        c = re.search(r"completed ([0-9\-: ]+)", message)
        d = re.search(r"allowed (\d+(\.\d+)?)", message)
        if not (a and c and d):
            return {"reply": "Provide: arrived <YYYY-MM-DD HH:MM>, completed <YYYY-MM-DD HH:MM>, allowed <days>.", "citations": []}
        out = compute_laytime(a.group(1), c.group(1), float(d.group(1)))
        reply = (
            f"Laytime result:\n"
            f"- Gross: {out['gross_hours']} h, Exclusions: {out['excluded_hours']} h\n"
            f"- Used: {out['used_hours']} h vs Allowed: {out['allowed_hours']} h\n"
            f"- Balance: {out['balance_hours']} h → **{out['status'].upper()}**"
        )
        return {"reply": reply, "citations": []}

    if intent == "distance":
        import re
        from app.tools.distance import distance_nm
        m = re.search(r"distance ([a-zA-Z \-]+) to ([a-zA-Z \-]+)", message.lower())
        if not m:
            return {"reply": "Say: distance <PORT A> to <PORT B> (e.g., distance Singapore to Rotterdam).", "citations": []}
        a, b = m.group(1).strip(), m.group(2).strip()
        nm = distance_nm(a, b)
        return {"reply": f"Great-circle distance {a.title()} → {b.title()}: **{nm} nm** (no routing/canals).", "citations": []}

    if intent == "stage":
        from app.tools.cp_glossary import stage_guidance
        stage = message.split()[-1]
        info = stage_guidance(stage)
        if not info["suggestions"]:
            return {"reply": "Stages I know: pre-fixture, post-fixture, loading, discharge.", "citations": []}
        bullets = "\n".join([f"- {x}" for x in info["suggestions"]])
        return {"reply": f"**{info['stage'].title()} stage – suggested documents:**\n{bullets}", "citations": []}

    # RAG fallback
    from app.rag import query_rag
    answer, cites = query_rag(message)
    return {"reply": answer, "citations": cites}
