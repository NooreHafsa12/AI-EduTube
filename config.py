import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "AI_StudyMate_Pro_2026_Super_Secret_Key"
    )

    # Gemini
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    # Folders
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    PDF_FOLDER = os.path.join(BASE_DIR, "generated", "pdfs")
    GENERATED_FOLDER = os.path.join(BASE_DIR, "generated")

    # Session
    SESSION_PERMANENT = False

    SESSION_COOKIE_NAME = "studymate_session"

    JSON_SORT_KEYS = False

    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB

    # Cache
    CACHE_TIMEOUT = 3600  # 1 hour

    # Create folders automatically
    os.makedirs(PDF_FOLDER, exist_ok=True)
    os.makedirs(GENERATED_FOLDER, exist_ok=True)