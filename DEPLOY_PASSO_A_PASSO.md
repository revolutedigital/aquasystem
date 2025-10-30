# 🚀 Deploy Railway - Passo a Passo Simplificado

**Projeto:** natacao-manager
**URL do Projeto:** https://railway.com/project/5aae4303-99da-4180-b246-ece0f97ec1f7

---

## ⚡ OPÇÃO 1: Executar Script Automatizado

Abra um novo terminal (com suporte a TTY) e execute:

```bash
cd /Users/yourapple/aquasystem/natacao-manager
./DEPLOY_RAILWAY_COMMANDS.sh
```

O script irá guiá-lo por todos os passos necessários.

---

## 📋 OPÇÃO 2: Comandos Manuais

Se preferir executar manualmente, siga os passos abaixo:

### 1️⃣ Adicionar PostgreSQL (via Dashboard Web)

**❗ Este passo DEVE ser feito pelo dashboard:**

1. Abra: https://railway.com/project/5aae4303-99da-4180-b246-ece0f97ec1f7
2. Clique em **"+ New"** (canto superior direito)
3. Selecione **"Database"**
4. Escolha **"Add PostgreSQL"**
5. Aguarde ~30 segundos para provisionamento

✅ PostgreSQL criado!

---

### 2️⃣ Deploy do Backend

Abra um terminal e execute:

```bash
cd /Users/yourapple/aquasystem/natacao-manager/backend
railway up --service backend
```

Aguarde o build e deploy (~2-3 minutos).

---

### 3️⃣ Configurar Variáveis do Backend

```bash
# Gerar e configurar SECRET_KEY
railway variables --set SECRET_KEY=a62f8c3619726a7e15c13ca998b77ebc4512e84ad1c62b34018f601db9f3d395 --service backend

# Configurar outras variáveis
railway variables --set ALGORITHM=HS256 --service backend
railway variables --set ACCESS_TOKEN_EXPIRE_MINUTES=1440 --service backend
railway variables --set ENVIRONMENT=production --service backend
```

---

### 4️⃣ Conectar PostgreSQL ao Backend (via Dashboard)

**❗ Este passo DEVE ser feito pelo dashboard:**

1. Vá para: https://railway.com/project/5aae4303-99da-4180-b246-ece0f97ec1f7
2. Clique no serviço **"backend"**
3. Vá na aba **"Variables"**
4. Clique em **"New Variable"** > **"Add Reference"**
5. Selecione o serviço **PostgreSQL**
6. Selecione a variável **DATABASE_URL**

Isso criará automaticamente `${{Postgres.DATABASE_URL}}`

✅ Banco conectado!

---

### 5️⃣ Obter URL do Backend

```bash
railway url --service backend
```

Copie a URL (será algo como: `backend-production-xxxx.up.railway.app`)

---

### 6️⃣ Deploy do Frontend

```bash
cd /Users/yourapple/aquasystem/natacao-manager/frontend
railway up --service frontend
```

Aguarde o build e deploy (~2-3 minutos).

---

### 7️⃣ Configurar API_URL no Frontend

Substitua `<BACKEND_URL>` pela URL copiada no passo 5:

```bash
railway variables --set API_URL=https://<BACKEND_URL> --service frontend
```

Exemplo:
```bash
railway variables --set API_URL=https://backend-production-xxxx.up.railway.app --service frontend
```

---

### 8️⃣ Obter URL do Frontend

```bash
railway url --service frontend
```

Copie a URL (será algo como: `frontend-production-xxxx.up.railway.app`)

---

### 9️⃣ Configurar CORS no Backend

Substitua `<FRONTEND_URL>` pela URL copiada no passo 8:

```bash
railway variables --set ALLOWED_ORIGINS=https://<FRONTEND_URL> --service backend
```

Exemplo:
```bash
railway variables --set ALLOWED_ORIGINS=https://frontend-production-xxxx.up.railway.app --service backend
```

---

### 🔄 Reiniciar Backend para Aplicar CORS

```bash
railway restart --service backend
```

---

## ✅ DEPLOY CONCLUÍDO!

### 📊 Verificar Status

```bash
railway status
```

### 📋 Ver Logs

```bash
# Logs do backend
railway logs --service backend

# Logs do frontend
railway logs --service frontend
```

### 🌐 Acessar o Sistema

1. Abra a URL do frontend no navegador
2. Faça login com:
   - **Email:** `admin@natacao.com`
   - **Senha:** `admin123`
3. **❗ ALTERE A SENHA IMEDIATAMENTE!**

---

## 🐛 Troubleshooting

### Backend não inicia

Verifique os logs:
```bash
railway logs --service backend
```

Causas comuns:
- DATABASE_URL não configurada
- Erro nas migrações do banco

### Frontend não conecta ao backend

Verifique:
1. A variável `API_URL` está configurada?
2. A URL é **HTTPS** (não HTTP)?
3. O backend está rodando?

### Verificar variáveis configuradas

```bash
# Backend
railway variables --service backend

# Frontend
railway variables --service frontend
```

---

## 📞 Informações Adicionais

### 🔑 SECRET_KEY Gerada

```
a62f8c3619726a7e15c13ca998b77ebc4512e84ad1c62b34018f601db9f3d395
```

### 🌐 Links Úteis

- **Dashboard do Projeto:** https://railway.com/project/5aae4303-99da-4180-b246-ece0f97ec1f7
- **Documentação Railway:** https://docs.railway.app/
- **CLI Reference:** https://docs.railway.app/develop/cli

### 💰 Custos Estimados

- Backend: ~$3/mês
- Frontend: ~$3/mês
- PostgreSQL: ~$5/mês
- **Total: ~$11/mês**

Railway oferece $5 de crédito grátis mensalmente.

---

## 🎯 Checklist de Deploy

- [ ] PostgreSQL adicionado pelo dashboard
- [ ] Backend deployado (`railway up --service backend`)
- [ ] Variáveis do backend configuradas
- [ ] DATABASE_URL conectada ao backend
- [ ] Frontend deployado (`railway up --service frontend`)
- [ ] API_URL configurada no frontend
- [ ] ALLOWED_ORIGINS configurada no backend
- [ ] Backend reiniciado
- [ ] Sistema testado e funcionando
- [ ] Senha padrão alterada

---

**🔗 Link do Projeto:** https://railway.com/project/5aae4303-99da-4180-b246-ece0f97ec1f7
