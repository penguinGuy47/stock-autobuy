import React, { useState } from 'react';
import api from '../services/api';
import { toast } from 'react-toastify';

function TradeForm({ action }) {
  const [ticker, setTicker] = useState('');
  const [broker, setBroker] = useState('');
  const [quantity, setQuantity] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Basic validation
    if (!ticker || !broker || !quantity || !username || !password) {
      toast.error('Please fill in all fields.');
      return;
    }

    // Additional validation for quantity
    if (!/^\d+$/.test(quantity) || parseInt(quantity) <= 0) {
      toast.error('Please enter a valid quantity.');
      return;
    }

    setLoading(true);
    try {
      const endpoint = action === 'buy' ? '/buy' : '/sell';
      const payload = { ticker, broker, quantity: parseInt(quantity), username, password };
      const response = await api.post(endpoint, payload);
      toast.success(`${action.charAt(0).toUpperCase() + action.slice(1)} successful.`);
      // Reset form fields
      setTicker('');
      setBroker('');
      setQuantity('');
      setUsername('');
      setPassword('');
    } catch (error) {
      console.error(`${action} failed:`, error.response ? error.response.data : error.message);
      toast.error(`${action.charAt(0).toUpperCase() + action.slice(1)} failed: ${error.response?.data?.error || 'Unknown error.'}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h3>{action.charAt(0).toUpperCase() + action.slice(1)} Stock</h3>
      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          type="text"
          placeholder="Ticker Symbol"
          value={ticker}
          onChange={(e) => setTicker(e.target.value.toUpperCase())}
          required
          style={styles.input}
        />
        <select
          value={broker}
          onChange={(e) => setBroker(e.target.value)}
          required
          style={styles.input}
        >
          <option value="">Select Broker</option>
          <option value="chase">Chase</option>
          <option value="fidelity">Fidelity</option>
          <option value="schwab">Schwab</option>
          {/* Add other brokers as needed */}
        </select>
        <input
          type="number"
          placeholder="Quantity"
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
          min="1"
          required
          style={styles.input}
        />
        <input
          type="text"
          placeholder="Broker Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          style={styles.input}
        />
        <input
          type="password"
          placeholder="Broker Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={styles.input}
        />
        <button type="submit" style={styles.button} disabled={loading}>
          {loading ? 'Processing...' : action.charAt(0).toUpperCase() + action.slice(1)}
        </button>
      </form>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: '500px',
    margin: '1rem auto',
    padding: '1rem',
    border: '1px solid #ccc',
    borderRadius: '5px',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
  },
  input: {
    padding: '0.5rem',
    margin: '0.5rem 0',
  },
  button: {
    padding: '0.5rem',
    backgroundColor: '#282c34',
    color: 'white',
    border: 'none',
    cursor: 'pointer',
  },
};

export default TradeForm;
