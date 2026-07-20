from pydantic import BaseModel, EmailStr
from typing import Optional

# القالب اللي اليوزر بيبعته وهو بيسجل حساب جديد (Register)
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# القالب اللي السيرفر بيرجعه كبيانات لليوزر (بدون الباسورد طبعاً للأمان!)
class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

# القالب اللي السيرفر بيرجعه بعد تسجيل الدخول الناجح (Login Response)
class Token(BaseModel):
    access_token: str
    token_type: str