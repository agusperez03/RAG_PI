import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
