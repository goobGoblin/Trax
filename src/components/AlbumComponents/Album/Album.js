import React, { useState, useEffect } from 'react';
import './Album.css';

const Album = ({ album }) => {
  const [detailedAlbum, setDetailedAlbum] = useState(null);
  const [showTrackList, setShowTrackList] = useState(false);

  // Fetch detailed information for this album
  useEffect(() => {
    const fetchAlbumDetails = async () => {
      try {
        const response = await fetch(`/api/albums/details/${album.AlbumID}`);
        const data = await response.json();
        setDetailedAlbum(data); // Assume data contains all album details
      } catch (error) {
        console.error('Error fetching detailed album info:', error);
        setDetailedAlbum(null); // Handle error by setting detailedAlbum to null
      }
    };

    fetchAlbumDetails();
  }, [album.AlbumID]); // Fetch details whenever the album ID changes

  const toggleTrackList = (e) => {
    e.stopPropagation(); // Prevent event from bubbling up to any parent components
    setShowTrackList(!showTrackList);
  };

  if (!detailedAlbum) {
    return <div>Loading detailed information...</div>;
  }

  return (
    <div className="album-item" onClick={toggleTrackList}>
      <h5 id = "album-artist">{detailedAlbum.ArtistName || 'Unknown Artist'}</h5>
			<h5 id = "album-title">{detailedAlbum.Title || 'No Title Available'}</h5>
      <p>Genres: {detailedAlbum.Genres || 'No Genres Listed'}</p>
      <p>Subgenres: {detailedAlbum.Subgenres || 'No Subgenres Listed'}</p>
      <p>Recommended: {detailedAlbum.recommended || 'Not Recommended'}</p>
      {showTrackList && (
        <div>
          <p>Tracks:</p>
          <ul>
            {detailedAlbum.TrackList && detailedAlbum.TrackList.split(', ').map((track, index) => (
              <li key={index}>{track}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Album;
