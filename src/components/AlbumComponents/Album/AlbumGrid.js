import React from 'react';
import Album from './Album';
import './AlbumGrid.css';

const AlbumGrid = ({ albums }) => {
  if (!Array.isArray(albums)) {
    console.error('AlbumGrid expected an array, but received:', albums);
    return <div>No albums available or data is incorrect.</div>;
  }

  // Filter out duplicate albums based on their ID
  const uniqueAlbums = albums.reduce((acc, current) => {
    const x = acc.find(item => item.AlbumID === current.AlbumID);
    if (!x) {
      return acc.concat([current]);
    } else {
      return acc;
    }
  }, []);

  return (
    <div className="album-grid-container">
      {uniqueAlbums.map(album => (
        <Album key={album.AlbumID} album={album} />  // Using AlbumID as key
      ))}
    </div>
  );
};

export default AlbumGrid;
