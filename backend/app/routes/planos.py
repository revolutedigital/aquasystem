"""
Rotas da API para Planos
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.auth import require_role
from app.models.plano import Plano
from app.schemas.plano import PlanoCreate, PlanoUpdate, PlanoResponse


router = APIRouter(
    dependencies=[Depends(require_role(["admin", "recepcionista"]))]
)


@router.post("/planos", response_model=PlanoResponse, status_code=201)
async def criar_plano(plano: PlanoCreate, db: Session = Depends(get_db)):
    """Criar novo plano"""
    db_plano = Plano(**plano.model_dump())
    db.add(db_plano)
    db.commit()
    db.refresh(db_plano)
    return db_plano


@router.get("/planos", response_model=List[PlanoResponse])
async def listar_planos(
    ativo: bool = True,
    db: Session = Depends(get_db)
):
    """Listar planos - por padrão apenas ativos"""
    query = db.query(Plano)
    if ativo is not None:
        query = query.filter(Plano.ativo == ativo)
    planos = query.order_by(Plano.valor_mensal).all()
    return planos


@router.get("/planos/{id}", response_model=PlanoResponse)
async def obter_plano(id: int, db: Session = Depends(get_db)):
    """Obter plano por ID"""
    plano = db.query(Plano).filter(Plano.id == id).first()
    if not plano:
        raise HTTPException(status_code=404, detail="Plano não encontrado")
    return plano


@router.put("/planos/{id}", response_model=PlanoResponse)
async def atualizar_plano(id: int, plano_data: PlanoUpdate, db: Session = Depends(get_db)):
    """Atualizar plano"""
    db_plano = db.query(Plano).filter(Plano.id == id).first()
    if not db_plano:
        raise HTTPException(status_code=404, detail="Plano não encontrado")

    # Atualizar apenas campos fornecidos
    for field, value in plano_data.model_dump(exclude_unset=True).items():
        setattr(db_plano, field, value)

    db.commit()
    db.refresh(db_plano)
    return db_plano


@router.delete("/planos/{id}", status_code=200)
async def deletar_plano(id: int, db: Session = Depends(get_db)):
    """Soft delete - desativar plano"""
    db_plano = db.query(Plano).filter(Plano.id == id).first()
    if not db_plano:
        raise HTTPException(status_code=404, detail="Plano não encontrado")

    # Soft delete: apenas marcar como inativo
    db_plano.ativo = False
    db.commit()
    return {"message": "Plano desativado com sucesso", "id": id}
