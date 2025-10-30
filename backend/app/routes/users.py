"""
Rotas para Gerenciamento de Usuários (CRUD)
Apenas admins podem acessar
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.routes.auth import get_current_user, require_role
from app.utils.auth import get_password_hash

router = APIRouter()


@router.post("/users", response_model=UserResponse, status_code=201)
async def criar_usuario(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """
    Criar novo usuário (apenas admin)

    Args:
        user: Dados do novo usuário
        db: Sessão do banco de dados
        current_user: Usuário admin autenticado

    Returns:
        UserResponse: Usuário criado

    Raises:
        HTTPException: Se email ou username já existe
    """
    # Verificar se email já existe
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Verificar se username já existe
    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username já cadastrado")

    # Criar hash da senha
    password_hash = get_password_hash(user.password)

    # Criar usuário
    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        password_hash=password_hash,
        role=user.role,
        is_active=True,
        is_superuser=(user.role == "admin")
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserResponse.model_validate(db_user)


@router.get("/users", response_model=List[UserResponse])
async def listar_usuarios(
    skip: int = Query(0, ge=0, description="Número de registros a pular"),
    limit: int = Query(50, ge=1, le=100, description="Número máximo de registros"),
    role: Optional[str] = Query(None, description="Filtrar por role"),
    is_active: Optional[bool] = Query(None, description="Filtrar por status ativo"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """
    Listar todos os usuários com paginação (apenas admin)

    Args:
        skip: Número de registros a pular
        limit: Número máximo de registros
        role: Filtro por role
        is_active: Filtro por status ativo
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        List[UserResponse]: Lista de usuários
    """
    query = db.query(User)

    # Aplicar filtros
    if role:
        query = query.filter(User.role == role)

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    # Paginação
    users = query.order_by(User.created_at.desc()).offset(skip).limit(limit).all()

    return [UserResponse.model_validate(u) for u in users]


@router.get("/users/{user_id}", response_model=UserResponse)
async def obter_usuario(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """
    Obter usuário por ID (apenas admin)

    Args:
        user_id: ID do usuário
        db: Sessão do banco de dados
        current_user: Usuário autenticado

    Returns:
        UserResponse: Usuário encontrado

    Raises:
        HTTPException: Se usuário não encontrado
    """
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return UserResponse.model_validate(user)


@router.put("/users/{user_id}", response_model=UserResponse)
async def atualizar_usuario(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """
    Atualizar usuário (apenas admin)

    Args:
        user_id: ID do usuário
        user_update: Dados a atualizar
        db: Sessão do banco de dados
        current_user: Usuário admin autenticado

    Returns:
        UserResponse: Usuário atualizado

    Raises:
        HTTPException: Se usuário não encontrado ou email/username duplicado
    """
    # Buscar usuário
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Atualizar apenas campos fornecidos
    update_data = user_update.model_dump(exclude_unset=True)

    # Verificar unicidade de email
    if "email" in update_data and update_data["email"] != db_user.email:
        existing_email = db.query(User).filter(User.email == update_data["email"]).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Verificar unicidade de username
    if "username" in update_data and update_data["username"] != db_user.username:
        existing_username = db.query(User).filter(User.username == update_data["username"]).first()
        if existing_username:
            raise HTTPException(status_code=400, detail="Username já cadastrado")

    # Se senha foi fornecida, fazer hash
    if "password" in update_data:
        update_data["password_hash"] = get_password_hash(update_data.pop("password"))

    # Atualizar is_superuser se role mudou
    if "role" in update_data:
        update_data["is_superuser"] = (update_data["role"] == "admin")

    # Aplicar atualizações
    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)

    return UserResponse.model_validate(db_user)


@router.delete("/users/{user_id}", status_code=200)
async def deletar_usuario(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """
    Desativar usuário (soft delete) (apenas admin)

    Args:
        user_id: ID do usuário
        db: Sessão do banco de dados
        current_user: Usuário admin autenticado

    Returns:
        dict: Mensagem de sucesso

    Raises:
        HTTPException: Se usuário não encontrado ou tentativa de deletar a si mesmo
    """
    # Buscar usuário
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Não permitir que admin delete a si mesmo
    if db_user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Você não pode desativar sua própria conta"
        )

    # Soft delete: apenas marcar como inativo
    db_user.is_active = False
    db.commit()

    return {
        "message": "Usuário desativado com sucesso",
        "user_id": user_id
    }


@router.post("/users/{user_id}/activate", response_model=UserResponse)
async def ativar_usuario(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    """
    Reativar usuário desativado (apenas admin)

    Args:
        user_id: ID do usuário
        db: Sessão do banco de dados
        current_user: Usuário admin autenticado

    Returns:
        UserResponse: Usuário reativado

    Raises:
        HTTPException: Se usuário não encontrado
    """
    # Buscar usuário
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Reativar usuário
    db_user.is_active = True
    db.commit()
    db.refresh(db_user)

    return UserResponse.model_validate(db_user)
