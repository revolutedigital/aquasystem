#!/bin/bash
# Script para Deploy no Railway - natacao-manager
# Execute estes comandos no seu terminal com suporte a TTY

echo "🚀 Deploy Railway - Sistema de Natação"
echo "======================================"
echo ""

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}📍 Projeto Railway:${NC} https://railway.com/project/5aae4303-99da-4180-b246-ece0f97ec1f7"
echo ""

# Variáveis
PROJECT_ID="5aae4303-99da-4180-b246-ece0f97ec1f7"
SECRET_KEY="a62f8c3619726a7e15c13ca998b77ebc4512e84ad1c62b34018f601db9f3d395"

echo -e "${YELLOW}PASSO 1: Adicionar PostgreSQL${NC}"
echo "❗ Este passo deve ser feito pelo DASHBOARD WEB:"
echo "   1. Abra: https://railway.com/project/5aae4303-99da-4180-b246-ece0f97ec1f7"
echo "   2. Clique em '+ New'"
echo "   3. Selecione 'Database'"
echo "   4. Escolha 'Add PostgreSQL'"
echo "   5. Aguarde o provisionamento (~30 segundos)"
echo ""
read -p "Pressione ENTER quando o PostgreSQL estiver criado..."
echo ""

echo -e "${YELLOW}PASSO 2: Deploy do Backend${NC}"
echo "Navegando para o diretório backend..."
cd /Users/yourapple/aquasystem/natacao-manager/backend

echo "Criando serviço backend..."
railway up --service backend

echo ""
echo -e "${YELLOW}PASSO 3: Configurar Variáveis do Backend${NC}"
echo "Configurando SECRET_KEY..."
railway variables --set SECRET_KEY=$SECRET_KEY --service backend

echo "Configurando outras variáveis..."
railway variables --set ALGORITHM=HS256 --service backend
railway variables --set ACCESS_TOKEN_EXPIRE_MINUTES=1440 --service backend
railway variables --set ENVIRONMENT=production --service backend

echo ""
echo -e "${GREEN}✅ Backend configurado!${NC}"
echo ""
echo -e "${YELLOW}❗ IMPORTANTE: Conectar DATABASE_URL${NC}"
echo "   No dashboard do Railway:"
echo "   1. Vá no serviço 'backend'"
echo "   2. Clique em 'Variables'"
echo "   3. Clique em 'New Variable' > 'Add Reference'"
echo "   4. Selecione PostgreSQL > DATABASE_URL"
echo ""
read -p "Pressione ENTER quando DATABASE_URL estiver conectada..."
echo ""

echo -e "${YELLOW}PASSO 4: Obter URL do Backend${NC}"
BACKEND_URL=$(railway url --service backend)
echo "Backend URL: https://$BACKEND_URL"
echo ""

echo -e "${YELLOW}PASSO 5: Deploy do Frontend${NC}"
cd /Users/yourapple/aquasystem/natacao-manager/frontend
echo "Criando serviço frontend..."
railway up --service frontend

echo ""
echo -e "${YELLOW}PASSO 6: Configurar Variáveis do Frontend${NC}"
echo "Configurando API_URL..."
railway variables --set API_URL=https://$BACKEND_URL --service frontend

echo ""
echo -e "${YELLOW}PASSO 7: Obter URL do Frontend${NC}"
FRONTEND_URL=$(railway url --service frontend)
echo "Frontend URL: https://$FRONTEND_URL"
echo ""

echo -e "${YELLOW}PASSO 8: Configurar CORS no Backend${NC}"
echo "Configurando ALLOWED_ORIGINS..."
railway variables --set ALLOWED_ORIGINS=https://$FRONTEND_URL --service backend

echo "Reiniciando backend para aplicar CORS..."
railway restart --service backend

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ DEPLOY CONCLUÍDO COM SUCESSO!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}📊 URLs dos Serviços:${NC}"
echo "   • Frontend: https://$FRONTEND_URL"
echo "   • Backend:  https://$BACKEND_URL"
echo ""
echo -e "${BLUE}🔐 Login Padrão:${NC}"
echo "   • Email: admin@natacao.com"
echo "   • Senha: admin123"
echo "   ❗ ALTERE A SENHA APÓS PRIMEIRO LOGIN!"
echo ""
echo -e "${BLUE}📊 Verificar Status:${NC}"
echo "   railway status"
echo ""
echo -e "${BLUE}📋 Ver Logs:${NC}"
echo "   railway logs --service backend"
echo "   railway logs --service frontend"
echo ""
echo -e "${BLUE}🌐 Dashboard:${NC}"
echo "   https://railway.com/project/5aae4303-99da-4180-b246-ece0f97ec1f7"
echo ""
