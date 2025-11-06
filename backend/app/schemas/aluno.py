"""
Schemas Pydantic para Alunos
"""
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List
from decimal import Decimal


class AlunoBase(BaseModel):
    """Schema base para Aluno com todos os campos"""
    nome_completo: str = Field(..., min_length=1, max_length=200)
    responsavel: Optional[str] = Field(None, max_length=200)
    tipo_aula: str = Field(..., pattern="^(natacao|hidroginastica)$")
    valor_mensalidade: Decimal = Field(..., ge=0)
    dia_vencimento: int = Field(..., ge=1, le=31)
    data_inicio_contrato: Optional[date] = None
    data_fim_contrato: Optional[date] = None
    duracao_contrato_meses: Optional[int] = Field(default=12, ge=1, le=60)
    ativo: bool = True
    telefone_whatsapp: Optional[str] = Field(None, max_length=20)
    observacoes: Optional[str] = None


class AlunoCreate(AlunoBase):
    """Schema para criação de Aluno"""
    pass


class AlunoUpdate(BaseModel):
    """Schema para atualização de Aluno - todos os campos opcionais"""
    nome_completo: Optional[str] = Field(None, min_length=1, max_length=200)
    responsavel: Optional[str] = Field(None, max_length=200)
    tipo_aula: Optional[str] = Field(None, pattern="^(natacao|hidroginastica)$")
    valor_mensalidade: Optional[Decimal] = Field(None, ge=0)
    dia_vencimento: Optional[int] = Field(None, ge=1, le=31)
    data_inicio_contrato: Optional[date] = None
    data_fim_contrato: Optional[date] = None
    duracao_contrato_meses: Optional[int] = Field(None, ge=1, le=60)
    ativo: Optional[bool] = None
    telefone_whatsapp: Optional[str] = Field(None, max_length=20)
    observacoes: Optional[str] = None


class AlunoResponse(AlunoBase):
    """Schema de resposta para Aluno incluindo metadados"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AlunoComPagamentos(AlunoResponse):
    """Schema de Aluno incluindo lista de pagamentos"""
    pagamentos: List["PagamentoResponse"] = []

    class Config:
        from_attributes = True


# Importação para resolver referência circular
from app.schemas.pagamento import PagamentoResponse
AlunoComPagamentos.model_rebuild()
