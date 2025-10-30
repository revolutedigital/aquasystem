"""
Testes Unitários dos Schemas Pydantic
Enterprise-grade: Validação completa de input/output
"""
import pytest
from decimal import Decimal
from datetime import date
from pydantic import ValidationError

from app.schemas.aluno import AlunoCreate, AlunoUpdate, AlunoResponse
from app.schemas.pagamento import PagamentoCreate, PagamentoUpdate
from app.schemas.horario import HorarioCreate
from app.schemas.user import UserCreate, UserLogin, Token


# ============================================================================
# TESTES DOS SCHEMAS DE ALUNO
# ============================================================================

@pytest.mark.unit
class TestAlunoSchemas:
    """Testes dos schemas de Aluno"""

    def test_aluno_create_valido(self):
        """Teste: Criar schema AlunoCreate com dados válidos"""
        aluno_data = {
            "nome_completo": "João Silva Santos",
            "responsavel": "Maria Silva",
            "tipo_aula": "natacao",
            "valor_mensalidade": Decimal("150.00"),
            "dia_vencimento": 10,
            "data_inicio_contrato": date(2025, 1, 15),
            "ativo": True,
            "telefone_whatsapp": "(11) 99999-9999"
        }

        aluno = AlunoCreate(**aluno_data)

        assert aluno.nome_completo == "João Silva Santos"
        assert aluno.tipo_aula == "natacao"
        assert aluno.valor_mensalidade == Decimal("150.00")

    def test_aluno_create_tipo_aula_invalido(self):
        """Teste: Validação falha com tipo_aula inválido"""
        aluno_data = {
            "nome_completo": "João Silva",
            "tipo_aula": "futebol",  # Inválido!
            "valor_mensalidade": Decimal("150.00"),
            "dia_vencimento": 10
        }

        with pytest.raises(ValidationError) as exc_info:
            AlunoCreate(**aluno_data)

        # Verificar que erro menciona tipo_aula
        errors = exc_info.value.errors()
        assert any("tipo_aula" in str(error) for error in errors)

    def test_aluno_create_valor_negativo(self):
        """Teste: Validação falha com valor_mensalidade negativo"""
        aluno_data = {
            "nome_completo": "João Silva",
            "tipo_aula": "natacao",
            "valor_mensalidade": Decimal("-50.00"),  # Negativo!
            "dia_vencimento": 10
        }

        with pytest.raises(ValidationError) as exc_info:
            AlunoCreate(**aluno_data)

        errors = exc_info.value.errors()
        assert any("valor_mensalidade" in str(error) for error in errors)

    def test_aluno_create_dia_vencimento_invalido(self):
        """Teste: Validação falha com dia_vencimento fora do range"""
        # Dia 0
        with pytest.raises(ValidationError):
            AlunoCreate(
                nome_completo="João",
                tipo_aula="natacao",
                valor_mensalidade=Decimal("150"),
                dia_vencimento=0  # Inválido
            )

        # Dia 32
        with pytest.raises(ValidationError):
            AlunoCreate(
                nome_completo="João",
                tipo_aula="natacao",
                valor_mensalidade=Decimal("150"),
                dia_vencimento=32  # Inválido
            )

    def test_aluno_update_parcial(self):
        """Teste: AlunoUpdate aceita campos parciais (todos opcionais)"""
        # Apenas valor_mensalidade
        update_data = AlunoUpdate(valor_mensalidade=Decimal("200.00"))
        assert update_data.valor_mensalidade == Decimal("200.00")
        assert update_data.nome_completo is None

        # Apenas ativo
        update_data2 = AlunoUpdate(ativo=False)
        assert update_data2.ativo is False

    def test_aluno_response_serialization(self, sample_aluno):
        """Teste: AlunoResponse serializa corretamente"""
        response = AlunoResponse.model_validate(sample_aluno)

        assert response.id == sample_aluno.id
        assert response.nome_completo == sample_aluno.nome_completo
        assert response.created_at is not None


# ============================================================================
# TESTES DOS SCHEMAS DE PAGAMENTO
# ============================================================================

@pytest.mark.unit
class TestPagamentoSchemas:
    """Testes dos schemas de Pagamento"""

    def test_pagamento_create_valido(self):
        """Teste: Criar PagamentoCreate com dados válidos"""
        pagamento_data = {
            "aluno_id": 1,
            "valor": Decimal("150.00"),
            "data_pagamento": date(2025, 10, 14),
            "mes_referencia": "2025-10",
            "forma_pagamento": "pix"
        }

        pagamento = PagamentoCreate(**pagamento_data)

        assert pagamento.valor == Decimal("150.00")
        assert pagamento.forma_pagamento == "pix"

    def test_pagamento_forma_pagamento_invalida(self):
        """Teste: Validação falha com forma_pagamento inválida"""
        with pytest.raises(ValidationError):
            PagamentoCreate(
                aluno_id=1,
                valor=Decimal("150"),
                data_pagamento=date(2025, 10, 14),
                mes_referencia="2025-10",
                forma_pagamento="bitcoin"  # Não permitido
            )

    def test_pagamento_valor_zero(self):
        """Teste: Validação falha com valor zero ou negativo"""
        with pytest.raises(ValidationError):
            PagamentoCreate(
                aluno_id=1,
                valor=Decimal("0"),  # Zero não permitido
                data_pagamento=date(2025, 10, 14),
                mes_referencia="2025-10",
                forma_pagamento="pix"
            )


# ============================================================================
# TESTES DOS SCHEMAS DE HORARIO
# ============================================================================

@pytest.mark.unit
class TestHorarioSchemas:
    """Testes dos schemas de Horário"""

    def test_horario_create_valido(self):
        """Teste: Criar HorarioCreate com dados válidos"""
        horario_data = {
            "dia_semana": "Segunda",
            "horario": "08:00:00",
            "capacidade_maxima": 20,
            "tipo_aula": "natacao"
        }

        horario = HorarioCreate(**horario_data)

        assert horario.dia_semana == "Segunda"
        assert horario.capacidade_maxima == 20

    def test_horario_capacidade_invalida(self):
        """Teste: Validação falha com capacidade inválida"""
        # Capacidade 0
        with pytest.raises(ValidationError):
            HorarioCreate(
                dia_semana="Segunda",
                horario="08:00:00",
                capacidade_maxima=0,  # Inválido
                tipo_aula="natacao"
            )

        # Capacidade negativa
        with pytest.raises(ValidationError):
            HorarioCreate(
                dia_semana="Segunda",
                horario="08:00:00",
                capacidade_maxima=-5,  # Inválido
                tipo_aula="natacao"
            )


# ============================================================================
# TESTES DOS SCHEMAS DE USER
# ============================================================================

@pytest.mark.unit
class TestUserSchemas:
    """Testes dos schemas de User"""

    def test_user_create_valido(self):
        """Teste: Criar UserCreate com dados válidos"""
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "password": "senha123",
            "role": "admin"
        }

        user = UserCreate(**user_data)

        assert user.email == "test@example.com"
        assert user.role == "admin"

    def test_user_email_invalido(self):
        """Teste: Validação falha com email inválido"""
        with pytest.raises(ValidationError):
            UserCreate(
                email="email_invalido",  # Sem @
                username="testuser",
                full_name="Test",
                password="senha123",
                role="admin"
            )

    def test_user_senha_curta(self):
        """Teste: Validação falha com senha muito curta"""
        with pytest.raises(ValidationError):
            UserCreate(
                email="test@example.com",
                username="testuser",
                full_name="Test",
                password="123",  # Muito curta (< 6 caracteres)
                role="admin"
            )

    def test_user_login_valido(self):
        """Teste: UserLogin aceita email e senha"""
        login_data = {
            "email": "admin@test.com",
            "password": "admin123"
        }

        login = UserLogin(**login_data)

        assert login.email == "admin@test.com"
        assert login.password == "admin123"

    def test_token_structure(self):
        """Teste: Token tem estrutura correta"""
        from app.schemas.user import UserResponse

        user_response = UserResponse(
            id=1,
            email="test@example.com",
            username="testuser",
            full_name="Test User",
            role="admin",
            is_active=True,
            created_at="2025-10-16T10:00:00"
        )

        token = Token(
            access_token="fake_jwt_token",
            token_type="bearer",
            expires_in=86400,
            user=user_response
        )

        assert token.access_token == "fake_jwt_token"
        assert token.token_type == "bearer"
        assert token.user.email == "test@example.com"
