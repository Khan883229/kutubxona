# backend/app/services/search_service.py
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from ..models import Book, SearchHistory
import re

logger = logging.getLogger(__name__)

class SearchService:
    def __init__(self, db: Session):
        self.db = db
    
    def intelligent_search(self, query: str, language: str = 'uz', user_id: Optional[int] = None) -> List[Book]:
        """Intelligent qidiruv algoritmi"""
        
        # Qidiruv so'rovini tozalash va optimallashtirish
        cleaned_query = self.clean_query(query)
        
        # Multi-language qidiruv
        books = self.multi_language_search(cleaned_query, language)
        
        # Semantic similarity qo'shish (soddalashtirilgan)
        books = self.add_semantic_scoring(books, cleaned_query, language)
        
        # Search history saqlash
        if user_id:
            self.save_search_history(user_id, query, len(books), language)
        
        return books
    
    def clean_query(self, query: str) -> str:
        """Qidiruv so'rovini tozalash"""
        # Maxsus belgilarni olib tashlash
        cleaned = re.sub(r'[^\w\s]', ' ', query)
        # Ortiqcha bo'sh joylarni olib tashlash
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned
    
    def multi_language_search(self, query: str, language: str) -> List[Book]:
        """Ko'p tilli qidiruv"""
        search_terms = query.lower().split()
        
        base_query = self.db.query(Book)
        
        # Har bir tilda qidirish
        language_fields = {
            'uz': ['title_uz', 'author_uz', 'description_uz'],
            'ru': ['title_ru', 'author_ru', 'description_ru'], 
            'en': ['title_en', 'author_en', 'description_en']
        }
        
        fields = language_fields.get(language, ['title', 'author', 'description'])
        
        # Qidiruv shartlarini qo'shish
        for term in search_terms:
            term_conditions = []
            for field in fields:
                # SQLAlchemy filter
                column = getattr(Book, field) if hasattr(Book, field) else getattr(Book, 'title')
                term_conditions.append(column.ilike(f'%{term}%'))
            
            # Har bir so'z uchun OR sharti
            from sqlalchemy import or_
            base_query = base_query.filter(or_(*term_conditions))
        
        return base_query.order_by(Book.title).all()
    
    def add_semantic_scoring(self, books: List[Book], query: str, language: str) -> List[Book]:
        """Semantic scoring qo'shish (soddalashtirilgan)"""
        # Haqiqiy loyihada BERT yoki boshqa NLP modellari ishlatiladi
        query_terms = set(query.lower().split())
        
        scored_books = []
        for book in books:
            score = 0
            
            # Title match
            title_field = f'title_{language}' if hasattr(book, f'title_{language}') else 'title'
            title = getattr(book, title_field, '').lower()
            
            # Author match  
            author_field = f'author_{language}' if hasattr(book, f'author_{language}') else 'author'
            author = getattr(book, author_field, '').lower()
            
            # Description match
            desc_field = f'description_{language}' if hasattr(book, f'description_{language}') else 'description'
            description = getattr(book, desc_field, '').lower()
            
            # Oddiy scoring algoritmi
            for term in query_terms:
                if term in title:
                    score += 3
                if term in author:
                    score += 2
                if term in description:
                    score += 1
            
            scored_books.append((book, score))
        
        # Score bo'yicha saralash
        scored_books.sort(key=lambda x: x[1], reverse=True)
        return [book for book, score in scored_books]
    
    def save_search_history(self, user_id: int, query: str, results_count: int, language: str):
        """Qidiruv tarixini saqlash"""
        search_history = SearchHistory(
            user_id=user_id,
            query=query,
            results_count=results_count,
            language=language
        )
        self.db.add(search_history)
        self.db.commit()