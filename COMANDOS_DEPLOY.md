# 🚀 Comandos para Deploy via CLI - Execute no seu Terminal

## ⚠️ IMPORTANTE
Execute estes comandos em um **terminal novo** (não neste ambiente), pois alguns comandos precisam de interação.

---

## 📋 PASSO 1: Adicionar PostgreSQL

**❗ Abra o dashboard web para adicionar PostgreSQL:**

```bash
open https://railway.com/project/5aae4303-99da-4180-b246-ece0f97ec1f7
```

No dashboard:
1. Clique em **"+ New"**
2. Selecione **"Database"**
3. Escolha **"Add PostgreSQL"**
4. Aguarde ~30 segundos

✅ Quando o PostgreSQL estiver criado, volte para o terminal e continue.

---

## 📋 PASSO 2: Deploy do Backend

```bash
cd /Users/yourapple/aquasystem/natacao-manager/backend
railway up
```

Quando perguntado pelo serviço, escolha criar um novo serviço chamado **"backend"**.

Aguarde o build e deploy (~2-3 minutos).

---

## 📋 PASSO 3: Configurar Variáveis do Backend

```bash
# Configurar SECRET_KEY
railway variables --set SECRET_KEY=a62f8c3619726a7e15c13ca998b77ebc4512e84ad1c62b34018f601db9f3d395

# Configurar ALGORITHM
railway variables --set ALGORITHM=HS256

# Configurar token expiration
railway variables --set ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Configurar ambiente
railway variables --set ENVIRONMENT=production
```

✅ Variáveis configuradas!

---

## 📋 PASSO 4: Conectar DATABASE_URL (via Dashboard)

**❗ Este passo deve ser feito no dashboard:**

1. Abra: https://railway.com/project/5aae4303-99da-4180-b246-ece0f97ec1f7
2. Clique no serviço **"backend"**
3. Vá na aba **"Variables"**
4. Clique em **"New Variable"** > **"Add Reference"**
5. Selecione **PostgreSQL** > **DATABASE_URL**

✅ DATABASE_URL conectada!

---

## 📋 PASSO 5: Obter URL do Backend

```bash
railway url
```

Copie a URL que aparecer (algo como: `backend-production-xxxx.up.railway.app`)

**Guarde esta URL para o próximo passo!**

---

## 📋 PASSO 6: Deploy do Frontend

```bash
cd /Users/yourapple/aquasystem/natacao-manager/frontend
railway up
```

Quando perguntado pelo serviço, escolha criar um novo serviço chamado **"frontend"**.

Aguarde o build e deploy (~2-3 minutos).

---

## 📋 PASSO 7: Configurar API_URL no Frontend

**Substitua `<BACKEND_URL>` pela URL que você copiou no PASSO 5:**

```bash
railway variables --set API_URL=https://<BACKEND_URL>
```

Exemplo:
```bash
railway variables --set API_URL=https://backend-production-xxxx.up.railway.app
```

✅ API_URL configurada!

---

## 📋 PASSO 8: Obter URL do Frontend

```bash
railway url
```

Copie a URL que aparecer (algo como: `frontend-production-xxxx.up.railway.app`)

**Guarde esta URL para o próximo passo!**

---

## 📋 PASSO 9: Configurar CORS no Backend

**Substitua `<FRONTEND_URL>` pela URL que você copiou no PASSO 8:**

```bash
cd /Users/yourapple/aquasystem/natacao-manager/backend
railway variables --set ALLOWED_ORIGINS=https://<FRONTEND_URL>
```

Exemplo:
```bash
railway variables --set ALLOWED_ORIGINS=https://frontend-production-xxxx.up.railway.app
```

✅ CORS configurado!

---

## 📋 PASSO 10: Reiniciar Backend

```bash
railway restart
```

Aguarde ~30 segundos para o backend reiniciar.

---

## 🎉 DEPLOY CONCLUÍDO!

### 📊 Verificar Status

```bash
cd /Users/yourapple/aquasystem/natacao-manager
railway status
```

### 📋 Ver Logs

```bash
# Logs do backend
cd /Users/yourapple/aquasystem/natacao-manager/backend
railway logs

# Logs do frontend
cd /Users/yourapple/aquasystem/natacao-manager/frontend
railway logs
```

### 🌐 Acessar o Sistema

Abra a URL do frontend no navegador e faça login:
- **Email:** admin@natacao.com
- **Senha:** admin123
- **❗ ALTERE A SENHA IMEDIATAMENTE!**

---

## 🔗 Links Úteis

- **Dashboard Railway:** https://railway.com/project/5aae4303-99da-4180-b246-ece0f97ec1f7
- **Repositório GitHub:** https://github.com/revolutedigital/aquasystem

---

## 💡 Comandos Úteis

### Verificar variáveis configuradas
```bash
# Backend
cd /Users/yourapple/aquasystem/natacao-manager/backend
railway variables

# Frontend
cd /Users/yourapple/aquasystem/natacao-manager/frontend
railway variables
```

### Abrir serviço no navegador
```bash
railway open
```

### Ver domínios/URLs
```bash
railway domain
```

---

## 🐛 Troubleshooting

### Backend não inicia
```bash
cd /Users/yourapple/aquasystem/natacao-manager/backend
railway logs
```

Verifique se:
- DATABASE_URL está configurada
- Todas as variáveis foram definidas

### Frontend não conecta
```bash
cd /Users/yourapple/aquasystem/natacao-manager/frontend
railway logs
```

Verifique se:
- API_URL está configurada com HTTPS
- Backend está rodando

### Redeployar um serviço
```bash
# Backend
cd /Users/yourapple/aquasystem/natacao-manager/backend
railway up --detach

# Frontend
cd /Users/yourapple/aquasystem/natacao-manager/frontend
railway up --detach
```

---

**🎯 Pronto! Agora é só executar os comandos acima no seu terminal!**
