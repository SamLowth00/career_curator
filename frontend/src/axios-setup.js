import axios from 'axios'

const axiosApi = axios.create({
  baseURL: 'http://localhost:8000', // Change to your backend URL if needed
  withCredentials: true
})

export default axiosApi