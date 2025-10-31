import { create } from 'zustand'
import { User } from '@/types'
import { authAPI } from '@/lib/api'
import { toast } from 'react-hot-toast'

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean

  // Actions
  login: (email: string, password: string) => Promise<boolean>
  logout: () => void
  checkAuth: () => void
  setUser: (user: User | null) => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: true,

  login: async (email: string, password: string) => {
    try {
      const response = await authAPI.login(email, password)

      // Salvar token e user no localStorage
      localStorage.setItem('access_token', response.access_token)
      localStorage.setItem('user', JSON.stringify(response.user))

      // Atualizar store
      set({
        user: response.user,
        token: response.access_token,
        isAuthenticated: true,
      })

      toast.success('Login realizado com sucesso!')
      return true
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Erro ao fazer login'
      toast.error(message)
      return false
    }
  },

  logout: () => {
    authAPI.logout()
    set({
      user: null,
      token: null,
      isAuthenticated: false,
    })
    toast.success('Logout realizado com sucesso!')
  },

  checkAuth: () => {
    const token = localStorage.getItem('access_token')
    const userStr = localStorage.getItem('user')

    if (token && userStr) {
      try {
        const user = JSON.parse(userStr)
        set({
          user,
          token,
          isAuthenticated: true,
          isLoading: false,
        })
      } catch {
        set({ isLoading: false })
      }
    } else {
      set({ isLoading: false })
    }
  },

  setUser: (user: User | null) => {
    set({ user })
  },
}))