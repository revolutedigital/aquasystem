"use client"

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import {
  FileText,
  Calendar,
  MessageCircle,
  ChevronRight
} from 'lucide-react'
import { alunosAPI } from '@/lib/api'
import type { Aluno } from '@/types'
import { formatCurrency } from '@/lib/utils'
import { toast } from 'sonner'
import Link from 'next/link'

export function ContratosExpirando() {
  const [contratos, setContratos] = useState<Aluno[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadContratos()
  }, [])

  const loadContratos = async () => {
    try {
      setLoading(true)
      const data = await alunosAPI.getContratosExpirando(30) // Próximos 30 dias
      setContratos(data)
    } catch {
      // Silently fail - contratos list will remain empty
    } finally {
      setLoading(false)
    }
  }

  const enviarPropostaRenovacao = (aluno: Aluno) => {
    if (!aluno.telefone_whatsapp) {
      toast.error('Aluno não possui WhatsApp cadastrado')
      return
    }

    const phone = aluno.telefone_whatsapp.replace(/\D/g, '')
    const formattedPhone = phone.startsWith('55') ? phone : `55${phone}`

    const dataFim = aluno.data_fim_contrato ? new Date(aluno.data_fim_contrato).toLocaleDateString('pt-BR') : 'em breve'

    const message = `Olá ${aluno.nome_completo.split(' ')[0]}! 👋

Seu contrato de ${aluno.tipo_aula === 'natacao' ? 'natação' : 'hidroginástica'} vence em ${dataFim}.

🎯 Queremos continuar com você na nossa equipe!

Preparamos uma proposta especial de renovação:
✅ Manutenção do valor atual: ${formatCurrency(Number(aluno.valor_mensalidade) || 0)}
✅ Flexibilidade de horários
✅ Acompanhamento personalizado

📲 Vamos conversar sobre a renovação? Estamos à disposição!`

    const encodedMessage = encodeURIComponent(message)
    const whatsappURL = `https://wa.me/${formattedPhone}?text=${encodedMessage}`
    window.open(whatsappURL, '_blank')

    toast.success('WhatsApp aberto para envio da proposta!')
  }

  const getDiasRestantes = (dataFim?: string) => {
    if (!dataFim) return null

    const hoje = new Date()
    const fim = new Date(dataFim)
    const diffTime = fim.getTime() - hoje.getTime()
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

    return diffDays
  }

  const getBadgeColor = (dias: number | null) => {
    if (dias === null) return 'secondary'
    if (dias <= 7) return 'destructive'
    if (dias <= 15) return 'warning'
    return 'default'
  }

  if (loading) {
    return (
      <Card className="hover:shadow-lg transition-shadow">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="h-5 w-5" />
            Contratos Expirando
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <FileText className="h-5 w-5 text-orange-500" />
            Contratos Expirando
          </div>
          {contratos.length > 0 && (
            <Badge variant="outline" className="ml-auto">
              {contratos.length} {contratos.length === 1 ? 'contrato' : 'contratos'}
            </Badge>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent>
        {contratos.length === 0 ? (
          <div className="text-center py-8">
            <div className="mx-auto w-12 h-12 rounded-full bg-green-500/10 flex items-center justify-center mb-3">
              <Calendar className="h-6 w-6 text-green-600" />
            </div>
            <p className="text-sm text-muted-foreground">
              Nenhum contrato expirando nos próximos 30 dias
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {contratos.slice(0, 5).map((contrato, i) => {
              const diasRestantes = getDiasRestantes(contrato.data_fim_contrato)

              return (
                <motion.div
                  key={contrato.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: i * 0.1 }}
                  className="flex items-center justify-between p-4 rounded-xl border hover:bg-accent/50 transition-all group"
                >
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <p className="font-semibold truncate">{contrato.nome_completo}</p>
                      <Badge
                        variant={getBadgeColor(diasRestantes) as "default" | "secondary" | "destructive" | "outline"}
                        className="shrink-0"
                      >
                        {diasRestantes !== null ? (
                          diasRestantes <= 0 ? 'Vencido' : `${diasRestantes}d`
                        ) : 'Sem data'}
                      </Badge>
                    </div>
                    <div className="flex items-center gap-3 text-sm text-muted-foreground">
                      <span className="flex items-center gap-1">
                        <Calendar className="h-3 w-3" />
                        {contrato.data_fim_contrato ? new Date(contrato.data_fim_contrato).toLocaleDateString('pt-BR') : 'Sem data'}
                      </span>
                      <span className="capitalize">{contrato.tipo_aula}</span>
                      <span>{formatCurrency(Number(contrato.valor_mensalidade) || 0)}</span>
                    </div>
                  </div>
                  <Button
                    size="sm"
                    variant="outline"
                    className="shrink-0 ml-2"
                    onClick={() => enviarPropostaRenovacao(contrato)}
                  >
                    <MessageCircle className="h-4 w-4 mr-1" />
                    Renovar
                  </Button>
                </motion.div>
              )
            })}

            {contratos.length > 5 && (
              <Link href="/alunos?filter=expiring">
                <Button variant="ghost" className="w-full justify-between group">
                  <span>Ver todos os {contratos.length} contratos</span>
                  <ChevronRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
                </Button>
              </Link>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
