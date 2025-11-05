"""
Rotas para gerenciamento de Professores
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.routes.auth import require_role
from app.models.professor import Professor
from app.schemas.professor import ProfessorCreate, ProfessorUpdate, ProfessorResponse


router = APIRouter(
    dependencies=[Depends(require_role(["admin", "recepcionista"]))]
)


@router.post("/professores", response_model=ProfessorResponse, status_code=200)
async def criar_professor(professor: ProfessorCreate, db: Session = Depends(get_db)):
    """Criar novo professor"""
    try:
        print(f"📝 Criando professor: {professor.nome}")
        print(f"   Dados: {professor.model_dump()}")

        # Verificar se já existe professor com mesmo email
        existing_email = db.query(Professor).filter(Professor.email == professor.email).first()
        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Já existe um professor cadastrado com este email"
            )

        # Verificar se já existe professor com mesmo CPF
        existing_cpf = db.query(Professor).filter(Professor.cpf == professor.cpf).first()
        if existing_cpf:
            raise HTTPException(
                status_code=400,
                detail="Já existe um professor cadastrado com este CPF"
            )

        db_professor = Professor(**professor.model_dump())
        db.add(db_professor)
        db.commit()
        db.refresh(db_professor)
        print(f"✅ Professor criado com sucesso: ID {db_professor.id}")
        return db_professor
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erro ao criar professor: {str(e)}")
        print(f"   Tipo do erro: {type(e).__name__}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar professor: {str(e)}"
        )


@router.get("/professores", response_model=List[ProfessorResponse])
async def listar_professores(
    ativo: Optional[bool] = Query(None, description="Filtrar por status ativo"),
    especialidade: Optional[str] = Query(None, description="Filtrar por especialidade (natacao, hidroginastica, ambos)"),
    db: Session = Depends(get_db)
):
    """Listar professores com filtros opcionais"""
    query = db.query(Professor)

    if ativo is not None:
        query = query.filter(Professor.is_active == ativo)

    if especialidade:
        query = query.filter(Professor.especialidade == especialidade.lower())

    professores = query.order_by(Professor.nome).all()
    return professores


@router.get("/professores/{professor_id}", response_model=ProfessorResponse)
async def obter_professor(professor_id: int, db: Session = Depends(get_db)):
    """Obter professor por ID"""
    professor = db.query(Professor).filter(Professor.id == professor_id).first()
    if not professor:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    return professor


@router.put("/professores/{professor_id}", response_model=ProfessorResponse)
async def atualizar_professor(
    professor_id: int,
    professor_update: ProfessorUpdate,
    db: Session = Depends(get_db)
):
    """Atualizar dados de um professor"""
    print(f"🔄 Atualizando professor ID {professor_id}")
    print(f"   Dados: {professor_update.model_dump(exclude_unset=True)}")

    db_professor = db.query(Professor).filter(Professor.id == professor_id).first()
    if not db_professor:
        raise HTTPException(status_code=404, detail="Professor não encontrado")

    # Validar email único (se estiver sendo atualizado)
    if professor_update.email and professor_update.email != db_professor.email:
        existing_email = db.query(Professor).filter(
            Professor.email == professor_update.email,
            Professor.id != professor_id
        ).first()
        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Já existe um professor cadastrado com este email"
            )

    # Validar CPF único (se estiver sendo atualizado)
    if professor_update.cpf and professor_update.cpf != db_professor.cpf:
        existing_cpf = db.query(Professor).filter(
            Professor.cpf == professor_update.cpf,
            Professor.id != professor_id
        ).first()
        if existing_cpf:
            raise HTTPException(
                status_code=400,
                detail="Já existe um professor cadastrado com este CPF"
            )

    try:
        # Atualizar apenas campos fornecidos
        update_data = professor_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_professor, field, value)

        db.commit()
        db.refresh(db_professor)
        print(f"✅ Professor atualizado com sucesso")
        return db_professor
    except Exception as e:
        print(f"❌ Erro ao atualizar professor: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao atualizar professor: {str(e)}"
        )


@router.delete("/professores/{professor_id}", status_code=200)
async def deletar_professor(professor_id: int, db: Session = Depends(get_db)):
    """Deletar professor (soft delete - marca como inativo)"""
    print(f"🗑️  Deletando professor ID {professor_id}")

    db_professor = db.query(Professor).filter(Professor.id == professor_id).first()
    if not db_professor:
        raise HTTPException(status_code=404, detail="Professor não encontrado")

    try:
        # Soft delete - apenas marca como inativo
        db_professor.is_active = False
        db.commit()
        print(f"✅ Professor marcado como inativo")
        return {"message": "Professor removido com sucesso"}
    except Exception as e:
        print(f"❌ Erro ao deletar professor: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao deletar professor: {str(e)}"
        )
