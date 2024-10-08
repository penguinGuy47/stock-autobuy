import React, { useState } from 'react';
import TradeForm from '../components/TradeForm';
import styled from 'styled-components';
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
    <Container>
      <Header>
        <Title>Welcome to Your Dashboard</Title>
        <ButtonGroup>
          <AddButton onClick={() => addTradeForm('buy')}>Add Buy Form</AddButton>
          <AddButton onClick={() => addTradeForm('sell')}>Add Sell Form</AddButton>
        </ButtonGroup>
      </Header>
      <GridContainer>
        {tradeForms.map((form) => (
          <TradeForm
            key={form.id}
            action={form.action}
            onRemove={() => removeTradeForm(form.id)}
          />
        ))}
      </GridContainer>
      <ToastContainer />
    </Container>
  );
}

const Container = styled.div`
  padding: 2rem;
  min-height: 100vh;
  box-sizing: border-box;
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
`;

const Title = styled.h1`
  margin: 0;
  font-size: 2rem;
  color: white;
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;

  @media (min-width: 600px) {
    margin-top: 0;
  }
`;

const AddButton = styled.button`
  padding: 0.7rem 1.2rem;
  background-color: #28a745;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: 1rem;
  
  &:hover {
    background-color: #218838;
  }
`;

const GridContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  justify-content: start;
  
  /* Limit to 5 columns on very large screens */
  @media (min-width: 1500px) {
    grid-template-columns: repeat(5, 1fr);
  }
  
  @media (min-width: 1200px) and (max-width: 1499px) {
    grid-template-columns: repeat(4, 1fr);
  }
  
  @media (min-width: 900px) and (max-width: 1199px) {
    grid-template-columns: repeat(3, 1fr);
  }
  
  @media (min-width: 600px) and (max-width: 899px) {
    grid-template-columns: repeat(2, 1fr);
  }
  
  @media (max-width: 599px) {
    grid-template-columns: 1fr;
  }
`;

export default Dashboard;
