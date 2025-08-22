from typing import Dict, Any
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from app.tools import get_all_tools

# Global agent instance
_AGENT = None

def get_agent():
    """
    Initializes and returns the ReActAgent.
    This is done lazily to avoid loading the model on startup.
    """
    global _AGENT
    if _AGENT is None:
        # It's better to load the LLM once and reuse it
        llm = OpenAI(model="gpt-4o-mini")
        _AGENT = ReActAgent(
            tools=get_all_tools(),
            llm=llm,
            verbose=True,  # Set to True for debugging agent steps
        )
    return _AGENT

def run_agent(message: str) -> Dict[str, Any]:
    """
    Runs the ReActAgent with the given message and returns the result.
    This function now acts as a simple wrapper around the agent.
    """
    agent = get_agent()

    try:
        response = agent.chat(message)
        # The agent's response object has the response string
        # and sources from the RAG tool if it was used.
        citations = [n.metadata.get("file_name", "doc") for n in response.source_nodes]
        citations = list(dict.fromkeys(citations))
        return {"reply": str(response), "citations": citations}
    except ValueError as e:
        # This will catch the API key error from the tool initialization
        if "OPENAI_API_KEY" in str(e):
            return {"reply": str(e), "citations": []}
        # Handle other potential errors gracefully
        return {"reply": "An unexpected error occurred.", "citations": []}
    except Exception as e:
        # General catch-all for other unexpected errors
        print(f"Agent error: {e}")
        return {"reply": "Sorry, I encountered an unexpected issue.", "citations": []}
