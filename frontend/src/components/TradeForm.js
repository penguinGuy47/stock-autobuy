import React, { useState } from 'react';
import api from '../services/api';
import { toast } from 'react-toastify';

function TradeForm({ action, onRemove }) {
  const [tickers, setTickers] = useState(['']);
  const [broker, setBroker] = useState('');
  const [quantity, setQuantity] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [twoFaCode, setTwoFaCode] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [method, setMethod] = useState(null); // 'text' or 'captcha_and_text'
  const [loading, setLoading] = useState(false);

  const handleTickerChange = (index, value) => {
    const newTickers = [...tickers];
    newTickers[index] = value.toUpperCase();
    setTickers(newTickers);
  };

  const addTickerField = () => {
    setTickers([...tickers, '']);
  };

  const removeTickerField = (index) => {
    const newTickers = [...tickers];
    newTickers.splice(index, 1);
    setTickers(newTickers);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Basic validation
    if (
      (action === 'buy' && tickers.some(ticker => ticker === '')) ||
      (action === 'sell' && !tickers.length) ||
      !broker ||
      !quantity ||
      !username ||
      !password
    ) {
      toast.error('Please fill in all required fields.');
      return;
    }

    // Validation for quantity
    if (!/^\d+$/.test(quantity) || parseInt(quantity) <= 0) {
      toast.error('Please enter a valid quantity.');
      return;
    }

    setLoading(true);
    try {
      const endpoint = action === 'buy' ? '/buy' : '/sell';
      const payload = {
        tickers: tickers,
        broker,
        quantity: parseInt(quantity),
        username,
        password,
      };
      const response = await api.post(endpoint, payload);

      if (response.data.status === 'success') {
        toast.success(`${capitalize(action)} successful.`);
        resetForm();
      } else if (response.data.status === '2FA_required') {
        setSessionId(response.data.session_id);
        setMethod(response.data.method); // 'text' or 'captcha_and_text'
        if (response.data.method === 'captcha_and_text') {
          toast.info('Captcha and 2FA are required. Please solve the Captcha in the browser and enter your 2FA code below.');
        } else {
          toast.info('2FA is required. Please enter your 2FA code below.');
        }
      } else {
        toast.error(`${capitalize(action)} failed: ${response.data.message || 'Unknown error.'}`);
        resetForm();
      }
    } catch (error) {
      console.error(`${capitalize(action)} failed:`, error.response ? error.response.data : error.message);
      toast.error(`${capitalize(action)} failed: ${error.response?.data?.error || 'Unknown error.'}`);
    } finally {
      setLoading(false);
    }
  };

  const handle2FASubmit = async (e) => {
    e.preventDefault();

    if ((method === 'text' || method === 'captcha_and_text') && !twoFaCode) {
      toast.error('Please enter the 2FA code.');
      return;
    }

    setLoading(true);
    try {
      const payload = {
        session_id: sessionId,
        two_fa_code: twoFaCode,
      };
      const response = await api.post('/complete_2fa', payload);

      if (response.data.status === 'success') {
        toast.success(`${capitalize(action)} successful.`);
        resetForm();
      } else {
        toast.error(`${capitalize(action)} failed: ${response.data.message || 'Unknown error.'}`);
        resetForm();
      }
    } catch (error) {
      console.error(`${capitalize(action)} failed during 2FA:`, error.response ? error.response.data : error.message);
      toast.error(`${capitalize(action)} failed during 2FA: ${error.response?.data?.error || 'Unknown error.'}`);
      resetForm();
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setTickers(['']);
    setBroker('');
    setQuantity('');
    setUsername('');
    setPassword('');
    setTwoFaCode('');
    setSessionId(null);
    setMethod(null);
  };

  const capitalize = (s) => s.charAt(0).toUpperCase() + s.slice(1);

  return (
    <div style={styles.container}>
      <h3>{capitalize(action)} Stock</h3>
      <button onClick={onRemove} style={styles.removeFormButton} disabled={loading}>
        Remove
      </button>
      {!sessionId ? (
        <form onSubmit={handleSubmit} style={styles.form}>
          {tickers.map((ticker, index) => (
            <div key={index} style={styles.tickerContainer}>
              <input
                type="text"
                placeholder="Ticker Symbol"
                value={ticker}
                onChange={(e) => handleTickerChange(index, e.target.value)}
                required
                style={styles.input}
              />
              {index === tickers.length - 1 && (
                <button type="button" onClick={addTickerField} style={styles.addTickerButton}>
                  +
                </button>
              )}
              {tickers.length > 1 && (
                <button type="button" onClick={() => removeTickerField(index)} style={styles.removeTickerButton}>
                  -
                </button>
              )}
            </div>
          ))}
          <select
            value={broker}
            onChange={(e) => setBroker(e.target.value)}
            required
            style={styles.input}
          >
            <option value="">Select Broker</option>
            <option value="chase">Chase</option>
            <option value="fidelity">Fidelity</option>
            <option value="firstrade">First Trade</option>
            <option value="schwab">Schwab</option>
            <option value="webull">Webull</option>
            <option value="wells">Wells Fargo</option>
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
            placeholder={broker === "webull" ? `Phone Number` : "Broker Username"}
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
            {loading ? 'Processing...' : capitalize(action)}
          </button>
        </form>
      ) : (
        <form onSubmit={handle2FASubmit} style={styles.form}>
          {method === 'captcha_and_text' && (
            <>
              <p>
                A Captcha has been detected in your trading browser. Please solve it manually in the browser window.
                After solving the Captcha, enter your 2FA code below.
              </p>
            </>
          )}
          <input
            type="text"
            placeholder={`Enter ${capitalize(broker)} 2FA Code`}
            value={twoFaCode}
            onChange={(e) => setTwoFaCode(e.target.value)}
            required
            style={styles.input}
          />
          <button type="submit" style={styles.button} disabled={loading}>
            {loading ? 'Submitting...' : 'Submit 2FA Code'}
          </button>
        </form>
      )}
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
  tickerContainer: {
    display: 'flex',
    alignItems: 'center',
  },
  input: {
    padding: '0.5rem',
    margin: '0.5rem 0',
    flex: 1,
  },
  addTickerButton: {
    padding: '0.5rem',
    marginLeft: '0.2rem',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    cursor: 'pointer',
    borderRadius: '3px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '30px',
    height: '30px',
  },
  removeTickerButton: {
    padding: '0.5rem',
    marginLeft: '0.2rem',
    backgroundColor: '#d9534f',
    color: 'white',
    border: 'none',
    cursor: 'pointer',
    borderRadius: '3px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '30px',
    height: '30px',
  },
  removeFormButton: {
    top: '10px',
    right: '10px',
    backgroundColor: '#dc3545',
    color: 'white',
    border: 'none',
    padding: '0.3rem 0.6rem',
    cursor: 'pointer',
    borderRadius: '3px',
  },
  button: {
    padding: '0.5rem',
    backgroundColor: '#282c34',
    color: 'white',
    border: 'none',
    cursor: 'pointer',
    marginTop: '1rem',
  },
};

export default TradeForm;
