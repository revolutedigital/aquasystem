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

    # Executar migrações
    try:
        from app.migrate_add_plano_id import migrate
        migrate()
    except Exception as e:
        print(f"⚠️  Aviso ao executar migração: {str(e)}")

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

# Configurar CORS
# Definir origens permitidas
ALLOWED_ORIGINS_STR = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:8501,http://localhost:9001,https://frontend-production-ef47.up.railway.app"
)

# Converter string para lista e remover espaços
ALLOWED_ORIGINS = [origin.strip() for origin in ALLOWED_ORIGINS_STR.split(",")]

# Adicionar origens do Railway dinamicamente se em produção
if os.getenv("RAILWAY_ENVIRONMENT"):
    # Adicionar URLs conhecidas do Railway
    railway_origins = [
        "https://frontend-production-ef47.up.railway.app",
        "https://frontend-next-production.up.railway.app",
        "https://aquaflow.up.railway.app",
    ]
    ALLOWED_ORIGINS.extend(railway_origins)

# Remover duplicatas
ALLOWED_ORIGINS = list(set(ALLOWED_ORIGINS))

print(f"🔐 CORS configurado para as seguintes origens:")
for origin in ALLOWED_ORIGINS:
    print(f"   ✅ {origin}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Importar e incluir routers
from app.routes import alunos, pagamentos, horarios, auth, users, planos

# Rotas de autenticação e usuários (públicas e protegidas)
app.include_router(auth.router, prefix="/api", tags=["Autenticação"])
app.include_router(users.router, prefix="/api", tags=["Usuários"])

# Rotas principais (serão protegidas depois)
app.include_router(alunos.router, prefix="/api", tags=["Alunos"])
app.include_router(pagamentos.router, prefix="/api", tags=["Pagamentos"])
app.include_router(horarios.router, prefix="/api", tags=["Horários"])
app.include_router(planos.router, prefix="/api", tags=["Planos"])


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
