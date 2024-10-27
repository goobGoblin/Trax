// src/components/NavigationBar/NavigationBar.jsx
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './NavigationBar.css'; // Import the CSS file for styling

const menuItems = [
  { id: 'search',   label: 'Search',  to: '/search'},
  { id: 'genres', 	label: 'Genres', 	to: '/genres' },
  { id: 'artists', 	label: 'Artists', to: '/artists' },
  { id: 'albums', 	label: 'Albums', 	to: '/albums' },
  { id: 'mixes', 		label: 'Mixes', 	to: '/mixes' },
  { id: 'labels', 	label: 'Labels',  to: '/labels'},
  // { id: 'account', 	label: 'Account', tp: '/account'},
];

function NavigationBar() {
  const [selected, setSelected] = useState(() => {
    const currentPath = window.location.pathname;
    const paths = ['search', 'genres', 'artists', 'albums', 'mixes'];
    return paths.find(path => currentPath.includes(`/${path}`)) || 'genres'; // Default to 'genres'
  });

  return (
    <nav className="navigation-bar">
          {menuItems.map((item) => (
            item.to ? (
              // Use Link for items with a 'to' property
              <Link
                to={item.to}
                key={item.id}
                className={`nav-item ${selected === item.id ? 'selected' : ''}`}
                onClick={() => setSelected(item.id)}
              >
                {item.label}
              </Link>
            ) : (
              // Fallback for items without a 'to' property
              <div
                key={item.id}
                className={`nav-item ${selected === item.id ? 'selected' : ''} ${item.label === 'Account' ? 'nav-item-account' : ''}`}
                onClick={() => setSelected(item.id)}
              >
                {item.label}
              </div>
            )
          ))}
        </nav>
  );
}

export default NavigationBar;
