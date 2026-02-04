"use client"

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { motion } from 'framer-motion'
import * as z from 'zod'
import { Loader2, Mail, Lock, Eye, EyeOff, Waves } from 'lucide-react'
import { useAuthStore } from '@/store/authStore'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Logo } from '@/components/brand/Logo'

const loginSchema = z.object({
  email: z.string().email('Email inválido'),
  password: z.string().min(1, 'Senha é obrigatória'),
})

type LoginFormValues = z.infer<typeof loginSchema>

export default function LoginPage() {
  const [isLoading, setIsLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const router = useRouter()
  const login = useAuthStore((state) => state.login)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: 'admin@natacao.com',
      password: 'admin123',
    },
  })

  const onSubmit = async (data: LoginFormValues) => {
    setIsLoading(true)
    const success = await login(data.email, data.password)

    if (success) {
      router.push('/')
    }

    setIsLoading(false)
  }

  return (
    <div className="min-h-screen relative flex items-center justify-center overflow-hidden">
      {/* Animated background */}
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-400 via-blue-500 to-blue-600">

        {/* Animated waves */}
        <motion.div
          className="absolute bottom-0 left-0 right-0"
          initial={{ y: 100 }}
          animate={{ y: 0 }}
          transition={{ duration: 1 }}
        >
          <svg viewBox="0 0 1440 320" className="w-full">
            <path
              fill="rgba(255,255,255,0.1)"
              d="M0,192L48,181.3C96,171,192,149,288,154.7C384,160,480,192,576,192C672,192,768,160,864,149.3C960,139,1056,149,1152,176C1248,203,1344,245,1392,266.7L1440,288L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
              className="animate-wave-slow"
            />
            <path
              fill="rgba(255,255,255,0.05)"
              d="M0,256L48,240C96,224,192,192,288,181.3C384,171,480,181,576,197.3C672,213,768,235,864,229.3C960,224,1056,192,1152,181.3C1248,171,1344,181,1392,186.7L1440,192L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
              className="animate-wave-slow-reverse"
            />
          </svg>
        </motion.div>
      </div>

      {/* Login Card */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="relative z-10 w-full max-w-md px-4"
      >
        <div className="glass rounded-2xl shadow-strong p-8">
          {/* Logo */}
          <motion.div
            initial={{ y: -20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="flex justify-center mb-8"
          >
            <Logo size="lg" variant="full" animated />
          </motion.div>

          {/* Welcome text */}
          <motion.div
            initial={{ y: -10, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="text-center mb-8"
          >
            <h2 className="text-2xl font-bold mb-2">Bem-vindo de volta!</h2>
            <p className="text-muted-foreground">
              Faça login para acessar o sistema
            </p>
          </motion.div>

          {/* Form */}
          <motion.form
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4 }}
            onSubmit={handleSubmit(onSubmit)}
            className="space-y-6"
          >
            {/* Email field */}
            <div className="space-y-2">
              <label htmlFor="email" className="text-sm font-medium flex items-center gap-2">
                <Mail className="h-4 w-4" />
                Email
              </label>
              <div className="relative">
                <Input
                  id="email"
                  type="email"
                  placeholder="seu.email@exemplo.com"
                  className="pl-10 h-12"
                  disabled={isLoading}
                  autoComplete="email"
                  {...register('email')}
                />
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
              </div>
              {errors.email && (
                <motion.p
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="text-sm text-error"
                >
                  {errors.email.message}
                </motion.p>
              )}
            </div>

            {/* Password field */}
            <div className="space-y-2">
              <label htmlFor="password" className="text-sm font-medium flex items-center gap-2">
                <Lock className="h-4 w-4" />
                Senha
              </label>
              <div className="relative">
                <Input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  placeholder="••••••••"
                  className="pl-10 pr-10 h-12"
                  disabled={isLoading}
                  autoComplete="current-password"
                  {...register('password')}
                />
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                >
                  {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                </button>
              </div>
              {errors.password && (
                <motion.p
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="text-sm text-error"
                >
                  {errors.password.message}
                </motion.p>
              )}
            </div>

            {/* Test credentials */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
              className="bg-info/10 border border-info/20 rounded-lg p-3 space-y-1"
            >
              <p className="text-xs font-medium text-info">Credenciais de teste:</p>
              <p className="text-xs text-info/80">Email: admin@natacao.com</p>
              <p className="text-xs text-info/80">Senha: admin123</p>
            </motion.div>

            {/* Submit button */}
            <Button
              type="submit"
              className="w-full h-12 text-base font-semibold bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600 shadow-lg"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                  Entrando...
                </>
              ) : (
                <>
                  Entrar no Sistema
                  <Waves className="ml-2 h-5 w-5" />
                </>
              )}
            </Button>
          </motion.form>

          {/* Footer */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6 }}
            className="mt-8 text-center"
          >
            <p className="text-xs text-muted-foreground">
              © 2024 AquaFlow Pro. Todos os direitos reservados.
            </p>
          </motion.div>
        </div>
      </motion.div>
    </div>
  )
}