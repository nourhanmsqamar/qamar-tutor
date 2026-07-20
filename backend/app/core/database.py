from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.app.core.config import settings

# 1. The Engine (المحرك اللي بيكلم الداتا بيز)
engine = create_engine(settings.DATABASE_URL)

# 2. SessionLocal (المصنع اللي بيطلع جلسات اتصال مؤقتة لكل ريكويست)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Base (الأساس اللي كل الجداول بتاعتنا هتورث منه عشان SQLAlchemy يتعرف عليها)
Base = declarative_base()

# 4. Dependency (الدالة اللي الـ Router هيستخدمها عشان يفتح ويقفل الاتصال)
def get_db():
    db = SessionLocal()
    try:
        yield db  # بنوقف الدالة هنا وندي الـ session للريكويست يشتغل بيه
    finally:
        db.close()  # أول ما الريكويست يخلص، الكود بيكمل ويقفل الاتصال فوراً