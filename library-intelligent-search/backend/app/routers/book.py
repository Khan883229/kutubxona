# backend/app/routes/books.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from .. import models, schemas, services
from ..auth import get_current_user

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/search", response_model=List[schemas.BookResponse])
async def search_books(
    q: str = Query(..., min_length=1),
    language: str = Query("uz", regex="^(uz|ru|en)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Intelligent kitob qidiruv"""
    search_service = services.SearchService(db)
    books = search_service.intelligent_search(q, language, current_user.id)
    
    # Pagination
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_books = books[start_idx:end_idx]
    
    return paginated_books

@router.get("/{book_id}", response_model=schemas.BookResponse)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    """Kitob ma'lumotlarini olish"""
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Kitob topilmadi")
    return book

@router.post("/{book_id}/favorite", response_model=Dict)
async def add_to_favorites(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Kitobni sevimlilarga qo'shish"""
    # Kitob mavjudligini tekshirish
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Kitob topilmadi")
    
    # Oldin qo'shilganmi tekshirish
    existing_fav = db.query(models.UserFavorite).filter(
        models.UserFavorite.user_id == current_user.id,
        models.UserFavorite.book_id == book_id
    ).first()
    
    if existing_fav:
        raise HTTPException(status_code=400, detail="Kitob allaqachon sevimlilarga qo'shilgan")
    
    # Yangi favorite yaratish
    favorite = models.UserFavorite(
        user_id=current_user.id,
        book_id=book_id
    )
    
    db.add(favorite)
    db.commit()
    
    return {"message": "Kitob sevimlilarga qo'shildi", "book_id": book_id}