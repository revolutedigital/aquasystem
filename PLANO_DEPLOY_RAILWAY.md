# 🚂 Plano de Deploy - Railway

> Deploy automatizado do Sistema de Gestão de Natação na plataforma Railway

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Pré-requisitos](#pré-requisitos)
3. [Arquitetura no Railway](#arquitetura-no-railway)
4. [Configuração Passo a Passo](#configuração-passo-a-passo)
5. [Variáveis de Ambiente](#variáveis-de-ambiente)
6. [Deploy Automático](#deploy-automático)
7. [Monitoramento](#monitoramento)
8. [Custos Estimados](#custos-estimados)

---

## 🎯 Visão Geral

O Railway é uma plataforma PaaS (Platform as a Service) que simplifica o deploy de aplicações containerizadas. Vamos deployar 3 serviços:

- **Backend** (FastAPI) - API REST
- **Frontend** (Streamlit) - Interface web
- **PostgreSQL** - Banco de dados (Railway Postgres)

### Vantagens do Railway:
✅ Deploy automático via Git
✅ PostgreSQL gerenciado (backups automáticos)
✅ SSL/HTTPS automático
✅ Logs centralizados
✅ Escalabilidade automática
✅ Zero configuração de infraestrutura

---

## ✅ Pré-requisitos

- [x] Railway CLI instalado
- [ ] Conta Railway criada (https://railway.app)
- [ ] Repositório Git com o código
- [ ] GitHub/GitLab conectado ao Railway

### Verificar Railway CLI:
```bash
railway --version
# Deve mostrar: railwaycli version X.X.X

# Fazer login
railway login
```

---

## 🏗️ Arquitetura no Railway

```
┌─────────────────────────────────────────────────┐
│              RAILWAY PROJECT                    │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────┐  ┌──────────────┐            │
│  │   Backend    │  │   Frontend   │            │
│  │   FastAPI    │  │  Streamlit   │            │
│  │  (Container) │  │  (Container) │            │
│  │              │  │              │            │
│  │ Port: 9000   │  │ Port: 8501   │            │
│  └──────┬───────┘  └──────────────┘            │
│         │                                       │
│         │ DATABASE_URL                          │
│         ▼                                       │
│  ┌──────────────┐                              │
│  │  PostgreSQL  │                              │
│  │   (Railway   │                              │
│  │   Managed)   │                              │
│  └──────────────┘                              │
│                                                 │
│  Domínios públicos:                            │
│  - backend-xxxxx.up.railway.app                │
│  - frontend-xxxxx.up.railway.app               │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 🔧 Configuração Passo a Passo

### Passo 1: Criar Projeto no Railway

```bash
# No diretório do projeto
cd /Users/yourapple/aquasystem/natacao-manager

# Inicializar projeto Railway
railway init

# Selecionar: "Create new project"
# Nome sugerido: natacao-manager
```

### Passo 2: Adicionar PostgreSQL

```bash
# Adicionar PostgreSQL ao projeto
railway add --database postgres

# Railway irá:
# ✅ Criar banco PostgreSQL
# ✅ Gerar DATABASE_URL automaticamente
# ✅ Configurar backups automáticos
```

### Passo 3: Deploy do Backend

```bash
# Criar serviço backend
railway up -s backend -d ./backend

# Railway irá:
# ✅ Detectar Dockerfile
# ✅ Fazer build da imagem
# ✅ Fazer deploy
# ✅ Gerar domínio público
```

### Passo 4: Configurar Variáveis do Backend

```bash
# Gerar SECRET_KEY
export SECRET_KEY=$(openssl rand -hex 32)

# Configurar variáveis no Railway
railway variables set SECRET_KEY=$SECRET_KEY -s backend
railway variables set ALGORITHM=HS256 -s backend
railway variables set ACCESS_TOKEN_EXPIRE_MINUTES=1440 -s backend

# DATABASE_URL é injetada automaticamente pelo Railway
```

### Passo 5: Deploy do Frontend

```bash
# Criar serviço frontend
railway up -s frontend -d ./frontend

# Obter URL do backend
BACKEND_URL=$(railway url -s backend)

# Configurar variável do frontend
railway variables set API_URL=$BACKEND_URL -s frontend
```

### Passo 6: Configurar Domínios Customizados (Opcional)

```bash
# Adicionar domínio ao backend
railway domain add api.seu-dominio.com -s backend

# Adicionar domínio ao frontend
railway domain add app.seu-dominio.com -s frontend

# Configurar DNS:
# - Criar registro CNAME apontando para o domínio Railway
# - Railway configura SSL automaticamente
```

---

## 🔐 Variáveis de Ambiente

### Backend (FastAPI)

| Variável | Descrição | Valor | Obrigatório |
|----------|-----------|-------|-------------|
| `DATABASE_URL` | URL do PostgreSQL | *Auto-injetada pelo Railway* | ✅ |
| `SECRET_KEY` | Chave JWT | `openssl rand -hex 32` | ✅ |
| `ALGORITHM` | Algoritmo JWT | `HS256` | ✅ |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiração token | `1440` (24h) | ✅ |
| `ALLOWED_ORIGINS` | CORS origins | `https://frontend-xxx.railway.app` | ✅ |
| `ENVIRONMENT` | Ambiente | `production` | ✅ |
| `EVOLUTION_API_URL` | WhatsApp API | `https://sua-api.com` | ⚪ |
| `EVOLUTION_API_KEY` | Chave WhatsApp | `sua_chave` | ⚪ |
| `EVOLUTION_INSTANCE_NAME` | Instância WhatsApp | `natacao` | ⚪ |

### Frontend (Streamlit)

| Variável | Descrição | Valor | Obrigatório |
|----------|-----------|-------|-------------|
| `API_URL` | URL do Backend | `https://backend-xxx.railway.app` | ✅ |

---

## 🚀 Deploy Automático

### Configurar Deploy Contínuo (CI/CD)

O Railway faz deploy automático quando você faz push para o repositório:

```bash
# 1. Conectar repositório Git ao Railway
railway link

# 2. Configurar branch de deploy
railway environment create production

# 3. Fazer push para deployar
git push origin main

# Railway irá automaticamente:
# ✅ Detectar mudanças
# ✅ Fazer rebuild dos containers
# ✅ Fazer deploy sem downtime
```

### Script de Deploy Manual

**Arquivo:** `scripts/deploy-railway.sh`

```bash
#!/bin/bash
set -e

echo "🚂 Iniciando deploy no Railway..."

# Verificar Railway CLI
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI não encontrado. Instale: npm i -g @railway/cli"
    exit 1
fi

# Backend
echo "📦 Fazendo deploy do Backend..."
cd backend
railway up -s backend
cd ..

# Frontend
echo "🎨 Fazendo deploy do Frontend..."
cd frontend
railway up -s frontend
cd ..

# Obter URLs
BACKEND_URL=$(railway url -s backend)
FRONTEND_URL=$(railway url -s frontend)

echo ""
echo "✅ Deploy concluído!"
echo ""
echo "📍 URLs dos serviços:"
echo "   Backend:  $BACKEND_URL"
echo "   Frontend: $FRONTEND_URL"
echo ""
echo "📊 Ver logs:"
echo "   railway logs -s backend"
echo "   railway logs -s frontend"
```

---

## 📊 Monitoramento

### Ver Logs em Tempo Real

```bash
# Logs do backend
railway logs -s backend -f

# Logs do frontend
railway logs -s frontend -f

# Logs do PostgreSQL
railway logs -s postgres -f
```

### Métricas e Status

```bash
# Ver status dos serviços
railway status

# Ver uso de recursos
railway metrics -s backend
railway metrics -s frontend

# Ver informações do banco
railway variables -s postgres
```

### Health Checks

O Railway monitora automaticamente:
- ✅ Status HTTP dos containers
- ✅ Uso de CPU e memória
- ✅ Restarts automáticos em caso de falha

### Acessar Banco de Dados

```bash
# Conectar via psql
railway connect postgres

# Ou obter credenciais
railway variables -s postgres

# Usar com ferramenta externa (DBeaver, pgAdmin)
PGHOST=$(railway variables get PGHOST -s postgres)
PGPORT=$(railway variables get PGPORT -s postgres)
PGUSER=$(railway variables get PGUSER -s postgres)
PGPASSWORD=$(railway variables get PGPASSWORD -s postgres)
PGDATABASE=$(railway variables get PGDATABASE -s postgres)
```

---

## 💰 Custos Estimados

### Plano Gratuito (Hobby)
- **Crédito mensal:** $5
- **Limites:**
  - 512MB RAM por serviço
  - 1GB disco por serviço
  - 100GB tráfego/mês

**Adequado para:** Testes e desenvolvimento

### Plano Starter ($20/mês)
- **Créditos:** $20/mês incluídos
- **Limites:**
  - 8GB RAM por serviço
  - 100GB disco
  - Tráfego ilimitado

**Adequado para:** Produção de pequenas academias (até 100 alunos)

### Estimativa para o Sistema:
```
Backend:    ~256MB RAM, 1GB disco   = ~$3/mês
Frontend:   ~256MB RAM, 1GB disco   = ~$3/mês
PostgreSQL: ~256MB RAM, 2GB disco   = ~$5/mês
────────────────────────────────────────────
Total:                                ~$11/mês
```

**Cabe tranquilamente no plano Starter!**

---

## 🔒 Segurança

### O que o Railway faz automaticamente:
✅ SSL/TLS (HTTPS) em todos os domínios
✅ Isolamento de rede entre serviços
✅ Backups automáticos do PostgreSQL
✅ Variáveis de ambiente criptografadas
✅ Proteção DDoS básica

### O que VOCÊ deve fazer:
- [ ] Alterar senha padrão do admin após primeiro deploy
- [ ] Configurar ALLOWED_ORIGINS corretamente
- [ ] Usar SECRET_KEY forte (32+ caracteres)
- [ ] Nunca commitar .env no Git
- [ ] Revisar logs regularmente

---

## 🐛 Troubleshooting

### Problema: Build falha no Railway

**Solução:**
```bash
# Ver logs de build
railway logs -s backend --build

# Verificar Dockerfile
cat backend/Dockerfile

# Testar build local
docker build -t test ./backend
```

### Problema: Backend não conecta no banco

**Solução:**
```bash
# Verificar DATABASE_URL
railway variables -s backend | grep DATABASE_URL

# Testar conexão
railway run -s backend "python -c 'from app.database import engine; print(engine)'"
```

### Problema: Frontend não conecta no backend

**Solução:**
```bash
# Verificar API_URL
railway variables -s frontend | grep API_URL

# Deve ser: https://backend-xxxxx.up.railway.app (não http://)

# Corrigir se necessário
BACKEND_URL=$(railway url -s backend)
railway variables set API_URL=$BACKEND_URL -s frontend

# Restart frontend
railway restart -s frontend
```

### Problema: Erro 502 Bad Gateway

**Causas comuns:**
1. Backend não está escutando na porta correta
2. Health check falhando
3. Backend crashando no startup

**Solução:**
```bash
# Ver logs
railway logs -s backend -f

# Verificar variável PORT
railway variables set PORT=9000 -s backend

# Verificar comando do Dockerfile
# Deve ter: --host 0.0.0.0 --port ${PORT:-9000}
```

---

## 📚 Comandos Úteis

```bash
# Ver todos os serviços
railway status

# Restart de serviço
railway restart -s backend

# Abrir dashboard web
railway open

# Ver variáveis de ambiente
railway variables -s backend

# Adicionar variável
railway variables set KEY=value -s backend

# Remover variável
railway variables delete KEY -s backend

# Baixar variáveis para .env
railway variables > .env.railway

# Executar comando no container
railway run -s backend "python -m pytest"

# Abrir shell no container
railway shell -s backend

# Ver uso de recursos
railway metrics -s backend

# Deletar serviço (CUIDADO!)
railway service delete backend
```

---

## 🎯 Checklist de Deploy

### Pré-Deploy
- [ ] Railway CLI instalado e logado
- [ ] Código commitado no Git
- [ ] Testes passando localmente
- [ ] Dockerfiles testados localmente

### Deploy Inicial
- [ ] Projeto Railway criado (`railway init`)
- [ ] PostgreSQL adicionado (`railway add postgres`)
- [ ] Backend deployado (`railway up -s backend`)
- [ ] Frontend deployado (`railway up -s frontend`)
- [ ] Variáveis de ambiente configuradas
- [ ] ALLOWED_ORIGINS configurado com URLs Railway
- [ ] SECRET_KEY forte configurada

### Pós-Deploy
- [ ] Testar acesso ao frontend
- [ ] Testar login no sistema
- [ ] Testar criação de aluno
- [ ] Testar criação de horário
- [ ] Testar registro de pagamento
- [ ] Alterar senha padrão do admin
- [ ] Configurar domínios customizados (opcional)
- [ ] Documentar URLs de produção

### Monitoramento
- [ ] Verificar logs sem erros
- [ ] Monitorar uso de recursos
- [ ] Configurar alertas (Railway Dashboard)
- [ ] Testar health checks
- [ ] Documentar processo de rollback

---

## 🚀 Deploy Rápido (TL;DR)

```bash
# 1. Login
railway login

# 2. Criar projeto
railway init

# 3. Adicionar PostgreSQL
railway add postgres

# 4. Deploy backend
cd backend
railway up -s backend
railway variables set SECRET_KEY=$(openssl rand -hex 32) -s backend
cd ..

# 5. Deploy frontend
cd frontend
railway up -s frontend
BACKEND_URL=$(railway url -s backend)
railway variables set API_URL=$BACKEND_URL -s frontend
cd ..

# 6. Abrir aplicação
railway open -s frontend
```

**Pronto! Sistema no ar em ~5 minutos! 🎉**

---

## 📞 Suporte

- **Railway Docs:** https://docs.railway.app
- **Railway Discord:** https://discord.gg/railway
- **Status Page:** https://status.railway.app

---

**Criado para deploy do Sistema de Gestão de Natação**
*Versão 1.0 - Otimizado para Railway*
