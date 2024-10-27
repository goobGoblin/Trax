import React, { useEffect, useState } from 'react';

function TestComponent() {
  const [genres, setGenres] = useState([]);

  useEffect(() => {
    fetch('/genres')
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
        return response.json();
      })
      .then(data => {
        setGenres(data); // Assuming data is an array of genre objects
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []);

  return (
    <div>
      <h2>Data from API:</h2>
      <ul>
        {genres.map(genre => (
          <li key={genre.id}>
            {genre.name} - {genre.description}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TestComponent;
