"use client"

import { useEffect, useState, useCallback, Suspense } from 'react'
import Link from 'next/link'
import { useSearchParams } from 'next/navigation'
import { motion } from 'framer-motion'
import {
  DollarSign,
  Plus,
  TrendingUp,
  TrendingDown,
  CreditCard,
  AlertCircle,
  Calendar,
  Download,
  Search,
  Receipt,
  Trash2,
  X,
  ArrowLeft
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs'
import { toast } from 'sonner'
import { pagamentosAPI, alunosAPI } from '@/lib/api'
import { RevenueChart } from '@/components/charts/RevenueChart'
import type { Aluno } from '@/types'

interface PagamentoComStatus {
  id: number
  aluno_id: number
  aluno_nome?: string
  valor: number
  data_pagamento: string | null
  mes_referencia: number
  ano_referencia: number
  forma_pagamento: string
  status: 'confirmado' | 'pendente' | 'cancelado'
  observacoes?: string
}

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value)
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('pt-BR')
}

function FinanceiroPageContent() {
  const searchParams = useSearchParams()
  const [pagamentos, setPagamentos] = useState<PagamentoComStatus[]>([])
  const [alunos, setAlunos] = useState<Aluno[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterStatus, setFilterStatus] = useState('all')
  const [filterMonth, setFilterMonth] = useState(new Date().getMonth() + 1)
  const [filterYear, setFilterYear] = useState(new Date().getFullYear())
  const [isAddModalOpen, setIsAddModalOpen] = useState(false)
  const [selectedPagamento, setSelectedPagamento] = useState<PagamentoComStatus | null>(null)

  // Form state
  const [formData, setFormData] = useState({
    aluno_id: '',
    valor: '',
    data_pagamento: new Date().toISOString().split('T')[0],
    mes_referencia: new Date().getMonth() + 1,
    ano_referencia: new Date().getFullYear(),
    forma_pagamento: 'pix',
    status: 'confirmado',
    observacoes: ''
  })

  // Stats
  const [stats, setStats] = useState({
    receitaTotal: 0,
    receitaMes: 0,
    pendente: 0,
    inadimplentes: 0
  })

  const loadData = useCallback(async () => {
    try {
      setLoading(true)
      const [pagamentosData, alunosData] = await Promise.all([
        pagamentosAPI.list(),
        alunosAPI.list()
      ])

      // Não usar dados mockados - usar lista vazia se falhar
      setPagamentos(pagamentosData || [])
      setAlunos(alunosData || [])

      // Calcular stats
      const pagamentosList = pagamentosData || []
      const total = pagamentosList
        .filter((p: PagamentoComStatus) => p.status === 'confirmado')
        .reduce((acc: number, p: PagamentoComStatus) => acc + p.valor, 0)

      const mesAtual = pagamentosList
        .filter((p: PagamentoComStatus) =>
          p.status === 'confirmado' &&
          p.mes_referencia === filterMonth &&
          p.ano_referencia === filterYear
        )
        .reduce((acc: number, p: PagamentoComStatus) => acc + p.valor, 0)

      const pendente = pagamentosList
        .filter((p: PagamentoComStatus) => p.status === 'pendente')
        .reduce((acc: number, p: PagamentoComStatus) => acc + p.valor, 0)

      setStats({
        receitaTotal: total,
        receitaMes: mesAtual,
        pendente: pendente,
        inadimplentes: alunosData.filter((a: Aluno) => !a.ativo).length
      })
    } catch (error) {
      console.error('Erro ao carregar dados:', error)
    } finally {
      setLoading(false)
    }
  }, [filterMonth, filterYear])

  useEffect(() => {
    loadData()
  }, [loadData])

  // Check for action parameter from quick actions
  useEffect(() => {
    if (searchParams.get('action') === 'new') {
      setIsAddModalOpen(true)
      // Clear the parameter after opening
      window.history.replaceState({}, '', '/financeiro')
    }
  }, [searchParams])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const pagamentoData = {
        aluno_id: parseInt(formData.aluno_id),
        valor: parseFloat(formData.valor),
        data_pagamento: formData.data_pagamento,
        mes_referencia: formData.mes_referencia,
        ano_referencia: formData.ano_referencia,
        forma_pagamento: formData.forma_pagamento as 'pix' | 'dinheiro' | 'cartao_credito' | 'cartao_debito',
        observacao: formData.observacoes
      }

      if (selectedPagamento) {
        await pagamentosAPI.update(selectedPagamento.id, pagamentoData)
        toast.success('Pagamento atualizado com sucesso!')
      } else {
        await pagamentosAPI.create(pagamentoData)
        toast.success('Pagamento registrado com sucesso!')
      }
      loadData()
      setIsAddModalOpen(false)
      resetForm()
    } catch (error) {
      console.error('Erro ao salvar pagamento:', error)
      toast.error('Erro ao salvar pagamento')
    }
  }

  const handleDelete = async (id: number) => {
    if (confirm('Tem certeza que deseja excluir este pagamento?')) {
      try {
        await pagamentosAPI.delete(id)
        toast.success('Pagamento excluído com sucesso!')
        loadData()
      } catch (error) {
        console.error('Erro ao excluir pagamento:', error)
        toast.error('Erro ao excluir pagamento')
      }
    }
  }


  const resetForm = () => {
    setFormData({
      aluno_id: '',
      valor: '',
      data_pagamento: new Date().toISOString().split('T')[0],
      mes_referencia: new Date().getMonth() + 1,
      ano_referencia: new Date().getFullYear(),
      forma_pagamento: 'pix',
      status: 'confirmado',
      observacoes: ''
    })
    setSelectedPagamento(null)
  }

  const filteredPagamentos = pagamentos.filter(pagamento => {
    const matchesSearch = pagamento.aluno_nome?.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = filterStatus === 'all' || pagamento.status === filterStatus
    const matchesMonth = pagamento.mes_referencia === filterMonth
    const matchesYear = pagamento.ano_referencia === filterYear
    return matchesSearch && matchesStatus && matchesMonth && matchesYear
  })

  const getStatusBadge = (status: string) => {
    switch(status) {
      case 'confirmado':
        return <Badge className="bg-green-500">Confirmado</Badge>
      case 'pendente':
        return <Badge className="bg-yellow-500">Pendente</Badge>
      case 'cancelado':
        return <Badge className="bg-red-500">Cancelado</Badge>
      default:
        return <Badge>{status}</Badge>
    }
  }

  const getFormaPagamento = (forma: string) => {
    const formas: Record<string, string> = {
      'pix': 'PIX',
      'cartao_credito': 'Cartão Crédito',
      'cartao_debito': 'Cartão Débito',
      'dinheiro': 'Dinheiro',
      'transferencia': 'Transferência'
    }
    return formas[forma] || forma
  }

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4"
      >
        <div className="flex items-start gap-4">
          <Link href="/">
            <Button variant="outline" size="icon" className="shadow-sm">
              <ArrowLeft className="h-4 w-4" />
            </Button>
          </Link>
          <div>
            <h1 className="text-3xl font-bold flex items-center gap-3">
              <div className="p-2 bg-primary/10 rounded-lg">
                <DollarSign className="h-6 w-6 text-primary" />
              </div>
              Financeiro
            </h1>
            <p className="text-muted-foreground mt-1">
              Gerencie pagamentos e receitas
            </p>
          </div>
        </div>

        <Dialog open={isAddModalOpen} onOpenChange={setIsAddModalOpen}>
          <DialogTrigger asChild>
            <Button
              size="lg"
              className="shadow-lg hover:shadow-xl transition-all"
              onClick={() => {
                resetForm()
                setIsAddModalOpen(true)
              }}
            >
              <Plus className="h-5 w-5 mr-2" />
              Novo Pagamento
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[600px]">
            <DialogHeader>
              <DialogTitle>
                {selectedPagamento ? 'Editar Pagamento' : 'Registrar Pagamento'}
              </DialogTitle>
              <DialogDescription>
                Preencha os dados do pagamento abaixo
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="col-span-2 space-y-2">
                  <Label htmlFor="aluno_id">Aluno*</Label>
                  <Select
                    value={formData.aluno_id}
                    onValueChange={(value) => setFormData({...formData, aluno_id: value})}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Selecione o aluno" />
                    </SelectTrigger>
                    <SelectContent>
                      {alunos.map(aluno => (
                        <SelectItem key={aluno.id} value={aluno.id.toString()}>
                          {aluno.nome_completo}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="valor">Valor*</Label>
                  <Input
                    id="valor"
                    type="number"
                    step="0.01"
                    value={formData.valor}
                    onChange={(e) => setFormData({...formData, valor: e.target.value})}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="forma_pagamento">Forma de Pagamento*</Label>
                  <Select
                    value={formData.forma_pagamento}
                    onValueChange={(value) => setFormData({...formData, forma_pagamento: value})}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Selecione a forma" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="pix">PIX</SelectItem>
                      <SelectItem value="cartao_credito">Cartão Crédito</SelectItem>
                      <SelectItem value="cartao_debito">Cartão Débito</SelectItem>
                      <SelectItem value="dinheiro">Dinheiro</SelectItem>
                      <SelectItem value="transferencia">Transferência</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="data_pagamento">Data Pagamento*</Label>
                  <Input
                    id="data_pagamento"
                    type="date"
                    value={formData.data_pagamento}
                    onChange={(e) => setFormData({...formData, data_pagamento: e.target.value})}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="mes_referencia">Mês Referência*</Label>
                  <Select
                    value={formData.mes_referencia.toString()}
                    onValueChange={(value) => setFormData({...formData, mes_referencia: parseInt(value)})}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Selecione o mês" />
                    </SelectTrigger>
                    <SelectContent>
                      {[...Array(12)].map((_, i) => (
                        <SelectItem key={i} value={(i + 1).toString()}>
                          {new Date(2000, i).toLocaleDateString('pt-BR', { month: 'long' })}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="ano_referencia">Ano Referência*</Label>
                  <Input
                    id="ano_referencia"
                    type="number"
                    value={formData.ano_referencia}
                    onChange={(e) => setFormData({...formData, ano_referencia: parseInt(e.target.value)})}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="status">Status*</Label>
                  <Select
                    value={formData.status}
                    onValueChange={(value) => setFormData({...formData, status: value})}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Selecione o status" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="confirmado">Confirmado</SelectItem>
                      <SelectItem value="pendente">Pendente</SelectItem>
                      <SelectItem value="cancelado">Cancelado</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="col-span-2 space-y-2">
                  <Label htmlFor="observacoes">Observações</Label>
                  <Input
                    id="observacoes"
                    value={formData.observacoes}
                    onChange={(e) => setFormData({...formData, observacoes: e.target.value})}
                  />
                </div>
              </div>
              <div className="flex justify-end gap-3">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setIsAddModalOpen(false)}
                >
                  Cancelar
                </Button>
                <Button type="submit">
                  {selectedPagamento ? 'Salvar Alterações' : 'Registrar'}
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </motion.div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
        >
          <Card className="p-6 glass border-0 shadow-medium">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Receita Total</p>
                <p className="text-2xl font-bold">{formatCurrency(stats.receitaTotal)}</p>
                <div className="flex items-center gap-1 mt-2 text-green-500">
                  <TrendingUp className="h-4 w-4" />
                  <span className="text-sm">+12.5%</span>
                </div>
              </div>
              <DollarSign className="h-8 w-8 text-green-500 opacity-50" />
            </div>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <Card className="p-6 glass border-0 shadow-medium">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Receita do Mês</p>
                <p className="text-2xl font-bold">{formatCurrency(stats.receitaMes)}</p>
                <div className="flex items-center gap-1 mt-2 text-blue-500">
                  <Calendar className="h-4 w-4" />
                  <span className="text-sm">
                    {new Date(filterYear, filterMonth - 1).toLocaleDateString('pt-BR', { month: 'short' })}
                  </span>
                </div>
              </div>
              <CreditCard className="h-8 w-8 text-blue-500 opacity-50" />
            </div>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <Card className="p-6 glass border-0 shadow-medium">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Pendente</p>
                <p className="text-2xl font-bold">{formatCurrency(stats.pendente)}</p>
                <div className="flex items-center gap-1 mt-2 text-yellow-500">
                  <AlertCircle className="h-4 w-4" />
                  <span className="text-sm">Aguardando</span>
                </div>
              </div>
              <Receipt className="h-8 w-8 text-yellow-500 opacity-50" />
            </div>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <Card className="p-6 glass border-0 shadow-medium">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Inadimplentes</p>
                <p className="text-2xl font-bold">{stats.inadimplentes}</p>
                <div className="flex items-center gap-1 mt-2 text-red-500">
                  <TrendingDown className="h-4 w-4" />
                  <span className="text-sm">Alunos</span>
                </div>
              </div>
              <X className="h-8 w-8 text-red-500 opacity-50" />
            </div>
          </Card>
        </motion.div>
      </div>

      {/* Tabs */}
      <Tabs defaultValue="pagamentos" className="space-y-4">
        <TabsList className="grid w-full max-w-md grid-cols-2">
          <TabsTrigger value="pagamentos">Pagamentos</TabsTrigger>
          <TabsTrigger value="relatorios">Relatórios</TabsTrigger>
        </TabsList>

        <TabsContent value="pagamentos" className="space-y-4">
          {/* Filters */}
          <Card className="p-6 glass border-0 shadow-medium">
            <div className="flex flex-col sm:flex-row gap-4">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                  <Input
                    placeholder="Buscar por aluno..."
                    className="pl-10"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                  />
                </div>
              </div>
              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger className="w-full sm:w-[200px]">
                  <SelectValue placeholder="Status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Todos</SelectItem>
                  <SelectItem value="confirmado">Confirmados</SelectItem>
                  <SelectItem value="pendente">Pendentes</SelectItem>
                  <SelectItem value="cancelado">Cancelados</SelectItem>
                </SelectContent>
              </Select>
              <Select
                value={filterMonth.toString()}
                onValueChange={(value) => setFilterMonth(parseInt(value))}
              >
                <SelectTrigger className="w-full sm:w-[150px]">
                  <SelectValue placeholder="Mês" />
                </SelectTrigger>
                <SelectContent>
                  {[...Array(12)].map((_, i) => (
                    <SelectItem key={i} value={(i + 1).toString()}>
                      {new Date(2000, i).toLocaleDateString('pt-BR', { month: 'long' })}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Select
                value={filterYear.toString()}
                onValueChange={(value) => setFilterYear(parseInt(value))}
              >
                <SelectTrigger className="w-full sm:w-[100px]">
                  <SelectValue placeholder="Ano" />
                </SelectTrigger>
                <SelectContent>
                  {[2023, 2024, 2025].map((year) => (
                    <SelectItem key={year} value={year.toString()}>
                      {year}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Button variant="outline" size="icon">
                <Download className="h-4 w-4" />
              </Button>
            </div>
          </Card>

          {/* Table */}
          <Card className="glass border-0 shadow-medium overflow-hidden">
            {loading ? (
              <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
              </div>
            ) : (
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Aluno</TableHead>
                    <TableHead>Valor</TableHead>
                    <TableHead>Referência</TableHead>
                    <TableHead>Data Pagamento</TableHead>
                    <TableHead>Forma</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead className="text-right">Ações</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredPagamentos.map((pagamento) => (
                    <TableRow key={pagamento.id}>
                      <TableCell className="font-medium">{pagamento.aluno_nome}</TableCell>
                      <TableCell>{formatCurrency(pagamento.valor)}</TableCell>
                      <TableCell>
                        {new Date(pagamento.ano_referencia, pagamento.mes_referencia - 1)
                          .toLocaleDateString('pt-BR', { month: 'short', year: 'numeric' })}
                      </TableCell>
                      <TableCell>
                        {pagamento.data_pagamento ? formatDate(pagamento.data_pagamento) : '-'}
                      </TableCell>
                      <TableCell>{getFormaPagamento(pagamento.forma_pagamento)}</TableCell>
                      <TableCell>{getStatusBadge(pagamento.status)}</TableCell>
                      <TableCell className="text-right">
                        <div className="flex items-center justify-end gap-2">
                          <Button
                            size="icon"
                            variant="ghost"
                            onClick={() => handleDelete(pagamento.id)}
                          >
                            <Trash2 className="h-4 w-4 text-destructive" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            )}
          </Card>
        </TabsContent>

        <TabsContent value="relatorios" className="space-y-4">
          <Card className="p-6 glass border-0 shadow-medium">
            <h3 className="text-lg font-semibold mb-4">Receita Mensal</h3>
            <RevenueChart
              data={[
                { name: 'Jan', value: 12500 },
                { name: 'Fev', value: 15000 },
                { name: 'Mar', value: 13500 },
                { name: 'Abr', value: 16000 },
                { name: 'Mai', value: 14500 },
                { name: 'Jun', value: 17000 }
              ]}
              title="Receita Mensal"
            />
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default function FinanceiroPage() {
  return (
    <Suspense fallback={<div className="p-6">Carregando...</div>}>
      <FinanceiroPageContent />
    </Suspense>
  )
}