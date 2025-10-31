# 🚀 DEPLOY COMPLETO NO RAILWAY - MANTENDO O BANCO

## ⚠️ IMPORTANTE: NÃO DELETE O BANCO PostgreSQL!

### O que fazer com cada serviço:

1. **PostgreSQL** → **MANTER** (tem seus dados!)
2. **Backend** → **MANTER** (já está funcionando)
3. **Frontend (Streamlit)** → **REMOVER** ou **PARAR**
4. **Frontend-Next** → **CRIAR NOVO**

---

## 📋 PASSO A PASSO COMPLETO

### 1️⃣ No Railway Dashboard

Você deve ter 3 serviços:
- ✅ **PostgreSQL** (NÃO MEXER - tem seus dados)
- ✅ **Backend** (FastAPI - já funcionando)
- ❌ **Frontend** (Streamlit - vamos remover)

### 2️⃣ Remover apenas o Streamlit

1. Clique no serviço **Frontend (Streamlit)**
2. Vá em **Settings**
3. Role até **Danger Zone**
4. Clique em **Remove Service**
5. Confirme a remoção

### 3️⃣ Adicionar o Frontend Next.js

No mesmo projeto Railway:

1. Clique em **"+ New"** → **"GitHub Repo"**
2. Selecione: `revolutedigital/aquasystem`
3. **IMPORTANTE**: Após conectar:
   - Clique em **Settings**
   - Em **Service Name**, coloque: `frontend-next`
   - Em **Root Directory**, coloque: `frontend-next`
   - Clique **Save**

4. Vá em **Variables** e adicione:
```
NEXT_PUBLIC_API_URL=https://backend-production-33ee.up.railway.app
```

5. O deploy vai começar automaticamente!

---

## 🔄 ALTERNATIVA: Criar Projeto Novo (Mantendo Dados)

Se preferir começar limpo mas MANTER OS DADOS:

### Opção A: Exportar/Importar Banco

1. **ANTES de deletar**, exporte os dados:
```bash
# No Railway, vá no PostgreSQL, copie a DATABASE_URL
pg_dump "SUA_DATABASE_URL_AQUI" > backup_natacao.sql
```

2. Crie novo projeto com 3 serviços:
   - PostgreSQL (novo)
   - Backend
   - Frontend-Next

3. Importe os dados:
```bash
psql "NOVA_DATABASE_URL" < backup_natacao.sql
```

### Opção B: Manter Projeto Atual (RECOMENDADO)

**Esta é a melhor opção** - apenas:
1. Remove o Streamlit
2. Adiciona o Frontend-Next
3. Mantém PostgreSQL e Backend intactos

---

## ✅ Resumo do que você tem agora:

### Serviços que devem ficar no Railway:

1. **PostgreSQL**
   - Status: ✅ Mantém como está
   - Dados: Preservados

2. **Backend (FastAPI)**
   - URL: https://backend-production-33ee.up.railway.app
   - Status: ✅ Funcionando
   - Variáveis: DATABASE_URL (já configurada)

3. **Frontend-Next** (NOVO)
   - URL: Será gerada após deploy
   - Root Directory: `frontend-next`
   - Variável: NEXT_PUBLIC_API_URL

---

## 🎯 Comando Rápido

Se quiser ver o status atual no Railway:

```bash
railway status
```

## 💡 Dica

NÃO precisa criar projeto novo! Apenas:
1. Remove Streamlit
2. Adiciona Frontend-Next no mesmo projeto
3. Banco e Backend continuam funcionando

Os dados dos alunos que você cadastrou estão no PostgreSQL - não perca eles!