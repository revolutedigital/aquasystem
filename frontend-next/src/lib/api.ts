import axios from 'axios'
import { useAuthStore } from '@/store/auth'
import type {
  AlunoCreateData,
  AlunoUpdateData,
  PagamentoCreateData,
  HorarioCreateData
} from '@/types'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

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
  list: () => api.get('/alunos').then(res => res.data),
  get: (id: number) => api.get(`/alunos/${id}`).then(res => res.data),
  create: (data: AlunoCreateData) => api.post('/alunos', data).then(res => res.data),
  update: (id: number, data: AlunoUpdateData) => api.put(`/alunos/${id}`, data).then(res => res.data),
  delete: (id: number) => api.delete(`/alunos/${id}`).then(res => res.data),
  getInadimplentes: () => api.get('/alunos/inadimplentes').then(res => res.data),
  getPagamentos: (id: number) => api.get(`/alunos/${id}/pagamentos`).then(res => res.data),
}

export const turmasAPI = {
  list: () => api.get('/turmas').then(res => res.data),
  get: (id: number) => api.get(`/turmas/${id}`).then(res => res.data),
  create: (data: Record<string, unknown>) => api.post('/turmas', data).then(res => res.data),
  update: (id: number, data: Record<string, unknown>) => api.put(`/turmas/${id}`, data).then(res => res.data),
  delete: (id: number) => api.delete(`/turmas/${id}`).then(res => res.data),
}

export const professoresAPI = {
  list: () => api.get('/professores').then(res => res.data),
  get: (id: number) => api.get(`/professores/${id}`).then(res => res.data),
  create: (data: Record<string, unknown>) => api.post('/professores', data).then(res => res.data),
  update: (id: number, data: Record<string, unknown>) => api.put(`/professores/${id}`, data).then(res => res.data),
  delete: (id: number) => api.delete(`/professores/${id}`).then(res => res.data),
}

export const pagamentosAPI = {
  list: () => api.get('/pagamentos').then(res => res.data),
  get: (id: number) => api.get(`/pagamentos/${id}`).then(res => res.data),
  create: (data: PagamentoCreateData) => api.post('/pagamentos', data).then(res => res.data),
  update: (id: number, data: Partial<PagamentoCreateData>) => api.put(`/pagamentos/${id}`, data).then(res => res.data),
  delete: (id: number) => api.delete(`/pagamentos/${id}`).then(res => res.data),
  getRelatorioMensal: (ano?: number, mes?: number) => {
    const params = new URLSearchParams()
    if (ano) params.append('ano', ano.toString())
    if (mes) params.append('mes', mes.toString())
    return api.get(`/pagamentos/relatorio-mensal?${params.toString()}`).then(res => res.data)
  },
}

export const horariosAPI = {
  list: () => api.get('/horarios').then(res => res.data),
  get: (id: number) => api.get(`/horarios/${id}`).then(res => res.data),
  create: (data: HorarioCreateData) => api.post('/horarios', data).then(res => res.data),
  update: (id: number, data: Partial<HorarioCreateData>) => api.put(`/horarios/${id}`, data).then(res => res.data),
  delete: (id: number) => api.delete(`/horarios/${id}`).then(res => res.data),
}

export const dashboardAPI = {
  getMetrics: () => api.get('/dashboard/metrics').then(res => res.data),
  getRevenueChart: () => api.get('/dashboard/revenue').then(res => res.data),
  getAttendanceChart: () => api.get('/dashboard/attendance').then(res => res.data),
}