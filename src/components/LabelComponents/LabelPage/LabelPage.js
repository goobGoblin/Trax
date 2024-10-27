// LabelPage.js
import React, { useState, useEffect } from 'react';
import LabelGrid from '../Label/LabelGrid';
import './LabelPage.css'; // Make sure to create appropriate CSS for styling

function LabelPage() {
  const [labels, setLabels] = useState([]);

  useEffect(() => {
    fetch('/api/labels')
      .then(response => response.json())
      .then(data => setLabels(data))
      .catch(error => console.error('Error fetching labels:', error));
  }, []);

  return (
    <div className="label-page-container">
      <h1>Labels</h1>
      <LabelGrid labels={labels} />
    </div>
  );
}

export default LabelPage;
