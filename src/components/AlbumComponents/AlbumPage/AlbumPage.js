import React, { useState, useEffect } from 'react';
import './AlbumPage.css';
import AlbumGrid from '../Album/AlbumGrid';
import Genre from '../../GenreComponents/Genre/Genre';
import Album from '../Album/Album';

import FilterSelector from './FilterSelector';

function AlbumPage() {
  const [albums, setAlbums] = useState([]);
  const [genres, setGenres] = useState([]);
  const [years, setYears] = useState(Array.from(new Array(30), (val, index) => 1995 + index)); // Example: years from 1990 to 2020
  const [selectedGenre, setSelectedGenre] = useState('');
  const [selectedYear, setSelectedYear] = useState('');
  const [selectedRecommended, setRecommended] = useState('1');

  useEffect(() => {
    fetch('/api/genres')
      .then(response => response.json())
      .then(data => setGenres(data))
      .catch(error => console.error('Error fetching genres:', error));
  }, []);

  // Fetch albums based on selected genre and/or year
  const fetchAlbums = () => {
    let url = '/api/albums/basic-albums';  // Assume this is a new API endpoint that can handle queries

    const params = new URLSearchParams();
    if (selectedGenre) params.append('genreID', selectedGenre);
    if (selectedYear) params.append('year', selectedYear);
    if (selectedRecommended) params.append('recommended', selectedRecommended);

    fetch(`${url}?${params.toString()}`)
      .then(response => response.json())
      .then(data => {
        console.log("Filtered Albums data:", data);
        setAlbums(data);
      })
      .catch(error => {
        console.error('Error fetching filtered album info:', error);
      });
  };

  // Trigger the fetchAlbums function when filters change
  useEffect(() => {
    fetchAlbums();
  }, [selectedGenre, selectedYear, selectedRecommended]);

  return (
    <div className="album-page-container">
      <FilterSelector
        genres={genres}
        years={years}
        selectedGenre={selectedGenre}
        selectedYear={selectedYear}
        selectedRecommended={selectedRecommended}
        onGenreSelect={setSelectedGenre}
        onYearSelect={setSelectedYear}
        onRecommendedSelect={setRecommended}
      />
      <AlbumGrid albums={albums} />
    </div>
  );
}

export default AlbumPage;