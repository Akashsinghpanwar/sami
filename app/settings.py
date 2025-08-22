import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "storage", "uploads")
VECTOR_DIR = os.path.join(BASE_DIR, "storage", "vector")
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "data", "knowledge")
PORTS_PATH = os.path.join(BASE_DIR, "data", "ports.json")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(VECTOR_DIR, exist_ok=True)
