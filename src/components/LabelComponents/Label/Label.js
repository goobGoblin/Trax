// Label.js
import React from 'react';
import './Label.css'; // Make sure to create appropriate CSS for styling

const Label = ({ label }) => {
  return (
    <div className="label-item">
      <h4>{label.Name}</h4>
    </div>
  );
};

export default Label;
