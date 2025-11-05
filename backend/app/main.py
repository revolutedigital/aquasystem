"""
Aplicação principal FastAPI - Sistema de Gestão de Natação
"""
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware
import os
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerenciador de ciclo de vida da aplicação"""
    # Startup: Inicializar banco de dados
    init_db()

    # Executar migrações
    try:
        from app.migrate_add_plano_id import migrate as migrate_plano
        migrate_plano()
    except Exception as e:
        print(f"⚠️  Aviso ao executar migração plano_id: {str(e)}")

    try:
        from app.migrate_add_professor import migrate as migrate_professor
        migrate_professor()
    except Exception as e:
        print(f"⚠️  Aviso ao executar migração professor: {str(e)}")

    print("✅ Sistema inicializado com sucesso!")
    yield
    # Shutdown: cleanup se necessário
    print("🔴 Sistema encerrado")


def get_real_ip(request: Request) -> str:
    """
    Obtém o IP real do cliente, considerando proxies reversos (Railway, etc)
    """
    # Tentar obter IP do header X-Forwarded-For (Railway usa isso)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # X-Forwarded-For pode ter múltiplos IPs, pegar o primeiro (cliente real)
        return forwarded_for.split(",")[0].strip()

    # Fallback para X-Real-IP
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip

    # Último fallback: IP direto da conexão
    return request.client.host if request.client else "unknown"


# Middleware de segurança para CSRF Protection e Security Headers
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware para adicionar security headers e validar Origin/Referer
    Proteção contra CSRF, XSS, Clickjacking, etc.
    """

    def __init__(self, app, allowed_origins: list):
        super().__init__(app)
        self.allowed_origins = set(allowed_origins)

    async def dispatch(self, request: Request, call_next):
        # Métodos que modificam dados (state-changing)
        state_changing_methods = {"POST", "PUT", "DELETE", "PATCH"}

        # Validar Origin/Referer para métodos que modificam dados
        if request.method in state_changing_methods:
            origin = request.headers.get("Origin") or request.headers.get("Referer")

            # Exceção: permitir requests sem Origin/Referer para certos endpoints
            # (necessário para alguns clientes como cURL, testes, etc.)
            allowed_without_origin = {
                "/health",
                "/",
                "/api/auth/login"  # Permitir login sem Origin (Safari em modo privado)
            }

            # Se Origin/Referer estiver presente, validar
            # Se não estiver presente, só bloquear se não for endpoint permitido
            if origin:
                # Normalizar origin (remover trailing slash e path)
                if origin.startswith("http"):
                    from urllib.parse import urlparse
                    parsed = urlparse(origin)
                    origin = f"{parsed.scheme}://{parsed.netloc}"

                # Validar se origin está na lista permitida
                if origin not in self.allowed_origins:
                    return JSONResponse(
                        status_code=status.HTTP_403_FORBIDDEN,
                        content={"detail": f"Origin {origin} not allowed"}
                    )
            else:
                # Sem Origin/Referer - bloquear apenas endpoints sensíveis
                # Permitir login e endpoints na whitelist
                if request.url.path not in allowed_without_origin:
                    # Para outros endpoints, exigir autenticação via token
                    # Se tiver Authorization header, permitir (request autenticado)
                    auth_header = request.headers.get("Authorization")
                    if not auth_header:
                        return JSONResponse(
                            status_code=status.HTTP_403_FORBIDDEN,
                            content={"detail": "Missing Origin or Referer header for unauthenticated request"}
                        )

        # Processar request
        response = await call_next(request)

        # Adicionar Security Headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        return response


# Configurar rate limiter com função customizada para proxies
limiter = Limiter(key_func=get_real_ip, default_limits=["100/minute"])

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

# Adicionar Security Headers Middleware (CSRF Protection + Security Headers)
app.add_middleware(SecurityHeadersMiddleware, allowed_origins=ALLOWED_ORIGINS)

print("🛡️  Security Headers Middleware ativado:")
print("   ✅ CSRF Protection via Origin/Referer validation")
print("   ✅ X-Content-Type-Options: nosniff")
print("   ✅ X-Frame-Options: DENY")
print("   ✅ X-XSS-Protection: 1; mode=block")
print("   ✅ Strict-Transport-Security (HSTS)")
print("   ✅ Referrer-Policy")
print("   ✅ Permissions-Policy")

# Importar e incluir routers
from app.routes import alunos, pagamentos, horarios, auth, users, planos, professores

# Rotas de autenticação e usuários (públicas e protegidas)
app.include_router(auth.router, prefix="/api", tags=["Autenticação"])
app.include_router(users.router, prefix="/api", tags=["Usuários"])

# Rotas principais (serão protegidas depois)
app.include_router(alunos.router, prefix="/api", tags=["Alunos"])
app.include_router(pagamentos.router, prefix="/api", tags=["Pagamentos"])
app.include_router(horarios.router, prefix="/api", tags=["Horários"])
app.include_router(planos.router, prefix="/api", tags=["Planos"])
app.include_router(professores.router, prefix="/api", tags=["Professores"])


@app.get("/")
@limiter.limit("10/minute")
async def root(request: Request):
    """Endpoint raiz da API"""
    return {
        "message": "API Sistema de Natação v2.0",
        "version": "2.0",
        "features": [
            "Autenticação JWT (1 hora)",
            "Gerenciamento de Usuários",
            "CRUD de Alunos",
            "CRUD de Pagamentos",
            "CRUD de Horários",
            "Rate Limiting (5/min login)",
            "CORS Restrito",
            "CSRF Protection",
            "Security Headers (HSTS, XSS, etc)",
            "Password Strength Validation"
        ],
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Endpoint de health check"""
    return {"status": "healthy", "service": "Sistema de Natação", "version": "2.0"}
