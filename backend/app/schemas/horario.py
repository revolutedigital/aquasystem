"""
Schemas Pydantic para Horários
"""
from pydantic import BaseModel, Field
from datetime import time
from typing import Optional, List


class HorarioBase(BaseModel):
    """Schema base para Horário"""
    dia_semana: str = Field(..., pattern="^(segunda|terca|quarta|quinta|sexta|sabado|domingo)$")
    horario: time
    capacidade_maxima: int = Field(default=10, ge=1, le=50)
    tipo_aula: str = Field(..., pattern="^(natacao|hidroginastica)$")
    professor_id: Optional[int] = None
    fila_espera: int = Field(default=0, ge=0)


class HorarioCreate(HorarioBase):
    """Schema para criação de Horário"""
    pass


class HorarioUpdate(BaseModel):
    """Schema para atualização de Horário - todos os campos opcionais"""
    dia_semana: Optional[str] = Field(None, pattern="^(segunda|terca|quarta|quinta|sexta|sabado|domingo)$")
    horario: Optional[time] = None
    capacidade_maxima: Optional[int] = Field(None, ge=1, le=50)
    tipo_aula: Optional[str] = Field(None, pattern="^(natacao|hidroginastica)$")
    professor_id: Optional[int] = None
    fila_espera: Optional[int] = Field(None, ge=0)


class HorarioResponse(HorarioBase):
    """Schema de resposta para Horário incluindo metadados"""
    id: int

    class Config:
        from_attributes = True


class AlunoSimplificado(BaseModel):
    """Schema simplificado de Aluno para listagem em horários"""
    id: int
    nome_completo: str
    telefone_whatsapp: Optional[str] = None

    class Config:
        from_attributes = True


class HorarioComAlunos(HorarioResponse):
    """Schema de Horário incluindo lista de alunos matriculados"""
    alunos: List[AlunoSimplificado] = []
    vagas_disponiveis: int
    professor_nome: Optional[str] = None

    class Config:
        from_attributes = True
