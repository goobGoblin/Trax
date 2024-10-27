import React from 'react';

// Ensure all props are listed here, including `selectedRecommended`
function FilterSelector({
  genres,
  years,
  selectedGenre,
  selectedYear,
  selectedRecommended,
  onGenreSelect,
  onYearSelect,
  onRecommendedSelect
}) {
    return (
        <div>
            <select value={selectedGenre} onChange={e => onGenreSelect(e.target.value)}>
                <option value="">Select Genre</option>
                {genres.map(genre => (
                    <option key={genre.GenreID} value={genre.GenreID}>{genre.Name}</option>
                ))}
            </select>
            <select value={selectedYear} onChange={e => onYearSelect(e.target.value)}>
                <option value="">Select Year</option>
                {years.map(year => (
                    <option key={year} value={year}>{year}</option>
                ))}
            </select>
            <select value={selectedRecommended} onChange={e => onRecommendedSelect(e.target.value)}>
                <option value="">All</option>
                <option value="1">Recommended</option>
                <option value="0">Not Recommended</option>
            </select>
        </div>
    );
}

export default FilterSelector;
