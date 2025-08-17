import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_API_BASE_URL = os.getenv("GOOGLE_API_BASE_URL")
MODEL_NAME = os.getenv("MODEL")

CONFIG_DIR = Path("./config/")
CONFIG_FILE = CONFIG_DIR / "session.yaml"
AGENT_CONFIG_FILE = CONFIG_DIR / "agents.yaml"
OUTPUT_DIR = Path("./output/")
