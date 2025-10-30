# 🚀 Deploy AGORA pelo Dashboard Railway

> ✅ Projeto Railway já criado: **natacao-manager**
> 🔗 URL: https://railway.com/project/5aae4303-99da-4180-b246-ece0f97ec1f7

## 📋 PASSOS PARA DEPLOY (10 minutos)

### 1️⃣ Abrir Dashboard (JÁ CRIADO!) ✅

Abra no navegador:
```
https://railway.com/project/5aae4303-99da-4180-b246-ece0f97ec1f7
```

Ou visite: https://railway.app e selecione o projeto **natacao-manager**

---

### 2️⃣ Adicionar PostgreSQL

1. Clique em **"+ New"** (canto superior direito)
2. Selecione **"Database"**
3. Escolha **"Add PostgreSQL"**
4. Aguarde o PostgreSQL ser provisionado (~30 segundos)

✅ **PostgreSQL criado automaticamente!**

---

### 3️⃣ Adicionar Backend (FastAPI)

1. Clique em **"+ New"** novamente
2. Selecione **"Empty Service"**
3. Clique nos 3 pontinhos (...) no card do serviço
4. Selecione **"Settings"**
5. Em **"Service Name"**, coloque: `backend`
6. Volte para a aba **"Settings"**
7. Role até **"Source"**
8. Clique em **"Connect Repo"** ou **"Deploy from GitHub"**
9. **OU** selecione **"Deploy from local directory"**
   - Se escolher local, use o Railway CLI:
   ```bash
   cd /Users/yourapple/aquasystem/natacao-manager/backend
   railway link 5aae4303-99da-4180-b246-ece0f97ec1f7
   railway up
   ```

**Configurar variáveis do Backend:**

1. No card do **backend**, clique em **"Variables"**
2. Adicione as seguintes variáveis:

```
SECRET_KEY = [clique em "Generate" ou cole: resultado de openssl rand -hex 32]
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
ENVIRONMENT = production
```

3. **DATABASE_URL** será adicionada automaticamente pelo Railway quando você conectar o PostgreSQL

**Conectar ao PostgreSQL:**

1. Ainda na aba Variables do backend
2. Clique em **"Reference"** ou **"New Variable"**
3. Selecione **"Add Reference"**
4. Escolha o serviço **PostgreSQL**
5. Selecione a variável **DATABASE_URL**
6. Isso cria automaticamente `${{Postgres.DATABASE_URL}}`

---

### 4️⃣ Adicionar Frontend (Streamlit)

1. Clique em **"+ New"** novamente
2. Selecione **"Empty Service"**
3. Nomeie como: `frontend`
4. Configure da mesma forma que o backend

**Configurar variáveis do Frontend:**

1. No card do **frontend**, clique em **"Variables"**
2. Aguarde o backend ter URL gerada
3. Copie a URL do backend (está em Settings > Domains)
4. Adicione a variável:

```
API_URL = https://backend-production-XXXX.up.railway.app
```

(Substitua pela URL real do backend)

---

### 5️⃣ Deploy Usando GitHub (RECOMENDADO)

**Se você tem o código no GitHub:**

1. Conecte o repositório ao Railway
2. Para o **backend**:
   - Root Directory: `backend`
   - Dockerfile: `Dockerfile`
3. Para o **frontend**:
   - Root Directory: `frontend`
   - Dockerfile: `Dockerfile`

**Railway irá automaticamente:**
- ✅ Detectar os Dockerfiles
- ✅ Fazer build das imagens
- ✅ Deploy automático
- ✅ Gerar URLs públicas

---

### 6️⃣ Configurar ALLOWED_ORIGINS

Depois que o frontend tiver URL:

1. Vá em **backend** > **Variables**
2. Adicione:

```
ALLOWED_ORIGINS = https://frontend-production-XXXX.up.railway.app
```

3. Clique em **"Restart"** no backend

---

## 🎯 ALTERNATIVA: Deploy via CLI Local

Se preferir usar a CLI (fora do ambiente atual):

```bash
# Passo 1: Linkar ao projeto
railway link 5aae4303-99da-4180-b246-ece0f97ec1f7

# Passo 2: Criar serviço PostgreSQL via dashboard web
# (não funciona bem via CLI sem TTY)

# Passo 3: Deploy backend
cd backend
railway up --service backend

# Passo 4: Configurar variáveis backend
railway variables set SECRET_KEY=$(openssl rand -hex 32) --service backend
railway variables set ALGORITHM=HS256 --service backend
railway variables set ACCESS_TOKEN_EXPIRE_MINUTES=1440 --service backend
railway variables set ENVIRONMENT=production --service backend

# Passo 5: Deploy frontend
cd ../frontend
railway up --service frontend

# Passo 6: Obter URL do backend
BACKEND_URL=$(railway url --service backend)

# Passo 7: Configurar API_URL no frontend
railway variables set API_URL=https://$BACKEND_URL --service frontend

# Passo 8: Configurar CORS no backend
FRONTEND_URL=$(railway url --service frontend)
railway variables set ALLOWED_ORIGINS=https://$FRONTEND_URL --service backend
railway restart --service backend
```

---

## 📊 Verificar Status

Depois do deploy:

1. **Backend**: https://railway.com/project/5aae4303-99da-4180-b246-ece0f97ec1f7
2. Clique em cada serviço para ver:
   - ✅ Status: Running
   - ✅ Logs (aba "Logs")
   - ✅ URL pública (aba "Settings" > "Domains")

---

## 🎉 Acessar o Sistema

1. Copie a URL do **frontend** (algo como: https://frontend-production-XXXX.up.railway.app)
2. Abra no navegador
3. Faça login:
   - Email: `admin@natacao.com`
   - Senha: `admin123`
4. **ALTERE A SENHA IMEDIATAMENTE!**

---

## 🐛 Troubleshooting

### Backend não inicia

**Ver logs:**
```bash
railway logs --service backend
```

Ou no dashboard: Backend > Logs

### Frontend não conecta ao backend

1. Verifique a variável `API_URL` no frontend
2. Deve ser **HTTPS**, não HTTP
3. Copie exatamente a URL do backend

### PostgreSQL

Se precisar acessar:
```bash
railway connect postgres
```

---

## 💰 Custo

Seu projeto atual:
- Backend: ~$3/mês
- Frontend: ~$3/mês
- PostgreSQL: ~$5/mês
- **Total: ~$11/mês**

---

## 📞 Próximos Passos

1. ✅ Projeto criado: **natacao-manager**
2. ⏳ Adicionar PostgreSQL (dashboard)
3. ⏳ Deploy backend (dashboard ou CLI)
4. ⏳ Deploy frontend (dashboard ou CLI)
5. ⏳ Configurar variáveis
6. ⏳ Testar sistema

**Abra agora:** https://railway.com/project/5aae4303-99da-4180-b246-ece0f97ec1f7

---

**🔗 Link do Projeto:** https://railway.com/project/5aae4303-99da-4180-b246-ece0f97ec1f7
