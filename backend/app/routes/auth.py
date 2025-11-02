"""
Rotas de Autenticação e Autorização
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from slowapi import Limiter

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserLogin, Token, UserResponse, TokenData
from app.utils.auth import verify_password, create_access_token, decode_access_token


def get_real_ip(request: Request) -> str:
    """Obtém IP real considerando proxies"""
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    return request.client.host if request.client else "unknown"


router = APIRouter()
security = HTTPBearer()
limiter = Limiter(key_func=get_real_ip)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency para obter usuário autenticado a partir do token JWT

    Args:
        credentials: Credenciais HTTP Bearer (token)
        db: Sessão do banco de dados

    Returns:
        User: Usuário autenticado

    Raises:
        HTTPException: Se token inválido ou usuário não encontrado
    """
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: int = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Buscar usuário no banco
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo",
        )

    return user


def require_role(allowed_roles: list[str]):
    """
    Dependency factory para verificar role do usuário

    Args:
        allowed_roles: Lista de roles permitidas (ex: ["admin", "recepcionista"])

    Returns:
        Dependency function
    """
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso negado. Requer uma das roles: {', '.join(allowed_roles)}"
            )
        return current_user
    return role_checker


@router.post("/auth/login", response_model=Token)
@limiter.limit("5/minute")  # Máximo 5 tentativas de login por minuto
async def login(request: Request, user_credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Endpoint de login - retorna token JWT
    Rate Limited: 5 tentativas por minuto por IP

    Args:
        request: Request object (necessário para rate limiting)
        user_credentials: Email e senha do usuário
        db: Sessão do banco de dados

    Returns:
        Token: Token JWT e informações do usuário

    Raises:
        HTTPException: Se credenciais inválidas ou rate limit excedido
    """
    # Buscar usuário por email
    user = db.query(User).filter(User.email == user_credentials.email).first()

    # Verificar se usuário existe e senha está correta
    if not user or not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verificar se usuário está ativo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo. Contate o administrador.",
        )

    # Criar token JWT
    access_token_expires = timedelta(minutes=1440)  # 24 horas
    access_token = create_access_token(
        data={
            "user_id": user.id,
            "email": user.email,
            "role": user.role,
            "username": user.username
        },
        expires_delta=access_token_expires
    )

    # Atualizar last_login
    user.last_login = datetime.utcnow()
    db.commit()

    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=1440 * 60,  # segundos
        user=UserResponse.model_validate(user)
    )


@router.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Endpoint para obter informações do usuário autenticado

    Args:
        current_user: Usuário autenticado (injetado via dependency)

    Returns:
        UserResponse: Informações do usuário
    """
    return UserResponse.model_validate(current_user)


@router.post("/auth/refresh", response_model=Token)
async def refresh_token(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Endpoint para renovar token JWT

    Args:
        current_user: Usuário autenticado
        db: Sessão do banco de dados

    Returns:
        Token: Novo token JWT
    """
    # Criar novo token
    access_token_expires = timedelta(minutes=1440)
    access_token = create_access_token(
        data={
            "user_id": current_user.id,
            "email": current_user.email,
            "role": current_user.role,
            "username": current_user.username
        },
        expires_delta=access_token_expires
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=1440 * 60,
        user=UserResponse.model_validate(current_user)
    )
