import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Qamar Tutor"
    
    # إعدادات Groq
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = "llama-3.1-8b-instant"  
    
    # إعدادات قاعدة البيانات
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # إعدادات الأمان والـ JWT (السطور الجديدة)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-fallback-key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # RAG Settings
    RAG_CHUNK_SIZE: int = int(os.getenv("RAG_CHUNK_SIZE", 800))
    RAG_CHUNK_OVERLAP: int = int(os.getenv("RAG_CHUNK_OVERLAP", 150))
    CHROMA_DB_DIR: str = os.getenv("CHROMA_DB_DIR", "./chroma_db")
    EMBEDDING_MODEL_NAME: str = os.getenv("EMBEDDING_MODEL_NAME", "paraphrase-multilingual-MiniLM-L12-v2")
    CHROMA_COLLECTION_NAME: str = os.getenv("CHROMA_COLLECTION_NAME", "qamar_documents")

settings = Settings()