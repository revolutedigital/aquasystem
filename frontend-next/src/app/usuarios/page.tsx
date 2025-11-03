"use client"

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { motion } from 'framer-motion'
import {
  UserCog,
  Plus,
  Shield,
  Mail,
  Edit,
  Trash2,
  Key,
  User,
  CheckCircle,
  Search,
  ArrowLeft,
  Check,
  X
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
import { usersAPI, type Usuario, type UsuarioCreate, type UsuarioUpdate } from '@/lib/api-users'

const roleLabels: Record<string, string> = {
  admin: 'Administrador',
  recepcionista: 'Recepcionista',
  aluno: 'Aluno'
}

const roleColors: Record<string, string> = {
  admin: 'bg-purple-500',
  recepcionista: 'bg-blue-500',
  aluno: 'bg-green-500'
}

// Password validation utilities
interface PasswordValidation {
  isValid: boolean
  errors: string[]
  strength: 'weak' | 'medium' | 'strong'
}

function validatePasswordStrength(password: string): PasswordValidation {
  const errors: string[] = []

  if (password.length < 12) {
    errors.push("Mínimo 12 caracteres")
  }
  if (!/[A-Z]/.test(password)) {
    errors.push("Pelo menos 1 letra maiúscula")
  }
  if (!/[a-z]/.test(password)) {
    errors.push("Pelo menos 1 letra minúscula")
  }
  if (!/\d/.test(password)) {
    errors.push("Pelo menos 1 número")
  }
  if (!/[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/~`]/.test(password)) {
    errors.push("Pelo menos 1 caractere especial")
  }

  const isValid = errors.length === 0
  let strength: 'weak' | 'medium' | 'strong' = 'weak'

  if (isValid) {
    strength = 'strong'
  } else if (errors.length <= 2 && password.length >= 8) {
    strength = 'medium'
  }

  return { isValid, errors, strength }
}

// Password Strength Indicator Component
function PasswordStrengthIndicator({ password }: { password: string }) {
  if (!password) return null

  const validation = validatePasswordStrength(password)
  const requirements = [
    { text: "Mínimo 12 caracteres", valid: password.length >= 12 },
    { text: "1 letra maiúscula", valid: /[A-Z]/.test(password) },
    { text: "1 letra minúscula", valid: /[a-z]/.test(password) },
    { text: "1 número", valid: /\d/.test(password) },
    { text: "1 caractere especial", valid: /[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/~`]/.test(password) }
  ]

  const strengthColors = {
    weak: 'bg-red-500',
    medium: 'bg-yellow-500',
    strong: 'bg-green-500'
  }

  const strengthLabels = {
    weak: 'Fraca',
    medium: 'Média',
    strong: 'Forte'
  }

  return (
    <div className="space-y-3 mt-2 p-3 bg-muted/30 rounded-lg border">
      <div className="flex items-center gap-2">
        <div className="flex-1 h-2 bg-muted rounded-full overflow-hidden">
          <div
            className={`h-full transition-all ${strengthColors[validation.strength]}`}
            style={{
              width: validation.strength === 'strong' ? '100%' : validation.strength === 'medium' ? '60%' : '30%'
            }}
          />
        </div>
        <span className={`text-sm font-medium ${
          validation.strength === 'strong' ? 'text-green-600' :
          validation.strength === 'medium' ? 'text-yellow-600' :
          'text-red-600'
        }`}>
          {strengthLabels[validation.strength]}
        </span>
      </div>
      <div className="space-y-1">
        {requirements.map((req, index) => (
          <div key={index} className="flex items-center gap-2 text-xs">
            {req.valid ? (
              <Check className="h-3 w-3 text-green-600" />
            ) : (
              <X className="h-3 w-3 text-muted-foreground" />
            )}
            <span className={req.valid ? 'text-green-600' : 'text-muted-foreground'}>
              {req.text}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
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
    username: '',
    full_name: '',
    email: '',
    role: 'recepcionista',
    password: '',
    confirmPassword: ''
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
      const data = await usersAPI.list()
      setUsuarios(data)
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

    // Validate password strength for new users
    if (!selectedUsuario) {
      const validation = validatePasswordStrength(formData.password)
      if (!validation.isValid) {
        toast.error(`Senha fraca: ${validation.errors.join('; ')}`)
        return
      }
    }

    try {
      if (selectedUsuario) {
        // Atualizar usuário
        const updateData: UsuarioUpdate = {
          username: formData.username,
          full_name: formData.full_name,
          email: formData.email,
          role: formData.role
        }
        await usersAPI.update(selectedUsuario.id, updateData)
        toast.success('Usuário atualizado com sucesso!')
      } else {
        // Criar novo usuário
        const createData: UsuarioCreate = {
          username: formData.username,
          full_name: formData.full_name,
          email: formData.email,
          password: formData.password,
          role: formData.role
        }
        await usersAPI.create(createData)
        toast.success('Usuário cadastrado com sucesso!')
      }
      loadUsuarios() // Recarregar lista
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

    // Validate password strength
    const validation = validatePasswordStrength(passwordData.newPassword)
    if (!validation.isValid) {
      toast.error(`Senha fraca: ${validation.errors.join('; ')}`)
      return
    }

    try {
      if (selectedUsuario) {
        await usersAPI.changePassword(selectedUsuario.id, passwordData.newPassword)
        toast.success('Senha alterada com sucesso!')
        setIsPasswordModalOpen(false)
        setPasswordData({ newPassword: '', confirmPassword: '' })
        setSelectedUsuario(null)
      }
    } catch (error) {
      console.error('Erro ao alterar senha:', error)
      toast.error('Erro ao alterar senha')
    }
  }

  const handleDelete = async (id: number) => {
    if (confirm('Tem certeza que deseja excluir este usuário?')) {
      try {
        await usersAPI.delete(id)
        toast.success('Usuário excluído com sucesso!')
        loadUsuarios() // Recarregar lista
      } catch (error) {
        console.error('Erro ao excluir usuário:', error)
        toast.error('Erro ao excluir usuário')
      }
    }
  }

  const handleToggleStatus = async (id: number, is_active: boolean) => {
    try {
      const usuario = usuarios.find(u => u.id === id)
      if (usuario) {
        await usersAPI.update(id, { is_active })
        toast.success(`Usuário ${is_active ? 'ativado' : 'desativado'} com sucesso!`)
        loadUsuarios() // Recarregar lista
      }
    } catch (error) {
      console.error('Erro ao alterar status:', error)
      toast.error('Erro ao alterar status do usuário')
    }
  }

  const resetForm = () => {
    setFormData({
      username: '',
      full_name: '',
      email: '',
      role: 'recepcionista',
      password: '',
      confirmPassword: ''
    })
    setSelectedUsuario(null)
  }

  const filteredUsuarios = usuarios.filter(usuario => {
    const matchesSearch = usuario.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         usuario.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         usuario.username.toLowerCase().includes(searchTerm.toLowerCase())
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
        <div className="flex items-start gap-4">
          <Link href="/">
            <Button variant="outline" size="icon" className="shadow-sm">
              <ArrowLeft className="h-4 w-4" />
            </Button>
          </Link>
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
                  <Label htmlFor="full_name">Nome Completo*</Label>
                  <Input
                    id="full_name"
                    value={formData.full_name}
                    onChange={(e) => setFormData({...formData, full_name: e.target.value})}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="username">Username*</Label>
                  <Input
                    id="username"
                    value={formData.username}
                    onChange={(e) => setFormData({...formData, username: e.target.value})}
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
                      <SelectItem value="recepcionista">Recepcionista</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                {!selectedUsuario && (
                  <>
                    <div className="col-span-2 space-y-2">
                      <Label htmlFor="password">Senha*</Label>
                      <Input
                        id="password"
                        type="password"
                        value={formData.password}
                        onChange={(e) => setFormData({...formData, password: e.target.value})}
                        required={!selectedUsuario}
                      />
                      <PasswordStrengthIndicator password={formData.password} />
                    </div>
                    <div className="col-span-2 space-y-2">
                      <Label htmlFor="confirmPassword">Confirmar Senha*</Label>
                      <Input
                        id="confirmPassword"
                        type="password"
                        value={formData.confirmPassword}
                        onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})}
                        required={!selectedUsuario}
                      />
                      {formData.password && formData.confirmPassword && (
                        <div className="flex items-center gap-2 text-sm mt-2">
                          {formData.password === formData.confirmPassword ? (
                            <>
                              <Check className="h-4 w-4 text-green-600" />
                              <span className="text-green-600">As senhas coincidem</span>
                            </>
                          ) : (
                            <>
                              <X className="h-4 w-4 text-red-600" />
                              <span className="text-red-600">As senhas não coincidem</span>
                            </>
                          )}
                        </div>
                      )}
                    </div>
                  </>
                )}
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
                Digite a nova senha para o usuário {selectedUsuario?.full_name}
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
                <PasswordStrengthIndicator password={passwordData.newPassword} />
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
                {passwordData.newPassword && passwordData.confirmPassword && (
                  <div className="flex items-center gap-2 text-sm mt-2">
                    {passwordData.newPassword === passwordData.confirmPassword ? (
                      <>
                        <Check className="h-4 w-4 text-green-600" />
                        <span className="text-green-600">As senhas coincidem</span>
                      </>
                    ) : (
                      <>
                        <X className="h-4 w-4 text-red-600" />
                        <span className="text-red-600">As senhas não coincidem</span>
                      </>
                    )}
                  </div>
                )}
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
                  {usuarios.filter(u => u.is_active).length}
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
              <SelectItem value="recepcionista">Recepcionistas</SelectItem>
              <SelectItem value="aluno">Alunos</SelectItem>
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
                  <TableCell className="font-medium">{usuario.full_name}</TableCell>
                  <TableCell>
                    <div className="space-y-1">
                      <div className="flex items-center gap-1 text-sm">
                        <Mail className="h-3 w-3" />
                        {usuario.email}
                      </div>
                      <div className="flex items-center gap-1 text-sm text-muted-foreground">
                        <User className="h-3 w-3" />
                        @{usuario.username}
                      </div>
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge className={roleColors[usuario.role]}>
                      {roleLabels[usuario.role]}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    <Switch
                      checked={usuario.is_active}
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
                            username: usuario.username,
                            full_name: usuario.full_name,
                            email: usuario.email,
                            role: usuario.role,
                            password: '',
                            confirmPassword: ''
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