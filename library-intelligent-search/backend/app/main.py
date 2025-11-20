from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Kutubxona Intelligent Qidiruv Tizimi",
    description="Kutubxona asosidagi intelligent qidiruv tizimi",
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

# Test kitoblar
sample_books = [
    Book(id=1, title="O'tkan Kunlar", author="Abdulla Qodiriy", description="O'zbek adabiyotining durdona asari", year=1926, language="uz"),
    Book(id=2, title="Mehrobdan Chayon", author="Abdulla Qodiriy", description="Tarixiy roman", year=1929, language="uz"),
    Book(id=3, title="Kecha va Kunduz", author="Cho'lpon", description="Realistik roman", year=1936, language="uz"),
]

@app.get("/")
async def root():
    return {"message": "Kutubxona API ishlayapti! 🚀", "status": "success"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}

@app.get("/api/books")
async def get_books():
    return sample_books

@app.get("/api/books/search")
async def search_books(q: str = ""):
    if not q:
        return sample_books
    
    results = []
    for book in sample_books:
        if (q.lower() in book.title.lower() or 
            q.lower() in book.author.lower() or 
            (book.description and q.lower() in book.description.lower())):
            results.append(book)
    
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
