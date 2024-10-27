// Mix.js

import React from 'react';
import './Mix.css';

const Mix = ({ mix }) => {
  return (
    <div className="mix-item">
      <h5>{mix.name}</h5>
      <p>{mix.description}</p>
    </div>
  );
};

export default Mix;
