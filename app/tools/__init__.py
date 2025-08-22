# This file makes the 'tools' directory a Python package.
# It gathers all tools for the agent.

from app.rag import get_rag_tool
from .laytime import laytime_tool
from .distance import distance_tool
from .cp_glossary import stage_guidance_tool

def get_all_tools():
    """
    Initializes and returns a list of all tools available to the agent.
    The RAG tool is loaded lazily to avoid issues with API key checks at import time.
    """
    return [
        laytime_tool,
        distance_tool,
        stage_guidance_tool,
        get_rag_tool(),
    ]
