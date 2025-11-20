// frontend/src/components/SearchBox.tsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

interface SearchBoxProps {
  initialQuery?: string;
  onSearch?: (query: string, language: string) => void;
}

const SearchBox: React.FC<SearchBoxProps> = ({ initialQuery = '', onSearch }) => {
  const [query, setQuery] = useState(initialQuery);
  const [language, setLanguage] = useState('uz');
  const navigate = useNavigate();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      if (onSearch) {
        onSearch(query, language);
      } else {
        navigate(`/search?q=${encodeURIComponent(query)}&lang=${language}`);
      }
    }
  };

  return (
    <div className="search-box">
      <form onSubmit={handleSearch} className="search-form">
        <div className="search-input-group">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Kitob, muallif yoki mavzu bo'yicha qidiring..."
            className="search-input"
          />
          <select 
            value={language} 
            onChange={(e) => setLanguage(e.target.value)}
            className="language-select"
          >
            <option value="uz">O'zbek</option>
            <option value="ru">Русский</option>
            <option value="en">English</option>
          </select>
          <button type="submit" className="search-button">
            🔍 Qidirish
          </button>
        </div>
      </form>
    </div>
  );
};

export default SearchBox;