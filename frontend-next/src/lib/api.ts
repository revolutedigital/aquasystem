import axios from 'axios'
import { useAuthStore } from '@/store/auth'
import type {
  AlunoCreateData,
  AlunoUpdateData,
  PagamentoCreateData,
  HorarioCreateData
} from '@/types'

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
    api.post('/api/auth/login', { email, password }),
}

export const alunosAPI = {
  list: (includeInactive = false) => {
    // Backend já filtra apenas ativos por padrão
    const params = includeInactive ? { ativo: false } : {}
    return api.get('/api/alunos', { params }).then(res => res.data)
  },
  get: (id: number) => api.get(`/api/alunos/${id}`).then(res => res.data),
  create: (data: AlunoCreateData) => api.post('/api/alunos', data).then(res => res.data),
  update: (id: number, data: AlunoUpdateData) => api.put(`/api/alunos/${id}`, data).then(res => res.data),
  delete: (id: number) => api.delete(`/api/alunos/${id}`).then(res => res.data),
  getInadimplentes: () => api.get('/api/alunos/inadimplentes').then(res => res.data),
  getPagamentos: (id: number) => api.get(`/api/alunos/${id}/pagamentos`).then(res => res.data),
}

export const turmasAPI = {
  list: () => api.get('/api/turmas').then(res => res.data),
  get: (id: number) => api.get(`/api/turmas/${id}`).then(res => res.data),
  create: (data: Record<string, unknown>) => api.post('/api/turmas', data).then(res => res.data),
  update: (id: number, data: Record<string, unknown>) => api.put(`/api/turmas/${id}`, data).then(res => res.data),
  delete: (id: number) => api.delete(`/api/turmas/${id}`).then(res => res.data),
}

export const professoresAPI = {
  list: () => api.get('/api/professores').then(res => res.data),
  get: (id: number) => api.get(`/api/professores/${id}`).then(res => res.data),
  create: (data: Record<string, unknown>) => api.post('/api/professores', data).then(res => res.data),
  update: (id: number, data: Record<string, unknown>) => api.put(`/api/professores/${id}`, data).then(res => res.data),
  delete: (id: number) => api.delete(`/api/professores/${id}`).then(res => res.data),
}

export const pagamentosAPI = {
  list: () => api.get('/api/pagamentos').then(res => res.data),
  get: (id: number) => api.get(`/api/pagamentos/${id}`).then(res => res.data),
  create: (data: PagamentoCreateData) => api.post('/api/pagamentos', data).then(res => res.data),
  update: (id: number, data: Partial<PagamentoCreateData>) => api.put(`/api/pagamentos/${id}`, data).then(res => res.data),
  delete: (id: number) => api.delete(`/api/pagamentos/${id}`).then(res => res.data),
  getRelatorioMensal: (ano?: number, mes?: number) => {
    const params = new URLSearchParams()
    if (ano) params.append('ano', ano.toString())
    if (mes) params.append('mes', mes.toString())
    return api.get(`/api/pagamentos/relatorio-mensal?${params.toString()}`).then(res => res.data)
  },
}

export const horariosAPI = {
  list: () => api.get('/api/horarios').then(res => res.data),
  get: (id: number) => api.get(`/api/horarios/${id}`).then(res => res.data),
  create: (data: HorarioCreateData) => api.post('/api/horarios', data).then(res => res.data),
  update: (id: number, data: Partial<HorarioCreateData>) => api.put(`/api/horarios/${id}`, data).then(res => res.data),
  delete: (id: number) => api.delete(`/api/horarios/${id}`).then(res => res.data),
}

export const planosAPI = {
  list: (includeInactive = false) => {
    const params = includeInactive ? { ativo: false } : {}
    return api.get('/api/planos', { params }).then(res => res.data)
  },
  get: (id: number) => api.get(`/api/planos/${id}`).then(res => res.data),
  create: (data: Record<string, unknown>) => api.post('/api/planos', data).then(res => res.data),
  update: (id: number, data: Record<string, unknown>) => api.put(`/api/planos/${id}`, data).then(res => res.data),
  delete: (id: number) => api.delete(`/api/planos/${id}`).then(res => res.data),
}

export const dashboardAPI = {
  getMetrics: () => api.get('/api/dashboard/metrics').then(res => res.data),
  getRevenueChart: () => api.get('/api/dashboard/revenue').then(res => res.data),
  getAttendanceChart: () => api.get('/api/dashboard/attendance').then(res => res.data),
}