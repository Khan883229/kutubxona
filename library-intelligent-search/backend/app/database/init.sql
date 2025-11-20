-- backend/database/init.sql
CREATE DATABASE library_search;

-- Books jadvali uchun indexlar
CREATE INDEX idx_books_title ON books(title);
CREATE INDEX idx_books_author ON books(author);
CREATE INDEX idx_books_category ON books(category);
CREATE INDEX idx_books_title_uz ON books(title_uz);
CREATE INDEX idx_books_title_ru ON books(title_ru);
CREATE INDEX idx_books_title_en ON books(title_en);

-- Search history uchun index
CREATE INDEX idx_search_history_user_date ON search_history(user_id, created_at);