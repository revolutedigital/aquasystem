#!/bin/bash

# Script de Deploy Automatizado para Railway
# Sistema de Gestão de Natação

set -e  # Exit on error

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🚂 Deploy Automático no Railway${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Verificar Railway CLI
if ! command -v railway &> /dev/null; then
    echo -e "${RED}❌ Railway CLI não encontrado${NC}"
    echo ""
    echo "Instale com:"
    echo "  npm i -g @railway/cli"
    echo "ou"
    echo "  brew install railway"
    exit 1
fi

echo -e "${GREEN}✅ Railway CLI encontrado${NC}"
echo ""

# Verificar se está logado
if ! railway whoami &> /dev/null; then
    echo -e "${YELLOW}⚠️  Você não está logado no Railway${NC}"
    echo "Fazendo login..."
    railway login
    echo ""
fi

RAILWAY_USER=$(railway whoami 2>/dev/null || echo "Unknown")
echo -e "${GREEN}✅ Logado como: ${RAILWAY_USER}${NC}"
echo ""

# Função para verificar se serviço existe
service_exists() {
    railway service list 2>/dev/null | grep -q "$1"
}

# Função para gerar SECRET_KEY
generate_secret() {
    openssl rand -hex 32
}

# Step 1: Verificar/Criar Projeto
echo -e "${YELLOW}📦 Step 1: Verificando projeto Railway...${NC}"
if ! railway status &> /dev/null; then
    echo "Projeto não encontrado. Criando novo projeto..."
    railway init
    echo -e "${GREEN}✅ Projeto criado${NC}"
else
    echo -e "${GREEN}✅ Projeto já existe${NC}"
fi
echo ""

# Step 2: Adicionar PostgreSQL
echo -e "${YELLOW}🗄️  Step 2: Configurando PostgreSQL...${NC}"
if ! service_exists "postgres"; then
    echo "Adicionando PostgreSQL ao projeto..."
    railway add --database postgres
    echo -e "${GREEN}✅ PostgreSQL adicionado${NC}"
    echo "⏳ Aguardando PostgreSQL inicializar (30s)..."
    sleep 30
else
    echo -e "${GREEN}✅ PostgreSQL já existe${NC}"
fi
echo ""

# Step 3: Deploy Backend
echo -e "${YELLOW}🔧 Step 3: Deploy do Backend...${NC}"
cd backend

# Configurar variáveis do backend
echo "Configurando variáveis de ambiente..."

# Gerar SECRET_KEY se não existir
if ! railway variables get SECRET_KEY -s backend &> /dev/null; then
    SECRET_KEY=$(generate_secret)
    railway variables set SECRET_KEY=$SECRET_KEY -s backend
    echo -e "${GREEN}✅ SECRET_KEY gerada${NC}"
fi

# Configurar outras variáveis
railway variables set ALGORITHM=HS256 -s backend 2>/dev/null || true
railway variables set ACCESS_TOKEN_EXPIRE_MINUTES=1440 -s backend 2>/dev/null || true
railway variables set ENVIRONMENT=production -s backend 2>/dev/null || true

# Deploy backend
echo "Fazendo deploy do backend..."
railway up -s backend -d .

echo -e "${GREEN}✅ Backend deployado${NC}"
cd ..
echo ""

# Aguardar backend ficar online
echo "⏳ Aguardando backend inicializar (30s)..."
sleep 30

# Step 4: Deploy Frontend
echo -e "${YELLOW}🎨 Step 4: Deploy do Frontend...${NC}"
cd frontend

# Obter URL do backend
echo "Obtendo URL do backend..."
BACKEND_URL=$(railway url -s backend)

if [ -z "$BACKEND_URL" ]; then
    echo -e "${RED}❌ Não foi possível obter URL do backend${NC}"
    echo "Tente novamente em alguns minutos após o backend estar completamente online"
    exit 1
fi

echo "Backend URL: $BACKEND_URL"

# Configurar API_URL
railway variables set API_URL=https://$BACKEND_URL -s frontend

# Deploy frontend
echo "Fazendo deploy do frontend..."
railway up -s frontend -d .

echo -e "${GREEN}✅ Frontend deployado${NC}"
cd ..
echo ""

# Aguardar frontend ficar online
echo "⏳ Aguardando frontend inicializar (30s)..."
sleep 30

# Step 5: Obter URLs finais
echo -e "${YELLOW}🌐 Step 5: Obtendo URLs dos serviços...${NC}"
BACKEND_URL=$(railway url -s backend)
FRONTEND_URL=$(railway url -s frontend)

# Step 6: Configurar ALLOWED_ORIGINS no backend
echo -e "${YELLOW}🔒 Step 6: Configurando CORS...${NC}"
ALLOWED_ORIGINS="https://$FRONTEND_URL,http://localhost:8501,http://localhost:9001"
railway variables set ALLOWED_ORIGINS=$ALLOWED_ORIGINS -s backend
railway restart -s backend

echo -e "${GREEN}✅ CORS configurado${NC}"
echo ""

# Resumo Final
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 Deploy Concluído com Sucesso!${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}📍 URLs dos Serviços:${NC}"
echo ""
echo -e "   ${GREEN}Frontend:${NC}  https://$FRONTEND_URL"
echo -e "   ${GREEN}Backend:${NC}   https://$BACKEND_URL"
echo -e "   ${GREEN}API Docs:${NC}  https://$BACKEND_URL/docs"
echo ""
echo -e "${BLUE}📊 Comandos Úteis:${NC}"
echo ""
echo "   Ver logs backend:   railway logs -s backend -f"
echo "   Ver logs frontend:  railway logs -s frontend -f"
echo "   Abrir dashboard:    railway open"
echo "   Ver variáveis:      railway variables -s backend"
echo ""
echo -e "${YELLOW}⚠️  IMPORTANTE:${NC}"
echo "   1. Acesse o frontend e faça login com:"
echo "      Email: admin@natacao.com"
echo "      Senha: admin123"
echo ""
echo "   2. ALTERE A SENHA PADRÃO imediatamente!"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
