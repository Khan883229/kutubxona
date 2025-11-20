# backend/scripts/seed_data.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Book

# Database connection
engine = create_engine("postgresql://postgres:password@localhost:5432/library_search")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_books():
    db = SessionLocal()
    
    sample_books = [
        Book(
            title="O'tkan Kunlar",
            title_uz="O'tkan Kunlar",
            title_ru="Минувшие дни", 
            title_en="Bygone Days",
            author="Abdulla Qodiriy",
            author_uz="Abdulla Qodiriy",
            author_ru="Абдулла Кадыри",
            author_en="Abdulla Qodiriy",
            description="O'zbek adabiyotining durdona asari",
            description_uz="O'zbek adabiyotining durdona asari",
            description_ru="Жемчужина узбекской литературы",
            description_en="Pearl of Uzbek literature",
            publication_year=1926,
            category="Roman",
            available_copies=5
        ),
        # Ko'proq kitoblar...
    ]
    
    db.add_all(sample_books)
    db.commit()
    print("Test ma'lumotlari qo'shildi!")

if __name__ == "__main__":
    seed_books()