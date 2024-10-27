import React, { useState, useEffect } from 'react';
import './TemporarySearchPage.css';

function SearchPage() {
  function fetchTracksByID(genreID) {
    // Return the promise chain from fetch
    return fetch(`/api/tracks?genreID=${genreID}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Fetched tracks:', data);
            return data;
        })
        .catch(error => {
            console.error('Error fetching tracks:', error);
            throw error;
        });
  }


  function fetchTracksByTitle(title) {
    // Return the promise chain from fetch
    return fetch(`/api/search?title=${title}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Fetched tracks:', data);
            return data;
        })
        .catch(error => {
            console.error('Error fetching tracks:', error);
            throw error;
        });
  }

  function fetchArtistsByGenreID(genreID) {
    // Return the promise chain from fetch
    return fetch(`/api/artists?genreID=${genreID}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Fetched tracks:', data);
            return data;
        })
        .catch(error => {
            console.error('Error fetching tracks:', error);
            throw error;
        });
  }

  function fetchTracksByArtist(name) {
    // Return the promise chain from fetch
    return fetch(`/api/tracksByArtist?artistName=${name}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Fetched tracks:', data);
            return data;
        })
        .catch(error => {
            console.error('Error fetching tracks:', error);
            throw error;
        });
  }

  useEffect(() => {

  }, []);


  const genreSearchClick = async () => {
    let genre = document.getElementById("trackGenreName").value;
    try {
      let result = await fetchTracksByID(genre);
      let string_result = "";
      for (let i = 0; i < result.length; i++) {
        string_result += "Track " + result[i].TrackID + ": " + result[i].Title + "\n";
      }
      document.getElementById("textarea1").value = string_result;
    } catch (error) {
        console.error('Failed to fetch tracks:', error);
    }
  };

  const artistSearchClick = async () => {
    let genre = document.getElementById("artistGenreName").value;
    try {
      let result = await fetchArtistsByGenreID(genre);
      let string_result = "";
      for (let i = 0; i < result.length; i++) {
        string_result += result[i].Name + ": " + result[i].Biography + "\n";
      }
      document.getElementById("textarea2").value = string_result;
    } catch (error) {
      console.error('Failed to fetch artists:', error);
    }
  }

  const titleSearchClick = async () => {
    let title = document.getElementById("songName").value;
    try {
      let result = await fetchTracksByTitle(title);
      let string_result = "";
      for (let i = 0; i < result.length; i++) {
        string_result += "Track " + result[i].TrackID + ": " + result[i].Title + "\n";
      }
      document.getElementById("textarea3").value = string_result;
    } catch (error) {
      console.error('Failed to fetch tracks:', error);
    }
  }

  const tracksByArtistSearchClick = async () => {
    let artist = document.getElementById("artistName").value;
    try {
      let result = await fetchTracksByArtist(artist);
      let string_result = "";
      for (let i = 0; i < result.length; i++) {
        string_result += result[i].Title + " - " + result[i].Name + "\n";
      }
      document.getElementById("textarea4").value = string_result;
    } catch (error) {
      console.error('Failed to fetch tracks:', error);
    }
  }

  return (
    <div className="search-page-container">
      <div className="search-container">
        <h2>Search Tracks by Genre</h2>
        <select id="trackGenreName">
          <option value="1">Ambient</option>
          <option value="2">Blues</option>
          <option value="3">Classical Music</option>
          <option value="4">Dance Music</option>
          <option value="5">Electronic</option>
          <option value="6">Industrial & Noise</option>
          <option value="7">Jazz</option>
          <option value="8">Metal</option>
          <option value="9">Musical Theater and Entertainment</option>
          <option value="10">New Age</option>
          <option value="11">Pop</option>
          <option value="12">Psychedelia</option>
          <option value="13">Punk</option>
          <option value="14">R&B</option>
          <option value="15">Singer-Songwriter</option>
          <option value="16">Spoken Word</option>
        </select>
        <button id="genreSearch" onClick={genreSearchClick}>Search</button>
        <br></br><p>Results:</p>
        <textarea id="textarea1" rows="4" cols="70" readOnly></textarea>
      </div>

      <div className="search-container">
        <h2>Search Artists by Genre</h2>
        <select id="artistGenreName">
          <option value="1">Ambient</option>
          <option value="2">Blues</option>
          <option value="3">Classical Music</option>
          <option value="4">Dance Music</option>
          <option value="5">Electronic</option>
          <option value="6">Industrial & Noise</option>
          <option value="7">Jazz</option>
          <option value="8">Metal</option>
          <option value="9">Musical Theater and Entertainment</option>
          <option value="10">New Age</option>
          <option value="11">Pop</option>
          <option value="12">Psychedelia</option>
          <option value="13">Punk</option>
          <option value="14">R&B</option>
          <option value="15">Singer-Songwriter</option>
          <option value="16">Spoken Word</option>
        </select>
        <button id="artistSearch" onClick={artistSearchClick}>Search</button>
        <br></br><p>Results:</p>
        <textarea id="textarea2" rows="4" cols="70" readOnly></textarea>
      </div>

      <div className="search-container">
        <h2>Search Tracks by Song Name</h2>
        <input type="text" id="songName" />
        <button id="titleSearch" onClick={titleSearchClick}>Search</button>
        <br></br><p>Results:</p>
        <textarea id="textarea3"rows="10" cols="70" readOnly></textarea>
      </div>

      <div className="search-container">
        <h2>Search Tracks by Artist</h2>
        <input type="text" id="artistName" />
        <button id="tracksByArtist" onClick={tracksByArtistSearchClick}>Search</button>
        <br></br><p>Results:</p>
        <textarea id="textarea4"rows="10" cols="70" readOnly></textarea>
      </div>
    </div>
  );
}

export default SearchPage;
