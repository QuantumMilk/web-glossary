import React, { useEffect, useState } from 'react';
import { fetchTerms } from '../api';
import '../App.css';

export default function Glossary() {
  const [terms, setTerms] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState(null);

  useEffect(() => {
    loadTerms();
  }, []);

  const loadTerms = async () => {
    const data = await fetchTerms();
    setTerms(data);
  };

  const handleCardClick = (index) => {
    setSelectedIndex(index);
  };

  return (
    <div className="container">
      <h2>Глоссарий</h2>
      <div className="card-grid">
        {terms.map((term, index) => (
          <div
            key={term.id}
            className={`card ${selectedIndex === index ? 'card-selected' : ''}`}
            onClick={() => handleCardClick(index)}
          >
            <h3>{term.name}</h3>
            <p>{term.definition}</p>
            {term.source && <p style={{ fontStyle: 'italic' }}>Источник: {term.source}</p>}
          </div>
        ))}
      </div>
    </div>
  );
}
