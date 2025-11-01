"use client"

import { useEffect, useState, Suspense } from 'react'
import Link from 'next/link'
import { useSearchParams } from 'next/navigation'
import { motion } from 'framer-motion'
import {
  Users,
  Plus,
  Search,
  Download,
  Edit,
  Trash2,
  Phone,
  Calendar,
  AlertCircle,
  User,
  ArrowLeft
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card } from '@/components/ui/card'
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
import { Badge } from '@/components/ui/badge'
import { toast } from 'sonner'
import { alunosAPI } from '@/lib/api'
import type { Aluno } from '@/types'

function AlunosPageContent() {
  const searchParams = useSearchParams()
  const [alunos, setAlunos] = useState<Aluno[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterStatus, setFilterStatus] = useState('all')
  const [isAddModalOpen, setIsAddModalOpen] = useState(false)
  const [selectedAluno, setSelectedAluno] = useState<Aluno | null>(null)

  // Form state
  const [formData, setFormData] = useState({
    nome_completo: '',
    responsavel: '',
    tipo_aula: 'natacao' as 'natacao' | 'hidroginastica',
    valor_mensalidade: 250,
    dia_vencimento: 10,
    data_inicio_contrato: new Date().toISOString().split('T')[0],
    telefone_whatsapp: '',
    observacoes: ''
  })

  useEffect(() => {
    loadAlunos()
  }, [])

  // Check for action parameter from quick actions
  useEffect(() => {
    if (searchParams.get('action') === 'new') {
      setIsAddModalOpen(true)
      // Clear the parameter after opening
      window.history.replaceState({}, '', '/alunos')
    }
  }, [searchParams])

  const loadAlunos = async () => {
    try {
      setLoading(true)
      const data = await alunosAPI.list()
      setAlunos(data)
    } catch (error) {
      console.error('Erro ao carregar alunos:', error)
      toast.error('Erro ao carregar lista de alunos')
      // Se falhar, não usar dados mockados - lista vazia
      setAlunos([])
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      if (selectedAluno) {
        await alunosAPI.update(selectedAluno.id, formData)
        toast.success('Aluno atualizado com sucesso!')
      } else {
        await alunosAPI.create(formData)
        toast.success('Aluno cadastrado com sucesso!')
      }
      loadAlunos()
      setIsAddModalOpen(false)
      resetForm()
    } catch (error) {
      console.error('Erro ao salvar aluno:', error)
      toast.error('Erro ao salvar aluno')
    }
  }

  const handleDelete = async (id: number) => {
    if (confirm('Tem certeza que deseja excluir este aluno?')) {
      try {
        await alunosAPI.delete(id)
        toast.success('Aluno excluído com sucesso!')
        // Reload the list immediately after deletion
        await loadAlunos()
      } catch (error) {
        console.error('Erro ao excluir aluno:', error)
        let errorMessage = 'Erro ao excluir aluno'
        if (error && typeof error === 'object' && 'response' in error) {
          const response = error as { response?: { data?: { detail?: string } } }
          errorMessage = response.response?.data?.detail || errorMessage
        }
        toast.error(errorMessage)
      }
    }
  }

  const resetForm = () => {
    setFormData({
      nome_completo: '',
      responsavel: '',
      tipo_aula: 'natacao' as 'natacao' | 'hidroginastica',
      valor_mensalidade: 250,
      dia_vencimento: 10,
      data_inicio_contrato: new Date().toISOString().split('T')[0],
      telefone_whatsapp: '',
      observacoes: ''
    })
    setSelectedAluno(null)
  }

  const filteredAlunos = alunos.filter(aluno => {
    const matchesSearch = aluno.nome_completo.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         aluno.telefone_whatsapp?.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesFilter = filterStatus === 'all' ||
                         (filterStatus === 'active' && aluno.ativo) ||
                         (filterStatus === 'inactive' && !aluno.ativo)
    return matchesSearch && matchesFilter
  })

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
                <Users className="h-6 w-6 text-primary" />
              </div>
              Alunos
            </h1>
            <p className="text-muted-foreground mt-1">
              Gerencie os alunos matriculados
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
              Novo Aluno
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[600px]">
            <DialogHeader>
              <DialogTitle>
                {selectedAluno ? 'Editar Aluno' : 'Cadastrar Novo Aluno'}
              </DialogTitle>
              <DialogDescription>
                Preencha os dados do aluno abaixo
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="nome_completo">Nome Completo*</Label>
                  <Input
                    id="nome_completo"
                    value={formData.nome_completo}
                    onChange={(e) => setFormData({...formData, nome_completo: e.target.value})}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="responsavel">Responsável</Label>
                  <Input
                    id="responsavel"
                    value={formData.responsavel}
                    onChange={(e) => setFormData({...formData, responsavel: e.target.value})}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="telefone_whatsapp">WhatsApp</Label>
                  <Input
                    id="telefone_whatsapp"
                    value={formData.telefone_whatsapp}
                    onChange={(e) => setFormData({...formData, telefone_whatsapp: e.target.value})}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="tipo_aula">Tipo de Aula*</Label>
                  <Select
                    value={formData.tipo_aula}
                    onValueChange={(value: 'natacao' | 'hidroginastica') => setFormData({...formData, tipo_aula: value})}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Selecione o tipo" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="natacao">Natação</SelectItem>
                      <SelectItem value="hidroginastica">Hidroginástica</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="valor_mensalidade">Valor Mensalidade*</Label>
                  <Input
                    id="valor_mensalidade"
                    type="number"
                    step="0.01"
                    value={formData.valor_mensalidade}
                    onChange={(e) => setFormData({...formData, valor_mensalidade: parseFloat(e.target.value)})}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="dia_vencimento">Dia Vencimento*</Label>
                  <Input
                    id="dia_vencimento"
                    type="number"
                    min="1"
                    max="31"
                    value={formData.dia_vencimento}
                    onChange={(e) => setFormData({...formData, dia_vencimento: parseInt(e.target.value)})}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="data_inicio_contrato">Data Início*</Label>
                  <Input
                    id="data_inicio_contrato"
                    type="date"
                    value={formData.data_inicio_contrato}
                    onChange={(e) => setFormData({...formData, data_inicio_contrato: e.target.value})}
                    required
                  />
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
                  {selectedAluno ? 'Salvar Alterações' : 'Cadastrar'}
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
                <p className="text-sm text-muted-foreground">Total de Alunos</p>
                <p className="text-2xl font-bold">{alunos.length}</p>
              </div>
              <Users className="h-8 w-8 text-primary opacity-50" />
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
                <p className="text-sm text-muted-foreground">Ativos</p>
                <p className="text-2xl font-bold">
                  {alunos.filter(a => a.ativo).length}
                </p>
              </div>
              <div className="h-8 w-8 rounded-full bg-green-500/20 flex items-center justify-center">
                <div className="h-3 w-3 rounded-full bg-green-500" />
              </div>
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
                <p className="text-sm text-muted-foreground">Inadimplentes</p>
                <p className="text-2xl font-bold">
                  {alunos.filter(a => !a.ativo).length}
                </p>
              </div>
              <AlertCircle className="h-8 w-8 text-yellow-500 opacity-50" />
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
                <p className="text-sm text-muted-foreground">Novos (30 dias)</p>
                <p className="text-2xl font-bold">
                  {alunos.filter(a => {
                    const createdAt = new Date(a.created_at || '')
                    const thirtyDaysAgo = new Date()
                    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30)
                    return createdAt > thirtyDaysAgo
                  }).length}
                </p>
              </div>
              <Calendar className="h-8 w-8 text-blue-500 opacity-50" />
            </div>
          </Card>
        </motion.div>
      </div>

      {/* Filters */}
      <Card className="p-6 glass border-0 shadow-medium">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
              <Input
                placeholder="Buscar por nome ou email..."
                className="pl-10"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
          <Select value={filterStatus} onValueChange={setFilterStatus}>
            <SelectTrigger className="w-full sm:w-[200px]">
              <SelectValue placeholder="Filtrar por status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todos</SelectItem>
              <SelectItem value="active">Ativos</SelectItem>
              <SelectItem value="inactive">Inativos</SelectItem>
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
                <TableHead>Nome</TableHead>
                <TableHead>Contato</TableHead>
                <TableHead>Nível</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Pagamento</TableHead>
                <TableHead className="text-right">Ações</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredAlunos.map((aluno) => (
                <TableRow key={aluno.id}>
                  <TableCell className="font-medium">{aluno.nome_completo}</TableCell>
                  <TableCell>
                    <div className="space-y-1">
                      {aluno.responsavel && (
                        <div className="flex items-center gap-1 text-sm text-muted-foreground">
                          <User className="h-3 w-3" />
                          {aluno.responsavel}
                        </div>
                      )}
                      {aluno.telefone_whatsapp && (
                        <div className="flex items-center gap-1 text-sm text-muted-foreground">
                          <Phone className="h-3 w-3" />
                          {aluno.telefone_whatsapp}
                        </div>
                      )}
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="secondary">
                      {aluno.tipo_aula === 'hidroginastica' ? 'Hidroginástica' : 'Natação'}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Badge
                      variant={aluno.ativo ? "default" : "secondary"}
                      className={aluno.ativo ? "bg-green-500" : ""}
                    >
                      {aluno.ativo ? 'Ativo' : 'Inativo'}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Badge
                      variant={!aluno.ativo ? "destructive" : "default"}
                      className={aluno.ativo ? "bg-green-500" : ""}
                    >
                      {!aluno.ativo ? 'Inadimplente' : 'Em dia'}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="flex items-center justify-end gap-2">
                      <Button
                        size="icon"
                        variant="ghost"
                        onClick={() => {
                          setSelectedAluno(aluno)
                          setFormData({
                            nome_completo: aluno.nome_completo,
                            responsavel: aluno.responsavel || '',
                            tipo_aula: (aluno.tipo_aula || 'natacao') as 'natacao' | 'hidroginastica',
                            valor_mensalidade: aluno.valor_mensalidade || 250,
                            dia_vencimento: aluno.dia_vencimento || 10,
                            data_inicio_contrato: aluno.data_inicio_contrato || new Date().toISOString().split('T')[0],
                            telefone_whatsapp: aluno.telefone_whatsapp || '',
                            observacoes: aluno.observacoes || ''
                          })
                          setIsAddModalOpen(true)
                        }}
                      >
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button
                        size="icon"
                        variant="ghost"
                        onClick={() => handleDelete(aluno.id)}
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
    </div>
  )
}

export default function AlunosPage() {
  return (
    <Suspense fallback={<div className="p-6">Carregando...</div>}>
      <AlunosPageContent />
    </Suspense>
  )
}