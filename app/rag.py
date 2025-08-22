import os, glob
from typing import List, Tuple
from openai import AuthenticationError
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Settings,
    StorageContext,
    load_index_from_storage,
)
from llama_index.embeddings.openai import OpenAIEmbedding

# NOTE: do NOT build the index at import time.
# Build only when functions are called, to avoid uvicorn reloader issues.

_BASE_DIR = os.path.dirname(os.path.dirname(__file__))
_VECTOR_DIR = os.path.join(_BASE_DIR, "storage", "vector")
_KNOWLEDGE_DIR = os.path.join(_BASE_DIR, "data", "knowledge")

_INDEX = None
_EMBED_MODEL = None

def _ensure_dirs():
    os.makedirs(_VECTOR_DIR, exist_ok=True)
    os.makedirs(_KNOWLEDGE_DIR, exist_ok=True)

def _seed_if_empty() -> list:
    # Make sure there is at least one small file so index creation succeeds
    paths = []
    for ext in ("*.md", "*.pdf", "*.txt"):
        paths.extend(glob.glob(os.path.join(_KNOWLEDGE_DIR, ext)))
    if not paths:
        primer = os.path.join(_KNOWLEDGE_DIR, "cp_primer.md")
        with open(primer, "w", encoding="utf-8") as f:
            f.write("# GENCON Basics\nLaytime = allowed time for cargo ops.\nDemurrage = rate per day for excess time.\n")
        paths.append(primer)
    return paths

def get_index():
    """Return a live VectorStoreIndex, building or loading as needed."""
    global _INDEX, _EMBED_MODEL
    _ensure_dirs()

    if _INDEX is not None:
        return _INDEX

    # Configure embedding lazily (avoid heavy import on module import)
    if _EMBED_MODEL is None:
        _EMBED_MODEL = OpenAIEmbedding(model="text-embedding-3-small")
        Settings.embed_model = _EMBED_MODEL

    # Load if previously persisted
    if os.path.exists(os.path.join(_VECTOR_DIR, "docstore.json")):
        storage_context = StorageContext.from_defaults(persist_dir=_VECTOR_DIR)
        _INDEX = load_index_from_storage(storage_context)
        return _INDEX

    # First-time build
    paths = _seed_if_empty()
    docs = SimpleDirectoryReader(input_files=paths).load_data()
    try:
        _INDEX = VectorStoreIndex.from_documents(docs)
        _INDEX.storage_context.persist(persist_dir=_VECTOR_DIR)
        return _INDEX
    except AuthenticationError as e:
        raise ValueError(
            "OpenAI API key is missing or invalid. "
            "Please set the OPENAI_API_KEY environment variable."
        )

def add_files(filepaths: List[str]) -> int:
    """Add files to the vector index and persist."""
    try:
        idx = get_index()
        docs = SimpleDirectoryReader(input_files=filepaths).load_data()
        nodes = idx.service_context.node_parser.get_nodes_from_documents(docs)
        idx.insert_nodes(nodes)
        idx.storage_context.persist(persist_dir=_VECTOR_DIR)
        return len(filepaths)
    except AuthenticationError as e:
        raise ValueError(
            "OpenAI API key is missing or invalid. "
            "Please set the OPENAI_API_KEY environment variable."
        )

def query_rag(q: str) -> Tuple[str, list]:
    """Query the index and return (answer, [citations])."""
    try:
        idx = get_index()
        engine = idx.as_query_engine(similarity_top_k=4)
        res = engine.query(q)
        citations = []
        for n in res.source_nodes:
            meta = n.node.metadata or {}
            citations.append(meta.get("file_name", "doc"))
        # De-dup citations, preserve order
        citations = list(dict.fromkeys(citations))
        return str(res), citations
    except AuthenticationError as e:
        return (
            "OpenAI API key is missing or invalid. "
            "Please set the OPENAI_API_KEY environment variable."
        , [])
