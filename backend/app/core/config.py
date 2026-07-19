import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Qamar Tutor"
    
    # إعدادات Groq الجديدة
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = "llama-3.1-8b-instant"  # موديل سريع جداً ومستقر ومجاني تماماً

settings = Settings()