# 🏊 Sistema de Gestão para Academia de Natação

Sistema completo de gestão para academias de natação e hidroginástica, desenvolvido com **FastAPI**, **Streamlit**, **PostgreSQL** e **Docker**. Inclui notificações automatizadas via **WhatsApp** usando Evolution API.

## 📋 Descrição do Projeto

O **Natação Manager** é uma solução integrada que permite gerenciar todos os aspectos de uma academia de natação de forma eficiente e automatizada. O sistema oferece controle completo de alunos, pagamentos, horários, turmas e envio automatizado de notificações via WhatsApp.

### ✨ Principais Benefícios

- 🎨 Interface web moderna e intuitiva com Streamlit
- 📱 Automação de lembretes de pagamento via WhatsApp (Evolution API)
- 💰 Controle financeiro detalhado com relatórios
- 📅 Gestão de turmas e horários com controle de capacidade
- 📊 Dashboard com métricas em tempo real e gráficos interativos
- 🐳 Totalmente containerizado com Docker para fácil implantação
- 🔄 API REST completa com documentação automática

## 🚀 Funcionalidades Detalhadas

### 1. 📝 Cadastro de Alunos
- Registro completo de informações pessoais (nome completo, responsável, telefone WhatsApp)
- Controle de modalidade (natação ou hidroginástica)
- Definição de valor de mensalidade e dia de vencimento personalizados
- Data de início do contrato
- Status ativo/inativo (soft delete)
- Validação de telefone brasileiro
- Filtros por tipo de aula e status

### 2. 💰 Controle Financeiro
- Registro de pagamentos com data, valor e forma de pagamento
- Mês de referência para controle de pagamentos retroativos
- 4 formas de pagamento: dinheiro, pix, cartão, transferência
- Histórico completo de pagamentos por aluno
- Relatório mensal com totais agregados (GROUP BY)
- **Controle de inadimplência**: alunos com 45+ dias sem pagar
- Formatação de valores em padrão brasileiro (R$ 1.234,56)
- Botões para enviar cobrança via WhatsApp

### 3. 📅 Grade de Horários
- Criação de horários por dia da semana (Segunda a Sábado)
- Definição de capacidade máxima por turma
- Vinculação de alunos aos horários (matrícula)
- **Validação automática de capacidade** antes de matricular
- Visualização da grade completa com ocupação
- **Indicadores visuais de capacidade**: 🟢 (<70%), 🟡 (70-90%), 🔴 (>90%)
- Remoção de alunos de horários
- Listagem de alunos matriculados em cada turma

### 4. 📊 Dashboard e Relatórios
- **Métricas em tempo real**:
  - Total de alunos ativos
  - Quantidade de inadimplentes
  - Receita dos últimos 30 dias
  - Taxa de ocupação média dos horários
- **Gráficos interativos com Plotly**:
  - Receita mensal dos últimos 6 meses (gráfico de barras)
  - Distribuição de alunos por tipo de aula (gráfico de pizza)
  - Formas de pagamento mais usadas (gráfico de barras horizontal)
- **Tabelas analíticas**:
  - Top 5 horários mais ocupados
  - Próximos vencimentos (7 dias)

### 5. 📱 Notificações Automáticas via WhatsApp (Evolution API)

O sistema envia automaticamente:
- **Lembretes de vencimento**: 3 dias antes da data de vencimento
- **Avisos de atraso**: 5 dias após a data de vencimento
- **Execução diária**: APScheduler roda verificações às 9h (horário de Brasília)

## 🛠️ Tecnologias Utilizadas

- **Backend**: FastAPI 0.104.1 (Python 3.11)
- **Frontend**: Streamlit 1.28.1
- **Banco de Dados**: PostgreSQL 15 Alpine
- **Containerização**: Docker & Docker Compose
- **ORM**: SQLAlchemy 2.0.23
- **Validação**: Pydantic 2.5.0
- **Agendamento**: APScheduler 3.10.4
- **API WhatsApp**: Evolution API (integração via httpx)
- **Gráficos**: Plotly 5.18.0

## 📁 Estrutura do Projeto

```
natacao-manager/
├── backend/                    # API FastAPI
│   ├── app/
│   │   ├── models/            # Modelos SQLAlchemy
│   │   │   ├── aluno.py       # Modelo de Aluno
│   │   │   ├── pagamento.py   # Modelo de Pagamento
│   │   │   ├── horario.py     # Modelo de Horário
│   │   │   └── turma.py       # Tabela associativa Aluno-Horário
│   │   ├── schemas/           # Schemas Pydantic
│   │   │   ├── aluno.py       # AlunoCreate, AlunoUpdate, AlunoResponse
│   │   │   ├── pagamento.py   # PagamentoCreate, PagamentoUpdate, etc
│   │   │   └── horario.py     # HorarioCreate, HorarioUpdate, etc
│   │   ├── routes/            # Endpoints da API
│   │   │   ├── alunos.py      # 7 endpoints de alunos
│   │   │   ├── pagamentos.py  # 6 endpoints de pagamentos
│   │   │   └── horarios.py    # 9 endpoints de horários
│   │   ├── services/          # Lógica de negócio
│   │   │   ├── whatsapp_service.py       # Integração Evolution API
│   │   │   └── notificacao_service.py    # APScheduler
│   │   ├── utils/             # Funções auxiliares
│   │   │   └── helpers.py     # 11 funções úteis (formatação, validação)
│   │   ├── database.py        # Configuração SQLAlchemy
│   │   └── main.py            # Aplicação FastAPI principal
│   ├── requirements.txt       # Dependências Python
│   └── Dockerfile             # Imagem Docker do backend
├── frontend/                  # Interface Streamlit
│   ├── pages/                 # Páginas da aplicação
│   │   ├── 1_Cadastro_Alunos.py    # Cadastro e listagem de alunos
│   │   ├── 2_Financeiro.py         # Pagamentos e inadimplentes
│   │   ├── 3_Grade_Horarios.py     # Gestão de horários e matrículas
│   │   └── 4_Dashboard.py          # Métricas e gráficos
│   ├── streamlit_app.py       # Página inicial
│   ├── requirements.txt       # Dependências Python
│   └── Dockerfile             # Imagem Docker do frontend
├── docker-compose.yml         # Orquestração dos 3 containers
├── .env.example              # Exemplo de variáveis de ambiente
├── .env                      # Suas configurações (não commitado)
└── README.md                 # Este arquivo
```

## 📦 Requisitos

- **Docker** (versão 20.10+)
- **Docker Compose** (versão 2.0+)

> Não é necessário instalar Python, PostgreSQL ou outras dependências. Tudo roda em containers!

## ⚙️ Instalação e Execução

### 1️⃣ Clone o repositório

```bash
git clone <url-do-repositorio>
cd natacao-manager
```

### 2️⃣ Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:

```env
# Configurações do Banco de Dados PostgreSQL
POSTGRES_USER=natacao_user
POSTGRES_PASSWORD=natacao_password
POSTGRES_DB=natacao_db
POSTGRES_PORT=5432

# Configurações das Portas
BACKEND_PORT=9000
FRONTEND_PORT=9001

# Configurações do WhatsApp Evolution API (Opcional)
EVOLUTION_API_URL=https://sua-api.evolution.com
EVOLUTION_API_KEY=sua_chave_api
EVOLUTION_INSTANCE_NAME=nome_da_instancia
```

### 3️⃣ Inicie os containers

```bash
docker-compose up -d --build
```

Este comando irá:
- Baixar as imagens base do PostgreSQL e Python
- Construir as imagens do backend e frontend
- Criar 3 containers: `natacao_postgres`, `natacao_backend`, `natacao_frontend`
- Criar volumes para persistência de dados
- Configurar rede interna entre os containers

### 4️⃣ Aguarde a inicialização

```bash
docker-compose logs -f
```

Aguarde até ver as mensagens:
- Backend: `Application startup complete.`
- Frontend: `You can now view your Streamlit app in your browser.`

### 5️⃣ Acesse as aplicações

- **Frontend (Streamlit)**: http://localhost:9001
- **Backend (API)**: http://localhost:9000
- **Documentação da API (Swagger)**: http://localhost:9000/docs
- **PostgreSQL**: localhost:5434 (externo) / postgres:5432 (interno)

## 📱 Configuração do WhatsApp (Evolution API)

### O que é Evolution API?

Evolution API é uma solução open-source para integração com WhatsApp, permitindo envio de mensagens programaticamente. É uma alternativa ao Twilio e outras APIs pagas.

### Passos para Configurar

#### 1. Instalação da Evolution API

**Opção A: Docker (Recomendado)**

```bash
docker run -d \
  --name evolution-api \
  -p 8080:8080 \
  -e AUTHENTICATION_API_KEY=sua_chave_secreta_aqui \
  atendai/evolution-api:latest
```

**Opção B: Usando o repositório oficial**

```bash
git clone https://github.com/EvolutionAPI/evolution-api.git
cd evolution-api
cp .env.example .env
# Edite o .env conforme necessário
docker-compose up -d
```

Acesse http://localhost:8080 para verificar se está rodando.

#### 2. Criar uma Instância

Faça uma requisição POST para criar uma instância:

```bash
curl -X POST http://localhost:8080/instance/create \
  -H "apikey: sua_chave_secreta_aqui" \
  -H "Content-Type: application/json" \
  -d '{
    "instanceName": "natacao_manager",
    "qrcode": true
  }'
```

#### 3. Conectar o WhatsApp

A resposta da requisição acima incluirá um QR Code. Escaneie com seu WhatsApp:

1. Abra o WhatsApp no celular
2. Vá em **Configurações** → **Aparelhos Conectados**
3. Toque em **Conectar Aparelho**
4. Escaneie o QR Code retornado pela API

#### 4. Configurar o `.env` do Natação Manager

Atualize seu `.env`:

```env
EVOLUTION_API_URL=http://localhost:8080
EVOLUTION_API_KEY=sua_chave_secreta_aqui
EVOLUTION_INSTANCE_NAME=natacao_manager
```

Se a Evolution API estiver em outro servidor:

```env
EVOLUTION_API_URL=https://sua-api.evolution.com
EVOLUTION_API_KEY=sua_chave_api
EVOLUTION_INSTANCE_NAME=natacao_manager
```

#### 5. Reinicie o Backend

```bash
docker-compose restart backend
```

#### 6. Teste o Envio

No backend, o serviço de notificações:
- Verifica vencimentos **às 9h todos os dias**
- Envia lembretes **3 dias antes** do vencimento
- Envia avisos de atraso **5 dias após** o vencimento

Para testar manualmente, você pode chamar o endpoint (se implementado):

```bash
curl -X POST http://localhost:9000/api/notificacoes/testar \
  -H "Content-Type: application/json" \
  -d '{"aluno_id": 1}'
```

### Formato das Mensagens

**Lembrete de Vencimento (3 dias antes):**
```
Olá [Nome do Aluno]!

Este é um lembrete que sua mensalidade da Academia de Natação vence em 3 dias ([Data]).

Valor: R$ [Valor]

Por favor, realize o pagamento até a data de vencimento.

Obrigado!
```

**Aviso de Atraso (5 dias depois):**
```
Olá [Nome do Aluno],

Verificamos que sua mensalidade da Academia de Natação está em atraso há [X] dias.

Valor: R$ [Valor]
Vencimento: [Data]

Por favor, regularize sua situação o quanto antes.

Obrigado!
```

### Troubleshooting Evolution API

**Problema**: QR Code não aparece
- **Solução**: Verifique os logs do container Evolution API: `docker logs evolution-api`

**Problema**: Mensagens não são enviadas
- **Solução**: Verifique se a instância está conectada: `curl http://localhost:8080/instance/connectionState/natacao_manager -H "apikey: sua_chave"`

**Problema**: Erro 401 Unauthorized
- **Solução**: Verifique se a `EVOLUTION_API_KEY` no `.env` está correta

## 📖 Uso

### Interface Web (Streamlit)

O frontend oferece 5 páginas:

#### 🏠 Home (streamlit_app.py)
- Visão geral do sistema
- Cards com estatísticas principais:
  - Total de alunos ativos
  - Inadimplentes
  - Receita mensal (últimos 30 dias)
- Informações sobre como usar o sistema

#### 📝 Cadastro de Alunos (1_Cadastro_Alunos.py)

**Tab "Novo Aluno":**
- Formulário completo com validação
- Campos: nome, telefone, responsável, tipo de aula, mensalidade, dia de vencimento
- Validação de telefone brasileiro (10 ou 11 dígitos)
- Formatação automática: (11) 99999-9999

**Tab "Listar Alunos":**
- Filtros por tipo de aula (natação/hidroginástica) e status (ativo/inativo)
- Cards expansíveis com todas as informações
- Indicadores visuais: 🟢 ativo, 🔴 inativo, 🏊 natação, 💧 hidroginástica

**Tab "Buscar/Editar":**
- Busca por ID
- Formulário de edição pré-preenchido
- Botão para atualizar informações
- Botão para inativar aluno (soft delete)

#### 💰 Financeiro (2_Financeiro.py)

**Tab "Registrar Pagamento":**
- Seleção do aluno ativo
- Campos: valor, data de pagamento, mês de referência (YYYY-MM)
- 4 formas de pagamento: dinheiro, pix, cartão, transferência
- Confirmação visual após registro

**Tab "Histórico de Pagamentos":**
- Filtros por aluno e mês de referência
- Lista de todos os pagamentos
- Valores formatados em BRL
- Botão para deletar pagamento

**Tab "Inadimplentes":**
- Lista de alunos com 45+ dias sem pagar
- Mostra: nome, telefone, dias de atraso, valor da mensalidade
- **Botão "Enviar WhatsApp"**: abre chat direto com link wa.me

#### 📅 Grade de Horários (3_Grade_Horarios.py)

**Tab "Criar Horário":**
- Seleção do dia da semana (Segunda a Sábado)
- Time picker para horário
- Capacidade máxima (1-30 alunos)
- Tipo de aula (natação/hidroginástica)

**Tab "Grade Completa":**
- Visualização organizada por dia da semana
- Indicadores de capacidade: 🟢 🟡 🔴
- Lista de alunos matriculados em cada horário
- Botões para remover aluno ou deletar horário

**Tab "Matricular Aluno":**
- Seleção de aluno ativo
- Seleção de horário (mostra capacidade)
- Validação automática pelo backend
- Feedback visual de sucesso/erro

#### 📊 Dashboard (4_Dashboard.py)

**Métricas:**
- 4 cards com st.metric mostrando KPIs principais

**Gráficos:**
- **Receita Mensal**: últimos 6 meses em barras (Plotly)
- **Distribuição por Tipo**: pizza com natação vs hidroginástica
- **Formas de Pagamento**: barras horizontais

**Tabelas:**
- Top 5 horários mais ocupados (percentual de capacidade)
- Próximos vencimentos (7 dias)

### API REST (FastAPI)

Acesse http://localhost:9000/docs para documentação interativa (Swagger UI).

#### Endpoints de Alunos

```bash
# Listar todos os alunos (com filtros opcionais)
GET /api/alunos?ativo=true&tipo_aula=natacao

# Buscar aluno por ID
GET /api/alunos/1

# Criar novo aluno
POST /api/alunos
Content-Type: application/json
{
  "nome_completo": "João Silva Santos",
  "responsavel": "Maria Silva",
  "tipo_aula": "natacao",
  "valor_mensalidade": 150.00,
  "dia_vencimento": 10,
  "data_inicio_contrato": "2025-01-15",
  "ativo": true,
  "telefone_whatsapp": "(11) 99999-9999",
  "observacoes": "Sem restrições médicas"
}

# Atualizar aluno
PUT /api/alunos/1
Content-Type: application/json
{
  "valor_mensalidade": 180.00,
  "dia_vencimento": 5
}

# Inativar aluno (soft delete)
DELETE /api/alunos/1

# Listar inadimplentes (45+ dias sem pagar)
GET /api/alunos/inadimplentes
```

#### Endpoints de Pagamentos

```bash
# Listar todos os pagamentos
GET /api/pagamentos

# Buscar pagamento por ID
GET /api/pagamentos/1

# Listar pagamentos de um aluno
GET /api/pagamentos/aluno/1

# Relatório mensal agregado
GET /api/pagamentos/relatorio-mensal?ano=2025&mes=10

# Registrar pagamento
POST /api/pagamentos
Content-Type: application/json
{
  "aluno_id": 1,
  "valor": 150.00,
  "data_pagamento": "2025-10-14",
  "mes_referencia": "2025-10",
  "forma_pagamento": "pix",
  "observacoes": "Pagamento via PIX"
}

# Deletar pagamento
DELETE /api/pagamentos/1
```

#### Endpoints de Horários

```bash
# Listar todos os horários
GET /api/horarios

# Buscar horário por ID
GET /api/horarios/1

# Grade completa (com alunos matriculados)
GET /api/horarios/grade-completa

# Criar horário
POST /api/horarios
Content-Type: application/json
{
  "dia_semana": "Segunda",
  "horario": "08:00:00",
  "capacidade_maxima": 20,
  "tipo_aula": "natacao"
}

# Atualizar horário
PUT /api/horarios/1
Content-Type: application/json
{
  "capacidade_maxima": 25
}

# Deletar horário
DELETE /api/horarios/1

# Matricular aluno (valida capacidade)
POST /api/horarios/1/alunos/5

# Remover aluno do horário
DELETE /api/horarios/1/alunos/5
```

## 🗄️ Banco de Dados

O sistema utiliza **PostgreSQL 15** com 4 tabelas principais:

### Tabela: `alunos`
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer (PK) | ID único |
| nome_completo | String(200) | Nome completo do aluno |
| responsavel | String(200) | Nome do responsável (se menor) |
| tipo_aula | String(20) | "natacao" ou "hidroginastica" |
| valor_mensalidade | Numeric(10,2) | Valor da mensalidade |
| dia_vencimento | Integer | Dia do mês (1-31) |
| data_inicio_contrato | Date | Data de início |
| ativo | Boolean | Status (soft delete) |
| telefone_whatsapp | String(20) | Telefone para WhatsApp |
| observacoes | Text | Observações gerais |
| created_at | DateTime | Data de criação |
| updated_at | DateTime | Última atualização |

### Tabela: `pagamentos`
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer (PK) | ID único |
| aluno_id | Integer (FK) | Referência para alunos.id |
| valor | Numeric(10,2) | Valor pago |
| data_pagamento | Date | Data do pagamento |
| mes_referencia | String(7) | Formato "YYYY-MM" |
| forma_pagamento | String(20) | dinheiro/pix/cartao/transferencia |
| observacoes | Text | Observações |
| created_at | DateTime | Data de criação |

### Tabela: `horarios`
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer (PK) | ID único |
| dia_semana | String(20) | Segunda/Terça/Quarta/etc |
| horario | Time | Horário da aula (HH:MM:SS) |
| capacidade_maxima | Integer | Máximo de alunos |
| tipo_aula | String(20) | "natacao" ou "hidroginastica" |
| created_at | DateTime | Data de criação |

### Tabela: `aluno_horario` (Many-to-Many)
| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer (PK) | ID único |
| aluno_id | Integer (FK) | Referência para alunos.id |
| horario_id | Integer (FK) | Referência para horarios.id |
| created_at | DateTime | Data de matrícula |

### Relacionamentos
- `alunos` → `pagamentos`: One-to-Many (um aluno tem vários pagamentos)
- `alunos` ↔ `horarios`: Many-to-Many através de `aluno_horario`

## 🔧 Comandos Úteis

### Gerenciamento de Containers

```bash
# Ver status dos containers
docker-compose ps

# Ver logs em tempo real
docker-compose logs -f

# Ver logs de um container específico
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres

# Parar os containers
docker-compose stop

# Parar e remover containers
docker-compose down

# Parar, remover containers E volumes (APAGA DADOS!)
docker-compose down -v

# Reiniciar um container específico
docker-compose restart backend

# Reconstruir as imagens
docker-compose build

# Subir novamente forçando rebuild
docker-compose up -d --build
```

### Acesso ao Banco de Dados

```bash
# Conectar via psql
docker exec -it natacao_postgres psql -U natacao_user -d natacao_db

# Executar query diretamente
docker exec -it natacao_postgres psql -U natacao_user -d natacao_db -c "SELECT * FROM alunos;"

# Verificar tabelas existentes
docker exec -it natacao_postgres psql -U natacao_user -d natacao_db -c "\dt"
```

### Backup e Restore

```bash
# Criar backup completo
docker exec natacao_postgres pg_dump -U natacao_user natacao_db > backup_$(date +%Y%m%d).sql

# Restaurar backup
docker exec -i natacao_postgres psql -U natacao_user natacao_db < backup_20251014.sql

# Backup apenas de uma tabela
docker exec natacao_postgres pg_dump -U natacao_user -t alunos natacao_db > alunos_backup.sql
```

### Desenvolvimento Local (sem Docker)

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

pip install -r requirements.txt

# Configure DATABASE_URL no .env para apontar para localhost:5434
export DATABASE_URL="postgresql://natacao_user:natacao_password@localhost:5434/natacao_db"

# Inicie o servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 9000
```

#### Frontend

```bash
cd frontend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

pip install -r requirements.txt

# Configure API_URL no .env
export API_URL="http://localhost:9000"

# Inicie o Streamlit
streamlit run streamlit_app.py --server.port=9001 --server.address=0.0.0.0
```

## 🐛 Troubleshooting

### Problema: Porta 5434 já está em uso

**Erro:** `Bind for 0.0.0.0:5434 failed: port is already allocated`

**Solução:**
```bash
# Encontre o processo usando a porta
lsof -i :5434  # Mac/Linux
netstat -ano | findstr :5434  # Windows

# Mate o processo ou altere a porta no docker-compose.yml
# Linha 14: "5435:5432" por exemplo
```

### Problema: Backend não inicia (erro Pydantic)

**Erro:** `ValueError: Unknown constraint decimal_places`

**Solução:** Já foi corrigido! Use Pydantic 2.5.0+ que não usa `decimal_places`. Se ainda ocorrer, verifique se os schemas estão usando apenas `ge=0` em vez de `ge=0, decimal_places=2`.

### Problema: Frontend não conecta ao backend

**Sintomas:** "Erro de conexão com o backend"

**Soluções:**
1. Verifique se o backend está rodando: `docker-compose logs backend`
2. Teste o endpoint: `curl http://localhost:9000/`
3. Verifique se o container frontend consegue acessar: `docker exec natacao_frontend ping backend`
4. Reinicie o frontend: `docker-compose restart frontend`

### Problema: Banco de dados não inicializa

**Sintomas:** Backend mostra erros de conexão

**Soluções:**
1. Verifique se o PostgreSQL está saudável: `docker-compose ps`
2. Veja os logs: `docker-compose logs postgres`
3. Aguarde o healthcheck passar (pode levar até 30 segundos)
4. Se necessário, recrie o volume: `docker-compose down -v && docker-compose up -d`

### Problema: WhatsApp não envia mensagens

**Soluções:**
1. Verifique se a Evolution API está rodando
2. Teste a conexão: `curl http://localhost:8080/instance/connectionState/natacao_manager -H "apikey: sua_chave"`
3. Verifique se o QR Code foi escaneado e a instância está conectada
4. Veja os logs do backend: `docker-compose logs backend | grep WhatsApp`

## 📚 Arquitetura do Sistema

```
┌─────────────┐         ┌──────────────┐         ┌──────────────┐
│             │         │              │         │              │
│  Streamlit  │────────▶│   FastAPI    │────────▶│  PostgreSQL  │
│  Frontend   │  HTTP   │   Backend    │  SQL    │   Database   │
│ (Port 9001) │         │ (Port 9000)  │         │ (Port 5434)  │
│             │         │              │         │              │
└─────────────┘         └──────┬───────┘         └──────────────┘
                               │
                               │ HTTP
                               ▼
                        ┌──────────────┐
                        │              │
                        │  Evolution   │
                        │  WhatsApp    │
                        │     API      │
                        │              │
                        └──────────────┘
```

### Fluxo de Dados

1. **Usuário** acessa o Streamlit (porta 9001)
2. **Streamlit** faz requisições HTTP para FastAPI (porta 9000)
3. **FastAPI** executa queries no PostgreSQL (porta 5434)
4. **FastAPI** retorna JSON para o Streamlit
5. **Streamlit** renderiza a interface
6. **APScheduler** (no backend) verifica vencimentos às 9h
7. **WhatsApp Service** envia mensagens via Evolution API

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

### Guidelines de Código

- Use **type hints** em Python
- Docstrings em **português brasileiro**
- Siga **PEP 8** para formatação
- Adicione **testes** para novas features
- Atualize a **documentação** quando necessário

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

- **Issues**: Abra uma issue no GitHub
- **Email**: suporte@exemplo.com
- **Documentação**: Este README e http://localhost:9000/docs

## 🗺️ Roadmap

### Versão 2.0 (Planejado)
- [ ] Autenticação de usuários (JWT)
- [ ] Permissões por nível (admin, recepcionista, aluno)
- [ ] Sistema de check-in/check-out com QR Code
- [ ] Integração com plataforma de pagamentos online (Stripe, Mercado Pago)

### Versão 3.0 (Futuro)
- [ ] App mobile (React Native ou Flutter)
- [ ] Sistema de avaliação física dos alunos
- [ ] Controle de equipamentos e materiais
- [ ] Exportação de relatórios em PDF
- [ ] Sistema de mensagens entre alunos e administração
- [ ] Agenda de aulas experimentais

## 👥 Autores

- **Desenvolvedor Principal** - Implementação inicial

## 🙏 Agradecimentos

- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno e rápido
- [Streamlit](https://streamlit.io/) - Criação fácil de interfaces web
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM poderoso
- [Evolution API](https://github.com/EvolutionAPI/evolution-api) - Integração WhatsApp
- [Plotly](https://plotly.com/) - Gráficos interativos
- Comunidade Python 🐍

---

**Desenvolvido com ❤️ para academias de natação**

*Versão 1.0.0 - Outubro 2025*
