import React from 'react';
import TradeForm from '../components/TradeForm';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function Dashboard() {
  return (
    <div style={styles.container}>
      <h1>Welcome to Your Dashboard</h1>
      <TradeForm action="buy" />
      <TradeForm action="sell" />
      {/* Add more components like Portfolio, Recent Trades, etc. */}
      <ToastContainer />
    </div>
  );
}

const styles = {
  container: {
    padding: '2rem',
    textAlign: 'center',
  },
};

export default Dashboard;
