from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI(
    title="Kutubxona Intelligent Qidiruv Tizimi",
    description="Kutubxona asosidagi intelligent qidiruv tizimi - Borkuuu! 🎉",
    version="1.0.0"
)

# CORS sozlamalari
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Kitob modeli
class Book(BaseModel):
    id: int
    title: str
    author: str
    description: Optional[str] = None
    year: Optional[int] = None
    language: str = "uz"
    available: bool = True

# Test kitoblar ro'yxati
sample_books = [
    Book(
        id=1,
        title="O'tkan Kunlar",
        author="Abdulla Qodiriy",
        description="O'zbek adabiyotining durdona asari",
        year=1926,
        language="uz"
    ),
    Book(
        id=2,
        title="Mehrobdan Chayon", 
        author="Abdulla Qodiriy",
        description="Tarixiy roman",
        year=1929,
        language="uz"
    ),
    Book(
        id=3,
        title="Kecha va Kunduz",
        author="Cho'lpon", 
        description="Realistik roman",
        year=1936,
        language="uz"
    ),
    Book(
        id=4,
        title="Уткан кунлар",
        author="Абдулла Кадыри",
        description="Жемчужина узбекской литературы", 
        year=1926,
        language="ru"
    ),
    Book(
        id=5,
        title="Bygone Days",
        author="Abdulla Qodiriy",
        description="Pearl of Uzbek literature",
        year=1926, 
        language="en"
    )
]

@app.get("/")
async def root():
    return {
        "message": "Kutubxona Intelligent Qidiruv Tizimi", 
        "status": "Ishlayapti 🚀",
        "version": "1.0.0",
        "developer": "Borkuuu! 🎉"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Server ishlayapti"}

@app.get("/api/books", response_model=List[Book])
async def get_books():
    """Barcha kitoblarni olish"""
    return sample_books

@app.get("/api/books/search")
async def search_books(q: str = "", lang: str = "uz"):
    """Kitoblarni qidirish"""
    if not q:
        return sample_books
    
    results = []
    for book in sample_books:
        if (q.lower() in book.title.lower() or 
            q.lower() in book.author.lower() or 
            q.lower() in book.description.lower()):
            results.append(book)
    
    return results

@app.get("/api/books/{book_id}")
async def get_book(book_id: int):
    """ID bo'yicha kitob olish"""
    for book in sample_books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Kitob topilmadi")

@app.get("/api/languages")
async def get_languages():
    """Qo'llab-quvvatlanadigan tillar"""
    return {
        "languages": ["uz", "ru", "en"],
        "default": "uz"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
