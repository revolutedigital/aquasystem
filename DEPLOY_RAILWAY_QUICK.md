# 🚀 Deploy Rápido no Railway

> Coloque seu sistema no ar em 5 minutos!

## Opção 1: Script Automático (Recomendado) 🤖

```bash
# Execute o script de deploy
./scripts/deploy-railway.sh
```

**Pronto!** O script faz tudo automaticamente:
- ✅ Cria projeto Railway
- ✅ Adiciona PostgreSQL
- ✅ Deploya backend e frontend
- ✅ Configura todas as variáveis
- ✅ Gera URLs públicas

---

## Opção 2: Passo a Passo Manual 👨‍💻

### 1. Login no Railway
```bash
railway login
```

### 2. Criar Projeto
```bash
railway init
# Escolha: "Create new project"
# Nome: natacao-manager
```

### 3. Adicionar PostgreSQL
```bash
railway add postgres
```

### 4. Deploy Backend
```bash
cd backend
railway up -s backend

# Configurar variáveis
railway variables set SECRET_KEY=$(openssl rand -hex 32) -s backend
railway variables set ALGORITHM=HS256 -s backend
railway variables set ACCESS_TOKEN_EXPIRE_MINUTES=1440 -s backend
railway variables set ENVIRONMENT=production -s backend

cd ..
```

### 5. Deploy Frontend
```bash
cd frontend
railway up -s frontend

# Obter URL do backend e configurar
BACKEND_URL=$(railway url -s backend)
railway variables set API_URL=https://$BACKEND_URL -s frontend

cd ..
```

### 6. Configurar CORS
```bash
# Obter URL do frontend
FRONTEND_URL=$(railway url -s frontend)

# Configurar ALLOWED_ORIGINS no backend
railway variables set ALLOWED_ORIGINS=https://$FRONTEND_URL -s backend

# Restart backend para aplicar
railway restart -s backend
```

### 7. Acessar o Sistema
```bash
# Ver URLs
echo "Frontend: https://$(railway url -s frontend)"
echo "Backend: https://$(railway url -s backend)"

# Abrir no navegador
railway open -s frontend
```

---

## 📊 Verificar Status

```bash
# Ver logs em tempo real
railway logs -s backend -f
railway logs -s frontend -f

# Ver status dos serviços
railway status

# Abrir dashboard web
railway open
```

---

## 🔒 Pós-Deploy (IMPORTANTE!)

1. **Acesse o frontend**
2. **Faça login:**
   - Email: `admin@natacao.com`
   - Senha: `admin123`
3. **ALTERE A SENHA IMEDIATAMENTE:**
   - Vá em: Menu > Usuários > Editar Admin
   - Defina uma senha forte

---

## 🐛 Solução de Problemas

### Backend não conecta no banco
```bash
# Verificar DATABASE_URL
railway variables -s backend | grep DATABASE_URL
```

### Frontend não conecta no backend
```bash
# Verificar API_URL
railway variables -s frontend | grep API_URL

# Deve ser HTTPS, não HTTP!
# Corrigir se necessário:
BACKEND_URL=$(railway url -s backend)
railway variables set API_URL=https://$BACKEND_URL -s frontend
railway restart -s frontend
```

### Ver erros detalhados
```bash
railway logs -s backend --tail 100
railway logs -s frontend --tail 100
```

---

## 💰 Custo Estimado

**Plano Starter ($20/mês):**
- Backend: ~$3/mês
- Frontend: ~$3/mês
- PostgreSQL: ~$5/mês
- **Total: ~$11/mês**

Sobram $9 de crédito! 💰

---

## 📚 Comandos Úteis

```bash
# Restart serviço
railway restart -s backend

# Ver variáveis
railway variables -s backend

# Adicionar variável
railway variables set KEY=value -s backend

# Conectar ao banco
railway connect postgres

# Ver uso de recursos
railway metrics -s backend

# Deletar serviço
railway service delete backend
```

---

## 🎯 Checklist Pós-Deploy

- [ ] Backend está online
- [ ] Frontend está online
- [ ] Consegue fazer login
- [ ] Senha do admin foi alterada
- [ ] Consegue criar aluno
- [ ] Consegue criar horário
- [ ] Consegue registrar pagamento
- [ ] APIs retornam 200 OK
- [ ] Logs sem erros críticos

---

## 📞 Ajuda

- **Documentação Completa:** `PLANO_DEPLOY_RAILWAY.md`
- **Railway Docs:** https://docs.railway.app
- **Discord Railway:** https://discord.gg/railway

---

**🎉 Sistema online em produção!**

*Versão 1.0 - Deploy Simplificado*
