"use client"

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import {
  Calendar,
  Plus,
  Clock,
  Users,
  MapPin,
  Edit,
  Trash2
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { toast } from 'sonner'
import { horariosAPI } from '@/lib/api'

interface HorarioDetalhado {
  id: number
  dia_semana: string
  hora_inicio: string
  hora_fim: string
  turma: string
  professor: string
  nivel: string
  sala_piscina: string
  capacidade: number
  alunos_matriculados: number
}

const diasSemana = [
  'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'
]

const horarios = [
  '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
  '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'
]

const niveis = ['Iniciante', 'Intermediário', 'Avançado', 'Competição']

const cores = {
  'Iniciante': 'bg-blue-500',
  'Intermediário': 'bg-green-500',
  'Avançado': 'bg-purple-500',
  'Competição': 'bg-red-500'
}

export default function HorariosPage() {
  const [horariosList, setHorariosList] = useState<HorarioDetalhado[]>([])
  const [loading, setLoading] = useState(true)
  const [viewMode, setViewMode] = useState<'week' | 'list'>('week')
  const [isAddModalOpen, setIsAddModalOpen] = useState(false)
  const [selectedHorario, setSelectedHorario] = useState<HorarioDetalhado | null>(null)

  // Form state
  const [formData, setFormData] = useState({
    dia_semana: '',
    hora_inicio: '',
    hora_fim: '',
    turma: '',
    professor: '',
    nivel: 'Iniciante',
    sala_piscina: '',
    capacidade: 10,
    alunos_matriculados: 0
  })

  useEffect(() => {
    loadHorarios()
  }, [])

  const loadHorarios = async () => {
    try {
      setLoading(true)
      const data = await horariosAPI.list()
      setHorariosList(data)
    } catch (error) {
      console.error('Erro ao carregar horários:', error)
      // Usar dados mockados se a API falhar
      setHorariosList([
        {
          id: 1,
          dia_semana: 'Segunda',
          hora_inicio: '07:00',
          hora_fim: '08:00',
          turma: 'Iniciante A',
          professor: 'João Silva',
          nivel: 'Iniciante',
          sala_piscina: 'Piscina 1',
          capacidade: 10,
          alunos_matriculados: 8
        },
        {
          id: 2,
          dia_semana: 'Segunda',
          hora_inicio: '08:00',
          hora_fim: '09:00',
          turma: 'Intermediário B',
          professor: 'Maria Santos',
          nivel: 'Intermediário',
          sala_piscina: 'Piscina 2',
          capacidade: 12,
          alunos_matriculados: 10
        },
        {
          id: 3,
          dia_semana: 'Terça',
          hora_inicio: '07:00',
          hora_fim: '08:00',
          turma: 'Avançado C',
          professor: 'Pedro Costa',
          nivel: 'Avançado',
          sala_piscina: 'Piscina 1',
          capacidade: 8,
          alunos_matriculados: 6
        },
        {
          id: 4,
          dia_semana: 'Quarta',
          hora_inicio: '18:00',
          hora_fim: '19:00',
          turma: 'Competição',
          professor: 'Ana Oliveira',
          nivel: 'Competição',
          sala_piscina: 'Piscina Olímpica',
          capacidade: 15,
          alunos_matriculados: 12
        }
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const horarioData = {
        dia_semana: formData.dia_semana,
        horario: formData.hora_inicio,
        tipo_aula: 'natacao' as 'natacao' | 'hidroginastica',
        professor: formData.professor,
        capacidade_maxima: formData.capacidade
      }

      if (selectedHorario) {
        await horariosAPI.update(selectedHorario.id, horarioData)
        toast.success('Horário atualizado com sucesso!')
      } else {
        await horariosAPI.create(horarioData)
        toast.success('Horário cadastrado com sucesso!')
      }
      loadHorarios()
      setIsAddModalOpen(false)
      resetForm()
    } catch (error) {
      console.error('Erro ao salvar horário:', error)
      toast.error('Erro ao salvar horário')
    }
  }

  const handleDelete = async (id: number) => {
    if (confirm('Tem certeza que deseja excluir este horário?')) {
      try {
        await horariosAPI.delete(id)
        toast.success('Horário excluído com sucesso!')
        loadHorarios()
      } catch (error) {
        console.error('Erro ao excluir horário:', error)
        toast.error('Erro ao excluir horário')
      }
    }
  }

  const resetForm = () => {
    setFormData({
      dia_semana: '',
      hora_inicio: '',
      hora_fim: '',
      turma: '',
      professor: '',
      nivel: 'Iniciante',
      sala_piscina: '',
      capacidade: 10,
      alunos_matriculados: 0
    })
    setSelectedHorario(null)
  }

  const getHorarioForSlot = (dia: string, hora: string) => {
    return horariosList.find(
      h => h.dia_semana === dia && h.hora_inicio === hora
    )
  }

  const WeekView = () => (
    <Card className="glass border-0 shadow-medium overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-muted/50">
            <tr>
              <th className="p-3 text-left font-medium">Horário</th>
              {diasSemana.map(dia => (
                <th key={dia} className="p-3 text-center font-medium min-w-[150px]">
                  {dia}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {horarios.map(hora => (
              <tr key={hora} className="border-t">
                <td className="p-3 font-medium">{hora}</td>
                {diasSemana.map(dia => {
                  const horario = getHorarioForSlot(dia, hora)
                  return (
                    <td key={`${dia}-${hora}`} className="p-2 text-center">
                      {horario ? (
                        <motion.div
                          initial={{ opacity: 0, scale: 0.9 }}
                          animate={{ opacity: 1, scale: 1 }}
                          className={`${cores[horario.nivel as keyof typeof cores]} text-white rounded-lg p-2 cursor-pointer hover:opacity-90 transition-opacity`}
                          onClick={() => {
                            setSelectedHorario(horario)
                            setFormData({
                              dia_semana: horario.dia_semana,
                              hora_inicio: horario.hora_inicio,
                              hora_fim: horario.hora_fim,
                              turma: horario.turma,
                              professor: horario.professor,
                              nivel: horario.nivel,
                              sala_piscina: horario.sala_piscina,
                              capacidade: horario.capacidade,
                              alunos_matriculados: horario.alunos_matriculados
                            })
                            setIsAddModalOpen(true)
                          }}
                        >
                          <div className="text-xs font-semibold">{horario.turma}</div>
                          <div className="text-xs opacity-90">{horario.professor}</div>
                          <div className="text-xs mt-1">
                            <Users className="inline h-3 w-3 mr-1" />
                            {horario.alunos_matriculados}/{horario.capacidade}
                          </div>
                        </motion.div>
                      ) : (
                        <button
                          className="w-full h-full min-h-[60px] hover:bg-muted/50 rounded-lg transition-colors"
                          onClick={() => {
                            resetForm()
                            setFormData(prev => ({
                              ...prev,
                              dia_semana: dia,
                              hora_inicio: hora
                            }))
                            setIsAddModalOpen(true)
                          }}
                        >
                          <Plus className="h-4 w-4 mx-auto text-muted-foreground" />
                        </button>
                      )}
                    </td>
                  )
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  )

  const ListView = () => (
    <div className="grid gap-4">
      {horariosList.map((horario) => (
        <motion.div
          key={horario.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <Card className="p-6 glass border-0 shadow-medium hover:shadow-lg transition-shadow">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className={`${cores[horario.nivel as keyof typeof cores]} text-white p-3 rounded-lg`}>
                  <Clock className="h-6 w-6" />
                </div>
                <div>
                  <h3 className="font-semibold text-lg">{horario.turma}</h3>
                  <div className="flex items-center gap-4 mt-1 text-sm text-muted-foreground">
                    <span className="flex items-center gap-1">
                      <Calendar className="h-3 w-3" />
                      {horario.dia_semana}
                    </span>
                    <span className="flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      {horario.hora_inicio} - {horario.hora_fim}
                    </span>
                    <span className="flex items-center gap-1">
                      <MapPin className="h-3 w-3" />
                      {horario.sala_piscina}
                    </span>
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-4">
                <div className="text-right">
                  <p className="text-sm text-muted-foreground">Professor</p>
                  <p className="font-medium">{horario.professor}</p>
                </div>
                <div className="text-right">
                  <p className="text-sm text-muted-foreground">Ocupação</p>
                  <div className="flex items-center gap-1">
                    <Users className="h-4 w-4" />
                    <span className="font-medium">
                      {horario.alunos_matriculados}/{horario.capacidade}
                    </span>
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button
                    size="icon"
                    variant="ghost"
                    onClick={() => {
                      setSelectedHorario(horario)
                      setFormData({
                        dia_semana: horario.dia_semana,
                        hora_inicio: horario.hora_inicio,
                        hora_fim: horario.hora_fim,
                        turma: horario.turma,
                        professor: horario.professor,
                        nivel: horario.nivel,
                        sala_piscina: horario.sala_piscina,
                        capacidade: horario.capacidade,
                        alunos_matriculados: horario.alunos_matriculados
                      })
                      setIsAddModalOpen(true)
                    }}
                  >
                    <Edit className="h-4 w-4" />
                  </Button>
                  <Button
                    size="icon"
                    variant="ghost"
                    onClick={() => handleDelete(horario.id)}
                  >
                    <Trash2 className="h-4 w-4 text-destructive" />
                  </Button>
                </div>
              </div>
            </div>
          </Card>
        </motion.div>
      ))}
    </div>
  )

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4"
      >
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-3">
            <div className="p-2 bg-primary/10 rounded-lg">
              <Calendar className="h-6 w-6 text-primary" />
            </div>
            Horários
          </h1>
          <p className="text-muted-foreground mt-1">
            Gerencie os horários das aulas
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex rounded-lg border p-1">
            <Button
              size="sm"
              variant={viewMode === 'week' ? 'default' : 'ghost'}
              onClick={() => setViewMode('week')}
            >
              Semana
            </Button>
            <Button
              size="sm"
              variant={viewMode === 'list' ? 'default' : 'ghost'}
              onClick={() => setViewMode('list')}
            >
              Lista
            </Button>
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
                Novo Horário
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[600px]">
              <DialogHeader>
                <DialogTitle>
                  {selectedHorario ? 'Editar Horário' : 'Cadastrar Novo Horário'}
                </DialogTitle>
                <DialogDescription>
                  Preencha os dados do horário abaixo
                </DialogDescription>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="turma">Nome da Turma*</Label>
                    <Input
                      id="turma"
                      value={formData.turma}
                      onChange={(e) => setFormData({...formData, turma: e.target.value})}
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="nivel">Nível*</Label>
                    <Select
                      value={formData.nivel}
                      onValueChange={(value) => setFormData({...formData, nivel: value})}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Selecione o nível" />
                      </SelectTrigger>
                      <SelectContent>
                        {niveis.map(nivel => (
                          <SelectItem key={nivel} value={nivel}>{nivel}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="dia_semana">Dia da Semana*</Label>
                    <Select
                      value={formData.dia_semana}
                      onValueChange={(value) => setFormData({...formData, dia_semana: value})}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Selecione o dia" />
                      </SelectTrigger>
                      <SelectContent>
                        {diasSemana.map(dia => (
                          <SelectItem key={dia} value={dia}>{dia}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="hora_inicio">Hora Início*</Label>
                    <Input
                      id="hora_inicio"
                      type="time"
                      value={formData.hora_inicio}
                      onChange={(e) => setFormData({...formData, hora_inicio: e.target.value})}
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="hora_fim">Hora Fim*</Label>
                    <Input
                      id="hora_fim"
                      type="time"
                      value={formData.hora_fim}
                      onChange={(e) => setFormData({...formData, hora_fim: e.target.value})}
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="professor">Professor*</Label>
                    <Input
                      id="professor"
                      value={formData.professor}
                      onChange={(e) => setFormData({...formData, professor: e.target.value})}
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="sala_piscina">Piscina/Sala*</Label>
                    <Input
                      id="sala_piscina"
                      value={formData.sala_piscina}
                      onChange={(e) => setFormData({...formData, sala_piscina: e.target.value})}
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="capacidade">Capacidade*</Label>
                    <Input
                      id="capacidade"
                      type="number"
                      min="1"
                      value={formData.capacidade}
                      onChange={(e) => setFormData({...formData, capacidade: parseInt(e.target.value)})}
                      required
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
                    {selectedHorario ? 'Salvar Alterações' : 'Cadastrar'}
                  </Button>
                </div>
              </form>
            </DialogContent>
          </Dialog>
        </div>
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
                <p className="text-sm text-muted-foreground">Total de Turmas</p>
                <p className="text-2xl font-bold">{horariosList.length}</p>
              </div>
              <Calendar className="h-8 w-8 text-primary opacity-50" />
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
                <p className="text-sm text-muted-foreground">Alunos Matriculados</p>
                <p className="text-2xl font-bold">
                  {horariosList.reduce((acc, h) => acc + h.alunos_matriculados, 0)}
                </p>
              </div>
              <Users className="h-8 w-8 text-green-500 opacity-50" />
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
                <p className="text-sm text-muted-foreground">Capacidade Total</p>
                <p className="text-2xl font-bold">
                  {horariosList.reduce((acc, h) => acc + h.capacidade, 0)}
                </p>
              </div>
              <div className="h-8 w-8 rounded-full bg-blue-500/20 flex items-center justify-center">
                <div className="h-3 w-3 rounded-full bg-blue-500" />
              </div>
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
                <p className="text-sm text-muted-foreground">Taxa Ocupação</p>
                <p className="text-2xl font-bold">
                  {horariosList.length > 0
                    ? Math.round((horariosList.reduce((acc, h) => acc + h.alunos_matriculados, 0) /
                        horariosList.reduce((acc, h) => acc + h.capacidade, 0)) * 100)
                    : 0}%
                </p>
              </div>
              <div className="h-8 w-8 rounded-full bg-purple-500/20 flex items-center justify-center">
                <div className="h-3 w-3 rounded-full bg-purple-500" />
              </div>
            </div>
          </Card>
        </motion.div>
      </div>

      {/* Content */}
      {loading ? (
        <Card className="glass border-0 shadow-medium">
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
          </div>
        </Card>
      ) : viewMode === 'week' ? (
        <WeekView />
      ) : (
        <ListView />
      )}
    </div>
  )
}