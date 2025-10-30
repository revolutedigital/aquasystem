"""
Schemas Pydantic para Usuários
"""
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Schema base para User"""
    email: EmailStr = Field(..., description="Email único do usuário")
    username: str = Field(..., min_length=3, max_length=100, description="Username único")
    full_name: str = Field(..., min_length=1, max_length=200, description="Nome completo")
    role: str = Field(default="recepcionista", pattern="^(admin|recepcionista|aluno)$", description="Papel do usuário")


class UserCreate(UserBase):
    """Schema para criação de User"""
    password: str = Field(..., min_length=6, max_length=100, description="Senha (mínimo 6 caracteres)")


class UserUpdate(BaseModel):
    """Schema para atualização de User - todos campos opcionais"""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    full_name: Optional[str] = Field(None, min_length=1, max_length=200)
    role: Optional[str] = Field(None, pattern="^(admin|recepcionista|aluno)$")
    password: Optional[str] = Field(None, min_length=6, max_length=100)
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class UserResponse(BaseModel):
    """Schema de resposta para User (sem password_hash)"""
    id: int
    email: str
    username: str
    full_name: str
    role: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema para login"""
    email: str = Field(..., description="Email do usuário")
    password: str = Field(..., description="Senha")


class Token(BaseModel):
    """Schema de resposta do token JWT"""
    access_token: str
    token_type: str
    expires_in: int
    user: UserResponse


class TokenData(BaseModel):
    """Schema de dados decodificados do token"""
    user_id: int
    email: str
    role: str
