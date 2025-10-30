"""
Testes Unitários dos Models
Enterprise-grade: Validação completa de models SQLAlchemy
"""
import pytest
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy.exc import IntegrityError

from app.models.aluno import Aluno
from app.models.pagamento import Pagamento
from app.models.horario import Horario
from app.models.turma import AlunoHorario
from app.models.user import User


# ============================================================================
# TESTES DO MODEL ALUNO
# ============================================================================

@pytest.mark.unit
class TestAlunoModel:
    """Testes do model Aluno"""

    def test_criar_aluno_completo(self, db_session):
        """Teste: Criar aluno com todos os campos"""
        aluno = Aluno(
            nome_completo="João Silva Santos",
            responsavel="Maria Silva",
            tipo_aula="natacao",
            valor_mensalidade=Decimal("150.00"),
            dia_vencimento=10,
            data_inicio_contrato=date(2025, 1, 15),
            ativo=True,
            telefone_whatsapp="(11) 99999-9999",
            observacoes="Teste completo"
        )

        db_session.add(aluno)
        db_session.commit()
        db_session.refresh(aluno)

        assert aluno.id is not None
        assert aluno.nome_completo == "João Silva Santos"
        assert aluno.tipo_aula == "natacao"
        assert aluno.valor_mensalidade == Decimal("150.00")
        assert aluno.ativo is True
        assert aluno.created_at is not None

    def test_criar_aluno_minimo(self, db_session):
        """Teste: Criar aluno apenas com campos obrigatórios"""
        aluno = Aluno(
            nome_completo="Pedro Costa",
            tipo_aula="hidroginastica",
            valor_mensalidade=Decimal("120.00"),
            dia_vencimento=5
        )

        db_session.add(aluno)
        db_session.commit()

        assert aluno.id is not None
        assert aluno.ativo is True  # Default
        assert aluno.responsavel is None

    def test_soft_delete_aluno(self, sample_aluno):
        """Teste: Soft delete (marcar como inativo)"""
        assert sample_aluno.ativo is True

        sample_aluno.ativo = False

        assert sample_aluno.ativo is False
        assert sample_aluno.id is not None  # Não foi deletado fisicamente

    def test_aluno_repr(self, sample_aluno):
        """Teste: Método __repr__ do aluno"""
        repr_str = repr(sample_aluno)

        assert "Aluno" in repr_str
        assert str(sample_aluno.id) in repr_str
        assert sample_aluno.nome_completo in repr_str
        assert sample_aluno.tipo_aula in repr_str

    def test_aluno_timestamps_automaticos(self, db_session):
        """Teste: Timestamps created_at e updated_at"""
        aluno = Aluno(
            nome_completo="Ana Paula",
            tipo_aula="natacao",
            valor_mensalidade=Decimal("150.00"),
            dia_vencimento=15
        )

        db_session.add(aluno)
        db_session.commit()
        db_session.refresh(aluno)

        # created_at deve ser preenchido automaticamente
        assert aluno.created_at is not None
        assert isinstance(aluno.created_at, datetime)

    def test_relacionamento_aluno_pagamentos(self, db_session, sample_aluno, pagamento_factory):
        """Teste: Relacionamento 1:N com Pagamentos"""
        # Criar 3 pagamentos para o aluno
        for i in range(3):
            pagamento_factory.create(
                db_session,
                aluno=sample_aluno,
                valor=Decimal("150.00")
            )

        db_session.refresh(sample_aluno)

        # Verificar backref
        assert len(sample_aluno.pagamentos) == 3
        assert all(p.aluno_id == sample_aluno.id for p in sample_aluno.pagamentos)


# ============================================================================
# TESTES DO MODEL PAGAMENTO
# ============================================================================

@pytest.mark.unit
class TestPagamentoModel:
    """Testes do model Pagamento"""

    def test_criar_pagamento_completo(self, db_session, sample_aluno):
        """Teste: Criar pagamento com todos os campos"""
        pagamento = Pagamento(
            aluno_id=sample_aluno.id,
            valor=Decimal("150.00"),
            data_pagamento=date(2025, 10, 14),
            mes_referencia="2025-10",
            forma_pagamento="pix",
            observacoes="Pagamento via PIX"
        )

        db_session.add(pagamento)
        db_session.commit()
        db_session.refresh(pagamento)

        assert pagamento.id is not None
        assert pagamento.valor == Decimal("150.00")
        assert pagamento.forma_pagamento == "pix"
        assert pagamento.created_at is not None

    def test_relacionamento_pagamento_aluno(self, sample_pagamento, sample_aluno):
        """Teste: Relacionamento N:1 com Aluno"""
        assert sample_pagamento.aluno_id == sample_aluno.id
        assert sample_pagamento.aluno.nome_completo == sample_aluno.nome_completo

    def test_cascade_delete_pagamentos(self, db_session, sample_aluno, pagamento_factory):
        """Teste: Cascade delete quando aluno é deletado"""
        # Criar pagamento
        pagamento = pagamento_factory.create(db_session, aluno=sample_aluno)
        pagamento_id = pagamento.id

        # Deletar aluno (hard delete para testar cascade)
        db_session.delete(sample_aluno)
        db_session.commit()

        # Pagamento deve ter sido deletado também
        pagamento_deletado = db_session.query(Pagamento).filter(
            Pagamento.id == pagamento_id
        ).first()

        assert pagamento_deletado is None


# ============================================================================
# TESTES DO MODEL HORARIO
# ============================================================================

@pytest.mark.unit
class TestHorarioModel:
    """Testes do model Horário"""

    def test_criar_horario_completo(self, db_session):
        """Teste: Criar horário com todos os campos"""
        horario = Horario(
            dia_semana="Segunda",
            horario="08:00:00",
            capacidade_maxima=20,
            tipo_aula="natacao"
        )

        db_session.add(horario)
        db_session.commit()
        db_session.refresh(horario)

        assert horario.id is not None
        assert horario.dia_semana == "Segunda"
        assert str(horario.horario) == "08:00:00"
        assert horario.capacidade_maxima == 20

    def test_relacionamento_horario_alunos(self, db_session, sample_horario, sample_alunos):
        """Teste: Relacionamento M:N com Alunos"""
        # Matricular 3 alunos no horário
        for aluno in sample_alunos[:3]:
            matricula = AlunoHorario(
                aluno_id=aluno.id,
                horario_id=sample_horario.id
            )
            db_session.add(matricula)

        db_session.commit()
        db_session.refresh(sample_horario)

        # Verificar relacionamento
        matriculas = db_session.query(AlunoHorario).filter(
            AlunoHorario.horario_id == sample_horario.id
        ).all()

        assert len(matriculas) == 3


# ============================================================================
# TESTES DO MODEL USER
# ============================================================================

@pytest.mark.unit
class TestUserModel:
    """Testes do model User"""

    def test_criar_user_admin(self, db_session):
        """Teste: Criar usuário admin"""
        from app.utils.auth import get_password_hash

        user = User(
            email="admin@test.com",
            username="admin_test",
            full_name="Admin Test",
            password_hash=get_password_hash("admin123"),
            role="admin",
            is_active=True
        )

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.id is not None
        assert user.email == "admin@test.com"
        assert user.role == "admin"
        assert user.is_active is True

    def test_user_password_hash_diferente(self, db_session):
        """Teste: Password hash é diferente da senha original"""
        from app.utils.auth import get_password_hash

        senha_original = "senha123"
        hash_senha = get_password_hash(senha_original)

        assert hash_senha != senha_original
        assert len(hash_senha) > 50  # Hash bcrypt é longo

    def test_user_repr(self, admin_user):
        """Teste: Método __repr__ do user"""
        repr_str = repr(admin_user)

        assert "User" in repr_str
        assert admin_user.username in repr_str or admin_user.email in repr_str
