"use client"

import { useState } from 'react'
import Link from 'next/link'
import { motion } from 'framer-motion'
import {
  Settings,
  Bell,
  Shield,
  Globe,
  Database,
  CreditCard,
  Save,
  ArrowLeft,
  Moon,
  Sun,
  Monitor
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Switch } from '@/components/ui/switch'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Separator } from '@/components/ui/separator'
import { toast } from 'sonner'

export default function ConfiguracoesPage() {
  const [loading, setLoading] = useState(false)
  const [theme, setTheme] = useState('system')

  // Configurações gerais
  const [config, setConfig] = useState({
    nomeEscola: 'AquaFlow Pro',
    endereco: 'Rua das Águas, 123',
    telefone: '(11) 98765-4321',
    email: 'contato@aquaflow.com.br',
    cnpj: '12.345.678/0001-90',

    // Notificações
    notificacoesEmail: true,
    notificacoesWhatsapp: false,
    lembretesPagamento: true,
    lembretesAulas: true,
    relatoriosMensais: false,

    // Financeiro
    diaFechamento: 25,
    taxaJuros: 2,
    diasTolerancia: 5,
    valorMulta: 10,

    // Aulas
    duracaoAula: 50,
    intervaloAulas: 10,
    maximoAlunos: 8,
    idadeMinima: 4,

    // Sistema
    backupAutomatico: true,
    frequenciaBackup: 'diario',
    limparLogsAntigos: true,
    diasManterLogs: 30
  })

  const handleSave = async (section: string) => {
    setLoading(true)
    try {
      // Simulação de salvamento
      await new Promise(resolve => setTimeout(resolve, 1000))
      toast.success(`${section} salvas com sucesso!`)
    } catch {
      toast.error('Erro ao salvar configurações')
    } finally {
      setLoading(false)
    }
  }

  const ThemeToggle = () => (
    <div className="flex items-center gap-4 p-4 glass rounded-xl">
      <button
        onClick={() => setTheme('light')}
        className={`p-3 rounded-lg transition-all ${
          theme === 'light' ? 'bg-primary text-primary-foreground' : 'hover:bg-accent'
        }`}
      >
        <Sun className="h-5 w-5" />
      </button>
      <button
        onClick={() => setTheme('dark')}
        className={`p-3 rounded-lg transition-all ${
          theme === 'dark' ? 'bg-primary text-primary-foreground' : 'hover:bg-accent'
        }`}
      >
        <Moon className="h-5 w-5" />
      </button>
      <button
        onClick={() => setTheme('system')}
        className={`p-3 rounded-lg transition-all ${
          theme === 'system' ? 'bg-primary text-primary-foreground' : 'hover:bg-accent'
        }`}
      >
        <Monitor className="h-5 w-5" />
      </button>
    </div>
  )

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
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
        <div className="flex-1">
          <h1 className="text-3xl font-bold flex items-center gap-3">
            <div className="p-2 bg-primary/10 rounded-lg">
              <Settings className="h-6 w-6 text-primary" />
            </div>
            Configurações
          </h1>
          <p className="text-muted-foreground mt-1">
            Gerencie as configurações do sistema
          </p>
        </div>
      </motion.div>

      <Tabs defaultValue="geral" className="space-y-4">
        <TabsList className="grid grid-cols-5 w-full glass">
          <TabsTrigger value="geral" className="flex items-center gap-2">
            <Settings className="h-4 w-4" />
            <span className="hidden sm:inline">Geral</span>
          </TabsTrigger>
          <TabsTrigger value="notificacoes" className="flex items-center gap-2">
            <Bell className="h-4 w-4" />
            <span className="hidden sm:inline">Notificações</span>
          </TabsTrigger>
          <TabsTrigger value="financeiro" className="flex items-center gap-2">
            <CreditCard className="h-4 w-4" />
            <span className="hidden sm:inline">Financeiro</span>
          </TabsTrigger>
          <TabsTrigger value="aulas" className="flex items-center gap-2">
            <Globe className="h-4 w-4" />
            <span className="hidden sm:inline">Aulas</span>
          </TabsTrigger>
          <TabsTrigger value="sistema" className="flex items-center gap-2">
            <Database className="h-4 w-4" />
            <span className="hidden sm:inline">Sistema</span>
          </TabsTrigger>
        </TabsList>

        {/* Configurações Gerais */}
        <TabsContent value="geral" className="space-y-4">
          <Card className="glass">
            <CardHeader>
              <CardTitle>Informações da Escola</CardTitle>
              <CardDescription>
                Dados básicos da instituição
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="nomeEscola">Nome da Escola</Label>
                  <Input
                    id="nomeEscola"
                    value={config.nomeEscola}
                    onChange={(e) => setConfig({ ...config, nomeEscola: e.target.value })}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="cnpj">CNPJ</Label>
                  <Input
                    id="cnpj"
                    value={config.cnpj}
                    onChange={(e) => setConfig({ ...config, cnpj: e.target.value })}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="telefone">Telefone</Label>
                  <Input
                    id="telefone"
                    value={config.telefone}
                    onChange={(e) => setConfig({ ...config, telefone: e.target.value })}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    value={config.email}
                    onChange={(e) => setConfig({ ...config, email: e.target.value })}
                  />
                </div>
                <div className="col-span-2 space-y-2">
                  <Label htmlFor="endereco">Endereço</Label>
                  <Input
                    id="endereco"
                    value={config.endereco}
                    onChange={(e) => setConfig({ ...config, endereco: e.target.value })}
                  />
                </div>
              </div>

              <Separator className="my-6" />

              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Tema da Interface</h3>
                <ThemeToggle />
              </div>

              <div className="flex justify-end">
                <Button
                  onClick={() => handleSave('Configurações gerais')}
                  disabled={loading}
                  className="shadow-lg"
                >
                  <Save className="h-4 w-4 mr-2" />
                  Salvar Alterações
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Notificações */}
        <TabsContent value="notificacoes" className="space-y-4">
          <Card className="glass">
            <CardHeader>
              <CardTitle>Preferências de Notificação</CardTitle>
              <CardDescription>
                Configure como e quando receber notificações
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label htmlFor="notificacoesEmail">Notificações por Email</Label>
                    <p className="text-sm text-muted-foreground">
                      Receber atualizações importantes por email
                    </p>
                  </div>
                  <Switch
                    id="notificacoesEmail"
                    checked={config.notificacoesEmail}
                    onCheckedChange={(checked) =>
                      setConfig({ ...config, notificacoesEmail: checked })
                    }
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label htmlFor="notificacoesWhatsapp">Notificações por WhatsApp</Label>
                    <p className="text-sm text-muted-foreground">
                      Receber mensagens via WhatsApp Business
                    </p>
                  </div>
                  <Switch
                    id="notificacoesWhatsapp"
                    checked={config.notificacoesWhatsapp}
                    onCheckedChange={(checked) =>
                      setConfig({ ...config, notificacoesWhatsapp: checked })
                    }
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label htmlFor="lembretesPagamento">Lembretes de Pagamento</Label>
                    <p className="text-sm text-muted-foreground">
                      Notificar sobre pagamentos pendentes
                    </p>
                  </div>
                  <Switch
                    id="lembretesPagamento"
                    checked={config.lembretesPagamento}
                    onCheckedChange={(checked) =>
                      setConfig({ ...config, lembretesPagamento: checked })
                    }
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label htmlFor="lembretesAulas">Lembretes de Aulas</Label>
                    <p className="text-sm text-muted-foreground">
                      Avisos sobre horários e mudanças de aulas
                    </p>
                  </div>
                  <Switch
                    id="lembretesAulas"
                    checked={config.lembretesAulas}
                    onCheckedChange={(checked) =>
                      setConfig({ ...config, lembretesAulas: checked })
                    }
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label htmlFor="relatoriosMensais">Relatórios Mensais</Label>
                    <p className="text-sm text-muted-foreground">
                      Receber relatórios de desempenho mensal
                    </p>
                  </div>
                  <Switch
                    id="relatoriosMensais"
                    checked={config.relatoriosMensais}
                    onCheckedChange={(checked) =>
                      setConfig({ ...config, relatoriosMensais: checked })
                    }
                  />
                </div>
              </div>

              <div className="flex justify-end">
                <Button
                  onClick={() => handleSave('Notificações')}
                  disabled={loading}
                  className="shadow-lg"
                >
                  <Save className="h-4 w-4 mr-2" />
                  Salvar Preferências
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Financeiro */}
        <TabsContent value="financeiro" className="space-y-4">
          <Card className="glass">
            <CardHeader>
              <CardTitle>Configurações Financeiras</CardTitle>
              <CardDescription>
                Parâmetros para gestão financeira
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="diaFechamento">Dia de Fechamento</Label>
                  <Select
                    value={config.diaFechamento.toString()}
                    onValueChange={(value) =>
                      setConfig({ ...config, diaFechamento: parseInt(value) })
                    }
                  >
                    <SelectTrigger id="diaFechamento">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {Array.from({ length: 28 }, (_, i) => i + 1).map(day => (
                        <SelectItem key={day} value={day.toString()}>
                          Dia {day}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="diasTolerancia">Dias de Tolerância</Label>
                  <Input
                    id="diasTolerancia"
                    type="number"
                    value={config.diasTolerancia}
                    onChange={(e) =>
                      setConfig({ ...config, diasTolerancia: parseInt(e.target.value) || 0 })
                    }
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="taxaJuros">Taxa de Juros (%)</Label>
                  <Input
                    id="taxaJuros"
                    type="number"
                    step="0.1"
                    value={config.taxaJuros}
                    onChange={(e) =>
                      setConfig({ ...config, taxaJuros: parseFloat(e.target.value) || 0 })
                    }
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="valorMulta">Valor da Multa (R$)</Label>
                  <Input
                    id="valorMulta"
                    type="number"
                    step="0.01"
                    value={config.valorMulta}
                    onChange={(e) =>
                      setConfig({ ...config, valorMulta: parseFloat(e.target.value) || 0 })
                    }
                  />
                </div>
              </div>

              <div className="flex justify-end">
                <Button
                  onClick={() => handleSave('Configurações financeiras')}
                  disabled={loading}
                  className="shadow-lg"
                >
                  <Save className="h-4 w-4 mr-2" />
                  Salvar Configurações
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Aulas */}
        <TabsContent value="aulas" className="space-y-4">
          <Card className="glass">
            <CardHeader>
              <CardTitle>Configurações de Aulas</CardTitle>
              <CardDescription>
                Parâmetros padrão para aulas e turmas
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="duracaoAula">Duração da Aula (minutos)</Label>
                  <Input
                    id="duracaoAula"
                    type="number"
                    value={config.duracaoAula}
                    onChange={(e) =>
                      setConfig({ ...config, duracaoAula: parseInt(e.target.value) || 50 })
                    }
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="intervaloAulas">Intervalo entre Aulas (minutos)</Label>
                  <Input
                    id="intervaloAulas"
                    type="number"
                    value={config.intervaloAulas}
                    onChange={(e) =>
                      setConfig({ ...config, intervaloAulas: parseInt(e.target.value) || 10 })
                    }
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="maximoAlunos">Máximo de Alunos por Turma</Label>
                  <Input
                    id="maximoAlunos"
                    type="number"
                    value={config.maximoAlunos}
                    onChange={(e) =>
                      setConfig({ ...config, maximoAlunos: parseInt(e.target.value) || 8 })
                    }
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="idadeMinima">Idade Mínima (anos)</Label>
                  <Input
                    id="idadeMinima"
                    type="number"
                    value={config.idadeMinima}
                    onChange={(e) =>
                      setConfig({ ...config, idadeMinima: parseInt(e.target.value) || 4 })
                    }
                  />
                </div>
              </div>

              <div className="flex justify-end">
                <Button
                  onClick={() => handleSave('Configurações de aulas')}
                  disabled={loading}
                  className="shadow-lg"
                >
                  <Save className="h-4 w-4 mr-2" />
                  Salvar Configurações
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Sistema */}
        <TabsContent value="sistema" className="space-y-4">
          <Card className="glass">
            <CardHeader>
              <CardTitle>Configurações do Sistema</CardTitle>
              <CardDescription>
                Backup, segurança e manutenção
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label htmlFor="backupAutomatico">Backup Automático</Label>
                    <p className="text-sm text-muted-foreground">
                      Realizar backup dos dados automaticamente
                    </p>
                  </div>
                  <Switch
                    id="backupAutomatico"
                    checked={config.backupAutomatico}
                    onCheckedChange={(checked) =>
                      setConfig({ ...config, backupAutomatico: checked })
                    }
                  />
                </div>

                {config.backupAutomatico && (
                  <div className="space-y-2 ml-4">
                    <Label htmlFor="frequenciaBackup">Frequência de Backup</Label>
                    <Select
                      value={config.frequenciaBackup}
                      onValueChange={(value) =>
                        setConfig({ ...config, frequenciaBackup: value })
                      }
                    >
                      <SelectTrigger id="frequenciaBackup">
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="diario">Diário</SelectItem>
                        <SelectItem value="semanal">Semanal</SelectItem>
                        <SelectItem value="mensal">Mensal</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                )}

                <div className="flex items-center justify-between">
                  <div className="space-y-0.5">
                    <Label htmlFor="limparLogsAntigos">Limpar Logs Antigos</Label>
                    <p className="text-sm text-muted-foreground">
                      Remover logs antigos automaticamente
                    </p>
                  </div>
                  <Switch
                    id="limparLogsAntigos"
                    checked={config.limparLogsAntigos}
                    onCheckedChange={(checked) =>
                      setConfig({ ...config, limparLogsAntigos: checked })
                    }
                  />
                </div>

                {config.limparLogsAntigos && (
                  <div className="space-y-2 ml-4">
                    <Label htmlFor="diasManterLogs">Dias para Manter Logs</Label>
                    <Input
                      id="diasManterLogs"
                      type="number"
                      value={config.diasManterLogs}
                      onChange={(e) =>
                        setConfig({ ...config, diasManterLogs: parseInt(e.target.value) || 30 })
                      }
                    />
                  </div>
                )}
              </div>

              <Separator />

              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Ações do Sistema</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Button variant="outline" className="justify-start">
                    <Database className="h-4 w-4 mr-2" />
                    Fazer Backup Manual
                  </Button>
                  <Button variant="outline" className="justify-start">
                    <Shield className="h-4 w-4 mr-2" />
                    Verificar Integridade
                  </Button>
                </div>
              </div>

              <div className="flex justify-end">
                <Button
                  onClick={() => handleSave('Configurações do sistema')}
                  disabled={loading}
                  className="shadow-lg"
                >
                  <Save className="h-4 w-4 mr-2" />
                  Salvar Configurações
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}