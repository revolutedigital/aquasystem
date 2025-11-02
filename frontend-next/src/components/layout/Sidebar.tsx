"use client"

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'
import {
  LayoutDashboard,
  Users,
  Calendar,
  DollarSign,
  UserCog,
  LogOut,
  Menu,
  X,
  Settings,
  Bell,
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Logo } from '@/components/brand/Logo'
import { CommandPalette } from '@/components/command/CommandPalette'
import { useAuthStore } from '@/store/authStore'
import { useState } from 'react'

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard, id: 'dashboard' },
  { name: 'Alunos', href: '/alunos', icon: Users, id: 'students' },
  { name: 'Horários', href: '/horarios', icon: Calendar, id: 'schedules' },
  { name: 'Financeiro', href: '/financeiro', icon: DollarSign, id: 'financial' },
  { name: 'Usuários', href: '/usuarios', icon: UserCog, id: 'users' },
  { name: 'Configurações', href: '/configuracoes', icon: Settings, id: 'settings' },
]

export function Sidebar() {
  const pathname = usePathname()
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const { user, logout } = useAuthStore()

  return (
    <>
      {/* Mobile menu button */}
      <motion.button
        className="lg:hidden fixed top-4 left-4 z-50 p-2.5 rounded-xl glass shadow-medium"
        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
      </motion.button>

      {/* Sidebar */}
      <div
        className={cn(
          "fixed inset-y-0 left-0 z-40 w-72 glass border-r transform transition-all duration-300 ease-in-out",
          isMobileMenuOpen ? "translate-x-0" : "-translate-x-full",
          "lg:translate-x-0 lg:static lg:inset-0"
        )}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center justify-center h-20 px-6 border-b">
            <Logo size="md" animated />
          </div>

          {/* Search */}
          <div className="px-4 py-4">
            <CommandPalette />
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-2 space-y-1 overflow-y-auto">
            {navigation.map((item, index) => {
              const isActive = pathname === item.href
              return (
                <motion.div
                  key={item.name}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                >
                  <Link
                    id={item.id}
                    href={item.href}
                    className={cn(
                      "group flex items-center px-4 py-3 text-sm font-medium rounded-xl transition-all duration-200 relative overflow-hidden",
                      isActive
                        ? "text-white shadow-lg"
                        : "text-foreground hover:bg-accent"
                    )}
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    {isActive && (
                      <motion.div
                        layoutId="activeTab"
                        className="absolute inset-0 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-xl"
                        transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                      />
                    )}
                    <item.icon className={cn(
                      "relative mr-3 h-5 w-5 transition-transform group-hover:scale-110",
                      isActive && "text-white"
                    )} />
                    <span className="relative">{item.name}</span>
                  </Link>
                </motion.div>
              )
            })}
          </nav>

          {/* User section */}
          <div className="p-4 border-t">
            <motion.div
              className="flex items-center mb-4 p-3 rounded-xl bg-gradient-to-r from-cyan-500/10 to-blue-500/10 border border-primary/20"
              whileHover={{ scale: 1.02 }}
              transition={{ type: "spring", stiffness: 400 }}
            >
              <div className="flex-shrink-0">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-cyan-500 to-blue-500 flex items-center justify-center shadow-lg">
                  <span className="text-sm font-bold text-white">
                    {user?.name?.[0]?.toUpperCase() || user?.email?.[0]?.toUpperCase() || 'U'}
                  </span>
                </div>
              </div>
              <div className="ml-3 flex-1 min-w-0">
                <p className="text-sm font-semibold truncate">
                  {user?.name || user?.email}
                </p>
                <p className="text-xs text-muted-foreground capitalize">
                  {user?.role || 'Usuário'}
                </p>
              </div>
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8"
              >
                <Bell className="h-4 w-4" />
              </Button>
            </motion.div>

            <div className="space-y-2">
              <Button
                variant="outline"
                className="w-full justify-start hover:bg-accent"
                onClick={() => {}}
              >
                <Settings className="mr-2 h-4 w-4" />
                Configurações
              </Button>
              <Button
                variant="outline"
                className="w-full justify-start hover:bg-error/10 hover:text-error hover:border-error transition-all"
                onClick={logout}
              >
                <LogOut className="mr-2 h-4 w-4" />
                Sair
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile overlay */}
      {isMobileMenuOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="lg:hidden fixed inset-0 z-30 bg-black/60 backdrop-blur-sm"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}
    </>
  )
}