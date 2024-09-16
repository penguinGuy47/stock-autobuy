import React, { useState } from 'react';

function TradingUI() {
  const [useUniversalTicker, setUseUniversalTicker] = useState(true);
  const [universalTicker, setUniversalTicker] = useState('');
  const [brokers, setBrokers] = useState([
    { name: 'Chase', enabled: false, ticker: '' },
    { name: 'Fidelity', enabled: false, ticker: '' },
    { name: 'First Trade', enabled: false, ticker: '' },
    // { name: 'Public', enabled: false, ticker: '' },
    { name: 'Robinhood', enabled: false, ticker: '' },
    { name: 'Schwab', enabled: false, ticker: '' },
    { name: 'Tradier', enabled: false, ticker: '' },
  ]);

  const handleBrokerToggle = (index) => {
    const updatedBrokers = [...brokers];
    updatedBrokers[index].enabled = !updatedBrokers[index].enabled;
    setBrokers(updatedBrokers);
  };

  const handleIndividualTickerChange = (index, value) => {
    const updatedBrokers = [...brokers];
    updatedBrokers[index].ticker = value;
    setBrokers(updatedBrokers);
  };

  const handleUniversalTickerChange = (value) => {
    setUniversalTicker(value);
  };

  const handleUniversalToggle = () => {
    setUseUniversalTicker(!useUniversalTicker);
  };

  return (
    <div>
      <h2>Trading Setup</h2>
      
      {/* Universal Ticker Input */}
      <label>
        <input
          type="checkbox"
          checked={useUniversalTicker}
          onChange={handleUniversalToggle}
        />
        Use Universal Ticker
      </label>
      <br />
      <input
        type="text"
        value={universalTicker}
        onChange={(e) => handleUniversalTickerChange(e.target.value)}
        disabled={!useUniversalTicker}
        placeholder="Universal Ticker"
      />

      {/* Brokers List */}
      {brokers.map((broker, index) => (
        <div key={index}>
            <br />
            <hr />
            <h3>{broker.name}</h3>
            <label>
                <input
                type="checkbox"
                checked={broker.enabled}
                onChange={() => handleBrokerToggle(index)}
                />
                Enable Trade
            </label>
            <br />
            <input
                type="text"
                value={broker.ticker}
                onChange={(e) => handleIndividualTickerChange(index, e.target.value)}
                disabled={useUniversalTicker || !broker.enabled}
                placeholder={`${broker.name} Ticker`}
            />
        </div>
      ))}
    </div>
  );
}

export default TradingUI;
