import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { User } from '@/types'
import { authAPI } from '@/lib/api'
import toast from 'react-hot-toast'

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
            user: user,
            token: access_token,
            isAuthenticated: true,
            isLoading: false,
          })

          toast.success('Login realizado com sucesso!')
          return true
        } catch (error) {
          set({ isLoading: false })
          const message = error instanceof Error
            ? error.message
            : (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Erro ao fazer login'
          toast.error(message)
          return false
        }
      },

      logout: () => {
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        })
        toast.success('Logout realizado com sucesso!')
      },

      checkAuth: () => {
        // Zustand persist will automatically restore state
        set({ isLoading: false })
      },

      setUser: (user: User | null) => {
        set({ user })
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)