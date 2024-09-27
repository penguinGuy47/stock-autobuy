import React, { useState } from 'react';
import TradeForm from '../components/TradeForm';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function Dashboard() {
  const [tradeForms, setTradeForms] = useState([
    { id: 1, action: 'buy' },
    { id: 2, action: 'sell' },
  ]);

  const addTradeForm = (action) => {
    const newForm = {
      id: Date.now(), // Unique identifier
      action: action, // 'buy' or 'sell'
    };
    setTradeForms([...tradeForms, newForm]);
  };

  const removeTradeForm = (id) => {
    setTradeForms(tradeForms.filter(form => form.id !== id));
    toast.info('Trade form removed.');
  };

  return (
    <div style={styles.container}>
      <h1>Welcome to Your Dashboard</h1>
      <div style={styles.buttonContainer}>
        <button onClick={() => addTradeForm('buy')} style={styles.addButton}>
          Add Another Buy
        </button>
        <button onClick={() => addTradeForm('sell')} style={styles.addButton}>
          Add Another Sell
        </button>
      </div>
      {tradeForms.map((form) => (
        <TradeForm
          key={form.id}
          action={form.action}
          onRemove={() => removeTradeForm(form.id)}
        />
      ))}
      <ToastContainer />
    </div>
  );
}

const styles = {
  container: {
    padding: '2rem',
    textAlign: 'center',
  },
  buttonContainer: {
    marginBottom: '1rem',
  },
  addButton: {
    padding: '0.7rem 1.2rem',
    margin: '0 0.5rem',
    backgroundColor: '#28a745',
    color: 'white',
    border: 'none',
    cursor: 'pointer',
    borderRadius: '5px',
    fontSize: '1rem',
  },
};

export default Dashboard;
