"""
Schemas Pydantic para Usuários
"""
from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime
from typing import Optional
import re


class UserBase(BaseModel):
    """Schema base para User"""
    email: EmailStr = Field(..., description="Email único do usuário")
    username: str = Field(..., min_length=3, max_length=100, description="Username único")
    full_name: str = Field(..., min_length=1, max_length=200, description="Nome completo")
    role: str = Field(default="recepcionista", pattern="^(admin|recepcionista|aluno)$", description="Papel do usuário")


class UserCreate(UserBase):
    """Schema para criação de User"""
    password: str = Field(..., min_length=12, max_length=100, description="Senha forte (mínimo 12 caracteres)")

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """
        Valida força da senha:
        - Mínimo 12 caracteres
        - Pelo menos 1 letra maiúscula
        - Pelo menos 1 letra minúscula
        - Pelo menos 1 número
        - Pelo menos 1 caractere especial
        """
        errors = []

        if len(v) < 12:
            errors.append("Senha deve ter no mínimo 12 caracteres")

        if not re.search(r"[A-Z]", v):
            errors.append("Senha deve conter pelo menos uma letra maiúscula")

        if not re.search(r"[a-z]", v):
            errors.append("Senha deve conter pelo menos uma letra minúscula")

        if not re.search(r"\d", v):
            errors.append("Senha deve conter pelo menos um número")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=\[\]\\\/~`]", v):
            errors.append("Senha deve conter pelo menos um caractere especial (!@#$%^&* etc)")

        if errors:
            raise ValueError("; ".join(errors))

        return v


class UserUpdate(BaseModel):
    """Schema para atualização de User - todos campos opcionais"""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    full_name: Optional[str] = Field(None, min_length=1, max_length=200)
    role: Optional[str] = Field(None, pattern="^(admin|recepcionista|aluno)$")
    password: Optional[str] = Field(None, min_length=12, max_length=100, description="Senha forte (mínimo 12 caracteres)")
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: Optional[str]) -> Optional[str]:
        """Valida força da senha se fornecida"""
        if v is None:
            return v

        errors = []

        if len(v) < 12:
            errors.append("Senha deve ter no mínimo 12 caracteres")

        if not re.search(r"[A-Z]", v):
            errors.append("Senha deve conter pelo menos uma letra maiúscula")

        if not re.search(r"[a-z]", v):
            errors.append("Senha deve conter pelo menos uma letra minúscula")

        if not re.search(r"\d", v):
            errors.append("Senha deve conter pelo menos um número")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=\[\]\\\/~`]", v):
            errors.append("Senha deve conter pelo menos um caractere especial (!@#$%^&* etc)")

        if errors:
            raise ValueError("; ".join(errors))

        return v


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
