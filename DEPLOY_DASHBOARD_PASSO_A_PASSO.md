# 🚀 Deploy pelo Dashboard Railway - Guia Visual Completo

**Projeto:** natacao-manager
**Tempo estimado:** 15-20 minutos
**Dashboard:** https://railway.com/project/5aae4303-99da-4180-b246-ece0f97ec1f7

---

## 📋 VISÃO GERAL

Vamos criar 3 serviços no Railway:
1. ✅ **PostgreSQL** - Banco de dados
2. ✅ **Backend** - API FastAPI
3. ✅ **Frontend** - Dashboard Streamlit

---

## 🎯 PASSO 1: Abrir o Dashboard

1. Abra no navegador: https://railway.com/project/5aae4303-99da-4180-b246-ece0f97ec1f7
2. Você verá uma tela vazia ou com poucos serviços

---

## 🗄️ PASSO 2: Adicionar PostgreSQL

### 2.1 Criar o banco de dados

1. Clique no botão **"+ New"** (canto superior direito)
2. No menu que abrir, selecione **"Database"**
3. Clique em **"Add PostgreSQL"**
4. Aguarde ~30 segundos enquanto o PostgreSQL é provisionado

✅ **Pronto!** Um card do PostgreSQL aparecerá no dashboard.

### 2.2 Verificar o PostgreSQL

1. Clique no card do **PostgreSQL**
2. Vá na aba **"Variables"**
3. Você verá várias variáveis, incluindo **DATABASE_URL**
4. **Não precisa fazer nada aqui ainda**, apenas confirmar que existe

---

## 🔧 PASSO 3: Adicionar Backend (FastAPI)

### 3.1 Criar o serviço

1. Volte para a tela principal (clique em "natacao-manager" no topo)
2. Clique em **"+ New"** novamente
3. Selecione **"GitHub Repo"**
4. Você verá uma lista de repositórios. Procure por **"revolutedigital/aquasystem"**
5. Clique no repositório **aquasystem**

### 3.2 Configurar o Backend

Após selecionar o repositório, você verá uma tela de configuração:

1. **Service Name:** Digite `backend`
2. **Root Directory:** Digite `backend`
3. Clique em **"Add Service"** ou **"Deploy"**

⏳ O Railway vai:
- Detectar o Dockerfile em `backend/Dockerfile`
- Fazer o build da imagem Docker
- Fazer o deploy (isso leva ~2-3 minutos)

### 3.3 Aguardar o build

1. Você será levado para a tela do serviço backend
2. Vá na aba **"Deployments"**
3. Aguarde até aparecer um ✅ verde (significa sucesso)
4. Se aparecer ❌ vermelho, clique para ver os logs

### 3.4 Configurar variáveis do Backend

Agora vamos configurar as variáveis de ambiente:

1. No serviço **backend**, clique na aba **"Variables"**
2. Clique no botão **"New Variable"** (ou **"Add Variable"**)
3. Adicione as seguintes variáveis **uma por uma**:

**Variável 1:**
```
Nome: SECRET_KEY
Valor: a62f8c3619726a7e15c13ca998b77ebc4512e84ad1c62b34018f601db9f3d395
```

**Variável 2:**
```
Nome: ALGORITHM
Valor: HS256
```

**Variável 3:**
```
Nome: ACCESS_TOKEN_EXPIRE_MINUTES
Valor: 1440
```

**Variável 4:**
```
Nome: ENVIRONMENT
Valor: production
```

### 3.5 Conectar o PostgreSQL ao Backend

Agora vamos conectar o banco de dados:

1. Ainda na aba **"Variables"** do backend
2. Clique em **"New Variable"**
3. Em vez de adicionar uma variável manual, clique em **"Add Reference"** (ou procure por uma opção de referenciar outro serviço)
4. Selecione o serviço **PostgreSQL**
5. Selecione a variável **DATABASE_URL**
6. Clique em **"Add"**

✅ Isso cria automaticamente uma variável `DATABASE_URL` que aponta para o PostgreSQL!

### 3.6 O backend vai redeploy automaticamente

Após adicionar as variáveis, o Railway vai fazer redeploy automático do backend. Aguarde ~2 minutos.

### 3.7 Obter a URL do Backend

1. No serviço **backend**, vá na aba **"Settings"**
2. Role até a seção **"Networking"** ou **"Domains"**
3. Clique em **"Generate Domain"** (se não houver um domínio ainda)
4. Copie a URL gerada (será algo como: `backend-production-xxxx.up.railway.app`)
5. **GUARDE ESTA URL!** Você vai usar no próximo passo

📋 **Exemplo de URL:** `https://backend-production-5aae.up.railway.app`

---

## 🎨 PASSO 4: Adicionar Frontend (Streamlit)

### 4.1 Criar o serviço

1. Volte para a tela principal (clique em "natacao-manager" no topo)
2. Clique em **"+ New"** novamente
3. Selecione **"GitHub Repo"**
4. Selecione o repositório **"revolutedigital/aquasystem"** novamente

### 4.2 Configurar o Frontend

1. **Service Name:** Digite `frontend`
2. **Root Directory:** Digite `frontend`
3. Clique em **"Add Service"** ou **"Deploy"**

⏳ O Railway vai fazer o build e deploy (~2-3 minutos)

### 4.3 Aguardar o build

1. Vá na aba **"Deployments"** do frontend
2. Aguarde até aparecer um ✅ verde

### 4.4 Configurar variável do Frontend

Agora vamos configurar o frontend para se conectar ao backend:

1. No serviço **frontend**, clique na aba **"Variables"**
2. Clique em **"New Variable"**
3. Adicione a variável:

```
Nome: API_URL
Valor: https://<URL_DO_BACKEND_DO_PASSO_3.7>
```

**Exemplo:**
```
Nome: API_URL
Valor: https://backend-production-5aae.up.railway.app
```

⚠️ **IMPORTANTE:** Use a URL **HTTPS** (não HTTP) que você copiou no Passo 3.7!

### 4.5 Frontend vai redeploy automaticamente

Aguarde ~2 minutos para o redeploy.

### 4.6 Obter a URL do Frontend

1. No serviço **frontend**, vá na aba **"Settings"**
2. Role até a seção **"Networking"** ou **"Domains"**
3. Clique em **"Generate Domain"** (se não houver um domínio ainda)
4. Copie a URL gerada (será algo como: `frontend-production-xxxx.up.railway.app`)
5. **GUARDE ESTA URL!** Você vai usar no próximo passo

📋 **Exemplo de URL:** `https://frontend-production-7b3c.up.railway.app`

---

## 🔒 PASSO 5: Configurar CORS no Backend

Agora vamos permitir que o frontend se comunique com o backend:

### 5.1 Adicionar ALLOWED_ORIGINS

1. Volte para o serviço **backend**
2. Vá na aba **"Variables"**
3. Clique em **"New Variable"**
4. Adicione a variável:

```
Nome: ALLOWED_ORIGINS
Valor: https://<URL_DO_FRONTEND_DO_PASSO_4.6>
```

**Exemplo:**
```
Nome: ALLOWED_ORIGINS
Valor: https://frontend-production-7b3c.up.railway.app
```

⚠️ **IMPORTANTE:** Use a URL **HTTPS** (não HTTP) que você copiou no Passo 4.6!

### 5.2 Redeploy do Backend

1. Ainda no serviço **backend**, vá na aba **"Deployments"**
2. Clique nos 3 pontinhos (**...**) no deployment mais recente
3. Clique em **"Redeploy"** ou **"Restart"**
4. Aguarde ~1-2 minutos

---

## 🎉 PASSO 6: DEPLOY CONCLUÍDO!

### ✅ Checklist Final

Verifique se todos os serviços estão rodando:

- [ ] **PostgreSQL** - Status: Running (verde)
- [ ] **Backend** - Status: Running (verde) + tem URL pública
- [ ] **Frontend** - Status: Running (verde) + tem URL pública

### 🌐 Acessar o Sistema

1. Abra a URL do **frontend** no navegador
2. Você verá a tela de login
3. Faça login com:
   - **Email:** `admin@natacao.com`
   - **Senha:** `admin123`
4. **❗ ALTERE A SENHA IMEDIATAMENTE após o primeiro login!**

---

## 📊 PASSO 7: Verificar Funcionamento

### 7.1 Testar o Backend

Abra no navegador: `https://<URL_DO_BACKEND>/docs`

Exemplo: `https://backend-production-5aae.up.railway.app/docs`

Você deve ver a documentação interativa da API (Swagger UI).

### 7.2 Testar o Frontend

1. Acesse a URL do frontend
2. Faça login
3. Navegue pelas páginas:
   - Dashboard
   - Cadastro de Alunos
   - Grade de Horários
   - Financeiro
   - Usuários

### 7.3 Ver Logs

Se algo não funcionar:

**Logs do Backend:**
1. Vá no serviço **backend**
2. Clique na aba **"Logs"**
3. Veja os logs em tempo real

**Logs do Frontend:**
1. Vá no serviço **frontend**
2. Clique na aba **"Logs"**
3. Veja os logs em tempo real

---

## 🐛 TROUBLESHOOTING

### ❌ Backend não inicia

**Sintomas:** Status vermelho no backend

**Soluções:**
1. Verifique os logs na aba "Logs"
2. Confirme que todas as variáveis foram adicionadas:
   - `SECRET_KEY`
   - `ALGORITHM`
   - `ACCESS_TOKEN_EXPIRE_MINUTES`
   - `ENVIRONMENT`
   - `DATABASE_URL` (referência ao PostgreSQL)
3. Vá em "Deployments" e clique em "Redeploy"

### ❌ Frontend não conecta ao backend

**Sintomas:** Erro ao fazer login ou carregar dados

**Soluções:**
1. Verifique se a variável `API_URL` está correta
2. Certifique-se de que a URL é **HTTPS** (não HTTP)
3. Teste se o backend está funcionando acessando: `https://<URL_DO_BACKEND>/docs`
4. Verifique os logs do frontend

### ❌ Erro de CORS

**Sintomas:** Erro no console do navegador mencionando CORS

**Soluções:**
1. Verifique se a variável `ALLOWED_ORIGINS` no backend está correta
2. Certifique-se de que a URL do frontend está com **HTTPS**
3. Faça um redeploy do backend

### ❌ Erro de banco de dados

**Sintomas:** Erro ao criar/listar dados

**Soluções:**
1. Verifique se o PostgreSQL está com status "Running"
2. Confirme que a variável `DATABASE_URL` está conectada ao backend
3. Veja os logs do backend para detalhes do erro

---

## 📝 RESUMO DAS VARIÁVEIS

### Backend (5 variáveis)

```
SECRET_KEY = a62f8c3619726a7e15c13ca998b77ebc4512e84ad1c62b34018f601db9f3d395
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
ENVIRONMENT = production
DATABASE_URL = ${{Postgres.DATABASE_URL}} (referência)
ALLOWED_ORIGINS = https://<URL_DO_FRONTEND>
```

### Frontend (1 variável)

```
API_URL = https://<URL_DO_BACKEND>
```

---

## 💰 Custos Estimados

- **Backend:** ~$3/mês
- **Frontend:** ~$3/mês
- **PostgreSQL:** ~$5/mês
- **Total:** ~$11/mês

Railway oferece **$5 de crédito grátis** mensalmente.

---

## 🔗 Links Importantes

- **Dashboard do Projeto:** https://railway.com/project/5aae4303-99da-4180-b246-ece0f97ec1f7
- **Repositório GitHub:** https://github.com/revolutedigital/aquasystem
- **Documentação Railway:** https://docs.railway.app/

---

## 📞 Próximos Passos

Após o deploy:

1. ✅ Acessar o sistema e fazer login
2. ✅ **ALTERAR A SENHA PADRÃO**
3. ✅ Criar novos usuários se necessário
4. ✅ Cadastrar alunos
5. ✅ Configurar horários
6. ✅ Gerenciar pagamentos

---

## 🎯 DICAS IMPORTANTES

### Atualizar o código

Quando você fizer alterações no código e fizer push para o GitHub:

1. O Railway **detecta automaticamente** o push
2. Faz **redeploy automático** dos serviços
3. Você pode acompanhar na aba "Deployments"

### Desativar redeploy automático

Se quiser controlar manualmente:

1. Vá em **Settings** do serviço
2. Role até **"Deployment Triggers"**
3. Desative **"Auto Deploy"**

### Criar ambientes (staging/production)

1. No dashboard principal, clique em "production" no topo
2. Clique em **"New Environment"**
3. Configure staging com os mesmos passos

---

**🎉 Parabéns! Seu sistema está no ar!** 🎉

Se tiver qualquer problema, consulte a seção de Troubleshooting ou verifique os logs dos serviços.
