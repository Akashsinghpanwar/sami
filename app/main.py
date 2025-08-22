from fastapi import FastAPI, UploadFile, File
from typing import List
import os, shutil

app = FastAPI(title="Maritime Virtual Assistant")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ingest")
async def ingest(files: List[UploadFile] = File(...)):
    # Lazy import here to avoid heavy imports at startup/reloader time
    from app.rag import add_files
    base_dir = os.path.dirname(os.path.dirname(__file__))
    upload_dir = os.path.join(base_dir, "storage", "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    saved = []
    for f in files:
        dest = os.path.join(upload_dir, f.filename)
        with open(dest, "wb") as out:
            shutil.copyfileobj(f.file, out)
        saved.append(dest)

    added = add_files(saved) if saved else 0
    return {"added": added, "files": [os.path.basename(p) for p in saved]}

@app.post("/chat")
async def chat(payload: dict):
    # Lazy import here too
    from app.agent import run_agent
    message = (payload or {}).get("message", "").strip()
    if not message:
        return {"reply": "Send a 'message' field.", "citations": []}
    result = run_agent(message)
    return {"reply": result.get("reply", ""), "citations": result.get("citations", [])}
