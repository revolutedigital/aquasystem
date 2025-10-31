# 🔧 Corrigir Erro ao Salvar no Banco

## 🔍 Diagnóstico do Problema

O erro pode ter 2 causas principais:

1. **CORS bloqueando requisições** do frontend para o backend
2. **DATABASE_URL com formato incorreto** do Railway

---

## ✅ SOLUÇÃO 1: Verificar e Corrigir CORS

### Passo 1: Ver logs do backend

1. Acesse o dashboard do Railway: https://railway.com/project/5aae4303-99da-4180-b246-ece0f97ec1f7
2. Clique no serviço **backend**
3. Vá na aba **"Logs"**
4. Procure por erros relacionados a CORS como:
   ```
   CORS policy: No 'Access-Control-Allow-Origin' header
   ```

### Passo 2: Verificar variável ALLOWED_ORIGINS

1. No serviço **backend**, vá na aba **"Variables"**
2. Procure a variável **ALLOWED_ORIGINS**
3. Ela deve ter a URL do frontend, algo como:
   ```
   https://front-production-e008.up.railway.app
   ```

### Passo 3: Atualizar ALLOWED_ORIGINS (se necessário)

Se a variável estiver incorreta:

1. Vá no serviço **front**
2. Copie a URL completa (Settings > Domains)
3. Volte no serviço **backend** > Variables
4. Edite **ALLOWED_ORIGINS** e coloque a URL do frontend com **HTTPS**
5. Exemplo: `https://front-production-e008.up.railway.app`
6. Salve e aguarde o redeploy (~1 minuto)

---

## ✅ SOLUÇÃO 2: Verificar DATABASE_URL

### Passo 1: Ver formato da DATABASE_URL

1. No serviço **backend**, vá na aba **"Variables"**
2. Localize a variável **DATABASE_URL**
3. Ela deve estar apontando para o PostgreSQL

### Passo 2: Verificar se está referenciando o PostgreSQL

A variável DATABASE_URL deve ser uma **referência** ao PostgreSQL, não um valor manual.

Deve aparecer algo como:
```
${{Postgres.DATABASE_URL}}
```

**Se não estiver assim:**

1. Delete a variável DATABASE_URL atual
2. Clique em **"New Variable"** > **"Add Reference"**
3. Selecione **PostgreSQL**
4. Selecione **DATABASE_URL**
5. Salve

### Passo 3: Verificar formato da URL (Railway usa formato especial)

O Railway às vezes usa formato `postgresql://` mas o Python SQLAlchemy precisa de `postgresql+psycopg2://`.

**Vou criar um fix para isso automaticamente.**

---

## ✅ SOLUÇÃO 3: Verificar se PostgreSQL está rodando

1. No dashboard do Railway
2. Verifique se o serviço **PostgreSQL** está com status **"Running"** (verde)
3. Se estiver vermelho ou amarelo, há um problema

---

## ✅ SOLUÇÃO 4: Verificar logs detalhados

### Ver logs do backend:

1. Serviço **backend** > aba **"Logs"**
2. Procure por erros como:
   - `Connection refused`
   - `Could not connect to database`
   - `CORS error`
   - `No 'Access-Control-Allow-Origin'`

### Ver logs do frontend:

1. Serviço **front** > aba **"Logs"**
2. Procure por erros de conexão com a API

---

## 🔧 FIX RÁPIDO: Atualizar código do backend

Vou atualizar o código para:
1. **Aceitar múltiplas origens** no CORS
2. **Converter automaticamente** DATABASE_URL do Railway
3. **Adicionar logs** melhores para debug

---

## 📋 Checklist de Verificação

Execute estas verificações na ordem:

- [ ] PostgreSQL está com status "Running" (verde)
- [ ] Variável DATABASE_URL está configurada como referência ao Postgres
- [ ] Variável ALLOWED_ORIGINS tem a URL do frontend com HTTPS
- [ ] Backend está com status "Running" (verde)
- [ ] Frontend está com status "Running" (verde)
- [ ] Variável API_URL no frontend aponta para backend com HTTPS

---

## 🚨 Se nada funcionar

Me envie:
1. **Screenshot dos logs do backend** (últimas 20 linhas)
2. **Screenshot das variáveis do backend**
3. **Screenshot do erro no navegador** (console do navegador - F12)

---

## 💡 Teste Rápido

Para testar se o backend está funcionando:

1. Abra no navegador: `https://<URL_DO_BACKEND>/docs`
2. Exemplo: `https://backend-production-33ee.up.railway.app/docs`
3. Você deve ver a documentação da API (Swagger)
4. Tente fazer login usando a interface do Swagger:
   - Email: `admin@natacao.com`
   - Senha: `admin123`

Se o login funcionar no Swagger mas não no frontend, o problema é **CORS**.
Se o login não funcionar no Swagger, o problema é **DATABASE_URL**.

---

**Me diga qual erro você está vendo nos logs do backend!** 🔍
