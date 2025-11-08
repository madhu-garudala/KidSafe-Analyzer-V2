import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const checkSystemStatus = async () => {
  const response = await api.get('/api/status');
  return response.data;
};

export const getCereals = async () => {
  const response = await api.get('/api/cereals');
  return response.data;
};

export const configureAPIKeys = async (config) => {
  const response = await api.post('/api/configure', config);
  return response.data;
};

export const analyzeIngredients = async (cerealName, ingredients) => {
  const response = await api.post('/api/analyze', {
    cereal_name: cerealName,
    ingredients: ingredients,
  });
  return response.data;
};

export const sendChatMessage = async (chatData) => {
  const response = await api.post('/api/chat', chatData);
  return response.data;
};

export const searchProduct = async (productName) => {
  const response = await api.post('/api/search-product', {
    product_name: productName
  });
  return response.data;
};

export default api;

