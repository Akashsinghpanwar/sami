from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    reply: str
    citations: Optional[List[str]] = None

class IngestResponse(BaseModel):
    added: int
    files: List[str]
