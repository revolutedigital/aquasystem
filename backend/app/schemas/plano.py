"""
Schemas Pydantic para Planos
"""
from pydantic import BaseModel, Field
from typing import Optional


class PlanoBase(BaseModel):
    """Schema base para Plano"""
    nome: str = Field(..., min_length=3, max_length=100)
    descricao: Optional[str] = Field(None, max_length=500)
    valor_mensal: float = Field(..., ge=0)
    aulas_por_semana: int = Field(..., ge=1, le=7)
    duracao_aula_minutos: int = Field(default=50, ge=30, le=120)
    acesso_livre: bool = Field(default=False)
    permite_reposicao: bool = Field(default=True)
    dias_tolerancia: int = Field(default=5, ge=0, le=30)


class PlanoCreate(PlanoBase):
    """Schema para criação de Plano"""
    pass


class PlanoUpdate(BaseModel):
    """Schema para atualização de Plano - todos os campos opcionais"""
    nome: Optional[str] = Field(None, min_length=3, max_length=100)
    descricao: Optional[str] = Field(None, max_length=500)
    valor_mensal: Optional[float] = Field(None, ge=0)
    aulas_por_semana: Optional[int] = Field(None, ge=1, le=7)
    duracao_aula_minutos: Optional[int] = Field(None, ge=30, le=120)
    acesso_livre: Optional[bool] = None
    permite_reposicao: Optional[bool] = None
    dias_tolerancia: Optional[int] = Field(None, ge=0, le=30)
    ativo: Optional[bool] = None


class PlanoResponse(PlanoBase):
    """Schema de resposta para Plano"""
    id: int
    ativo: bool

    class Config:
        from_attributes = True
