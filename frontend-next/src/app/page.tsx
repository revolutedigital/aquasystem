"use client"

import { useEffect, useState } from 'react'
import { DashboardLayout } from '@/components/layout/DashboardLayout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { alunosAPI, pagamentosAPI } from '@/lib/api'
import { formatCurrency } from '@/lib/utils'
import { Users, DollarSign, AlertCircle, TrendingUp } from 'lucide-react'
import { Aluno } from '@/types'

export default function DashboardPage() {
  const [stats, setStats] = useState({
    totalAlunos: 0,
    alunosAtivos: 0,
    inadimplentes: 0,
    receitaMensal: 0,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      const [alunos, inadimplentes, pagamentos] = await Promise.all([
        alunosAPI.list(),
        alunosAPI.getInadimplentes(),
        pagamentosAPI.list(),
      ])

      const alunosAtivos = alunos.filter((a: Aluno) => a.ativo).length

      // Calcular receita dos últimos 30 dias
      const hoje = new Date()
      const trintaDiasAtras = new Date(hoje.getTime() - 30 * 24 * 60 * 60 * 1000)
      const receitaMensal = pagamentos
        .filter((p: any) => new Date(p.data_pagamento) >= trintaDiasAtras)
        .reduce((acc: number, p: any) => acc + p.valor, 0)

      setStats({
        totalAlunos: alunos.length,
        alunosAtivos,
        inadimplentes: inadimplentes.length,
        receitaMensal,
      })
    } catch (error) {
      console.error('Erro ao carregar dados:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-swimming-blue"></div>
            <p className="mt-2 text-gray-600">Carregando dados...</p>
          </div>
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600">Visão geral do sistema de natação</p>
        </div>

        {/* Stats Cards */}
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Total de Alunos
              </CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.totalAlunos}</div>
              <p className="text-xs text-muted-foreground">
                {stats.alunosAtivos} ativos
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Receita Mensal
              </CardTitle>
              <DollarSign className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {formatCurrency(stats.receitaMensal)}
              </div>
              <p className="text-xs text-muted-foreground">
                Últimos 30 dias
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Inadimplentes
              </CardTitle>
              <AlertCircle className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.inadimplentes}</div>
              <p className="text-xs text-muted-foreground">
                Sem pagamento há 45+ dias
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Taxa de Adimplência
              </CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {stats.alunosAtivos > 0
                  ? Math.round(((stats.alunosAtivos - stats.inadimplentes) / stats.alunosAtivos) * 100)
                  : 0}%
              </div>
              <p className="text-xs text-muted-foreground">
                Alunos em dia
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <CardTitle>Ações Rápidas</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-3">
              <a
                href="/alunos/novo"
                className="flex items-center p-4 border rounded-lg hover:bg-gray-50 transition-colors"
              >
                <Users className="h-8 w-8 text-swimming-blue mr-3" />
                <div>
                  <p className="font-medium">Novo Aluno</p>
                  <p className="text-sm text-gray-600">Cadastrar novo aluno</p>
                </div>
              </a>

              <a
                href="/financeiro"
                className="flex items-center p-4 border rounded-lg hover:bg-gray-50 transition-colors"
              >
                <DollarSign className="h-8 w-8 text-swimming-green mr-3" />
                <div>
                  <p className="font-medium">Registrar Pagamento</p>
                  <p className="text-sm text-gray-600">Lançar mensalidade</p>
                </div>
              </a>

              <a
                href="/horarios"
                className="flex items-center p-4 border rounded-lg hover:bg-gray-50 transition-colors"
              >
                <Calendar className="h-8 w-8 text-swimming-blue mr-3" />
                <div>
                  <p className="font-medium">Grade de Horários</p>
                  <p className="text-sm text-gray-600">Gerenciar aulas</p>
                </div>
              </a>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  )
}