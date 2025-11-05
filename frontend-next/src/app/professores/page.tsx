"use client"

import { useEffect, useState, Suspense } from 'react'
import { useSearchParams } from 'next/navigation'
import { motion } from 'framer-motion'
import {
  Users,
  Plus,
  Edit,
  Trash2,
  Mail,
  Phone,
  Award,
  ArrowLeft
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card } from '@/components/ui/card'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { toast } from 'sonner'
import { professoresAPI } from '@/lib/api'
import type { Professor, ProfessorCreateData } from '@/types'
import Link from 'next/link'

// Force dynamic rendering
export const dynamic = 'force-dynamic'

function ProfessoresPageContent() {
  const searchParams = useSearchParams()
  const [professores, setProfessores] = useState<Professor[]>([])
  const [loading, setLoading] = useState(true)
  const [isAddModalOpen, setIsAddModalOpen] = useState(false)
  const [selectedProfessor, setSelectedProfessor] = useState<Professor | null>(null)

  const [formData, setFormData] = useState<ProfessorCreateData>({
    nome: '',
    email: '',
    cpf: '',
    telefone: '',
    especialidade: 'natacao'
  })

  useEffect(() => {
    loadProfessores()
  }, [])

  useEffect(() => {
    if (searchParams.get('action') === 'new') {
      setIsAddModalOpen(true)
      window.history.replaceState({}, '', '/professores')
    }
  }, [searchParams])

  const loadProfessores = async () => {
    try {
      setLoading(true)
      const data = await professoresAPI.list()
      setProfessores(data)
    } catch (error) {
      console.error('Erro ao carregar professores:', error)
      toast.error('Erro ao carregar professores')
      setProfessores([])
    } finally {
      setLoading(false)
    }
  }

  const formatCPF = (value: string) => {
    // Remove tudo que não é número
    const numbers = value.replace(/\D/g, '')
    // Limita a 11 dígitos
    const limited = numbers.slice(0, 11)
    // Formata: XXX.XXX.XXX-XX
    return limited
      .replace(/(\d{3})(\d)/, '$1.$2')
      .replace(/(\d{3})(\d)/, '$1.$2')
      .replace(/(\d{3})(\d{1,2})$/, '$1-$2')
  }

  const formatPhone = (value: string) => {
    const numbers = value.replace(/\D/g, '')
    const limited = numbers.slice(0, 11)
    // (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
    if (limited.length <= 10) {
      return limited
        .replace(/(\d{2})(\d)/, '($1) $2')
        .replace(/(\d{4})(\d)/, '$1-$2')
    }
    return limited
      .replace(/(\d{2})(\d)/, '($1) $2')
      .replace(/(\d{5})(\d)/, '$1-$2')
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    // Validar CPF (11 dígitos)
    const cpfNumbers = formData.cpf.replace(/\D/g, '')
    if (cpfNumbers.length !== 11) {
      toast.error('CPF deve ter 11 dígitos')
      return
    }

    try {
      if (selectedProfessor) {
        await professoresAPI.update(selectedProfessor.id, formData)
        toast.success('Professor atualizado com sucesso!')
      } else {
        await professoresAPI.create(formData)
        toast.success('Professor criado com sucesso!')
      }
      loadProfessores()
      setIsAddModalOpen(false)
      resetForm()
    } catch (error) {
      console.error('Erro ao salvar professor:', error)
      const errorMsg = (error as { response?: { data?: { detail?: string } } }).response?.data?.detail || 'Erro ao salvar professor'
      toast.error(errorMsg)
    }
  }

  const handleDelete = async (id: number) => {
    if (!confirm('Tem certeza que deseja remover este professor?')) return

    try {
      await professoresAPI.delete(id)
      toast.success('Professor removido com sucesso!')
      loadProfessores()
    } catch (error) {
      console.error('Erro ao deletar professor:', error)
      const errorMsg = (error as { response?: { data?: { detail?: string } } }).response?.data?.detail || 'Erro ao deletar professor'
      toast.error(errorMsg)
    }
  }

  const handleEdit = (professor: Professor) => {
    setSelectedProfessor(professor)
    setFormData({
      nome: professor.nome,
      email: professor.email,
      cpf: professor.cpf,
      telefone: professor.telefone || '',
      especialidade: professor.especialidade || 'natacao'
    })
    setIsAddModalOpen(true)
  }

  const resetForm = () => {
    setFormData({
      nome: '',
      email: '',
      cpf: '',
      telefone: '',
      especialidade: 'natacao'
    })
    setSelectedProfessor(null)
  }

  const handleModalClose = () => {
    setIsAddModalOpen(false)
    resetForm()
  }

  const getEspecialidadeLabel = (esp?: string) => {
    switch (esp) {
      case 'natacao': return 'Natação'
      case 'hidroginastica': return 'Hidroginástica'
      case 'ambos': return 'Natação + Hidroginástica'
      default: return 'Não especificado'
    }
  }

  const getEspecialidadeBadge = (esp?: string) => {
    const colors = {
      natacao: 'bg-blue-100 text-blue-800',
      hidroginastica: 'bg-green-100 text-green-800',
      ambos: 'bg-purple-100 text-purple-800'
    }
    return colors[esp as keyof typeof colors] || 'bg-gray-100 text-gray-800'
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background p-4 md:p-8">
        <div className="max-w-7xl mx-auto">
          <div className="animate-pulse">
            <div className="h-8 bg-muted rounded w-1/4 mb-6"></div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {[1, 2, 3].map(i => (
                <div key={i} className="h-48 bg-muted rounded"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background p-4 md:p-8">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-4">
            <Link href="/">
              <Button variant="ghost" size="icon">
                <ArrowLeft className="h-5 w-5" />
              </Button>
            </Link>
            <div>
              <h1 className="text-3xl font-bold">Professores</h1>
              <p className="text-muted-foreground">
                {professores.length} {professores.length === 1 ? 'professor cadastrado' : 'professores cadastrados'}
              </p>
            </div>
          </div>
          <Button onClick={() => setIsAddModalOpen(true)}>
            <Plus className="h-4 w-4 mr-2" />
            Novo Professor
          </Button>
        </div>

        {/* Lista de Professores */}
        {professores.length === 0 ? (
          <Card className="p-12 text-center">
            <Users className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-2">Nenhum professor cadastrado</h3>
            <p className="text-muted-foreground mb-4">
              Comece adicionando o primeiro professor
            </p>
            <Button onClick={() => setIsAddModalOpen(true)}>
              <Plus className="h-4 w-4 mr-2" />
              Adicionar Professor
            </Button>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {professores.map(professor => (
              <motion.div
                key={professor.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
              >
                <Card className="p-6 hover:shadow-lg transition-shadow">
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex-1">
                      <h3 className="font-semibold text-lg mb-1">{professor.nome}</h3>
                      <span className={`inline-block px-2 py-1 rounded-full text-xs font-medium ${getEspecialidadeBadge(professor.especialidade)}`}>
                        {getEspecialidadeLabel(professor.especialidade)}
                      </span>
                    </div>
                    <div className="flex gap-2">
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => handleEdit(professor)}
                      >
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => handleDelete(professor.id)}
                      >
                        <Trash2 className="h-4 w-4 text-destructive" />
                      </Button>
                    </div>
                  </div>

                  <div className="space-y-2 text-sm">
                    <div className="flex items-center gap-2 text-muted-foreground">
                      <Mail className="h-4 w-4" />
                      <span>{professor.email}</span>
                    </div>
                    {professor.telefone && (
                      <div className="flex items-center gap-2 text-muted-foreground">
                        <Phone className="h-4 w-4" />
                        <span>{professor.telefone}</span>
                      </div>
                    )}
                    <div className="flex items-center gap-2 text-muted-foreground">
                      <Award className="h-4 w-4" />
                      <span className="font-mono">{professor.cpf}</span>
                    </div>
                  </div>

                  {!professor.is_active && (
                    <div className="mt-4 pt-4 border-t">
                      <span className="text-xs text-muted-foreground">
                        ⚠️ Professor inativo
                      </span>
                    </div>
                  )}
                </Card>
              </motion.div>
            ))}
          </div>
        )}

        {/* Modal Adicionar/Editar Professor */}
        <Dialog open={isAddModalOpen} onOpenChange={handleModalClose}>
          <DialogContent className="max-w-md">
            <DialogHeader>
              <DialogTitle>
                {selectedProfessor ? 'Editar Professor' : 'Novo Professor'}
              </DialogTitle>
              <DialogDescription>
                {selectedProfessor
                  ? 'Atualize as informações do professor'
                  : 'Preencha os dados do novo professor'}
              </DialogDescription>
            </DialogHeader>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label htmlFor="nome">Nome Completo *</Label>
                <Input
                  id="nome"
                  value={formData.nome}
                  onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
                  required
                  placeholder="João da Silva"
                />
              </div>

              <div>
                <Label htmlFor="email">Email *</Label>
                <Input
                  id="email"
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  required
                  placeholder="joao@example.com"
                />
              </div>

              <div>
                <Label htmlFor="cpf">CPF *</Label>
                <Input
                  id="cpf"
                  value={formData.cpf}
                  onChange={(e) => setFormData({ ...formData, cpf: formatCPF(e.target.value) })}
                  required
                  placeholder="000.000.000-00"
                  maxLength={14}
                />
              </div>

              <div>
                <Label htmlFor="telefone">Telefone</Label>
                <Input
                  id="telefone"
                  value={formData.telefone}
                  onChange={(e) => setFormData({ ...formData, telefone: formatPhone(e.target.value) })}
                  placeholder="(00) 00000-0000"
                  maxLength={15}
                />
              </div>

              <div>
                <Label htmlFor="especialidade">Especialidade</Label>
                <Select
                  value={formData.especialidade}
                  onValueChange={(value) => setFormData({ ...formData, especialidade: value })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="natacao">Natação</SelectItem>
                    <SelectItem value="hidroginastica">Hidroginástica</SelectItem>
                    <SelectItem value="ambos">Natação + Hidroginástica</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="flex gap-2 pt-4">
                <Button type="button" variant="outline" onClick={handleModalClose} className="flex-1">
                  Cancelar
                </Button>
                <Button type="submit" className="flex-1">
                  {selectedProfessor ? 'Atualizar' : 'Criar'}
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>
    </div>
  )
}

export default function ProfessoresPage() {
  return (
    <Suspense fallback={<div>Carregando...</div>}>
      <ProfessoresPageContent />
    </Suspense>
  )
}
