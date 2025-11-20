# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import redis
import jwt
from datetime import datetime, timedelta

from .database import SessionLocal, engine
from . import models, schemas, services

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Intelligent Library Search", version="1.0.0")

# CORS sozlamalari
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Kutubxona Intelligent Qidiruv Tizimi"}
