import React, { useState, useEffect } from 'react';
import './MixPage.css';
import Genre from '../../GenreComponents/Genre/Genre';
import DataGrid from '../../universal/DataGrid/DataGrid';
import Mix from '../Mix/Mix';  // Importing the Mix component

function MixPage() {
  const [genres, setGenres] = useState([]);

  const fetchMixes = (genreID) => {
    fetch(`/api/mixes?genreID=${genreID}`)
      .then(response => response.json())
      .then(data => {
        const newGenres = genres.map(genre => {
          if (genre.GenreID === genreID) {
            return { ...genre, mixes: data, showMixes: !genre.showMixes };
          }
          return genre;
        });
        setGenres(newGenres);
      })
      .catch(error => {
        console.error('Error fetching mixes:', error);
      });
  };

  useEffect(() => {
    fetch('/api/genres')
      .then(response => response.json())
      .then(data => {
        const updatedGenres = data.map(genre => ({
          ...genre,
          mixes: [],
          showMixes: false
        }));
        setGenres(updatedGenres);
      })
      .catch(error => {
        console.error('Error fetching genres:', error);
      });
  }, []);

  const handleGenreClick = (genreID) => {
    const genre = genres.find(g => g.GenreID === genreID);
    if (!genre.mixes.length) {
      fetchMixes(genreID);
    } else {
      toggleMixesDisplay(genreID);
    }
  };

  const toggleMixesDisplay = (genreID) => {
    const updatedGenres = genres.map(genre => ({
      ...genre,
      showMixes: genre.GenreID === genreID ? !genre.showMixes : genre.showMixes
    }));
    setGenres(updatedGenres);
  };

  return (
    <div className="mix-page-container">
      {genres.map(genre => (
        <div key={genre.GenreID}>
          <Genre genre={genre} onGenreClick={() => handleGenreClick(genre.GenreID)} />
          {genre.showMixes && (
            <DataGrid key={`mix-${genre.GenreID}`} items={genre.mixes} Component={Mix} />
          )}
        </div>
      ))}
    </div>
  );
}


export default MixPage;
