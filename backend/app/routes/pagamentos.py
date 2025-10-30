"""
Rotas para gerenciamento de Pagamentos
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List, Optional
from datetime import date
from app.database import get_db
from app.routes.auth import require_role
from app.models.pagamento import Pagamento
from app.models.aluno import Aluno
from app.schemas.pagamento import PagamentoCreate, PagamentoUpdate, PagamentoResponse


router = APIRouter(
    dependencies=[Depends(require_role(["admin", "recepcionista"]))]
)


@router.post("/pagamentos", response_model=PagamentoResponse, status_code=201)
async def criar_pagamento(pagamento: PagamentoCreate, db: Session = Depends(get_db)):
    """Criar novo pagamento"""
    # Verificar se aluno existe
    aluno = db.query(Aluno).filter(Aluno.id == pagamento.aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    db_pagamento = Pagamento(**pagamento.model_dump())
    db.add(db_pagamento)
    db.commit()
    db.refresh(db_pagamento)
    return db_pagamento


@router.get("/pagamentos", response_model=List[PagamentoResponse])
async def listar_pagamentos(
    data_inicio: Optional[date] = Query(None, description="Data inicial para filtro"),
    data_fim: Optional[date] = Query(None, description="Data final para filtro"),
    aluno_id: Optional[int] = Query(None, description="Filtrar por ID do aluno"),
    db: Session = Depends(get_db)
):
    """Listar pagamentos com filtros opcionais"""
    query = db.query(Pagamento)

    if aluno_id:
        query = query.filter(Pagamento.aluno_id == aluno_id)

    if data_inicio:
        query = query.filter(Pagamento.data_pagamento >= data_inicio)

    if data_fim:
        query = query.filter(Pagamento.data_pagamento <= data_fim)

    pagamentos = query.order_by(Pagamento.data_pagamento.desc()).all()
    return pagamentos


@router.get("/pagamentos/{id}", response_model=PagamentoResponse)
async def obter_pagamento(id: int, db: Session = Depends(get_db)):
    """Obter pagamento por ID"""
    pagamento = db.query(Pagamento).filter(Pagamento.id == id).first()
    if not pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    return pagamento


@router.put("/pagamentos/{id}", response_model=PagamentoResponse)
async def atualizar_pagamento(id: int, pagamento_update: PagamentoUpdate, db: Session = Depends(get_db)):
    """Atualizar pagamento"""
    db_pagamento = db.query(Pagamento).filter(Pagamento.id == id).first()
    if not db_pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")

    # Se está alterando aluno_id, verificar se novo aluno existe
    if pagamento_update.aluno_id:
        aluno = db.query(Aluno).filter(Aluno.id == pagamento_update.aluno_id).first()
        if not aluno:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")

    # Atualizar apenas campos fornecidos
    update_data = pagamento_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_pagamento, field, value)

    db.commit()
    db.refresh(db_pagamento)
    return db_pagamento


@router.delete("/pagamentos/{id}", status_code=200)
async def deletar_pagamento(id: int, db: Session = Depends(get_db)):
    """Deletar pagamento"""
    db_pagamento = db.query(Pagamento).filter(Pagamento.id == id).first()
    if not db_pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")

    db.delete(db_pagamento)
    db.commit()

    return {"message": "Pagamento deletado com sucesso", "id": id}


@router.get("/pagamentos/relatorio-mensal", response_model=List[dict])
async def relatorio_mensal(
    ano: Optional[int] = Query(None, description="Ano para o relatório"),
    mes: Optional[int] = Query(None, ge=1, le=12, description="Mês para o relatório (1-12)"),
    db: Session = Depends(get_db)
):
    """
    Gerar relatório mensal de pagamentos
    Retorna total de pagamentos e soma por forma de pagamento
    """
    query = db.query(
        Pagamento.mes_referencia,
        Pagamento.forma_pagamento,
        func.count(Pagamento.id).label('quantidade'),
        func.sum(Pagamento.valor).label('total')
    )

    # Filtrar por ano/mês se fornecido
    if ano and mes:
        mes_ref = f"{ano}-{mes:02d}"
        query = query.filter(Pagamento.mes_referencia == mes_ref)
    elif ano:
        query = query.filter(Pagamento.mes_referencia.like(f"{ano}-%"))

    # Agrupar por mês de referência e forma de pagamento
    relatorio = query.group_by(
        Pagamento.mes_referencia,
        Pagamento.forma_pagamento
    ).order_by(
        Pagamento.mes_referencia.desc(),
        Pagamento.forma_pagamento
    ).all()

    # Formatar resultado
    resultado = []
    for item in relatorio:
        resultado.append({
            "mes_referencia": item.mes_referencia,
            "forma_pagamento": item.forma_pagamento,
            "quantidade": item.quantidade,
            "total": float(item.total)
        })

    return resultado
