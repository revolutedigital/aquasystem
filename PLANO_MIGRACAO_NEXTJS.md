# 🚀 Plano de Migração: Streamlit → Next.js + React

## 📋 Visão Geral

Migrar o frontend atual de Streamlit para Next.js 14 com React, TypeScript, e Tailwind CSS.

**Objetivo:** Criar uma aplicação moderna, rápida, e com melhor UX.

---

## ✅ Vantagens da Migração

### Problemas Atuais (Streamlit)
- ❌ Navegação confusa entre páginas
- ❌ Problemas com autenticação persistente
- ❌ Performance ruim (recarrega página inteira)
- ❌ Limitações de customização de UI
- ❌ Erros com funções não disponíveis (`switch_page`)
- ❌ UX não intuitiva para usuários

### Benefícios do Next.js + React
- ✅ Navegação fluida (SPA - Single Page Application)
- ✅ Performance excelente (Server Side Rendering)
- ✅ Autenticação moderna com tokens persistentes
- ✅ UI totalmente customizável
- ✅ Componentes reutilizáveis
- ✅ TypeScript para código mais seguro
- ✅ Deploy otimizado
- ✅ SEO melhorado (se necessário no futuro)

---

## 🛠️ Stack Tecnológica

### Frontend
- **Framework:** Next.js 14 (App Router)
- **UI Library:** React 18
- **Linguagem:** TypeScript
- **Styling:** Tailwind CSS + shadcn/ui
- **State Management:** Zustand (leve e simples)
- **Forms:** React Hook Form + Zod (validação)
- **HTTP Client:** Axios
- **Gráficos:** Recharts ou Chart.js
- **Tabelas:** TanStack Table (React Table v8)
- **Notificações:** React Hot Toast

### Backend (Mantém o atual)
- **Framework:** FastAPI (já existente)
- **Banco:** PostgreSQL (já existente)
- **Deploy:** Railway (já existente)

---

## 📁 Estrutura de Pastas Proposta

```
natacao-manager/
├── backend/                    # Mantém o atual
│   └── (estrutura existente)
│
└── frontend-next/              # NOVO
    ├── public/
    │   ├── icons/
    │   └── images/
    │
    ├── src/
    │   ├── app/                # Next.js App Router
    │   │   ├── (auth)/
    │   │   │   ├── login/
    │   │   │   │   └── page.tsx
    │   │   │   └── layout.tsx
    │   │   │
    │   │   ├── (dashboard)/    # Rotas protegidas
    │   │   │   ├── layout.tsx  # Layout com sidebar
    │   │   │   ├── page.tsx    # Dashboard principal
    │   │   │   ├── alunos/
    │   │   │   │   ├── page.tsx
    │   │   │   │   ├── novo/
    │   │   │   │   │   └── page.tsx
    │   │   │   │   └── [id]/
    │   │   │   │       └── page.tsx
    │   │   │   ├── horarios/
    │   │   │   │   └── page.tsx
    │   │   │   ├── financeiro/
    │   │   │   │   └── page.tsx
    │   │   │   └── usuarios/
    │   │   │       └── page.tsx
    │   │   │
    │   │   ├── layout.tsx      # Root layout
    │   │   ├── globals.css
    │   │   └── not-found.tsx
    │   │
    │   ├── components/
    │   │   ├── ui/             # shadcn/ui components
    │   │   │   ├── button.tsx
    │   │   │   ├── input.tsx
    │   │   │   ├── card.tsx
    │   │   │   ├── table.tsx
    │   │   │   ├── dialog.tsx
    │   │   │   └── ...
    │   │   │
    │   │   ├── layout/
    │   │   │   ├── Sidebar.tsx
    │   │   │   ├── Header.tsx
    │   │   │   ├── Footer.tsx
    │   │   │   └── DashboardLayout.tsx
    │   │   │
    │   │   ├── forms/
    │   │   │   ├── AlunoForm.tsx
    │   │   │   ├── PagamentoForm.tsx
    │   │   │   └── HorarioForm.tsx
    │   │   │
    │   │   ├── cards/
    │   │   │   ├── StatCard.tsx
    │   │   │   ├── AlunoCard.tsx
    │   │   │   └── MetricCard.tsx
    │   │   │
    │   │   └── charts/
    │   │       ├── ReceitaChart.tsx
    │   │       └── DistribuicaoChart.tsx
    │   │
    │   ├── lib/
    │   │   ├── api.ts          # Axios instance
    │   │   ├── auth.ts         # Auth helpers
    │   │   └── utils.ts        # Utility functions
    │   │
    │   ├── hooks/
    │   │   ├── useAuth.ts
    │   │   ├── useAlunos.ts
    │   │   ├── usePagamentos.ts
    │   │   └── useHorarios.ts
    │   │
    │   ├── store/
    │   │   ├── authStore.ts    # Zustand store
    │   │   └── uiStore.ts
    │   │
    │   ├── types/
    │   │   ├── aluno.ts
    │   │   ├── pagamento.ts
    │   │   ├── horario.ts
    │   │   └── user.ts
    │   │
    │   └── constants/
    │       ├── routes.ts
    │       └── api-endpoints.ts
    │
    ├── .env.local
    ├── .env.example
    ├── next.config.js
    ├── tailwind.config.ts
    ├── tsconfig.json
    ├── package.json
    └── README.md
```

---

## 📝 Plano de Implementação (Fases)

### **FASE 1: Setup Inicial (Dia 1)**
- [ ] Criar projeto Next.js com TypeScript
- [ ] Configurar Tailwind CSS
- [ ] Instalar shadcn/ui
- [ ] Configurar Axios e variáveis de ambiente
- [ ] Criar estrutura de pastas
- [ ] Configurar tipos TypeScript básicos

**Resultado:** Projeto base funcionando

---

### **FASE 2: Autenticação (Dia 1-2)**
- [ ] Criar página de login
- [ ] Implementar sistema de auth com tokens
- [ ] Criar Zustand store para auth
- [ ] Implementar middleware de autenticação
- [ ] Criar hook `useAuth`
- [ ] Implementar persistência de token (localStorage)
- [ ] Criar rotas protegidas

**Resultado:** Login funcionando + Rotas protegidas

---

### **FASE 3: Layout e Navegação (Dia 2)**
- [ ] Criar componente Sidebar
- [ ] Criar componente Header com botão de logout
- [ ] Criar DashboardLayout
- [ ] Implementar navegação entre páginas
- [ ] Criar breadcrumbs
- [ ] Adicionar tema dark/light (opcional)

**Resultado:** Layout completo e navegação fluida

---

### **FASE 4: Dashboard (Dia 2-3)**
- [ ] Criar página Dashboard
- [ ] Implementar cards de métricas
- [ ] Criar gráficos (Receita, Distribuição)
- [ ] Buscar dados da API
- [ ] Adicionar loading states
- [ ] Implementar error handling

**Resultado:** Dashboard funcional com métricas

---

### **FASE 5: Gestão de Alunos (Dia 3-4)**
- [ ] Criar página de listagem de alunos
- [ ] Implementar filtros e busca
- [ ] Criar formulário de novo aluno
- [ ] Implementar máscara de telefone
- [ ] Criar página de edição de aluno
- [ ] Adicionar validações com Zod
- [ ] Implementar feedback visual (toasts)
- [ ] Adicionar paginação

**Resultado:** CRUD completo de alunos

---

### **FASE 6: Grade de Horários (Dia 4)**
- [ ] Criar página de horários
- [ ] Implementar grid visual de horários
- [ ] Criar formulário de horários
- [ ] Adicionar matrícula de alunos

**Resultado:** Gestão de horários funcional

---

### **FASE 7: Financeiro (Dia 4-5)**
- [ ] Criar página de pagamentos
- [ ] Implementar listagem de pagamentos
- [ ] Criar formulário de registro de pagamento
- [ ] Adicionar filtros por período
- [ ] Criar relatórios financeiros

**Resultado:** Gestão financeira completa

---

### **FASE 8: Gestão de Usuários (Dia 5)**
- [ ] Criar página de usuários
- [ ] Implementar CRUD de usuários
- [ ] Adicionar controle de roles

**Resultado:** Gestão de usuários funcional

---

### **FASE 9: Polish e Otimizações (Dia 5-6)**
- [ ] Adicionar loading skeletons
- [ ] Implementar error boundaries
- [ ] Otimizar imagens
- [ ] Adicionar animações (Framer Motion)
- [ ] Testar responsividade
- [ ] Melhorar acessibilidade
- [ ] Code review e refactoring

**Resultado:** Aplicação polida e otimizada

---

### **FASE 10: Deploy (Dia 6)**
- [ ] Configurar build de produção
- [ ] Deploy no Railway
- [ ] Configurar variáveis de ambiente
- [ ] Testar em produção
- [ ] Documentar deployment

**Resultado:** Sistema no ar em produção

---

## 🎨 Design System

### Cores Principais
```css
Primary: #1565C0 (Azul natação)
Secondary: #00952F (Verde aqua)
Success: #10B981
Warning: #F59E0B
Error: #EF4444
Background: #FFFFFF
Surface: #F9FAFB
Text: #111827
```

### Componentes Base (shadcn/ui)
- Button
- Input
- Card
- Table
- Dialog/Modal
- Select
- DatePicker
- Toast
- Tabs
- Badge
- Avatar

---

## 📦 Dependências Principais

```json
{
  "dependencies": {
    "next": "14.x",
    "react": "18.x",
    "react-dom": "18.x",
    "typescript": "5.x",
    "tailwindcss": "3.x",
    "axios": "^1.6.0",
    "zustand": "^4.4.0",
    "react-hook-form": "^7.48.0",
    "zod": "^3.22.0",
    "@hookform/resolvers": "^3.3.0",
    "react-hot-toast": "^2.4.0",
    "recharts": "^2.10.0",
    "@tanstack/react-table": "^8.10.0",
    "date-fns": "^2.30.0",
    "react-input-mask": "^2.0.4",
    "framer-motion": "^10.16.0"
  },
  "devDependencies": {
    "@types/node": "20.x",
    "@types/react": "18.x",
    "@types/react-dom": "18.x",
    "eslint": "8.x",
    "eslint-config-next": "14.x"
  }
}
```

---

## 🔄 Migração de Funcionalidades

### Mapeamento Streamlit → Next.js

| Streamlit | Next.js |
|-----------|---------|
| `st.session_state` | Zustand store |
| `st.rerun()` | `router.refresh()` |
| `st.form()` | React Hook Form |
| `st.error()` | React Hot Toast |
| `st.success()` | React Hot Toast |
| `st.balloons()` | Confetti library |
| `st.tabs()` | shadcn/ui Tabs |
| `st.columns()` | Tailwind grid |
| `st.metric()` | Custom StatCard |
| `st.plotly_chart()` | Recharts |

---

## 🚀 Deploy no Railway

### Configuração

1. **Criar novo serviço para frontend-next**
2. **Configurar variáveis:**
   ```
   NEXT_PUBLIC_API_URL=https://backend-production-xxxx.up.railway.app
   ```
3. **Build command:** `npm run build`
4. **Start command:** `npm start`
5. **Root directory:** `frontend-next`

---

## ⏱️ Timeline Estimado

- **Setup + Auth:** 1-2 dias
- **Layout + Dashboard:** 1 dia
- **CRUD Alunos:** 1-2 dias
- **Horários + Financeiro:** 1-2 dias
- **Usuários + Polish:** 1 dia
- **Deploy + Testes:** 1 dia

**TOTAL: 6-8 dias** para migração completa

---

## 🎯 Prioridades

### MVP (Mínimo Viável)
1. Login/Logout funcional
2. Dashboard com métricas
3. CRUD de Alunos (principal funcionalidade)
4. Gestão de Pagamentos

### Nice to Have (Depois)
1. Grade de Horários visual
2. Gestão de Usuários
3. Relatórios avançados
4. Notificações WhatsApp

---

## 📊 Comparação: Antes vs Depois

| Aspecto | Streamlit (Atual) | Next.js (Novo) |
|---------|-------------------|----------------|
| Performance | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| UX | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Customização | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Navegação | ⭐ | ⭐⭐⭐⭐⭐ |
| Manutenibilidade | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Autenticação | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| Deploy | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🚦 Próximos Passos

### Decisão Imediata
**Quer que eu comece a implementação agora?**

Se sim:
1. Vou criar o projeto Next.js
2. Implementar autenticação primeiro
3. Criar o layout base
4. Migrar funcionalidades aos poucos

**Ou prefere:**
- Manter Streamlit e apenas corrigir bugs?
- Ver um protótipo/demo do Next.js primeiro?

---

**Responda:**
- ✅ "Vamos migrar agora" → Começo a implementar
- 🤔 "Quero ver um exemplo primeiro" → Crio um protótipo pequeno
- 🛠️ "Corrige o Streamlit por agora" → Faço mais correções no atual

**Qual sua decisão?** 😊
