import api from './api'

export interface Usuario {
  id: number
  nome: string
  email: string
  telefone?: string
  role: string
  ativo: boolean
  created_at: string
  last_login?: string
}

export interface UsuarioCreate {
  nome: string
  email: string
  password: string
  telefone?: string
  role: string
  ativo: boolean
}

export interface UsuarioUpdate {
  nome?: string
  email?: string
  telefone?: string
  role?: string
  ativo?: boolean
}

export const usersAPI = {
  list: () => api.get('/api/users').then(res => res.data),
  get: (id: number) => api.get(`/api/users/${id}`).then(res => res.data),
  create: (data: UsuarioCreate) => api.post('/api/users', data).then(res => res.data),
  update: (id: number, data: UsuarioUpdate) => api.put(`/api/users/${id}`, data).then(res => res.data),
  delete: (id: number) => api.delete(`/api/users/${id}`).then(res => res.data),
  changePassword: (id: number, newPassword: string) =>
    api.put(`/api/users/${id}/password`, { new_password: newPassword }).then(res => res.data)
}