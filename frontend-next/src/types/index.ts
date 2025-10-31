export interface User {
  id: number
  email: string
  name: string
  role: 'admin' | 'recepcionista'
  is_active: boolean
}

export interface Aluno {
  id: number
  nome_completo: string
  responsavel?: string
  tipo_aula: 'natacao' | 'hidroginastica'
  valor_mensalidade: number
  dia_vencimento: number
  data_inicio_contrato: string
  ativo: boolean
  telefone_whatsapp?: string
  observacoes?: string
  created_at: string
  updated_at: string
}

export interface Pagamento {
  id: number
  aluno_id: number
  aluno?: Aluno
  valor: number
  data_pagamento: string
  mes_referencia: number
  ano_referencia: number
  forma_pagamento: 'dinheiro' | 'pix' | 'cartao_credito' | 'cartao_debito'
  observacao?: string
  created_at: string
}

export interface Horario {
  id: number
  dia_semana: string
  horario: string
  tipo_aula: 'natacao' | 'hidroginastica'
  professor: string
  capacidade_maxima: number
  alunos: Aluno[]
  created_at: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}

export interface Professor {
  id: number
  nome: string
  especialidade: string
  telefone?: string
  email?: string
  ativo: boolean
  created_at: string
  updated_at: string
}

export interface Turma {
  id: number
  nome: string
  horario_id: number
  professor_id?: number
  capacidade_maxima: number
  alunos?: Aluno[]
  created_at: string
}

export interface AlunoCreateData {
  nome_completo: string
  responsavel?: string
  tipo_aula: 'natacao' | 'hidroginastica'
  valor_mensalidade: number
  dia_vencimento: number
  data_inicio_contrato: string
  telefone_whatsapp?: string
  observacoes?: string
}

export interface AlunoUpdateData {
  nome_completo?: string
  responsavel?: string
  tipo_aula?: 'natacao' | 'hidroginastica'
  valor_mensalidade?: number
  dia_vencimento?: number
  data_inicio_contrato?: string
  ativo?: boolean
  telefone_whatsapp?: string
  observacoes?: string
}

export interface PagamentoCreateData {
  aluno_id: number
  valor: number
  data_pagamento: string
  mes_referencia: number
  ano_referencia: number
  forma_pagamento: 'dinheiro' | 'pix' | 'cartao_credito' | 'cartao_debito'
  observacao?: string
}

export interface HorarioCreateData {
  dia_semana: string
  horario: string
  tipo_aula: 'natacao' | 'hidroginastica'
  professor: string
  capacidade_maxima: number
}