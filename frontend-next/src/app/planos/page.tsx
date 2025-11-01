"use client"

import { useEffect, useState, Suspense } from 'react'
import Link from 'next/link'
import { useSearchParams } from 'next/navigation'
import { motion } from 'framer-motion'
import {
  CreditCard,
  Plus,
  Edit,
  Trash2,
  Check,
  X,
  ArrowLeft,
  Clock,
  Calendar
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
  DialogTrigger,
} from '@/components/ui/dialog'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { toast } from 'sonner'
import { planosAPI } from '@/lib/api'
import type { Plano } from '@/types'

// Force dynamic rendering
export const dynamic = 'force-dynamic'

function PlanosPageContent() {
  const searchParams = useSearchParams()
  const [planos, setPlanos] = useState<Plano[]>([])
  const [loading, setLoading] = useState(true)
  const [isAddModalOpen, setIsAddModalOpen] = useState(false)
  const [selectedPlano, setSelectedPlano] = useState<Plano | null>(null)

  const [formData, setFormData] = useState({
    nome: '',
    descricao: '',
    valor_mensal: 0,
    aulas_por_semana: 2,
    duracao_aula_minutos: 50,
    acesso_livre: false,
    permite_reposicao: true,
    dias_tolerancia: 5
  })

  useEffect(() => {
    loadPlanos()
  }, [])

  useEffect(() => {
    if (searchParams.get('action') === 'new') {
      setIsAddModalOpen(true)
      window.history.replaceState({}, '', '/planos')
    }
  }, [searchParams])

  const loadPlanos = async () => {
    try {
      setLoading(true)
      const data = await planosAPI.list()
      setPlanos(data)
    } catch (error) {
      console.error('Erro ao carregar planos:', error)
      toast.error('Erro ao carregar planos')
      setPlanos([])
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      if (selectedPlano) {
        await planosAPI.update(selectedPlano.id, formData)
        toast.success('Plano atualizado com sucesso!')
      } else {
        await planosAPI.create(formData)
        toast.success('Plano criado com sucesso!')
      }
      loadPlanos()
      setIsAddModalOpen(false)
      resetForm()
    } catch (error) {
      console.error('Erro ao salvar plano:', error)
      toast.error('Erro ao salvar plano')
    }
  }

  const handleDelete = async (id: number) => {
    if (confirm('Tem certeza que deseja excluir este plano?')) {
      try {
        await planosAPI.delete(id)
        toast.success('Plano excluído com sucesso!')
        await loadPlanos()
      } catch (error) {
        console.error('Erro ao excluir plano:', error)
        toast.error('Erro ao excluir plano')
      }
    }
  }

  const resetForm = () => {
    setFormData({
      nome: '',
      descricao: '',
      valor_mensal: 0,
      aulas_por_semana: 2,
      duracao_aula_minutos: 50,
      acesso_livre: false,
      permite_reposicao: true,
      dias_tolerancia: 5
    })
    setSelectedPlano(null)
  }

  return (
    <div className="p-6 space-y-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-start gap-4"
      >
        <Link href="/">
          <Button variant="outline" size="icon" className="shadow-sm">
            <ArrowLeft className="h-4 w-4" />
          </Button>
        </Link>
        <div className="flex-1 flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold flex items-center gap-3">
              <div className="p-2 bg-primary/10 rounded-lg">
                <CreditCard className="h-6 w-6 text-primary" />
              </div>
              Planos
            </h1>
            <p className="text-muted-foreground mt-1">
              Gerencie os planos de assinatura
            </p>
          </div>

          <Dialog open={isAddModalOpen} onOpenChange={setIsAddModalOpen}>
            <DialogTrigger asChild>
              <Button
                size="lg"
                className="shadow-lg"
                onClick={() => {
                  resetForm()
                  setIsAddModalOpen(true)
                }}
              >
                <Plus className="h-5 w-5 mr-2" />
                Novo Plano
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[600px]">
              <DialogHeader>
                <DialogTitle>
                  {selectedPlano ? 'Editar Plano' : 'Criar Novo Plano'}
                </DialogTitle>
                <DialogDescription>
                  Configure os detalhes do plano de assinatura
                </DialogDescription>
              </DialogHeader>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="col-span-2 space-y-2">
                    <Label htmlFor="nome">Nome do Plano *</Label>
                    <Input
                      id="nome"
                      value={formData.nome}
                      onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
                      required
                      placeholder="Ex: Plano Básico"
                    />
                  </div>

                  <div className="col-span-2 space-y-2">
                    <Label htmlFor="descricao">Descrição</Label>
                    <Input
                      id="descricao"
                      value={formData.descricao}
                      onChange={(e) => setFormData({ ...formData, descricao: e.target.value })}
                      placeholder="Descrição do plano"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="valor_mensal">Valor Mensal (R$) *</Label>
                    <Input
                      id="valor_mensal"
                      type="number"
                      step="0.01"
                      value={formData.valor_mensal}
                      onChange={(e) => setFormData({ ...formData, valor_mensal: parseFloat(e.target.value) })}
                      required
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="aulas_por_semana">Aulas por Semana *</Label>
                    <Input
                      id="aulas_por_semana"
                      type="number"
                      min="1"
                      max="7"
                      value={formData.aulas_por_semana}
                      onChange={(e) => setFormData({ ...formData, aulas_por_semana: parseInt(e.target.value) })}
                      required
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="duracao_aula_minutos">Duração da Aula (min)</Label>
                    <Input
                      id="duracao_aula_minutos"
                      type="number"
                      min="30"
                      max="120"
                      value={formData.duracao_aula_minutos}
                      onChange={(e) => setFormData({ ...formData, duracao_aula_minutos: parseInt(e.target.value) })}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="dias_tolerancia">Dias de Tolerância</Label>
                    <Input
                      id="dias_tolerancia"
                      type="number"
                      min="0"
                      max="30"
                      value={formData.dias_tolerancia}
                      onChange={(e) => setFormData({ ...formData, dias_tolerancia: parseInt(e.target.value) })}
                    />
                  </div>

                  <div className="col-span-2 space-y-4">
                    <div className="flex items-center justify-between">
                      <Label htmlFor="acesso_livre">Acesso Livre (Ilimitado)</Label>
                      <Switch
                        id="acesso_livre"
                        checked={formData.acesso_livre}
                        onCheckedChange={(checked) =>
                          setFormData({ ...formData, acesso_livre: checked })
                        }
                      />
                    </div>

                    <div className="flex items-center justify-between">
                      <Label htmlFor="permite_reposicao">Permite Reposição</Label>
                      <Switch
                        id="permite_reposicao"
                        checked={formData.permite_reposicao}
                        onCheckedChange={(checked) =>
                          setFormData({ ...formData, permite_reposicao: checked })
                        }
                      />
                    </div>
                  </div>
                </div>

                <div className="flex justify-end gap-2">
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => {
                      setIsAddModalOpen(false)
                      resetForm()
                    }}
                  >
                    Cancelar
                  </Button>
                  <Button type="submit">
                    {selectedPlano ? 'Atualizar' : 'Criar'} Plano
                  </Button>
                </div>
              </form>
            </DialogContent>
          </Dialog>
        </div>
      </motion.div>

      {loading ? (
        <div className="text-center py-8">Carregando planos...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {planos.map((plano, index) => (
            <motion.div
              key={plano.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <Card className="p-6 glass hover:shadow-lg transition-shadow">
                <div className="space-y-4">
                  <div>
                    <h3 className="text-2xl font-bold">{plano.nome}</h3>
                    {plano.descricao && (
                      <p className="text-sm text-muted-foreground mt-1">
                        {plano.descricao}
                      </p>
                    )}
                  </div>

                  <div className="text-3xl font-bold text-primary">
                    R$ {plano.valor_mensal.toFixed(2)}
                    <span className="text-sm font-normal text-muted-foreground">/mês</span>
                  </div>

                  <div className="space-y-2">
                    <div className="flex items-center gap-2 text-sm">
                      <Calendar className="h-4 w-4 text-muted-foreground" />
                      <span>{plano.aulas_por_semana}x por semana</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm">
                      <Clock className="h-4 w-4 text-muted-foreground" />
                      <span>{plano.duracao_aula_minutos} minutos/aula</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm">
                      {plano.permite_reposicao ? (
                        <Check className="h-4 w-4 text-green-500" />
                      ) : (
                        <X className="h-4 w-4 text-red-500" />
                      )}
                      <span>Permite reposição</span>
                    </div>
                    {plano.acesso_livre && (
                      <div className="flex items-center gap-2 text-sm">
                        <Check className="h-4 w-4 text-green-500" />
                        <span>Acesso livre</span>
                      </div>
                    )}
                  </div>

                  <div className="flex gap-2 pt-4 border-t">
                    <Button
                      variant="outline"
                      size="sm"
                      className="flex-1"
                      onClick={() => {
                        setSelectedPlano(plano)
                        setFormData({
                          nome: plano.nome,
                          descricao: plano.descricao || '',
                          valor_mensal: plano.valor_mensal,
                          aulas_por_semana: plano.aulas_por_semana,
                          duracao_aula_minutos: plano.duracao_aula_minutos,
                          acesso_livre: plano.acesso_livre,
                          permite_reposicao: plano.permite_reposicao,
                          dias_tolerancia: plano.dias_tolerancia
                        })
                        setIsAddModalOpen(true)
                      }}
                    >
                      <Edit className="h-4 w-4 mr-2" />
                      Editar
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleDelete(plano.id)}
                    >
                      <Trash2 className="h-4 w-4 text-destructive" />
                    </Button>
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>
      )}

      {!loading && planos.length === 0 && (
        <Card className="p-12 text-center glass">
          <CreditCard className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
          <h3 className="text-lg font-semibold mb-2">Nenhum plano cadastrado</h3>
          <p className="text-muted-foreground mb-4">
            Crie seu primeiro plano de assinatura
          </p>
          <Button onClick={() => setIsAddModalOpen(true)}>
            <Plus className="h-4 w-4 mr-2" />
            Criar Plano
          </Button>
        </Card>
      )}
    </div>
  )
}

export default function PlanosPage() {
  return (
    <Suspense fallback={<div className="p-6">Carregando...</div>}>
      <PlanosPageContent />
    </Suspense>
  )
}
