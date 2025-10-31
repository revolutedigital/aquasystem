# 🔍 Debug - Erro ao Criar Alunos

## 📋 Informações Necessárias

Para resolver o problema, preciso que você me envie:

---

## 1️⃣ Logs do Backend

### Como obter:

1. Acesse: https://railway.com/project/5aae4303-99da-4180-b246-ece0f97ec1f7
2. Clique no serviço **backend**
3. Vá na aba **"Logs"**
4. Role até o final
5. **Tente cadastrar um aluno no frontend**
6. **IMEDIATAMENTE** depois, volte nos logs do backend
7. **Copie as últimas 30-40 linhas** e me envie

### O que procurar nos logs:

```
✅ Sinais de sucesso:
- "✅ DATABASE_URL convertida para formato correto"
- "✅ Engine do banco de dados criada com sucesso!"
- "✅ Sistema inicializado com sucesso!"

❌ Sinais de erro:
- "Connection refused"
- "could not connect to server"
- "CORS"
- "No 'Access-Control-Allow-Origin'"
- "Traceback" (erro de Python)
- "ERROR"
- "FAILED"
```

---

## 2️⃣ Console do Navegador (Frontend)

### Como obter:

1. Abra o frontend do Railway
2. Aperte **F12** (ou Cmd+Option+I no Mac)
3. Vá na aba **"Console"**
4. **Limpe o console** (botão 🚫 ou Clear)
5. **Tente cadastrar um aluno**
6. **Copie TUDO que aparecer no console** e me envie

### O que procurar:

```
❌ Erros comuns:
- "Failed to fetch"
- "CORS policy"
- "Network Error"
- "500 Internal Server Error"
- "401 Unauthorized"
- "404 Not Found"
```

---

## 3️⃣ Variáveis de Ambiente do Backend

### Como obter:

1. No serviço **backend** do Railway
2. Vá na aba **"Variables"**
3. **Tire um screenshot** ou copie as seguintes variáveis:
   - `DATABASE_URL` (não precisa copiar o valor, só confirmar que existe)
   - `ALLOWED_ORIGINS`
   - `SECRET_KEY` (não precisa copiar, só confirmar)
   - `ALGORITHM`
   - `ACCESS_TOKEN_EXPIRE_MINUTES`
   - `ENVIRONMENT`

---

## 4️⃣ Status dos Serviços

Verifique se todos estão com status **"Running"** (verde):

- [ ] PostgreSQL - Running?
- [ ] backend - Running?
- [ ] front - Running?

---

## 5️⃣ Teste Rápido da API

Abra no navegador:

```
https://backend-production-33ee.up.railway.app/docs
```

(Substitua pela URL real do seu backend)

### O que testar:

1. A página do Swagger abre?
2. Consegue fazer login pelo Swagger?
   - Vá em `POST /api/auth/login`
   - Click "Try it out"
   - Coloque:
     ```json
     {
       "email": "admin@natacao.com",
       "password": "admin123"
     }
     ```
   - Click "Execute"
   - Funcionou? Qual foi a resposta?

3. Consegue criar um aluno pelo Swagger?
   - Copie o token da resposta do login
   - Vá em `POST /api/alunos`
   - Click no cadeado 🔒 e cole o token
   - Click "Try it out"
   - Coloque:
     ```json
     {
       "nome_completo": "Teste Silva",
       "tipo_aula": "natacao",
       "valor_mensalidade": 150,
       "dia_vencimento": 10,
       "ativo": true
     }
     ```
   - Click "Execute"
   - Funcionou? Qual foi a resposta?

---

## 6️⃣ Mensagem de Erro no Frontend

Quando você tenta cadastrar um aluno, qual mensagem aparece?

- [ ] "Sistema temporariamente indisponível"
- [ ] "Não foi possível salvar os dados"
- [ ] "Telefone inválido"
- [ ] Outra mensagem? Qual?

---

## 🎯 Checklist Rápido

Antes de me enviar as informações, verifique:

- [ ] PostgreSQL está rodando (status verde no Railway)
- [ ] Backend está rodando (status verde no Railway)
- [ ] Frontend está rodando (status verde no Railway)
- [ ] Variável ALLOWED_ORIGINS no backend tem a URL do frontend
- [ ] Variável API_URL no frontend tem a URL do backend
- [ ] Variável DATABASE_URL no backend está configurada (referência ao Postgres)

---

## 📤 Como me enviar

Copie e cole aqui as informações:

```
=== LOGS DO BACKEND ===
[Cole aqui as últimas 30-40 linhas]

=== CONSOLE DO NAVEGADOR ===
[Cole aqui o que apareceu no console]

=== VARIÁVEIS DO BACKEND ===
DATABASE_URL: [existe? sim/não]
ALLOWED_ORIGINS: [valor]
Outras variáveis: [confirmar que existem]

=== STATUS DOS SERVIÇOS ===
PostgreSQL: [Running/Stopped]
Backend: [Running/Stopped]
Frontend: [Running/Stopped]

=== TESTE DO SWAGGER ===
Swagger abre? [sim/não]
Login funciona? [sim/não - qual resposta]
Criar aluno funciona? [sim/não - qual resposta]

=== MENSAGEM DE ERRO NO FRONTEND ===
[Mensagem exata que aparece]
```

---

**Com essas informações vou conseguir identificar exatamente o problema!** 🔍
