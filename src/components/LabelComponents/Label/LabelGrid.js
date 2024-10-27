// LabelGrid.js
import React from 'react';
import Label from './Label';
import './LabelGrid.css'; // Make sure to create appropriate CSS for styling

const LabelGrid = ({ labels }) => {
  if (!labels || labels.length === 0) return <p>No labels found.</p>;

  return (
    <div className="label-grid-container">
      {labels.map(label => (
        <Label key={label.Name} label={label} />
      ))}
    </div>
  );
};

export default LabelGrid;
