"""
Schemas Pydantic para Pagamentos
"""
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from decimal import Decimal


class PagamentoBase(BaseModel):
    """Schema base para Pagamento"""
    aluno_id: int = Field(..., gt=0)
    valor: Decimal = Field(..., ge=0)
    data_pagamento: date
    mes_referencia: str = Field(..., pattern="^\\d{4}-\\d{2}$")  # Formato: YYYY-MM
    forma_pagamento: str = Field(..., pattern="^(dinheiro|pix|cartao_credito|cartao_debito|transferencia)$")
    observacoes: Optional[str] = None


class PagamentoCreate(PagamentoBase):
    """Schema para criação de Pagamento"""
    pass


class PagamentoUpdate(BaseModel):
    """Schema para atualização de Pagamento - todos os campos opcionais"""
    aluno_id: Optional[int] = Field(None, gt=0)
    valor: Optional[Decimal] = Field(None, ge=0)
    data_pagamento: Optional[date] = None
    mes_referencia: Optional[str] = Field(None, pattern="^\\d{4}-\\d{2}$")
    forma_pagamento: Optional[str] = Field(None, pattern="^(dinheiro|pix|cartao_credito|cartao_debito|transferencia)$")
    observacoes: Optional[str] = None


class PagamentoResponse(PagamentoBase):
    """Schema de resposta para Pagamento incluindo metadados"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
