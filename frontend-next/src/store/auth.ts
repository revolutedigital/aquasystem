import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { authAPI } from '@/lib/api'
import toast from 'react-hot-toast'

interface User {
  id: number
  nome: string
  email: string
  tipo: string
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<boolean>
  logout: () => void
  setUser: (user: User) => void
  setToken: (token: string) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,

      login: async (email: string, password: string) => {
        set({ isLoading: true })
        try {
          const response = await authAPI.login(email, password)
          const { access_token, user } = response.data

          set({
            token: access_token,
            user: user,
            isAuthenticated: true,
            isLoading: false
          })

          toast.success('Login realizado com sucesso!')
          return true
        } catch (error: any) {
          set({ isLoading: false })
          toast.error(error.response?.data?.detail || 'Erro ao fazer login')
          return false
        }
      },

      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false
        })
        toast.success('Logout realizado com sucesso!')
      },

      setUser: (user: User) => set({ user }),
      setToken: (token: string) => set({ token })
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated
      })
    }
  )
)