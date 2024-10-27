import React from 'react';
import './Subgenre.css';

const Subgenre = ({ subgenre }) => {
  return (
    <div className="subgenre-item">
      <h5>{subgenre.SubgenreName}</h5>
      <p>{subgenre.Description}</p>
    </div>
  );
};

export default Subgenre;
