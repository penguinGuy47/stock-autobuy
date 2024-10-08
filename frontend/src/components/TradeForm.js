import React, { useState } from 'react';
import api from '../services/api';
import { toast } from 'react-toastify';
import styled from 'styled-components';
import '../App.css';

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
    <FormContainer>
      <FormHeader>
        <FormTitle>{capitalize(action)} Stock</FormTitle>
        <RemoveButton onClick={onRemove} disabled={loading} aria-label="Remove Form">
          &times;
        </RemoveButton>
      </FormHeader>
      {!sessionId ? (
        <form onSubmit={handleSubmit}>
          {/* Ticker Fields */}
          <FormRow>
            <Label>Ticker Symbol(s)</Label>
            <TickerWrapper>
              {tickers.map((ticker, index) => (
                <TickerContainer key={index}>
                  <TickerInput
                    type="text"
                    placeholder="Ticker"
                    value={ticker}
                    onChange={(e) => handleTickerChange(index, e.target.value)}
                    required
                  />
                  {tickers.length > 1 && (
                    <RemoveTickerButton
                      type="button"
                      onClick={() => removeTickerField(index)}
                      disabled={loading}
                      aria-label="Remove Ticker"
                    >
                      &ndash;
                    </RemoveTickerButton>
                  )}
                  {index === tickers.length - 1 && (
                    <AddTickerButton
                      type="button"
                      onClick={addTickerField}
                      disabled={loading}
                      aria-label="Add Ticker"
                    >
                      +
                    </AddTickerButton>
                  )}
                </TickerContainer>
              ))}
            </TickerWrapper>
          </FormRow>

          {/* Broker Selection */}
          <FormRow>
            <Label>Broker</Label>
            <Select
              value={broker}
              onChange={(e) => setBroker(e.target.value)}
              required
            >
              <option value="">Select Broker</option>
              <option value="chase">Chase</option>
              <option value="fidelity">Fidelity</option>
              <option value="firstrade">First Trade</option>
              <option value="schwab">Schwab</option>
              <option value="webull">Webull</option>
              <option value="wells">Wells Fargo</option>
            </Select>
          </FormRow>

          {/* Quantity */}
          <FormRow>
            <Label>Quantity</Label>
            <Input
              type="number"
              placeholder="Quantity"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
              min="1"
              required
            />
          </FormRow>

          {/* Username */}
          <FormRow>
            <Label>{broker === 'webull' ? 'Phone Number' : 'Broker Username'}</Label>
            <Input
              type="text"
              placeholder={broker === 'webull' ? 'Phone Number' : 'Broker Username'}
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </FormRow>

          {/* Password */}
          <FormRow>
            <Label>Broker Password</Label>
            <Input
              type="password"
              placeholder="Broker Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </FormRow>

          {/* Submit Button */}
          <FormRow>
            <EmptyCell />
            <SubmitButton type="submit" disabled={loading}>
              {loading ? 'Processing...' : capitalize(action)}
            </SubmitButton>
          </FormRow>
        </form>
      ) : (
        <form onSubmit={handle2FASubmit}>
          {method === 'captcha_and_text' && (
            <InfoRow>
              <EmptyCell />
              <InfoText>
                A Captcha has been detected in your trading browser. Please solve it manually in the browser window.
                After solving the Captcha, enter your 2FA code below.
              </InfoText>
            </InfoRow>
          )}
          {method === 'text' && (
            <InfoRow>
              <EmptyCell />
              <InfoText>
                2FA is required. Please enter your 2FA code below.
              </InfoText>
            </InfoRow>
          )}
          <FormRow>
            <Label>2FA Code</Label>
            <Input
              type="text"
              placeholder={`Enter ${capitalize(broker)} 2FA Code`}
              value={twoFaCode}
              onChange={(e) => setTwoFaCode(e.target.value)}
              required
            />
          </FormRow>
          <FormRow>
            <EmptyCell />
            <SubmitButton type="submit" disabled={loading}>
              {loading ? 'Submitting...' : 'Submit 2FA Code'}
            </SubmitButton>
          </FormRow>
        </form>
      )}
    </FormContainer>
  );
}

const FormContainer = styled.div`
  background-color: #ffffff;
  padding: 1.5rem;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 300px; /* Adjust based on desired form width */
  box-sizing: border-box;
`;

const FormHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
`;

const FormTitle = styled.h3`
  margin: 0;
  font-size: 1.25rem;
  color: #333333;
`;

const RemoveButton = styled.button`
  background-color: #dc3545;
  color: white;
  border: none;
  font-size: 1.2rem;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  cursor: pointer;
  
  &:hover {
    background-color: #c82333;
  }
`;

const FormRow = styled.div`
  display: contents;
`;

const Label = styled.label`
  font-weight: bold;
  color: #555555;
  margin-bottom: 0.5rem;
  display: block;
`;

const EmptyCell = styled.div``;

const Input = styled.input`
  padding: 0.6rem;
  border: 1px solid #ced4da;
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
`;

const Select = styled.select`
  padding: 0.6rem;
  border: 1px solid #ced4da;
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
  background-color: #ffffff;
`;

const TickerWrapper = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const TickerContainer = styled.div`
  display: flex;
  align-items: center;
`;

const TickerInput = styled.input`
  flex: 1;
  padding: 0.6rem;
  border: 1px solid #ced4da;
  border-radius: 4px;
`;

const AddTickerButton = styled.button`
  margin-left: 0.5rem;
  padding: 0.6rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  
  &:hover {
    background-color: #218838;
  }
`;

const RemoveTickerButton = styled.button`
  margin-left: 0.5rem;
  padding: 0.6rem;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  
  &:hover {
    background-color: #c82333;
  }
`;

const SubmitButton = styled.button`
  margin-top: 10px;
  padding: 0.5rem;
  background-color: #16423C;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  
  &:hover {
    background-color: #0069d9;
  }
`;

const InfoRow = styled.div`
  display: contents;
`;

const InfoText = styled.p`
  color: #555555;
  font-size: 0.95rem;
  margin: 0;
`;

export default TradeForm;
