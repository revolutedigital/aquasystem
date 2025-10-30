"""
Módulo de Schemas Pydantic
"""
from app.schemas.aluno import (
    AlunoBase,
    AlunoCreate,
    AlunoUpdate,
    AlunoResponse,
    AlunoComPagamentos
)
from app.schemas.pagamento import (
    PagamentoBase,
    PagamentoCreate,
    PagamentoUpdate,
    PagamentoResponse
)
from app.schemas.horario import (
    HorarioBase,
    HorarioCreate,
    HorarioUpdate,
    HorarioResponse,
    HorarioComAlunos,
    AlunoSimplificado
)

__all__ = [
    # Aluno schemas
    "AlunoBase",
    "AlunoCreate",
    "AlunoUpdate",
    "AlunoResponse",
    "AlunoComPagamentos",
    # Pagamento schemas
    "PagamentoBase",
    "PagamentoCreate",
    "PagamentoUpdate",
    "PagamentoResponse",
    # Horario schemas
    "HorarioBase",
    "HorarioCreate",
    "HorarioUpdate",
    "HorarioResponse",
    "HorarioComAlunos",
    "AlunoSimplificado"
]
