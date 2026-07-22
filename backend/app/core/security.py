from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.database import get_db
from backend.app.models.user import User

# 1. إعداد محرك التشفير
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. تحديد المسار الذي يرسل منه العميل التوكن (Header Authorization)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_password_hash(password: str) -> str:
    """تحويل الباسورد إلى Hash لتخزينه بأمان"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """مقارنة الباسورد المدخل بالـ Hash المتخزن"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """صناعة الـ JWT Token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """حارس البوابة: يفحص التوكن ويرجع بيانات المستخدم الحالي"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="تعذر التحقق من الهوية، يرجى تسجيل الدخول مجدداً",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # فك شفرة الـ Token واستخراج الإيميل
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
        
    # البحث عن المستخدِم في قاعدة البيانات
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
        
    return user