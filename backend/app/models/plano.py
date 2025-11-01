"""
Modelo de Plano
"""
from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base


class Plano(Base):
    """Modelo de Plano de Assinatura"""
    __tablename__ = "planos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, index=True)
    descricao = Column(String(500))
    valor_mensal = Column(Float, nullable=False)
    aulas_por_semana = Column(Integer, nullable=False, default=2)
    duracao_aula_minutos = Column(Integer, nullable=False, default=50)
    ativo = Column(Boolean, default=True, nullable=False)

    # Recursos/Benefícios do plano
    acesso_livre = Column(Boolean, default=False)  # Acesso ilimitado
    permite_reposicao = Column(Boolean, default=True)
    dias_tolerancia = Column(Integer, default=5)  # Dias de tolerância para pagamento
