import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api/trade', // Adjust the base URL as needed
  headers: {
    'Content-Type': 'application/json',
  },
});

// Optional: Add interceptors if needed
// api.interceptors.response.use(
//   (response) => response,
//   (error) => {
//     // Handle errors globally if desired
//     return Promise.reject(error);
//   }
// );

export default api;
