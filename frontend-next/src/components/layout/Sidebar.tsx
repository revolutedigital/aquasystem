"use client"

import Link from 'next/link'
import { usePathname } from 'next/navigation'
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
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useAuthStore } from '@/store/authStore'
import { useState } from 'react'

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Alunos', href: '/alunos', icon: Users },
  { name: 'Horários', href: '/horarios', icon: Calendar },
  { name: 'Financeiro', href: '/financeiro', icon: DollarSign },
  { name: 'Usuários', href: '/usuarios', icon: UserCog },
]

export function Sidebar() {
  const pathname = usePathname()
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const { user, logout } = useAuthStore()

  return (
    <>
      {/* Mobile menu button */}
      <button
        className="lg:hidden fixed top-4 left-4 z-50 p-2 rounded-md bg-white shadow-md"
        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
      >
        {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Sidebar */}
      <div
        className={cn(
          "fixed inset-y-0 left-0 z-40 w-64 bg-white border-r transform transition-transform duration-300 ease-in-out",
          isMobileMenuOpen ? "translate-x-0" : "-translate-x-full",
          "lg:translate-x-0 lg:static lg:inset-0"
        )}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center justify-center h-16 px-4 border-b">
            <div className="flex items-center space-x-2">
              <span className="text-2xl">🏊‍♂️</span>
              <span className="text-xl font-bold text-swimming-blue">
                AquaSystem
              </span>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-4 space-y-1">
            {navigation.map((item) => {
              const isActive = pathname === item.href
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={cn(
                    "flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors",
                    isActive
                      ? "bg-swimming-blue text-white"
                      : "text-gray-700 hover:bg-gray-100"
                  )}
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  <item.icon className="mr-3 h-5 w-5" />
                  {item.name}
                </Link>
              )
            })}
          </nav>

          {/* User section */}
          <div className="p-4 border-t">
            <div className="flex items-center mb-3">
              <div className="flex-shrink-0">
                <div className="w-10 h-10 rounded-full bg-swimming-blue/10 flex items-center justify-center">
                  <span className="text-sm font-medium text-swimming-blue">
                    {user?.name?.[0]?.toUpperCase() || 'U'}
                  </span>
                </div>
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-900">
                  {user?.name || user?.email}
                </p>
                <p className="text-xs text-gray-500">{user?.role}</p>
              </div>
            </div>

            <Button
              variant="outline"
              className="w-full justify-start"
              onClick={logout}
            >
              <LogOut className="mr-2 h-4 w-4" />
              Sair
            </Button>
          </div>
        </div>
      </div>

      {/* Mobile overlay */}
      {isMobileMenuOpen && (
        <div
          className="lg:hidden fixed inset-0 z-30 bg-black bg-opacity-50"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}
    </>
  )
}