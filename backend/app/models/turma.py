"""
Model SQLAlchemy para relacionamento Aluno-Horário (Turma)
"""
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class AlunoHorario(Base):
    """
    Modelo de relacionamento many-to-many entre Aluno e Horário.
    Representa a matrícula de um aluno em uma turma/horário específico.
    """
    __tablename__ = "aluno_horario"

    # Campos principais
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id", ondelete="CASCADE"), nullable=False, index=True)
    horario_id = Column(Integer, ForeignKey("horarios.id", ondelete="CASCADE"), nullable=False, index=True)

    # Relacionamentos
    aluno = relationship("Aluno", backref="horarios_matriculados")
    horario = relationship("Horario", backref="alunos_matriculados")

    def __repr__(self):
        return f"<AlunoHorario(id={self.id}, aluno_id={self.aluno_id}, horario_id={self.horario_id})>"
