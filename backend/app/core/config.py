import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Qamar Tutor"
    
    # إعدادات Groq
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = "llama-3.1-8b-instant"  
    
    # إعدادات قاعدة البيانات (السطر الجديد)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

settings = Settings()