import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api/trade',
  headers: {
    'Content-Type': 'application/json',
  },
});


// api.interceptors.response.use(
//   (response) => response,
//   (error) => {
//     // Handle errors globally
//     return Promise.reject(error);
//   }
// );

export default api;
