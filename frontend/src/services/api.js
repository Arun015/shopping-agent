import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const sendMessage = async (message, sessionId = null) => {
  const response = await api.post('/api/chat', {
    message,
    session_id: sessionId,
  });
  return response.data;
};

export const getPhones = async () => {
  const response = await api.get('/api/phones');
  return response.data;
};

export const getPhone = async (phoneId) => {
  const response = await api.get(`/api/phones/${phoneId}`);
  return response.data;
};

export default api;



