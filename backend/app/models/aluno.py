"""
Model SQLAlchemy para Alunos
"""
from sqlalchemy import Column, Integer, String, Numeric, Date, Boolean, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Aluno(Base):
    """Modelo de Aluno da academia de natação"""
    __tablename__ = "alunos"

    # Campos principais
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome_completo = Column(String(200), nullable=False, index=True)
    responsavel = Column(String(200), nullable=True)

    # Informações da aula e pagamento
    tipo_aula = Column(String(50), nullable=False)  # 'natacao' ou 'hidroginastica'
    valor_mensalidade = Column(Numeric(10, 2), nullable=False)
    dia_vencimento = Column(Integer, nullable=False)  # 1-31
    data_inicio_contrato = Column(Date, nullable=True)
    data_fim_contrato = Column(Date, nullable=True)
    duracao_contrato_meses = Column(Integer, nullable=True, default=12)  # Duração padrão: 12 meses

    # Plano associado
    plano_id = Column(Integer, ForeignKey('planos.id'), nullable=True)
    plano = relationship("Plano", backref="alunos")

    # Status e contato
    ativo = Column(Boolean, default=True, nullable=False)
    telefone_whatsapp = Column(String(20), nullable=True)
    observacoes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)

    def __repr__(self):
        return f"<Aluno(id={self.id}, nome='{self.nome_completo}', tipo_aula='{self.tipo_aula}', ativo={self.ativo})>"
