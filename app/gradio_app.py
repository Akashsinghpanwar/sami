

# app/gradio_app.py
import gradio as gr
import os, shutil
from typing import List

from app.settings import UPLOAD_DIR

os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------- Ingest ----------
def ingest_files(file_paths: List[str]) -> str:
    """
    Gradio File component is set to type='filepath', so we get List[str].
    We copy them into storage/uploads and index them lazily.
    """
    if not file_paths:
        return "No files selected."
    saved = []
    for fp in file_paths:
        dest = os.path.join(UPLOAD_DIR, os.path.basename(fp))
        shutil.copyfile(fp, dest)
        saved.append(dest)

    # Lazy import to avoid heavy imports at app startup
    from app.rag import add_files
    add_files(saved)

    names = [os.path.basename(x) for x in saved]
    return f"Ingested {len(saved)} file(s): {', '.join(names)}"

# ---------- Chat ----------
def chat_fn(message: str, history: List[dict]):
    """
    With Chatbot(type='messages'), `history` is a list of dicts:
      {"role": "user"|"assistant", "content": "..."}
    Return (cleared_input, updated_history).
    """
    if not message or not message.strip():
        return "", history

    # Lazy import
    from app.agent import run_agent
    result = run_agent(message.strip())
    reply = result.get("reply", "")
    cites = result.get("citations", [])
    if cites:
        reply += "\n\n— Sources: " + ", ".join(sorted(set(cites)))

    history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": reply},
    ]
    return "", history

# ---------- Demo layout ----------
with gr.Blocks(title="Maritime Virtual Assistant") as demo:
    gr.Markdown("# 🚢 Maritime Virtual Assistant — Demo\nUpload CP/SOF PDFs, then chat.")

    with gr.Tab("Upload & Index"):
        # type='filepath' -> we receive List[str] in the handler
        files = gr.File(label="Upload PDFs/MD/TXT", file_count="multiple", type="filepath")
        ingest_btn = gr.Button("Ingest into Knowledge Base")
        ingest_out = gr.Textbox(label="Ingestion Log", interactive=False)
        ingest_btn.click(ingest_files, inputs=[files], outputs=[ingest_out])

    with gr.Tab("Chat"):
        # Use messages format to avoid deprecation
        chatbox = gr.Chatbot(label="Assistant", type="messages")
        msg = gr.Textbox(label="Your message", placeholder="e.g., distance Singapore to Rotterdam")
        send = gr.Button("Send")
        clear = gr.Button("Clear")

        send.click(fn=chat_fn, inputs=[msg, chatbox], outputs=[msg, chatbox])
        # Reset to empty list for messages-style Chatbot
        clear.click(lambda: [], outputs=chatbox)

demo.queue()

if __name__ == "__main__":
    # Let Gradio find a free port automatically (recommended).
    # If you *must* pin a port and it's free, do:
    # demo.launch(server_name="0.0.0.0", server_port=7861)
    demo.launch(server_name="127.0.0.1")
