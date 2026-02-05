"use client"

import Link from 'next/link'
import { motion } from 'framer-motion'
import {
  Settings,
  ArrowLeft,
  Info
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export default function ConfiguracoesPage() {
  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-start gap-4"
      >
        <Link href="/">
          <Button variant="outline" size="icon" className="shadow-sm" aria-label="Voltar para o início">
            <ArrowLeft className="h-4 w-4" />
          </Button>
        </Link>
        <div className="flex-1">
          <h1 className="text-3xl font-bold flex items-center gap-3">
            <div className="p-2 bg-primary/10 rounded-lg">
              <Settings className="h-6 w-6 text-primary" />
            </div>
            Configurações
          </h1>
          <p className="text-muted-foreground mt-1">
            Configurações do sistema
          </p>
        </div>
      </motion.div>

      {/* Info Card */}
      <Card className="glass">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Info className="h-5 w-5" />
            Em Desenvolvimento
          </CardTitle>
          <CardDescription>
            Esta seção está sendo desenvolvida
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            As configurações do sistema serão adicionadas em breve. Por enquanto, você pode gerenciar:
          </p>
          <ul className="list-disc list-inside mt-4 space-y-2 text-muted-foreground">
            <li>Alunos e matrículas</li>
            <li>Horários e grade de aulas</li>
            <li>Pagamentos e relatórios financeiros</li>
            <li>Usuários do sistema</li>
          </ul>
        </CardContent>
      </Card>
    </div>
  )
}