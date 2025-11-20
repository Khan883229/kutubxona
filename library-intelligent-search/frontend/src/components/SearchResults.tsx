// frontend/src/components/SearchResults.tsx
import React from 'react';
import { Book } from '../types';

interface SearchResultsProps {
  books: Book[];
  loading: boolean;
  language: string;
}

const SearchResults: React.FC<SearchResultsProps> = ({ books, loading, language }) => {
  if (loading) {
    return <div className="loading">Qidiruv natijalari yuklanmoqda...</div>;
  }

  if (books.length === 0) {
    return <div className="no-results">Hech qanday natija topilmadi</div>;
  }

  return (
    <div className="search-results">
      <h3>Topilgan natijalar: {books.length}</h3>
      <div className="books-grid">
        {books.map((book) => (
          <div key={book.id} className="book-card">
            <div className="book-thumbnail">
              {book.thumbnail_url ? (
                <img src={book.thumbnail_url} alt={book.title} />
              ) : (
                <div className="thumbnail-placeholder">📚</div>
              )}
            </div>
            <div className="book-info">
              <h4 className="book-title">
                {book[`title_${language}` as keyof Book] || book.title}
              </h4>
              <p className="book-author">
                {book[`author_${language}` as keyof Book] || book.author}
              </p>
              <p className="book-description">
                {(book[`description_${language}` as keyof Book] as string) || book.description}
              </p>
              {book.video_url && (
                <button 
                  className="video-button"
                  onClick={() => window.open(book.video_url, '_blank')}
                >
                  🎬 Video ko'rish
                </button>
              )}
              <div className="book-meta">
                <span>Yil: {book.publication_year}</span>
                <span>Nusxa: {book.available_copies}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SearchResults;