"""
Schemas Pydantic para Professor
"""
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
import re


class ProfessorBase(BaseModel):
    """Schema base de Professor"""
    nome: str
    email: EmailStr
    cpf: str
    telefone: Optional[str] = None
    especialidade: Optional[str] = None  # 'natacao', 'hidroginastica', 'ambos'

    @field_validator('cpf')
    @classmethod
    def validate_cpf(cls, v: str) -> str:
        """Valida formato CPF (XXX.XXX.XXX-XX ou XXXXXXXXXXX)"""
        # Remove caracteres não numéricos
        cpf_digits = re.sub(r'\D', '', v)

        if len(cpf_digits) != 11:
            raise ValueError('CPF deve ter 11 dígitos')

        # Formatar CPF com pontos e traço
        return f"{cpf_digits[:3]}.{cpf_digits[3:6]}.{cpf_digits[6:9]}-{cpf_digits[9:]}"

    @field_validator('especialidade')
    @classmethod
    def validate_especialidade(cls, v: Optional[str]) -> Optional[str]:
        """Valida especialidade do professor"""
        if v is None:
            return v

        valid_especialidades = ['natacao', 'hidroginastica', 'ambos']
        if v.lower() not in valid_especialidades:
            raise ValueError(f'Especialidade deve ser uma de: {", ".join(valid_especialidades)}')

        return v.lower()


class ProfessorCreate(ProfessorBase):
    """Schema para criação de Professor"""
    pass


class ProfessorUpdate(BaseModel):
    """Schema para atualização de Professor"""
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    especialidade: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator('cpf')
    @classmethod
    def validate_cpf(cls, v: Optional[str]) -> Optional[str]:
        """Valida formato CPF se fornecido"""
        if v is None:
            return v

        cpf_digits = re.sub(r'\D', '', v)

        if len(cpf_digits) != 11:
            raise ValueError('CPF deve ter 11 dígitos')

        return f"{cpf_digits[:3]}.{cpf_digits[3:6]}.{cpf_digits[6:9]}-{cpf_digits[9:]}"

    @field_validator('especialidade')
    @classmethod
    def validate_especialidade(cls, v: Optional[str]) -> Optional[str]:
        """Valida especialidade do professor"""
        if v is None:
            return v

        valid_especialidades = ['natacao', 'hidroginastica', 'ambos']
        if v.lower() not in valid_especialidades:
            raise ValueError(f'Especialidade deve ser uma de: {", ".join(valid_especialidades)}')

        return v.lower()


class ProfessorResponse(ProfessorBase):
    """Schema de resposta de Professor"""
    id: int
    is_active: bool

    class Config:
        from_attributes = True
