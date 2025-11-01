"use client"

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import {
  UserCog,
  Plus,
  Shield,
  Mail,
  Phone,
  Edit,
  Trash2,
  Key,
  User,
  CheckCircle,
  Search
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Switch } from '@/components/ui/switch'
import { toast } from 'sonner'

interface Usuario {
  id: number
  nome: string
  email: string
  telefone?: string
  role: string
  ativo: boolean
  created_at: string
  last_login?: string
}

const roleLabels: Record<string, string> = {
  admin: 'Administrador',
  professor: 'Professor',
  atendente: 'Atendente',
  user: 'Usuário'
}

const roleColors: Record<string, string> = {
  admin: 'bg-purple-500',
  professor: 'bg-blue-500',
  atendente: 'bg-green-500',
  user: 'bg-gray-500'
}

export default function UsuariosPage() {
  const [usuarios, setUsuarios] = useState<Usuario[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterRole, setFilterRole] = useState('all')
  const [isAddModalOpen, setIsAddModalOpen] = useState(false)
  const [isPasswordModalOpen, setIsPasswordModalOpen] = useState(false)
  const [selectedUsuario, setSelectedUsuario] = useState<Usuario | null>(null)

  // Form state
  const [formData, setFormData] = useState({
    nome: '',
    email: '',
    telefone: '',
    role: 'user',
    password: '',
    confirmPassword: '',
    ativo: true
  })

  const [passwordData, setPasswordData] = useState({
    newPassword: '',
    confirmPassword: ''
  })

  useEffect(() => {
    loadUsuarios()
  }, [])

  const loadUsuarios = async () => {
    try {
      setLoading(true)
      // Dados mockados
      const mockUsuarios = [
        {
          id: 1,
          nome: 'Admin Sistema',
          email: 'admin@natacao.com',
          telefone: '(11) 99999-9999',
          role: 'admin',
          ativo: true,
          created_at: '2024-01-01',
          last_login: '2024-01-20T10:30:00'
        },
        {
          id: 2,
          nome: 'João Silva',
          email: 'joao@natacao.com',
          telefone: '(11) 98888-8888',
          role: 'professor',
          ativo: true,
          created_at: '2024-01-05',
          last_login: '2024-01-19T14:20:00'
        },
        {
          id: 3,
          nome: 'Maria Santos',
          email: 'maria@natacao.com',
          telefone: '(11) 97777-7777',
          role: 'professor',
          ativo: true,
          created_at: '2024-01-05',
          last_login: '2024-01-20T08:00:00'
        },
        {
          id: 4,
          nome: 'Ana Costa',
          email: 'ana@natacao.com',
          telefone: '(11) 96666-6666',
          role: 'atendente',
          ativo: true,
          created_at: '2024-01-10',
          last_login: '2024-01-20T09:15:00'
        },
        {
          id: 5,
          nome: 'Pedro Oliveira',
          email: 'pedro@natacao.com',
          telefone: '(11) 95555-5555',
          role: 'user',
          ativo: false,
          created_at: '2024-01-15'
        }
      ]
      setUsuarios(mockUsuarios)
    } catch (error) {
      console.error('Erro ao carregar usuários:', error)
      toast.error('Erro ao carregar lista de usuários')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!selectedUsuario && formData.password !== formData.confirmPassword) {
      toast.error('As senhas não coincidem!')
      return
    }

    try {
      if (selectedUsuario) {
        // Atualizar usuário
        const updatedUsers = usuarios.map(u =>
          u.id === selectedUsuario.id
            ? { ...u, ...formData, password: undefined, confirmPassword: undefined }
            : u
        )
        setUsuarios(updatedUsers)
        toast.success('Usuário atualizado com sucesso!')
      } else {
        // Criar novo usuário
        const newUser = {
          id: usuarios.length + 1,
          nome: formData.nome,
          email: formData.email,
          telefone: formData.telefone,
          role: formData.role,
          ativo: formData.ativo,
          created_at: new Date().toISOString().split('T')[0]
        }
        setUsuarios([...usuarios, newUser])
        toast.success('Usuário cadastrado com sucesso!')
      }
      setIsAddModalOpen(false)
      resetForm()
    } catch (error) {
      console.error('Erro ao salvar usuário:', error)
      toast.error('Erro ao salvar usuário')
    }
  }

  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault()

    if (passwordData.newPassword !== passwordData.confirmPassword) {
      toast.error('As senhas não coincidem!')
      return
    }

    if (passwordData.newPassword.length < 6) {
      toast.error('A senha deve ter pelo menos 6 caracteres!')
      return
    }

    try {
      toast.success('Senha alterada com sucesso!')
      setIsPasswordModalOpen(false)
      setPasswordData({ newPassword: '', confirmPassword: '' })
      setSelectedUsuario(null)
    } catch (error) {
      console.error('Erro ao alterar senha:', error)
      toast.error('Erro ao alterar senha')
    }
  }

  const handleDelete = async (id: number) => {
    if (confirm('Tem certeza que deseja excluir este usuário?')) {
      try {
        setUsuarios(usuarios.filter(u => u.id !== id))
        toast.success('Usuário excluído com sucesso!')
      } catch (error) {
        console.error('Erro ao excluir usuário:', error)
        toast.error('Erro ao excluir usuário')
      }
    }
  }

  const handleToggleStatus = async (id: number, ativo: boolean) => {
    try {
      const updatedUsers = usuarios.map(u =>
        u.id === id ? { ...u, ativo } : u
      )
      setUsuarios(updatedUsers)
      toast.success(`Usuário ${ativo ? 'ativado' : 'desativado'} com sucesso!`)
    } catch (error) {
      console.error('Erro ao alterar status:', error)
      toast.error('Erro ao alterar status do usuário')
    }
  }

  const resetForm = () => {
    setFormData({
      nome: '',
      email: '',
      telefone: '',
      role: 'user',
      password: '',
      confirmPassword: '',
      ativo: true
    })
    setSelectedUsuario(null)
  }

  const filteredUsuarios = usuarios.filter(usuario => {
    const matchesSearch = usuario.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         usuario.email.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesRole = filterRole === 'all' || usuario.role === filterRole
    return matchesSearch && matchesRole
  })

  const formatDateTime = (date: string) => {
    return new Date(date).toLocaleString('pt-BR')
  }

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
              <UserCog className="h-6 w-6 text-primary" />
            </div>
            Usuários
          </h1>
          <p className="text-muted-foreground mt-1">
            Gerencie usuários e permissões
          </p>
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
              Novo Usuário
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[600px]">
            <DialogHeader>
              <DialogTitle>
                {selectedUsuario ? 'Editar Usuário' : 'Cadastrar Novo Usuário'}
              </DialogTitle>
              <DialogDescription>
                Preencha os dados do usuário abaixo
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="nome">Nome Completo*</Label>
                  <Input
                    id="nome"
                    value={formData.nome}
                    onChange={(e) => setFormData({...formData, nome: e.target.value})}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="email">Email*</Label>
                  <Input
                    id="email"
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="telefone">Telefone</Label>
                  <Input
                    id="telefone"
                    value={formData.telefone}
                    onChange={(e) => setFormData({...formData, telefone: e.target.value})}
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="role">Perfil*</Label>
                  <Select
                    value={formData.role}
                    onValueChange={(value) => setFormData({...formData, role: value})}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Selecione o perfil" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="admin">Administrador</SelectItem>
                      <SelectItem value="professor">Professor</SelectItem>
                      <SelectItem value="atendente">Atendente</SelectItem>
                      <SelectItem value="user">Usuário</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                {!selectedUsuario && (
                  <>
                    <div className="space-y-2">
                      <Label htmlFor="password">Senha*</Label>
                      <Input
                        id="password"
                        type="password"
                        value={formData.password}
                        onChange={(e) => setFormData({...formData, password: e.target.value})}
                        required={!selectedUsuario}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="confirmPassword">Confirmar Senha*</Label>
                      <Input
                        id="confirmPassword"
                        type="password"
                        value={formData.confirmPassword}
                        onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})}
                        required={!selectedUsuario}
                      />
                    </div>
                  </>
                )}
                <div className="col-span-2 flex items-center space-x-2">
                  <Switch
                    id="ativo"
                    checked={formData.ativo}
                    onCheckedChange={(checked) => setFormData({...formData, ativo: checked})}
                  />
                  <Label htmlFor="ativo">Usuário ativo</Label>
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
                  {selectedUsuario ? 'Salvar Alterações' : 'Cadastrar'}
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>

        {/* Password Modal */}
        <Dialog open={isPasswordModalOpen} onOpenChange={setIsPasswordModalOpen}>
          <DialogContent className="sm:max-w-[400px]">
            <DialogHeader>
              <DialogTitle>Alterar Senha</DialogTitle>
              <DialogDescription>
                Digite a nova senha para o usuário {selectedUsuario?.nome}
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={handlePasswordChange} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="newPassword">Nova Senha*</Label>
                <Input
                  id="newPassword"
                  type="password"
                  value={passwordData.newPassword}
                  onChange={(e) => setPasswordData({...passwordData, newPassword: e.target.value})}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="confirmNewPassword">Confirmar Nova Senha*</Label>
                <Input
                  id="confirmNewPassword"
                  type="password"
                  value={passwordData.confirmPassword}
                  onChange={(e) => setPasswordData({...passwordData, confirmPassword: e.target.value})}
                  required
                />
              </div>
              <div className="flex justify-end gap-3">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => {
                    setIsPasswordModalOpen(false)
                    setPasswordData({ newPassword: '', confirmPassword: '' })
                  }}
                >
                  Cancelar
                </Button>
                <Button type="submit">
                  Alterar Senha
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
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
                <p className="text-sm text-muted-foreground">Total de Usuários</p>
                <p className="text-2xl font-bold">{usuarios.length}</p>
              </div>
              <User className="h-8 w-8 text-primary opacity-50" />
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
                <p className="text-sm text-muted-foreground">Ativos</p>
                <p className="text-2xl font-bold">
                  {usuarios.filter(u => u.ativo).length}
                </p>
              </div>
              <CheckCircle className="h-8 w-8 text-green-500 opacity-50" />
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
                <p className="text-sm text-muted-foreground">Administradores</p>
                <p className="text-2xl font-bold">
                  {usuarios.filter(u => u.role === 'admin').length}
                </p>
              </div>
              <Shield className="h-8 w-8 text-purple-500 opacity-50" />
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
                <p className="text-sm text-muted-foreground">Professores</p>
                <p className="text-2xl font-bold">
                  {usuarios.filter(u => u.role === 'professor').length}
                </p>
              </div>
              <UserCog className="h-8 w-8 text-blue-500 opacity-50" />
            </div>
          </Card>
        </motion.div>
      </div>

      {/* Filters */}
      <Card className="p-6 glass border-0 shadow-medium">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
              <Input
                placeholder="Buscar por nome ou email..."
                className="pl-10"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
          <Select value={filterRole} onValueChange={setFilterRole}>
            <SelectTrigger className="w-full sm:w-[200px]">
              <SelectValue placeholder="Filtrar por perfil" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todos</SelectItem>
              <SelectItem value="admin">Administradores</SelectItem>
              <SelectItem value="professor">Professores</SelectItem>
              <SelectItem value="atendente">Atendentes</SelectItem>
              <SelectItem value="user">Usuários</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </Card>

      {/* Table */}
      <Card className="glass border-0 shadow-medium overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
          </div>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Nome</TableHead>
                <TableHead>Contato</TableHead>
                <TableHead>Perfil</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Último Acesso</TableHead>
                <TableHead className="text-right">Ações</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredUsuarios.map((usuario) => (
                <TableRow key={usuario.id}>
                  <TableCell className="font-medium">{usuario.nome}</TableCell>
                  <TableCell>
                    <div className="space-y-1">
                      <div className="flex items-center gap-1 text-sm">
                        <Mail className="h-3 w-3" />
                        {usuario.email}
                      </div>
                      {usuario.telefone && (
                        <div className="flex items-center gap-1 text-sm text-muted-foreground">
                          <Phone className="h-3 w-3" />
                          {usuario.telefone}
                        </div>
                      )}
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge className={roleColors[usuario.role]}>
                      {roleLabels[usuario.role]}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Switch
                      checked={usuario.ativo}
                      onCheckedChange={(checked) => handleToggleStatus(usuario.id, checked)}
                    />
                  </TableCell>
                  <TableCell>
                    {usuario.last_login ? (
                      <div className="text-sm">
                        <div>{formatDateTime(usuario.last_login)}</div>
                      </div>
                    ) : (
                      <span className="text-sm text-muted-foreground">Nunca acessou</span>
                    )}
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="flex items-center justify-end gap-2">
                      <Button
                        size="icon"
                        variant="ghost"
                        onClick={() => {
                          setSelectedUsuario(usuario)
                          setPasswordData({ newPassword: '', confirmPassword: '' })
                          setIsPasswordModalOpen(true)
                        }}
                      >
                        <Key className="h-4 w-4" />
                      </Button>
                      <Button
                        size="icon"
                        variant="ghost"
                        onClick={() => {
                          setSelectedUsuario(usuario)
                          setFormData({
                            nome: usuario.nome,
                            email: usuario.email,
                            telefone: usuario.telefone || '',
                            role: usuario.role,
                            password: '',
                            confirmPassword: '',
                            ativo: usuario.ativo
                          })
                          setIsAddModalOpen(true)
                        }}
                      >
                        <Edit className="h-4 w-4" />
                      </Button>
                      <Button
                        size="icon"
                        variant="ghost"
                        onClick={() => handleDelete(usuario.id)}
                      >
                        <Trash2 className="h-4 w-4 text-destructive" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </Card>
    </div>
  )
}