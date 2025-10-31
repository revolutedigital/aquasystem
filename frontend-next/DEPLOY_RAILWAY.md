# DEPLOY RÁPIDO NO RAILWAY - FRONTEND NEXT.JS

## Passos para Deploy Imediato:

### 1. Criar novo serviço no Railway (2 minutos)

1. Acesse: https://railway.app/dashboard
2. Clique em **"New Project"**
3. Selecione **"Deploy from GitHub repo"**
4. Escolha seu repositório: `aquasystem/natacao-manager`
5. **IMPORTANTE**: Após conectar, clique em **"Settings"**
6. Em **"Root Directory"**, coloque: `frontend-next`
7. Clique em **"Save"**

### 2. Configurar Variáveis de Ambiente (1 minuto)

No Railway, vá em **Variables** e adicione:

```
NEXT_PUBLIC_API_URL=https://backend-production-33ee.up.railway.app
```

### 3. Deploy Automático

O Railway vai iniciar o deploy automaticamente após configurar as variáveis.

### 4. Remover/Parar o Streamlit

No seu projeto Railway atual:
1. Vá no serviço do Streamlit (frontend antigo)
2. Clique em **Settings**
3. Role até **"Danger Zone"**
4. Clique em **"Remove Service"**

OU se quiser manter mas desativado:
1. Vá em **Settings**
2. Em **"Deploy"**, clique em **"Disable Trigger"**

### 5. Acessar o Novo Frontend

Após o deploy (cerca de 3-5 minutos), você terá uma URL como:
```
https://frontend-next-production-xxxx.up.railway.app
```

### Credenciais de Teste
- Email: admin@natacao.com
- Senha: admin123

## Comandos Git Rápidos (se precisar)

Se você ainda não fez commit das mudanças:

```bash
cd /Users/yourapple/aquasystem/natacao-manager
git add frontend-next/
git commit -m "Deploy frontend Next.js"
git push origin main
```

## Troubleshooting

Se der erro no build:
1. Verifique se o **Root Directory** está como `frontend-next`
2. Verifique se a variável `NEXT_PUBLIC_API_URL` está configurada
3. No Railway logs, procure por erros específicos

## URLs Importantes

- Backend (já funcionando): https://backend-production-33ee.up.railway.app
- Novo Frontend: Será gerado pelo Railway após deploy