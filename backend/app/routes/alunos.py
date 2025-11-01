"""
Rotas para gerenciamento de Alunos
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.database import get_db
from app.routes.auth import require_role
from app.models.aluno import Aluno
from app.models.pagamento import Pagamento
from app.schemas.aluno import AlunoCreate, AlunoUpdate, AlunoResponse, AlunoComPagamentos
from app.schemas.pagamento import PagamentoResponse


router = APIRouter(
    dependencies=[Depends(require_role(["admin", "recepcionista"]))]
)


@router.post("/alunos", response_model=AlunoResponse, status_code=200)
async def criar_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    """Criar novo aluno"""
    try:
        print(f"📝 Criando aluno: {aluno.nome_completo}")
        print(f"   Dados: {aluno.model_dump()}")
        db_aluno = Aluno(**aluno.model_dump())
        db.add(db_aluno)
        db.commit()
        db.refresh(db_aluno)
        print(f"✅ Aluno criado com sucesso: ID {db_aluno.id}")
        return db_aluno
    except Exception as e:
        print(f"❌ Erro ao criar aluno: {str(e)}")
        print(f"   Tipo do erro: {type(e).__name__}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar aluno: {str(e)}"
        )


@router.get("/alunos", response_model=List[AlunoResponse])
async def listar_alunos(
    ativo: Optional[bool] = Query(True, description="Filtrar por status ativo (padrão: apenas ativos)"),
    tipo_aula: Optional[str] = Query(None, description="Filtrar por tipo de aula (natacao ou hidroginastica)"),
    db: Session = Depends(get_db)
):
    """Listar alunos com filtros opcionais - por padrão lista apenas ativos"""
    query = db.query(Aluno)

    if ativo is not None:
        query = query.filter(Aluno.ativo == ativo)

    if tipo_aula:
        query = query.filter(Aluno.tipo_aula == tipo_aula)

    alunos = query.order_by(Aluno.nome_completo).all()
    return alunos


@router.get("/alunos/inadimplentes", response_model=List[AlunoResponse])
async def listar_alunos_inadimplentes(db: Session = Depends(get_db)):
    """
    Listar alunos inadimplentes (OTIMIZADO - 1 query em vez de N+1)
    Considera inadimplente: aluno ativo sem pagamento nos últimos 45 dias
    """
    from sqlalchemy import func, or_

    # Data limite: 45 dias atrás
    data_limite = datetime.now().date() - timedelta(days=45)

    # Subquery para obter a data do último pagamento de cada aluno
    subquery = db.query(
        Pagamento.aluno_id,
        func.max(Pagamento.data_pagamento).label('ultima_data')
    ).group_by(Pagamento.aluno_id).subquery()

    # Query principal com LEFT JOIN (1 query apenas!)
    alunos_inadimplentes = db.query(Aluno).outerjoin(
        subquery, Aluno.id == subquery.c.aluno_id
    ).filter(
        Aluno.ativo == True,
        or_(
            subquery.c.ultima_data == None,  # Nunca pagou
            subquery.c.ultima_data < data_limite  # Último pagamento há mais de 45 dias
        )
    ).order_by(Aluno.nome_completo).all()

    return alunos_inadimplentes


@router.get("/alunos/{id}", response_model=AlunoResponse)
async def obter_aluno(id: int, db: Session = Depends(get_db)):
    """Obter aluno por ID"""
    aluno = db.query(Aluno).filter(Aluno.id == id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno


@router.put("/alunos/{id}", response_model=AlunoResponse)
async def atualizar_aluno(id: int, aluno_update: AlunoUpdate, db: Session = Depends(get_db)):
    """Atualizar dados do aluno"""
    db_aluno = db.query(Aluno).filter(Aluno.id == id).first()
    if not db_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    # Atualizar apenas campos fornecidos
    update_data = aluno_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_aluno, field, value)

    db.commit()
    db.refresh(db_aluno)
    return db_aluno


@router.delete("/alunos/{id}", status_code=200)
async def deletar_aluno(id: int, db: Session = Depends(get_db)):
    """Soft delete - desativar aluno (set ativo=False)"""
    db_aluno = db.query(Aluno).filter(Aluno.id == id).first()
    if not db_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    # Soft delete: apenas marcar como inativo
    db_aluno.ativo = False
    db.commit()

    return {"message": "Aluno desativado com sucesso", "id": id}


@router.get("/alunos/{id}/pagamentos", response_model=List[PagamentoResponse])
async def listar_pagamentos_aluno(id: int, db: Session = Depends(get_db)):
    """Listar todos os pagamentos de um aluno"""
    # Verificar se aluno existe
    aluno = db.query(Aluno).filter(Aluno.id == id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    pagamentos = db.query(Pagamento).filter(
        Pagamento.aluno_id == id
    ).order_by(Pagamento.data_pagamento.desc()).all()

    return pagamentos
