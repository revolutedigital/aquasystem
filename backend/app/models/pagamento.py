"""
Model SQLAlchemy para Pagamentos
"""
from sqlalchemy import Column, Integer, String, Numeric, Date, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class Pagamento(Base):
    """Modelo de Pagamento de mensalidades"""
    __tablename__ = "pagamentos"

    # Campos principais
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id", ondelete="CASCADE"), nullable=False, index=True)

    # Informações do pagamento
    valor = Column(Numeric(10, 2), nullable=False)
    data_pagamento = Column(Date, nullable=False, index=True)
    mes_referencia = Column(String(7), nullable=False, index=True)  # Formato: 'YYYY-MM'
    forma_pagamento = Column(String(50), nullable=False)  # 'dinheiro', 'pix', 'cartao', 'transferencia'
    observacoes = Column(Text, nullable=True)

    # Timestamp
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relacionamento com Aluno (com cascade configurado)
    aluno = relationship("Aluno", backref="pagamentos", passive_deletes=True)

    def __repr__(self):
        return f"<Pagamento(id={self.id}, aluno_id={self.aluno_id}, valor={self.valor}, mes='{self.mes_referencia}')>"
