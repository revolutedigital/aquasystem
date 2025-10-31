# 🏊‍♂️ AquaSystem - Frontend Next.js

Sistema de gestão para academia de natação, construído com Next.js 14, React 18, TypeScript e Tailwind CSS.

## ✨ Features Implementadas

- ✅ **Autenticação JWT** com persistência de sessão
- ✅ **Dashboard** com métricas em tempo real
- ✅ **Sidebar responsiva** com navegação fluida
- ✅ **Página de login** moderna e funcional
- ✅ **Componentes UI** reutilizáveis (shadcn/ui)
- ✅ **Estado global** com Zustand
- ✅ **API Client** configurado com Axios
- ✅ **TypeScript** para type safety
- ✅ **Tailwind CSS** para estilização
- ✅ **Toast notifications** para feedback

## 🚀 Como Rodar

### 1. Instalar dependências

```bash
cd frontend-next
npm install
```

### 2. Configurar variáveis de ambiente

O arquivo `.env.local` já está configurado para desenvolvimento local.

Para produção, atualize com a URL do backend no Railway:

```env
NEXT_PUBLIC_API_URL=https://backend-production-33ee.up.railway.app
```

### 3. Rodar o backend (se local)

Em outro terminal:

```bash
cd ../backend
docker-compose up -d  # Para subir o PostgreSQL
python -m uvicorn app.main:app --reload --port 9000
```

### 4. Rodar o frontend

```bash
npm run dev
```

Acesse: http://localhost:3000

## 🔐 Login

Use as credenciais padrão:
- **Email:** admin@natacao.com
- **Senha:** admin123

## 📁 Estrutura do Projeto

```
src/
├── app/                    # Páginas e rotas
│   ├── login/             # Página de login
│   ├── layout.tsx         # Layout root
│   ├── page.tsx           # Dashboard
│   └── globals.css        # Estilos globais
│
├── components/            # Componentes React
│   ├── ui/               # Componentes base (Button, Card, Input)
│   └── layout/           # Layout components (Sidebar, DashboardLayout)
│
├── lib/                  # Utilitários
│   ├── api.ts           # Cliente API
│   └── utils.ts         # Funções auxiliares
│
├── store/               # Estado global (Zustand)
│   └── authStore.ts    # Store de autenticação
│
└── types/              # TypeScript types
    └── index.ts       # Definições de tipos
```

## 🎨 Páginas Prontas

### ✅ Login (`/login`)
- Formulário de autenticação
- Validação com Zod
- Feedback visual de loading
- Redirecionamento após login

### ✅ Dashboard (`/`)
- Cards com métricas principais
- Total de alunos
- Receita mensal
- Inadimplentes
- Taxa de adimplência
- Ações rápidas

### 🚧 Em Desenvolvimento
- `/alunos` - Gestão de alunos
- `/horarios` - Grade de horários
- `/financeiro` - Gestão financeira
- `/usuarios` - Gestão de usuários

## 🔧 Tecnologias

- **Next.js 14** - Framework React
- **React 18** - UI Library
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Zustand** - State management
- **Axios** - HTTP client
- **React Hook Form** - Forms
- **Zod** - Validation
- **Lucide React** - Icons
- **React Hot Toast** - Notifications

## 📦 Scripts

```bash
# Desenvolvimento
npm run dev

# Build de produção
npm run build

# Rodar build de produção
npm start

# Lint
npm run lint
```

## 🚀 Deploy no Railway

### 1. Criar novo serviço

No Railway, crie um novo serviço e conecte ao repositório.

### 2. Configurações

- **Root Directory:** `frontend-next`
- **Build Command:** `npm run build`
- **Start Command:** `npm start`
- **Port:** 3000

### 3. Variáveis de ambiente

Adicione no Railway:

```
NEXT_PUBLIC_API_URL=https://backend-production-xxxx.up.railway.app
```

### 4. Deploy

O Railway fará o deploy automaticamente após push no GitHub.

## 🐛 Troubleshooting

### Erro de CORS

Certifique-se de que o backend tem o frontend na lista de `ALLOWED_ORIGINS`.

### Erro 401 Unauthorized

Token expirou ou é inválido. Faça logout e login novamente.

### Backend não conecta

Verifique se:
1. Backend está rodando
2. `NEXT_PUBLIC_API_URL` está correto
3. Não há erro de CORS

## 📱 Responsividade

O sistema é totalmente responsivo:
- Desktop: Sidebar fixa
- Mobile: Sidebar com menu hambúrguer
- Tablets: Layout adaptativo

## 🎯 Próximos Passos

1. Implementar CRUD de alunos
2. Adicionar grade de horários visual
3. Sistema de pagamentos completo
4. Gestão de usuários
5. Relatórios e gráficos
6. Notificações WhatsApp

---

**Desenvolvido com ❤️ para gestão de academias de natação**