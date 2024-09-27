import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav style={styles.nav}>
      <h2 style={styles.title}>Stock Trading App V0.1</h2>
      <ul style={styles.navLinks}>
        <li><Link to="/" style={styles.link}>Dashboard</Link></li>
      </ul>
    </nav>
  );
}

const styles = {
  nav: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#282c34',
    padding: '1rem 2rem',
    color: 'white',
  },
  title: {
    margin: 0,
  },
  navLinks: {
    listStyle: 'none',
    display: 'flex',
    margin: 0,
    padding: 0,
  },
  link: {
    color: 'white',
    textDecoration: 'none',
    marginLeft: '1rem',
  },
};

export default Navbar;
