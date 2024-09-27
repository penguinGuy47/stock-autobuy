import React, { useState } from 'react';
import TradeForm from './TradeForm';
import { toast } from 'react-toastify';

function TradeManager() {
  const [forms, setForms] = useState([]);

  const addForm = (action) => {
    const newForm = {
      id: Date.now(), // Unique identifier
      action: action, // 'buy' or 'sell'
    };
    setForms([...forms, newForm]);
  };

  const removeForm = (id) => {
    setForms(forms.filter(form => form.id !== id));
    toast.info('Trade form removed.');
  };

  return (
    <div style={styles.container}>
      <h2>Trade Manager</h2>
      <div style={styles.buttonContainer}>
        <button onClick={() => addForm('buy')} style={styles.addButton}>
          Add Another Buy
        </button>
        <button onClick={() => addForm('sell')} style={styles.addButton}>
          Add Another Sell
        </button>
      </div>
      {forms.length === 0 && <p>No trade forms added yet.</p>}
      {forms.map((form) => (
        <TradeForm
          key={form.id}
          action={form.action}
          onRemove={() => removeForm(form.id)}
        />
      ))}
    </div>
  );
}

const styles = {
  container: {
    maxWidth: '800px',
    margin: '2rem auto',
    padding: '1rem',
    border: '2px solid #007bff',
    borderRadius: '10px',
  },
  buttonContainer: {
    display: 'flex',
    justifyContent: 'center',
    gap: '1rem',
    marginBottom: '1rem',
  },
  addButton: {
    padding: '0.7rem 1.2rem',
    backgroundColor: '#28a745',
    color: 'white',
    border: 'none',
    cursor: 'pointer',
    borderRadius: '5px',
    fontSize: '1rem',
  },
};

export default TradeManager;
