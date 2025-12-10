import axios from 'axios'

console.log('VITE_API_URL:', import.meta.env.VITE_API_URL)
console.log('All env vars:', import.meta.env)

const axiosApi = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  withCredentials: true
})

export default axiosApi