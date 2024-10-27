import React, { useState, useEffect } from 'react';
import Genre from '../../GenreComponents/Genre/Genre';
import Artist from '../Artist/Artist';
import DataGrid from '../../universal/DataGrid/DataGrid';
import './ArtistPage.css';

function ArtistPage() {
  const [genres, setGenres] = useState([]);

  const fetchArtists = (genreID) => {
    fetch(`/api/artists?genreID=${genreID}`)
      .then(response => response.json())
      .then(data => {
        const newGenres = genres.map(genre => {
          if (genre.GenreID === genreID) {
            return { ...genre, artists: data, showArtists: !genre.showArtists };
          }
          return genre;
        });
        setGenres(newGenres);
      })
      .catch(error => {
        console.error('Error fetching artists:', error);
      });
  };

  useEffect(() => {
    fetch('/api/genres')
      .then(response => response.json())
      .then(data => {
        const updatedGenres = data.map(genre => ({
          ...genre,
          artists: [],
          showArtists: false
        }));
        setGenres(updatedGenres);
      })
      .catch(error => {
        console.error('Error fetching genres:', error);
      });
  }, []);

  const handleGenreClick = (genreID) => {
    const genre = genres.find(g => g.GenreID === genreID);
    if (!genre.artists.length) {
      fetchArtists(genreID);
    } else {
      toggleArtistsDisplay(genreID);
    }
  };

  const toggleArtistsDisplay = (genreID) => {
    const updatedGenres = genres.map(genre => ({
      ...genre,
      showArtists: genre.GenreID === genreID ? !genre.showArtists : genre.showArtists
    }));
    setGenres(updatedGenres);
  };

  return (
   <div className="artist-page-container">
     {genres.map(genre => (
       <div key={genre.GenreID}>
         <Genre genre={genre} onGenreClick={() => handleGenreClick(genre.GenreID)} />
         {genre.showArtists && (
           <DataGrid key={`artist-${genre.GenreID}`} items={genre.artists} Component={Artist} />
         )}
       </div>
     ))}
   </div>
 );
}

export default ArtistPage;
