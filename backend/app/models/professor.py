"""
Model SQLAlchemy para Professores
"""
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Professor(Base):
    """Modelo de Professor"""
    __tablename__ = "professores"

    # Campos principais
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    cpf = Column(String(14), unique=True, nullable=False, index=True)
    telefone = Column(String(20), nullable=True)
    especialidade = Column(String(100), nullable=True)  # 'natacao', 'hidroginastica', 'ambos'
    is_active = Column(Boolean, default=True, nullable=False)

    # Relacionamento com horários (um professor pode ter vários horários)
    horarios = relationship("Horario", back_populates="professor")

    def __repr__(self):
        return f"<Professor(id={self.id}, nome='{self.nome}', especialidade='{self.especialidade}', ativo={self.is_active})>"
