import React from 'react';
import './Genre.css';

function Genre({ genre, onGenreClick }) {
  return (
    <div className="genre-container" onClick={() => onGenreClick(genre.GenreID)}>
      <h1>{genre.Name}</h1>
      <p>{genre.Description}</p>
    </div>
  );
}

export default Genre;
