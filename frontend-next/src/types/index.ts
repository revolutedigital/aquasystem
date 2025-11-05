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
  mes_referencia: string  // Formato: YYYY-MM
  forma_pagamento: 'dinheiro' | 'pix' | 'cartao_credito' | 'cartao_debito' | 'transferencia'
  observacoes?: string
  created_at: string
}

export interface Horario {
  id: number
  dia_semana: string
  horario: string
  tipo_aula: 'natacao' | 'hidroginastica'
  professor_id?: number
  professor_nome?: string
  capacidade_maxima: number
  fila_espera: number
  alunos?: Aluno[]
  vagas_disponiveis?: number
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}

export interface Professor {
  id: number
  nome: string
  email: string
  cpf: string
  telefone?: string
  especialidade?: string  // 'natacao' | 'hidroginastica' | 'ambos'
  is_active: boolean
}

export interface ProfessorCreateData {
  nome: string
  email: string
  cpf: string
  telefone?: string
  especialidade?: string
}

export interface ProfessorUpdateData {
  nome?: string
  email?: string
  cpf?: string
  telefone?: string
  especialidade?: string
  is_active?: boolean
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
  mes_referencia: string  // Formato: YYYY-MM
  forma_pagamento: 'dinheiro' | 'pix' | 'cartao_credito' | 'cartao_debito' | 'transferencia'
  observacoes?: string
}

export interface HorarioCreateData {
  dia_semana: string
  horario: string
  tipo_aula: 'natacao' | 'hidroginastica'
  capacidade_maxima: number
  professor_id?: number
  fila_espera?: number
}

export interface HorarioUpdateData {
  dia_semana?: string
  horario?: string
  tipo_aula?: 'natacao' | 'hidroginastica'
  capacidade_maxima?: number
  professor_id?: number
  fila_espera?: number
}

export interface Plano {
  id: number
  nome: string
  descricao?: string
  valor_mensal: number
  aulas_por_semana: number
  duracao_aula_minutos: number
  acesso_livre: boolean
  permite_reposicao: boolean
  dias_tolerancia: number
  ativo: boolean
}

export interface PlanoCreateData {
  nome: string
  descricao?: string
  valor_mensal: number
  aulas_por_semana: number
  duracao_aula_minutos?: number
  acesso_livre?: boolean
  permite_reposicao?: boolean
  dias_tolerancia?: number
}