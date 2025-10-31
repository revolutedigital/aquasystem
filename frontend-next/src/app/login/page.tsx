"use client"

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import { Loader2 } from 'lucide-react'
import { useAuthStore } from '@/store/authStore'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'

const loginSchema = z.object({
  email: z.string().email('Email inválido'),
  password: z.string().min(1, 'Senha é obrigatória'),
})

type LoginFormValues = z.infer<typeof loginSchema>

export default function LoginPage() {
  const [isLoading, setIsLoading] = useState(false)
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
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-swimming-blue/10 to-swimming-green/10">
      <div className="absolute inset-0 bg-grid-slate-100 [mask-image:radial-gradient(ellipse_at_center,transparent_20%,black)]"></div>

      <Card className="w-full max-w-md relative">
        <CardHeader className="space-y-1">
          <div className="flex justify-center mb-4">
            <div className="w-20 h-20 bg-swimming-blue/10 rounded-full flex items-center justify-center">
              <span className="text-4xl">🏊‍♂️</span>
            </div>
          </div>
          <CardTitle className="text-2xl font-bold text-center">
            Sistema de Natação
          </CardTitle>
          <CardDescription className="text-center">
            Faça login para acessar o sistema de gestão
          </CardDescription>
        </CardHeader>

        <form onSubmit={handleSubmit(onSubmit)}>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <label htmlFor="email" className="text-sm font-medium">
                Email
              </label>
              <Input
                id="email"
                type="email"
                placeholder="seu.email@exemplo.com"
                disabled={isLoading}
                {...register('email')}
              />
              {errors.email && (
                <p className="text-sm text-red-500">{errors.email.message}</p>
              )}
            </div>

            <div className="space-y-2">
              <label htmlFor="password" className="text-sm font-medium">
                Senha
              </label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                disabled={isLoading}
                {...register('password')}
              />
              {errors.password && (
                <p className="text-sm text-red-500">{errors.password.message}</p>
              )}
            </div>

            <div className="bg-blue-50 border border-blue-200 rounded-md p-3 space-y-1">
              <p className="text-xs font-medium text-blue-900">Credenciais de teste:</p>
              <p className="text-xs text-blue-700">Email: admin@natacao.com</p>
              <p className="text-xs text-blue-700">Senha: admin123</p>
            </div>
          </CardContent>

          <CardFooter>
            <Button
              type="submit"
              className="w-full"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Entrando...
                </>
              ) : (
                'Entrar'
              )}
            </Button>
          </CardFooter>
        </form>
      </Card>
    </div>
  )
}