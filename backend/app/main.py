"""
Aplicação principal FastAPI - Sistema de Gestão de Natação
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciador de ciclo de vida da aplicação"""
    # Startup: Inicializar banco de dados
    init_db()
    print("✅ Sistema inicializado com sucesso!")
    yield
    # Shutdown: cleanup se necessário
    print("🔴 Sistema encerrado")


# Configurar rate limiter
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

# Criar aplicação FastAPI
app = FastAPI(
    title="Sistema de Gestão - Natação",
    description="API para gerenciamento de alunos, pagamentos e horários de natação com autenticação JWT",
    version="2.0",
    lifespan=lifespan
)

# Configurar rate limiter na aplicação
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configurar CORS - RESTRITO (segurança)
# Definir origens permitidas
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:9001,http://localhost:8501,http://frontend:9001"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # ✅ Apenas origens confiáveis
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Content-Type", "Authorization"],
)

# Importar e incluir routers
from app.routes import alunos, pagamentos, horarios, auth, users

# Rotas de autenticação e usuários (públicas e protegidas)
app.include_router(auth.router, prefix="/api", tags=["Autenticação"])
app.include_router(users.router, prefix="/api", tags=["Usuários"])

# Rotas principais (serão protegidas depois)
app.include_router(alunos.router, prefix="/api", tags=["Alunos"])
app.include_router(pagamentos.router, prefix="/api", tags=["Pagamentos"])
app.include_router(horarios.router, prefix="/api", tags=["Horários"])


@app.get("/")
@limiter.limit("10/minute")
async def root(request: Request):
    """Endpoint raiz da API"""
    return {
        "message": "API Sistema de Natação v2.0",
        "version": "2.0",
        "features": [
            "Autenticação JWT",
            "Gerenciamento de Usuários",
            "CRUD de Alunos",
            "CRUD de Pagamentos",
            "CRUD de Horários",
            "Rate Limiting",
            "CORS Restrito"
        ],
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Endpoint de health check"""
    return {"status": "healthy", "service": "Sistema de Natação", "version": "2.0"}
