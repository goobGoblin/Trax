// src/components/universal/AccountDropdown.jsx
import React, { useState } from 'react';
import './AccountDropdown.css'; // Import the CSS file for styling

function AccountDropdown() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="account-dropdown">
      <button onClick={() => setIsOpen(!isOpen)}>Account</button>
      {isOpen && (
        <ul className="dropdown-menu">
          <li>Profile</li>
          <li>Settings</li>
          <li>Logout</li>
        </ul>
      )}
    </div>
  );
}

export default AccountDropdown;
