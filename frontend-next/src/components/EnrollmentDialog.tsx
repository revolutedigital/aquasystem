"use client"

import { useState, useEffect, useCallback } from 'react'
import { Users, X, Plus, Loader2 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { toast } from 'sonner'
import { horariosAPI, alunosAPI } from '@/lib/api'

interface Aluno {
  id: number
  nome_completo: string
  telefone_whatsapp?: string
  tipo_aula: string
  ativo: boolean
}

interface HorarioSimples {
  id: number
  dia_semana: string
  horario: string
  capacidade_maxima: number
  tipo_aula: string
}

interface EnrollmentDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  horarioId: number
  horarioInfo?: HorarioSimples
  onEnrollmentChange?: () => void
}

interface VagasData {
  horario_id: number
  capacidade_maxima: number
  alunos_matriculados: number
  vagas_disponiveis: number
}

export function EnrollmentDialog({
  open,
  onOpenChange,
  horarioId,
  horarioInfo,
  onEnrollmentChange
}: EnrollmentDialogProps) {
  const [alunos, setAlunos] = useState<Aluno[]>([])
  const [enrolledAlunos, setEnrolledAlunos] = useState<Aluno[]>([])
  const [selectedAlunoId, setSelectedAlunoId] = useState<string>('')
  const [loading, setLoading] = useState(false)
  const [adding, setAdding] = useState(false)
  const [vagas, setVagas] = useState<VagasData | null>(null)

  const loadData = useCallback(async () => {
    setLoading(true)
    try {
      // Load all active students
      const alunosData = await alunosAPI.list(false)
      setAlunos(alunosData)

      // Load schedule info with vagas
      const vagasData = await horariosAPI.getVagas(horarioId)
      setVagas(vagasData)

      // Load enrolled students through grade completa
      const gradeCompleta = await horariosAPI.getGradeCompleta()
      const horario = gradeCompleta.find((h: { id: number }) => h.id === horarioId)
      if (horario && horario.alunos) {
        setEnrolledAlunos(horario.alunos)
      } else {
        setEnrolledAlunos([])
      }
    } catch {
      toast.error('Erro ao carregar dados de matrícula')
    } finally {
      setLoading(false)
    }
  }, [horarioId])

  useEffect(() => {
    if (open) {
      loadData()
    }
  }, [open, loadData])

  const handleAddAluno = async () => {
    if (!selectedAlunoId) {
      toast.error('Selecione um aluno')
      return
    }

    setAdding(true)
    try {
      await horariosAPI.addAluno(horarioId, parseInt(selectedAlunoId))
      toast.success('Aluno adicionado ao horário')
      setSelectedAlunoId('')
      await loadData()
      onEnrollmentChange?.()
    } catch (error) {
      const errorMsg = (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Erro ao adicionar aluno ao horário'
      toast.error(errorMsg)
    } finally {
      setAdding(false)
    }
  }

  const handleRemoveAluno = async (alunoId: number) => {
    try {
      await horariosAPI.removeAluno(horarioId, alunoId)
      toast.success('Aluno removido do horário')
      await loadData()
      onEnrollmentChange?.()
    } catch (error) {
      const errorMsg = (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Erro ao remover aluno do horário'
      toast.error(errorMsg)
    }
  }

  // Filter students not enrolled and matching the schedule type
  const availableAlunos = alunos.filter(
    a => !enrolledAlunos.some(e => e.id === a.id) &&
         a.ativo &&
         (!horarioInfo?.tipo_aula || a.tipo_aula === horarioInfo.tipo_aula)
  )

  const diaSemanaNomes: Record<string, string> = {
    'segunda': 'Segunda',
    'terca': 'Terça',
    'quarta': 'Quarta',
    'quinta': 'Quinta',
    'sexta': 'Sexta',
    'sabado': 'Sábado',
    'domingo': 'Domingo'
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Users className="h-5 w-5" />
            Gerenciar Matrículas
          </DialogTitle>
          <DialogDescription>
            {horarioInfo && (
              <div className="mt-2 space-y-1">
                <p className="font-medium text-foreground">
                  {diaSemanaNomes[horarioInfo.dia_semana]} - {horarioInfo.horario}
                </p>
                {vagas && (
                  <div className="flex gap-4 text-sm">
                    <span>Capacidade: {vagas.capacidade_maxima}</span>
                    <span>Matriculados: {vagas.alunos_matriculados}</span>
                    <span className={vagas.vagas_disponiveis > 0 ? 'text-green-600' : 'text-red-600'}>
                      Vagas: {vagas.vagas_disponiveis}
                    </span>
                  </div>
                )}
              </div>
            )}
          </DialogDescription>
        </DialogHeader>

        {loading ? (
          <div className="flex items-center justify-center p-8">
            <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
          </div>
        ) : (
          <div className="space-y-6">
            {/* Add Student Section */}
            <div className="space-y-3">
              <h4 className="font-medium">Adicionar Aluno</h4>
              <div className="flex gap-2">
                <Select value={selectedAlunoId} onValueChange={setSelectedAlunoId}>
                  <SelectTrigger className="flex-1">
                    <SelectValue placeholder="Selecione um aluno..." />
                  </SelectTrigger>
                  <SelectContent>
                    {availableAlunos.length === 0 ? (
                      <div className="p-2 text-sm text-muted-foreground">
                        Nenhum aluno disponível
                      </div>
                    ) : (
                      availableAlunos.map(aluno => (
                        <SelectItem key={aluno.id} value={aluno.id.toString()}>
                          {aluno.nome_completo}
                        </SelectItem>
                      ))
                    )}
                  </SelectContent>
                </Select>
                <Button
                  onClick={handleAddAluno}
                  disabled={!selectedAlunoId || adding || (vagas?.vagas_disponiveis ?? 0) <= 0}
                  size="icon"
                >
                  {adding ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Plus className="h-4 w-4" />
                  )}
                </Button>
              </div>
              {vagas && vagas.vagas_disponiveis <= 0 && (
                <p className="text-sm text-red-600">
                  Horário com capacidade máxima atingida
                </p>
              )}
            </div>

            {/* Enrolled Students List */}
            <div className="space-y-3">
              <h4 className="font-medium">
                Alunos Matriculados ({enrolledAlunos.length})
              </h4>
              {enrolledAlunos.length === 0 ? (
                <p className="text-sm text-muted-foreground py-4 text-center">
                  Nenhum aluno matriculado neste horário
                </p>
              ) : (
                <div className="space-y-2">
                  {enrolledAlunos.map(aluno => (
                    <div
                      key={aluno.id}
                      className="flex items-center justify-between p-3 border rounded-lg hover:bg-muted/50 transition-colors"
                    >
                      <div className="flex-1">
                        <p className="font-medium">{aluno.nome_completo}</p>
                        {aluno.telefone_whatsapp && (
                          <p className="text-sm text-muted-foreground">
                            {aluno.telefone_whatsapp}
                          </p>
                        )}
                      </div>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => handleRemoveAluno(aluno.id)}
                        className="text-red-600 hover:text-red-700 hover:bg-red-50"
                      >
                        <X className="h-4 w-4" />
                      </Button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </DialogContent>
    </Dialog>
  )
}
