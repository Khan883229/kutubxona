# backend/app/auth.py
from fastapi import HTTPException, status
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
import random
import redis

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
redis_client = redis.Redis(host='localhost', port=6379, db=0)

SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"

def generate_verification_code(phone: str) -> str:
    """SMS uchun tasdiqlash kodi yaratish"""
    code = str(random.randint(1000, 9999))
    redis_client.setex(f"verification:{phone}", 300, code)  # 5 daqiqa
    return code

def verify_code(phone: str, code: str) -> bool:
    """Tasdiqlash kodini tekshirish"""
    stored_code = redis_client.get(f"verification:{phone}")
    return stored_code and stored_code.decode() == code

def create_access_token(data: dict, expires_delta: timedelta = None):
    """JWT token yaratish"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt