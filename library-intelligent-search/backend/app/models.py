# backend/app/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True, index=True, nullable=False)
    is_verified = Column(Boolean, default=False)
    language = Column(String(10), default='uz')
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    searches = relationship("SearchHistory", back_populates="user")
    favorites = relationship("UserFavorite", back_populates="user")

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    title_uz = Column(String(500))
    title_ru = Column(String(500))
    title_en = Column(String(500))
    author = Column(String(300), nullable=False)
    author_uz = Column(String(300))
    author_ru = Column(String(300))
    author_en = Column(String(300))
    description = Column(Text)
    description_uz = Column(Text)
    description_ru = Column(Text)
    description_en = Column(Text)
    publication_year = Column(Integer)
    category = Column(String(200))
    isbn = Column(String(50))
    library_location = Column(String(300))
    available_copies = Column(Integer, default=1)
    video_url = Column(String(500))
    thumbnail_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

class SearchHistory(Base):
    __tablename__ = "search_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    query = Column(String(500), nullable=False)
    results_count = Column(Integer, default=0)
    language = Column(String(10))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="searches")

class UserFavorite(Base):
    __tablename__ = "user_favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="favorites")
    book = relationship("Book")