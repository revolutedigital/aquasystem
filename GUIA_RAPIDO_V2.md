# 🚀 GUIA RÁPIDO - Sistema v2.0

## Como Iniciar o Sistema em 5 Minutos

### 1️⃣ Gerar Secret Key (30 segundos)
```bash
cd /Users/yourapple/aquasystem/natacao-manager
openssl rand -hex 32
```
Copie o resultado!

### 2️⃣ Atualizar .env (1 minuto)
```bash
# Editar arquivo .env
nano .env

# Adicionar/atualizar estas linhas:
SECRET_KEY=COLE_O_RESULTADO_AQUI
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ALLOWED_ORIGINS=http://localhost:9001,http://localhost:8501,http://frontend:9001
```

### 3️⃣ Rebuild e Iniciar (2 minutos)
```bash
# Parar containers antigos
docker-compose down

# Rebuild e iniciar
docker-compose up -d --build

# Verificar logs
docker-compose logs -f backend
```

**Aguarde ver:**
- ✅ Banco de dados inicializado com sucesso!
- ✅ Usuário admin criado com sucesso!
- ✅ Sistema inicializado com sucesso!

### 4️⃣ Acessar Sistema (30 segundos)
```
Frontend: http://localhost:9001
```

### 5️⃣ Fazer Login (30 segundos)
```
Email: admin@natacao.com
Senha: admin123
```

---

## ✅ Pronto! Sistema v2.0 Rodando

**Recursos Disponíveis:**
- 🔐 Autenticação JWT
- 👥 Gerenciamento de Usuários (Admin)
- 📝 Cadastro de Alunos
- 💰 Controle Financeiro
- 📅 Grade de Horários
- 📊 Dashboard
- 🔒 Segurança CORS + Rate Limit

**API Docs:** http://localhost:9000/docs

---

## 🎯 Próximos Passos

1. Alterar senha do admin (página Usuários)
2. Criar usuários para recepcionistas
3. Começar a cadastrar alunos!

---

## 🆘 Problemas?

**Backend não inicia?**
```bash
docker-compose logs backend
```

**Frontend não conecta?**
```bash
docker-compose logs frontend
```

**Banco não responde?**
```bash
docker-compose logs postgres
```

**Recomeçar do zero?**
```bash
docker-compose down -v  # APAGA DADOS!
docker-compose up -d --build
```

---

**Bom uso! 🎉**
