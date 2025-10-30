"""
Rotas para gerenciamento de Horários
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.routes.auth import require_role
from app.models.horario import Horario
from app.models.aluno import Aluno
from app.models.turma import AlunoHorario
from app.schemas.horario import HorarioCreate, HorarioUpdate, HorarioResponse, HorarioComAlunos, AlunoSimplificado


router = APIRouter(
    dependencies=[Depends(require_role(["admin", "recepcionista"]))]
)


@router.post("/horarios", response_model=HorarioResponse, status_code=201)
async def criar_horario(horario: HorarioCreate, db: Session = Depends(get_db)):
    """Criar novo horário"""
    db_horario = Horario(**horario.model_dump())
    db.add(db_horario)
    db.commit()
    db.refresh(db_horario)
    return db_horario


@router.get("/horarios", response_model=List[HorarioResponse])
async def listar_horarios(db: Session = Depends(get_db)):
    """Listar todos os horários"""
    horarios = db.query(Horario).order_by(Horario.dia_semana, Horario.horario).all()
    return horarios


@router.get("/horarios/{id}", response_model=HorarioResponse)
async def obter_horario(id: int, db: Session = Depends(get_db)):
    """Obter horário por ID"""
    horario = db.query(Horario).filter(Horario.id == id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horário não encontrado")
    return horario


@router.put("/horarios/{id}", response_model=HorarioResponse)
async def atualizar_horario(id: int, horario_update: HorarioUpdate, db: Session = Depends(get_db)):
    """Atualizar horário"""
    db_horario = db.query(Horario).filter(Horario.id == id).first()
    if not db_horario:
        raise HTTPException(status_code=404, detail="Horário não encontrado")

    # Atualizar apenas campos fornecidos
    update_data = horario_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_horario, field, value)

    db.commit()
    db.refresh(db_horario)
    return db_horario


@router.delete("/horarios/{id}", status_code=200)
async def deletar_horario(id: int, db: Session = Depends(get_db)):
    """Deletar horário"""
    db_horario = db.query(Horario).filter(Horario.id == id).first()
    if not db_horario:
        raise HTTPException(status_code=404, detail="Horário não encontrado")

    # Verificar se há alunos matriculados
    alunos_matriculados = db.query(AlunoHorario).filter(AlunoHorario.horario_id == id).count()
    if alunos_matriculados > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Não é possível deletar. Existem {alunos_matriculados} aluno(s) matriculado(s) neste horário."
        )

    db.delete(db_horario)
    db.commit()

    return {"message": "Horário deletado com sucesso", "id": id}


@router.post("/horarios/{id}/alunos/{aluno_id}", status_code=201)
async def adicionar_aluno_horario(id: int, aluno_id: int, db: Session = Depends(get_db)):
    """Adicionar aluno a um horário (matrícula)"""
    # Verificar se horário existe
    horario = db.query(Horario).filter(Horario.id == id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horário não encontrado")

    # Verificar se aluno existe e está ativo
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    if not aluno.ativo:
        raise HTTPException(status_code=400, detail="Aluno está inativo")

    # Verificar se aluno já está matriculado neste horário
    matricula_existente = db.query(AlunoHorario).filter(
        AlunoHorario.horario_id == id,
        AlunoHorario.aluno_id == aluno_id
    ).first()
    if matricula_existente:
        raise HTTPException(status_code=400, detail="Aluno já está matriculado neste horário")

    # Verificar capacidade do horário
    alunos_matriculados = db.query(AlunoHorario).filter(AlunoHorario.horario_id == id).count()
    if alunos_matriculados >= horario.capacidade_maxima:
        raise HTTPException(
            status_code=400,
            detail=f"Horário já está com capacidade máxima ({horario.capacidade_maxima} alunos)"
        )

    # Criar matrícula
    nova_matricula = AlunoHorario(horario_id=id, aluno_id=aluno_id)
    db.add(nova_matricula)
    db.commit()
    db.refresh(nova_matricula)

    return {
        "message": "Aluno adicionado ao horário com sucesso",
        "horario_id": id,
        "aluno_id": aluno_id,
        "matricula_id": nova_matricula.id
    }


@router.delete("/horarios/{id}/alunos/{aluno_id}", status_code=200)
async def remover_aluno_horario(id: int, aluno_id: int, db: Session = Depends(get_db)):
    """Remover aluno de um horário (desmatrícula)"""
    # Verificar se matrícula existe
    matricula = db.query(AlunoHorario).filter(
        AlunoHorario.horario_id == id,
        AlunoHorario.aluno_id == aluno_id
    ).first()

    if not matricula:
        raise HTTPException(
            status_code=404,
            detail="Aluno não está matriculado neste horário"
        )

    db.delete(matricula)
    db.commit()

    return {
        "message": "Aluno removido do horário com sucesso",
        "horario_id": id,
        "aluno_id": aluno_id
    }


@router.get("/horarios/{id}/vagas", response_model=dict)
async def obter_vagas_horario(id: int, db: Session = Depends(get_db)):
    """Obter informações sobre vagas disponíveis em um horário"""
    # Verificar se horário existe
    horario = db.query(Horario).filter(Horario.id == id).first()
    if not horario:
        raise HTTPException(status_code=404, detail="Horário não encontrado")

    # Contar alunos matriculados
    alunos_matriculados = db.query(AlunoHorario).filter(AlunoHorario.horario_id == id).count()
    vagas_disponiveis = horario.capacidade_maxima - alunos_matriculados

    return {
        "horario_id": id,
        "dia_semana": horario.dia_semana,
        "horario": str(horario.horario),
        "tipo_aula": horario.tipo_aula,
        "capacidade_maxima": horario.capacidade_maxima,
        "alunos_matriculados": alunos_matriculados,
        "vagas_disponiveis": vagas_disponiveis,
        "percentual_ocupacao": round((alunos_matriculados / horario.capacidade_maxima) * 100, 2)
    }


@router.get("/horarios/grade-completa", response_model=List[HorarioComAlunos])
async def obter_grade_completa(db: Session = Depends(get_db)):
    """
    Obter grade completa de horários com lista de alunos matriculados
    Útil para visualização da grade semanal
    """
    horarios = db.query(Horario).order_by(Horario.dia_semana, Horario.horario).all()

    grade_completa = []
    for horario in horarios:
        # Buscar alunos matriculados neste horário
        matriculas = db.query(AlunoHorario).filter(AlunoHorario.horario_id == horario.id).all()
        alunos = []

        for matricula in matriculas:
            aluno = db.query(Aluno).filter(Aluno.id == matricula.aluno_id).first()
            if aluno:
                alunos.append(AlunoSimplificado(
                    id=aluno.id,
                    nome_completo=aluno.nome_completo,
                    telefone_whatsapp=aluno.telefone_whatsapp
                ))

        # Calcular vagas disponíveis
        vagas_disponiveis = horario.capacidade_maxima - len(alunos)

        # Adicionar à grade
        grade_completa.append(HorarioComAlunos(
            id=horario.id,
            dia_semana=horario.dia_semana,
            horario=horario.horario,
            capacidade_maxima=horario.capacidade_maxima,
            tipo_aula=horario.tipo_aula,
            alunos=alunos,
            vagas_disponiveis=vagas_disponiveis
        ))

    return grade_completa
