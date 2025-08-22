STAGE_DOCS = {
  "pre-fixture": [
    "Charter Party draft (GENCON/ASBATANKVOY etc.)",
    "Vessel particulars, P&I, class certificates",
    "Port info & restrictions"
  ],
  "post-fixture": [
    "Fixture recap, NOR template, SOF template",
    "Bunkers plan, weather routing contact"
  ],
  "loading": [
    "NOR, SOF, Cargo docs, Stowage plan",
    "Laytime sheet initiation"
  ],
  "discharge": [
    "Discharge orders, Receivers contact, Final SOF",
    "Laytime finalization, Demurrage/Despatch calc"
  ]
}

def stage_guidance(stage: str):
    stage = stage.strip().lower()
    items = STAGE_DOCS.get(stage)
    if not items:
        return {"stage": stage, "suggestions": [], "note": "Unknown stage"}
    return {"stage": stage, "suggestions": items}
