// DataGrid.js
import React from 'react';
import './DataGrid.css';

const DataGrid = ({ items, Component }) => {
    console.log("DataGrid items:", items);  // Log to see what items DataGrid is receiving

    if (!items || items.length === 0) return <p>No data found.</p>;

    return (
        <div className="data-grid-container">
            {items.map((item, index) => (
                <Component key={index} subgenre={item} />
            ))}
        </div>
    );
};

export default DataGrid;