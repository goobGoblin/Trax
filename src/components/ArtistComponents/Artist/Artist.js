// Artist.js
import React from 'react';
import './Artist.css';

const Artist = ({ artist }) => {
  return (
    <div className="artist-item">
      <h5>{artist.Name}</h5> {/* Replace 'Name' with the property name for artist's name */}
      <p>{artist.Biograpraphy}</p> {/* Replace 'Biography' with the property name for artist's bio */}
      {/* Get the artists genres and subgenres */}
    </div>
  );
};

export default Artist;
