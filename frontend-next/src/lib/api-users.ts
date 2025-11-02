import api from './api'

export interface Usuario {
  id: number
  email: string
  username: string
  full_name: string
  role: string
  is_active: boolean
  is_superuser: boolean
  created_at: string
  updated_at?: string
  last_login?: string
}

export interface UsuarioCreate {
  email: string
  username: string
  full_name: string
  password: string
  role: string
}

export interface UsuarioUpdate {
  email?: string
  username?: string
  full_name?: string
  role?: string
  is_active?: boolean
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