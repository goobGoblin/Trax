import React, { useState, useEffect } from 'react';
import './GenrePage.css';
import DataGrid from '../../universal/DataGrid/DataGrid';
import Subgenre from '../Subgenre/Subgenre';
import Genre from '../Genre/Genre';

function GenrePage() {
  const [genres, setGenres] = useState([]);

  const fetchSubgenres = (genreID) => {
    fetch(`/api/subgenres?genreID=${genreID}`)
      .then(response => response.json())
      .then(data => {
        console.log("Subgenres data:", data);  // Add this line to inspect the data structure
        const newGenres = genres.map(genre => {
          if (genre.GenreID === genreID) {
            return { ...genre, subgenres: data, showSubgenres: !genre.showSubgenres };
          }
          return genre;
        });
        setGenres(newGenres);
      })
      .catch(error => {
        console.error('Error fetching subgenres:', error);
      });
  };

  useEffect(() => {
    fetch('/api/genres')
      .then(response => response.json())
      .then(data => {
        const updatedGenres = data.map(genre => ({
          ...genre,
          subgenres: [],
          showSubgenres: false
        }));
        setGenres(updatedGenres);
      })
      .catch(error => {
        console.error('Error fetching genres:', error);
      });
  }, []);

  const handleGenreClick = (genreID) => {
    const genre = genres.find(g => g.GenreID === genreID);
    if (!genre.subgenres.length) {
      fetchSubgenres(genreID);
    } else {
      toggleSubgenresDisplay(genreID);
    }
  };

  const toggleSubgenresDisplay = (genreID) => {
    const updatedGenres = genres.map(genre => ({
      ...genre,
      showSubgenres: genre.GenreID === genreID ? !genre.showSubgenres : genre.showSubgenres
    }));
    setGenres(updatedGenres);
  };

  return (
    <div className="genre-page-container">
      {genres.map(genre => (
        <div key={genre.GenreID}>
          <Genre genre={genre} onGenreClick={handleGenreClick} />
          {genre.showSubgenres && (
            <DataGrid key={`subgenre-${genre.GenreID}`} items={genre.subgenres} Component={Subgenre} contentType="subgenre" />
          )}
        </div>
      ))}
    </div>
  );
}

export default GenrePage;
