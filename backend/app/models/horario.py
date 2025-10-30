"""
Model SQLAlchemy para Horários
"""
from sqlalchemy import Column, Integer, String, Time
from app.database import Base

class Horario(Base):
    """Modelo de Horário de aulas"""
    __tablename__ = "horarios"

    # Campos principais
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    dia_semana = Column(String(20), nullable=False, index=True)  # 'segunda', 'terca', etc
    horario = Column(Time, nullable=False)
    capacidade_maxima = Column(Integer, nullable=False, default=10)
    tipo_aula = Column(String(50), nullable=False)  # 'natacao' ou 'hidroginastica'

    def __repr__(self):
        return f"<Horario(id={self.id}, dia='{self.dia_semana}', horario={self.horario}, tipo='{self.tipo_aula}')>"
