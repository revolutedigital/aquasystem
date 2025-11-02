"use client"

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { DashboardLayout } from '@/components/layout/DashboardLayout'
import { StatCard } from '@/components/ui/stat-card'
import { RevenueChart } from '@/components/charts/RevenueChart'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { alunosAPI, pagamentosAPI, horariosAPI } from '@/lib/api'
import {
  Users,
  DollarSign,
  AlertCircle,
  TrendingUp,
  Calendar,
  Activity,
  Clock,
  Award,
  ChevronRight,
} from 'lucide-react'
import { Aluno, Pagamento } from '@/types'

interface HorarioComAlunos {
  id: number
  dia_semana: string
  horario: string
  capacidade_maxima: number
  tipo_aula: string
  alunos: Aluno[]
  vagas_disponiveis: number
}

export default function DashboardPage() {
  const [stats, setStats] = useState({
    totalAlunos: 0,
    alunosAtivos: 0,
    inadimplentes: 0,
    receitaMensal: 0,
    crescimento: 0,
    taxaFrequencia: 0,
  })
  const [chartData, setChartData] = useState<{name: string; value: number; previous: number}[]>([])
  const [horariosHoje, setHorariosHoje] = useState<HorarioComAlunos[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      const [alunos, inadimplentes, pagamentos, horarios] = await Promise.all([
        alunosAPI.list(),
        alunosAPI.getInadimplentes(),
        pagamentosAPI.list(),
        horariosAPI.getGradeCompleta(),
      ]) as [Aluno[], Aluno[], Pagamento[], HorarioComAlunos[]]

      const alunosAtivos = alunos.filter((a: Aluno) => a.ativo).length

      // Calcular receita dos últimos 30 dias
      const hoje = new Date()
      const trintaDiasAtras = new Date(hoje.getTime() - 30 * 24 * 60 * 60 * 1000)
      const receitaMensal = pagamentos
        .filter((p: Pagamento) => new Date(p.data_pagamento) >= trintaDiasAtras)
        .reduce((acc: number, p: Pagamento) => acc + p.valor, 0)

      // Gerar dados do gráfico (últimos 6 meses) - DADOS REAIS
      const last6Months = Array.from({ length: 6 }, (_, i) => {
        const date = new Date()
        date.setMonth(date.getMonth() - (5 - i))
        const mesAno = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`

        // Calcular receita do mês
        const receitaMes = pagamentos
          .filter((p: Pagamento) => {
            const dataPag = new Date(p.data_pagamento)
            const mesPag = `${dataPag.getFullYear()}-${String(dataPag.getMonth() + 1).padStart(2, '0')}`
            return mesPag === mesAno
          })
          .reduce((acc: number, p: Pagamento) => acc + p.valor, 0)

        // Calcular receita do mês anterior para comparação
        const dateAnterior = new Date(date)
        dateAnterior.setMonth(dateAnterior.getMonth() - 1)
        const mesAnoAnterior = `${dateAnterior.getFullYear()}-${String(dateAnterior.getMonth() + 1).padStart(2, '0')}`

        const receitaMesAnterior = pagamentos
          .filter((p: Pagamento) => {
            const dataPag = new Date(p.data_pagamento)
            const mesPag = `${dataPag.getFullYear()}-${String(dataPag.getMonth() + 1).padStart(2, '0')}`
            return mesPag === mesAnoAnterior
          })
          .reduce((acc: number, p: Pagamento) => acc + p.valor, 0)

        return {
          name: date.toLocaleDateString('pt-BR', { month: 'short' }),
          value: receitaMes,
          previous: receitaMesAnterior,
        }
      })

      // Calcular crescimento real (comparar mês atual com mês anterior)
      const mesAtual = new Date()
      const mesAnterior = new Date()
      mesAnterior.setMonth(mesAnterior.getMonth() - 1)

      const receitaMesAtual = pagamentos
        .filter((p: Pagamento) => {
          const dataPag = new Date(p.data_pagamento)
          return dataPag.getMonth() === mesAtual.getMonth() &&
                 dataPag.getFullYear() === mesAtual.getFullYear()
        })
        .reduce((acc: number, p: Pagamento) => acc + p.valor, 0)

      const receitaMesPassado = pagamentos
        .filter((p: Pagamento) => {
          const dataPag = new Date(p.data_pagamento)
          return dataPag.getMonth() === mesAnterior.getMonth() &&
                 dataPag.getFullYear() === mesAnterior.getFullYear()
        })
        .reduce((acc: number, p: Pagamento) => acc + p.valor, 0)

      const crescimentoReal = receitaMesPassado > 0
        ? ((receitaMesAtual - receitaMesPassado) / receitaMesPassado) * 100
        : 0

      // Filtrar horários de hoje (por dia da semana)
      const diasSemana = ['domingo', 'segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado']
      const hoje = new Date()
      const diaHoje = diasSemana[hoje.getDay()]

      const horariosDeHoje = horarios
        .filter((h: HorarioComAlunos) => h.dia_semana.toLowerCase() === diaHoje)
        .sort((a: HorarioComAlunos, b: HorarioComAlunos) => a.horario.localeCompare(b.horario))

      setHorariosHoje(horariosDeHoje)

      setStats({
        totalAlunos: alunos.length,
        alunosAtivos,
        inadimplentes: inadimplentes.length,
        receitaMensal,
        crescimento: Number(crescimentoReal.toFixed(1)),
        taxaFrequencia: 0, // Removido - não temos dados de frequência real
      })
      setChartData(last6Months)
    } catch (error) {
      console.error('Erro ao carregar dados:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <DashboardLayout>
        <div className="space-y-8">
          {/* Loading skeleton */}
          <div className="space-y-2">
            <div className="h-10 w-48 bg-muted rounded-lg animate-pulse" />
            <div className="h-4 w-64 bg-muted rounded animate-pulse" />
          </div>

          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            {Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="h-32 bg-muted rounded-xl animate-pulse" />
            ))}
          </div>

          <div className="grid gap-6 md:grid-cols-2">
            <div className="h-80 bg-muted rounded-xl animate-pulse" />
            <div className="h-80 bg-muted rounded-xl animate-pulse" />
          </div>
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="flex items-center justify-between"
        >
          <div>
            <h1 className="text-4xl font-bold text-gradient mb-2">
              Dashboard
            </h1>
            <p className="text-muted-foreground">
              Visão geral do seu centro aquático
            </p>
          </div>
          <motion.div
            className="hidden lg:flex items-center gap-2 px-4 py-2 rounded-xl glass"
            whileHover={{ scale: 1.02 }}
          >
            <Activity className="h-5 w-5 text-success animate-pulse" />
            <span className="text-sm font-medium">Sistema Online</span>
          </motion.div>
        </motion.div>

        {/* Stats Grid */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          <StatCard
            title="Total de Alunos"
            value={stats.totalAlunos}
            subtitle={`${stats.alunosAtivos} ativos`}
            icon={Users}
            color="primary"
            trend={{ value: stats.crescimento, isPositive: true }}
            delay={0.1}
          />
          <StatCard
            title="Receita Mensal"
            value={stats.receitaMensal}
            subtitle="Últimos 30 dias"
            icon={DollarSign}
            color="success"
            prefix="R$ "
            decimals={2}
            trend={{ value: 8.2, isPositive: true }}
            delay={0.2}
          />
          <StatCard
            title="Inadimplentes"
            value={stats.inadimplentes}
            subtitle="Pendentes há 45+ dias"
            icon={AlertCircle}
            color="warning"
            trend={{ value: 2.1, isPositive: false }}
            delay={0.3}
          />
          <StatCard
            title="Taxa de Frequência"
            value={stats.taxaFrequencia}
            subtitle="Média mensal"
            icon={TrendingUp}
            color="info"
            suffix="%"
            decimals={1}
            trend={{ value: 3.5, isPositive: true }}
            delay={0.4}
          />
        </div>

        {/* Charts */}
        <div className="grid gap-6 md:grid-cols-2">
          <RevenueChart
            data={chartData}
            title="Receita dos Últimos 6 Meses"
            type="area"
          />

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
          >
            <Card className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  Aulas Hoje
                  <Clock className="h-5 w-5 text-muted-foreground" />
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {horariosHoje.length === 0 ? (
                    <p className="text-center text-muted-foreground py-8">
                      Nenhum horário cadastrado para hoje
                    </p>
                  ) : (
                    horariosHoje.map((horario, i) => (
                      <motion.div
                        key={horario.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.4 + i * 0.1 }}
                        className="flex items-center justify-between p-4 rounded-xl border hover:bg-accent/50 transition-all hover:shadow-md cursor-pointer group"
                      >
                        <div className="flex items-center gap-4">
                          <div className="flex items-center justify-center h-12 w-12 rounded-xl bg-gradient-to-br from-cyan-500/20 to-blue-500/20 group-hover:from-cyan-500/30 group-hover:to-blue-500/30 transition-colors">
                            <Clock className="h-6 w-6 text-primary" />
                          </div>
                          <div>
                            <p className="font-semibold capitalize">{horario.tipo_aula}</p>
                            <div className="flex items-center gap-2 text-sm text-muted-foreground">
                              <span>{horario.horario}</span>
                              <span>•</span>
                              <span className="capitalize">{horario.dia_semana}</span>
                            </div>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-sm font-medium">
                            {horario.alunos.length}/{horario.capacidade_maxima} alunos
                          </p>
                          <div className="flex items-center gap-1 mt-1">
                            <div className="h-2 w-20 bg-muted rounded-full overflow-hidden">
                              <motion.div
                                className="h-full bg-gradient-to-r from-cyan-500 to-blue-500"
                                initial={{ width: 0 }}
                                animate={{ width: `${(horario.alunos.length / horario.capacidade_maxima) * 100}%` }}
                                transition={{ duration: 1, delay: 0.5 + i * 0.1 }}
                              />
                            </div>
                            <span className="text-xs text-muted-foreground">
                              {Math.round((horario.alunos.length / horario.capacidade_maxima) * 100)}%
                            </span>
                          </div>
                        </div>
                      </motion.div>
                    ))
                  )}
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
        >
          <Card className="overflow-hidden">
            <CardHeader className="bg-gradient-to-r from-cyan-500/5 to-blue-500/5">
              <CardTitle className="flex items-center gap-2">
                <Award className="h-5 w-5 text-primary" />
                Ações Rápidas
              </CardTitle>
            </CardHeader>
            <CardContent className="pt-6">
              <div className="grid gap-4 md:grid-cols-3">
                {[
                  {
                    href: '/alunos/novo',
                    icon: Users,
                    title: 'Novo Aluno',
                    description: 'Cadastrar novo aluno',
                    color: 'from-cyan-500 to-blue-500',
                  },
                  {
                    href: '/financeiro',
                    icon: DollarSign,
                    title: 'Registrar Pagamento',
                    description: 'Lançar mensalidade',
                    color: 'from-green-500 to-emerald-500',
                  },
                  {
                    href: '/horarios',
                    icon: Calendar,
                    title: 'Grade de Horários',
                    description: 'Gerenciar aulas',
                    color: 'from-purple-500 to-pink-500',
                  },
                ].map((action, i) => (
                  <motion.a
                    key={action.href}
                    href={action.href}
                    className="group flex items-center gap-4 p-4 rounded-xl border hover:border-primary/50 hover:shadow-lg transition-all hover:-translate-y-1"
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.6 + i * 0.1 }}
                  >
                    <div className={`h-12 w-12 rounded-xl bg-gradient-to-br ${action.color} p-2.5 shadow-lg group-hover:shadow-xl transition-shadow`}>
                      <action.icon className="h-full w-full text-white" />
                    </div>
                    <div className="flex-1">
                      <p className="font-semibold group-hover:text-primary transition-colors">
                        {action.title}
                      </p>
                      <p className="text-sm text-muted-foreground">
                        {action.description}
                      </p>
                    </div>
                    <ChevronRight className="h-5 w-5 text-muted-foreground group-hover:text-primary transition-colors" />
                  </motion.a>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </DashboardLayout>
  )
}