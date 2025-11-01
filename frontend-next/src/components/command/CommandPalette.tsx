"use client"

import { useEffect, useState, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { Command } from 'cmdk'
import { motion, AnimatePresence } from 'framer-motion'
import {
  LayoutDashboard,
  Users,
  Calendar,
  DollarSign,
  UserCog,
  Search,
  Plus,
  Settings,
  CreditCard,
  LogOut,
} from 'lucide-react'

interface CommandItem {
  id: string
  label: string
  icon: React.ReactNode
  action: () => void
  keywords?: string[]
  group?: string
}

export function CommandPalette() {
  const [open, setOpen] = useState(false)
  const [search, setSearch] = useState('')
  const router = useRouter()

  const commands: CommandItem[] = [
    // Navegação
    {
      id: 'dashboard',
      label: 'Ir para Dashboard',
      icon: <LayoutDashboard className="h-4 w-4" />,
      action: () => router.push('/'),
      keywords: ['home', 'inicio', 'painel'],
      group: 'Navegação',
    },
    {
      id: 'students',
      label: 'Ver Alunos',
      icon: <Users className="h-4 w-4" />,
      action: () => router.push('/alunos'),
      keywords: ['students', 'alunos', 'estudantes'],
      group: 'Navegação',
    },
    {
      id: 'schedules',
      label: 'Grade de Horários',
      icon: <Calendar className="h-4 w-4" />,
      action: () => router.push('/horarios'),
      keywords: ['schedule', 'aulas', 'turmas', 'agenda'],
      group: 'Navegação',
    },
    {
      id: 'financial',
      label: 'Financeiro',
      icon: <DollarSign className="h-4 w-4" />,
      action: () => router.push('/financeiro'),
      keywords: ['finance', 'pagamentos', 'receita', 'dinheiro'],
      group: 'Navegação',
    },
    {
      id: 'users',
      label: 'Usuários',
      icon: <UserCog className="h-4 w-4" />,
      action: () => router.push('/usuarios'),
      keywords: ['users', 'admin', 'gestão'],
      group: 'Navegação',
    },
    {
      id: 'planos',
      label: 'Planos',
      icon: <CreditCard className="h-4 w-4" />,
      action: () => router.push('/planos'),
      keywords: ['planos', 'assinatura', 'mensalidade', 'pacotes'],
      group: 'Navegação',
    },
    // Ações
    {
      id: 'new-student',
      label: 'Novo Aluno',
      icon: <Plus className="h-4 w-4" />,
      action: () => router.push('/alunos?action=new'),
      keywords: ['add', 'adicionar', 'criar', 'cadastrar'],
      group: 'Ações',
    },
    {
      id: 'new-class',
      label: 'Nova Turma',
      icon: <Plus className="h-4 w-4" />,
      action: () => router.push('/horarios?action=new'),
      keywords: ['add', 'adicionar', 'criar', 'turma'],
      group: 'Ações',
    },
    {
      id: 'new-payment',
      label: 'Registrar Pagamento',
      icon: <Plus className="h-4 w-4" />,
      action: () => router.push('/financeiro?action=new'),
      keywords: ['add', 'adicionar', 'pagamento', 'receber'],
      group: 'Ações',
    },
    // Sistema
    {
      id: 'settings',
      label: 'Configurações',
      icon: <Settings className="h-4 w-4" />,
      action: () => router.push('/configuracoes'),
      keywords: ['settings', 'config', 'preferencias'],
      group: 'Sistema',
    },
    {
      id: 'logout',
      label: 'Sair',
      icon: <LogOut className="h-4 w-4" />,
      action: () => {
        // Implement logout
        router.push('/login')
      },
      keywords: ['logout', 'sair', 'desconectar'],
      group: 'Sistema',
    },
  ]

  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
      e.preventDefault()
      setOpen((open) => !open)
    }
  }, [])

  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [handleKeyDown])

  const handleSelect = (action: () => void) => {
    action()
    setOpen(false)
    setSearch('')
  }

  const groupedCommands = commands.reduce((acc, command) => {
    const group = command.group || 'Outros'
    if (!acc[group]) {
      acc[group] = []
    }
    acc[group].push(command)
    return acc
  }, {} as Record<string, CommandItem[]>)

  return (
    <>
      {/* Trigger Button */}
      <button
        onClick={() => setOpen(true)}
        className="hidden lg:flex items-center gap-2 px-3 py-2 text-sm text-muted-foreground border rounded-lg hover:bg-accent transition-colors w-full max-w-sm"
      >
        <Search className="h-4 w-4" />
        <span className="flex-1 text-left">Buscar...</span>
        <kbd className="pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground">
          <span className="text-xs">⌘</span>K
        </kbd>
      </button>

      {/* Mobile trigger */}
      <button
        onClick={() => setOpen(true)}
        className="lg:hidden p-2 hover:bg-accent rounded-lg transition-colors"
      >
        <Search className="h-5 w-5" />
      </button>

      <AnimatePresence>
        {open && (
          <>
            {/* Overlay */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-black/50 z-50 backdrop-blur-sm"
              onClick={() => setOpen(false)}
            />

            {/* Command Dialog */}
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: -20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: -20 }}
              transition={{ duration: 0.2 }}
              className="fixed top-[20%] left-1/2 -translate-x-1/2 w-full max-w-2xl z-50 px-4"
            >
              <Command className="glass rounded-2xl border border-border shadow-strong overflow-hidden bg-background/95">
                <div className="flex items-center border-b border-border px-4">
                  <Search className="h-4 w-4 text-muted-foreground shrink-0" />
                  <Command.Input
                    value={search}
                    onValueChange={setSearch}
                    placeholder="Buscar comando ou página..."
                    className="flex-1 bg-transparent border-0 py-4 px-4 text-sm outline-none placeholder:text-muted-foreground"
                  />
                  <kbd className="hidden sm:inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground">
                    ESC
                  </kbd>
                </div>

                <Command.List className="max-h-[400px] overflow-y-auto p-2">
                  <Command.Empty className="py-6 text-center text-sm text-muted-foreground">
                    Nenhum resultado encontrado.
                  </Command.Empty>

                  {Object.entries(groupedCommands).map(([group, items]) => (
                    <Command.Group
                      key={group}
                      heading={group}
                      className="px-2 py-1.5 text-xs font-semibold text-muted-foreground"
                    >
                      {items.map((command) => (
                        <Command.Item
                          key={command.id}
                          value={`${command.label} ${command.keywords?.join(' ')}`}
                          onSelect={() => handleSelect(command.action)}
                          className="flex items-center gap-3 px-3 py-2.5 rounded-lg cursor-pointer hover:bg-accent transition-colors data-[selected=true]:bg-accent group"
                        >
                          <div className="flex items-center justify-center h-8 w-8 rounded-md bg-primary/10 text-primary group-data-[selected=true]:bg-primary/20">
                            {command.icon}
                          </div>
                          <span className="flex-1 text-sm">{command.label}</span>
                          {command.id === 'new-student' && (
                            <kbd className="hidden sm:inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1 font-mono text-[10px] font-medium text-muted-foreground">
                              ⌘N
                            </kbd>
                          )}
                        </Command.Item>
                      ))}
                    </Command.Group>
                  ))}
                </Command.List>

                <div className="border-t border-border p-3 text-xs text-muted-foreground flex items-center justify-between">
                  <div className="flex gap-4">
                    <span className="flex items-center gap-1">
                      <kbd className="px-1.5 py-0.5 bg-muted rounded text-[10px]">↑</kbd>
                      <kbd className="px-1.5 py-0.5 bg-muted rounded text-[10px]">↓</kbd>
                      navegar
                    </span>
                    <span className="flex items-center gap-1">
                      <kbd className="px-1.5 py-0.5 bg-muted rounded text-[10px]">↵</kbd>
                      selecionar
                    </span>
                  </div>
                  <span>AquaFlow Pro v1.0</span>
                </div>
              </Command>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  )
}