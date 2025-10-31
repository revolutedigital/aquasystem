import axios from 'axios'
import { useAuthStore } from '@/store/auth'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api

// API endpoints
export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/auth/login', { email, password }),
}

export const alunosAPI = {
  list: () => api.get('/alunos'),
  get: (id: number) => api.get(`/alunos/${id}`),
  create: (data: any) => api.post('/alunos', data),
  update: (id: number, data: any) => api.put(`/alunos/${id}`, data),
  delete: (id: number) => api.delete(`/alunos/${id}`),
}

export const turmasAPI = {
  list: () => api.get('/turmas'),
  get: (id: number) => api.get(`/turmas/${id}`),
  create: (data: any) => api.post('/turmas', data),
  update: (id: number, data: any) => api.put(`/turmas/${id}`, data),
  delete: (id: number) => api.delete(`/turmas/${id}`),
}

export const professoresAPI = {
  list: () => api.get('/professores'),
  get: (id: number) => api.get(`/professores/${id}`),
  create: (data: any) => api.post('/professores', data),
  update: (id: number, data: any) => api.put(`/professores/${id}`, data),
  delete: (id: number) => api.delete(`/professores/${id}`),
}

export const pagamentosAPI = {
  list: () => api.get('/pagamentos'),
  get: (id: number) => api.get(`/pagamentos/${id}`),
  create: (data: any) => api.post('/pagamentos', data),
  update: (id: number, data: any) => api.put(`/pagamentos/${id}`, data),
  delete: (id: number) => api.delete(`/pagamentos/${id}`),
}

export const dashboardAPI = {
  getMetrics: () => api.get('/dashboard/metrics'),
  getRevenueChart: () => api.get('/dashboard/revenue'),
  getAttendanceChart: () => api.get('/dashboard/attendance'),
}