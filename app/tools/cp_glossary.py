from llama_index.core.tools import FunctionTool

# A real implementation would use a database or a more structured file.
_STAGES = {
    "pre-fixture": {
        "description": "Activities before the charter party is signed.",
        "suggestions": [
            "Negotiate freight rate and key terms",
            "Vessel nomination and acceptance",
            "Draft charter party for review",
        ],
    },
    "post-fixture": {
        "description": "Activities after the charter party is signed, before voyage.",
        "suggestions": [
            "Issue voyage instructions to the vessel",
            "Finalize and sign the charter party",
            "Prepare notice of readiness (NOR)",
        ],
    },
    "loading": {
        "description": "Activities related to loading the cargo.",
        "suggestions": [
            "Tender Notice of Readiness (NOR)",
            "Prepare and sign bill of lading (B/L)",
            "Prepare statement of facts (SOF)",
        ],
    },
    "discharge": {
        "description": "Activities related to discharging the cargo.",
        "suggestions": [
            "Tender Notice of Readiness (NOR) at discharge port",
            "Collect freight and other costs from receiver",
            "Release bill of lading (B/L) for cargo release",
            "Prepare and finalize laytime calculation",
        ],
    },
}

def stage_guidance(stage_name: str) -> dict:
    """
    Provides a list of suggested actions and documents for a given voyage stage.

    Args:
        stage_name (str): The name of the voyage stage. Known stages are:
                          pre-fixture, post-fixture, loading, discharge.
    """
    stage_key = stage_name.lower()
    if stage_key not in _STAGES:
        return {"error": f"Stage '{stage_name}' not recognized. Try one of: {', '.join(_STAGES.keys())}"}

    info = _STAGES[stage_key]
    return {
        "stage": stage_name,
        "description": info["description"],
        "suggestions": info["suggestions"],
    }

stage_guidance_tool = FunctionTool.from_defaults(
    fn=stage_guidance,
    name="voyage_stage_guidance",
    description="Provides suggested actions and documents for a specific voyage stage (e.g., loading, discharge).",
)
