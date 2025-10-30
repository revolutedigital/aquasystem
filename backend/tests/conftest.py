"""
Fixtures e configurações globais de testes - Enterprise Grade
Nível superior aos top 10 players do mercado

Features:
- Database fixtures com transação rollback
- Test client com autenticação automática
- Factories para criação de dados
- Mocks para serviços externos
- Performance monitoring
- Isolation entre testes
"""
import pytest
import os
import sys
from typing import Generator, Dict, Any
from datetime import datetime, timedelta
from decimal import Decimal

# Adicionar app ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models.aluno import Aluno
from app.models.pagamento import Pagamento
from app.models.horario import Horario
from app.models.turma import AlunoHorario
from app.models.user import User
from app.utils.auth import get_password_hash, create_access_token


# ============================================================================
# CONFIGURAÇÃO DE BANCO DE DADOS DE TESTE (IN-MEMORY)
# ============================================================================

@pytest.fixture(scope="session")
def test_engine():
    """
    Engine SQLite in-memory para testes
    Escopo: session (criado uma vez por sessão de testes)
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False  # Não logar queries em testes
    )

    # Criar todas as tabelas
    Base.metadata.create_all(bind=engine)

    yield engine

    # Cleanup
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(test_engine) -> Generator[Session, None, None]:
    """
    Sessão de banco de dados com rollback automático
    Escopo: function (nova sessão para cada teste)

    Garante isolamento total entre testes
    """
    connection = test_engine.connect()
    transaction = connection.begin()

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = SessionLocal()

    yield session

    # Rollback para desfazer todas as alterações do teste
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """
    Test client do FastAPI com banco de dados mockado
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# ============================================================================
# FIXTURES DE AUTENTICAÇÃO
# ============================================================================

@pytest.fixture
def admin_user(db_session: Session) -> User:
    """Criar usuário admin para testes"""
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
    return user


@pytest.fixture
def recepcionista_user(db_session: Session) -> User:
    """Criar usuário recepcionista para testes"""
    user = User(
        email="recep@test.com",
        username="recep_test",
        full_name="Recepcionista Test",
        password_hash=get_password_hash("recep123"),
        role="recepcionista",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def aluno_user(db_session: Session) -> User:
    """Criar usuário aluno para testes"""
    user = User(
        email="aluno@test.com",
        username="aluno_test",
        full_name="Aluno Test",
        password_hash=get_password_hash("aluno123"),
        role="aluno",
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def admin_token(admin_user: User) -> str:
    """Token JWT para usuário admin"""
    return create_access_token(
        data={
            "user_id": admin_user.id,
            "email": admin_user.email,
            "role": admin_user.role,
            "username": admin_user.username
        },
        expires_delta=timedelta(hours=1)
    )


@pytest.fixture
def recepcionista_token(recepcionista_user: User) -> str:
    """Token JWT para usuário recepcionista"""
    return create_access_token(
        data={
            "user_id": recepcionista_user.id,
            "email": recepcionista_user.email,
            "role": recepcionista_user.role,
            "username": recepcionista_user.username
        },
        expires_delta=timedelta(hours=1)
    )


@pytest.fixture
def aluno_token(aluno_user: User) -> str:
    """Token JWT para usuário aluno"""
    return create_access_token(
        data={
            "user_id": aluno_user.id,
            "email": aluno_user.email,
            "role": aluno_user.role,
            "username": aluno_user.username
        },
        expires_delta=timedelta(hours=1)
    )


@pytest.fixture
def auth_headers(admin_token: str) -> Dict[str, str]:
    """Headers com autenticação admin (padrão)"""
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def recep_auth_headers(recepcionista_token: str) -> Dict[str, str]:
    """Headers com autenticação recepcionista"""
    return {"Authorization": f"Bearer {recepcionista_token}"}


@pytest.fixture
def aluno_auth_headers(aluno_token: str) -> Dict[str, str]:
    """Headers com autenticação aluno"""
    return {"Authorization": f"Bearer {aluno_token}"}


# ============================================================================
# FACTORIES DE MODELOS (Pattern: Factory)
# ============================================================================

class AlunoFactory:
    """Factory para criar alunos de teste"""

    @staticmethod
    def create(
        db_session: Session,
        nome_completo: str = "João Silva Santos",
        responsavel: str = "Maria Silva",
        tipo_aula: str = "natacao",
        valor_mensalidade: Decimal = Decimal("150.00"),
        dia_vencimento: int = 10,
        ativo: bool = True,
        telefone_whatsapp: str = "(11) 99999-9999",
        **kwargs
    ) -> Aluno:
        """Criar aluno com dados padrão ou customizados"""
        aluno = Aluno(
            nome_completo=nome_completo,
            responsavel=responsavel,
            tipo_aula=tipo_aula,
            valor_mensalidade=valor_mensalidade,
            dia_vencimento=dia_vencimento,
            ativo=ativo,
            telefone_whatsapp=telefone_whatsapp,
            data_inicio_contrato=datetime.now().date(),
            **kwargs
        )
        db_session.add(aluno)
        db_session.commit()
        db_session.refresh(aluno)
        return aluno

    @staticmethod
    def create_batch(db_session: Session, count: int = 10, **kwargs) -> list[Aluno]:
        """Criar múltiplos alunos"""
        alunos = []
        for i in range(count):
            aluno = AlunoFactory.create(
                db_session,
                nome_completo=f"Aluno Test {i+1}",
                **kwargs
            )
            alunos.append(aluno)
        return alunos


class PagamentoFactory:
    """Factory para criar pagamentos de teste"""

    @staticmethod
    def create(
        db_session: Session,
        aluno: Aluno,
        valor: Decimal = Decimal("150.00"),
        data_pagamento: datetime = None,
        mes_referencia: str = None,
        forma_pagamento: str = "pix",
        **kwargs
    ) -> Pagamento:
        """Criar pagamento com dados padrão ou customizados"""
        if data_pagamento is None:
            data_pagamento = datetime.now().date()
        if mes_referencia is None:
            mes_referencia = datetime.now().strftime("%Y-%m")

        pagamento = Pagamento(
            aluno_id=aluno.id,
            valor=valor,
            data_pagamento=data_pagamento,
            mes_referencia=mes_referencia,
            forma_pagamento=forma_pagamento,
            **kwargs
        )
        db_session.add(pagamento)
        db_session.commit()
        db_session.refresh(pagamento)
        return pagamento


class HorarioFactory:
    """Factory para criar horários de teste"""

    @staticmethod
    def create(
        db_session: Session,
        dia_semana: str = "Segunda",
        horario: str = "08:00:00",
        capacidade_maxima: int = 20,
        tipo_aula: str = "natacao",
        **kwargs
    ) -> Horario:
        """Criar horário com dados padrão ou customizados"""
        horario_obj = Horario(
            dia_semana=dia_semana,
            horario=horario,
            capacidade_maxima=capacidade_maxima,
            tipo_aula=tipo_aula,
            **kwargs
        )
        db_session.add(horario_obj)
        db_session.commit()
        db_session.refresh(horario_obj)
        return horario_obj


# Fixtures dos factories
@pytest.fixture
def aluno_factory():
    """Fixture da factory de alunos"""
    return AlunoFactory


@pytest.fixture
def pagamento_factory():
    """Fixture da factory de pagamentos"""
    return PagamentoFactory


@pytest.fixture
def horario_factory():
    """Fixture da factory de horários"""
    return HorarioFactory


# ============================================================================
# FIXTURES DE DADOS PRÉ-POPULADOS
# ============================================================================

@pytest.fixture
def sample_aluno(db_session: Session, aluno_factory: AlunoFactory) -> Aluno:
    """Aluno de amostra para testes"""
    return aluno_factory.create(db_session)


@pytest.fixture
def sample_alunos(db_session: Session, aluno_factory: AlunoFactory) -> list[Aluno]:
    """Lista de alunos de amostra (10 alunos)"""
    return aluno_factory.create_batch(db_session, count=10)


@pytest.fixture
def sample_pagamento(db_session: Session, sample_aluno: Aluno, pagamento_factory: PagamentoFactory) -> Pagamento:
    """Pagamento de amostra para testes"""
    return pagamento_factory.create(db_session, aluno=sample_aluno)


@pytest.fixture
def sample_horario(db_session: Session, horario_factory: HorarioFactory) -> Horario:
    """Horário de amostra para testes"""
    return horario_factory.create(db_session)


# ============================================================================
# FIXTURES DE MOCK PARA SERVIÇOS EXTERNOS
# ============================================================================

@pytest.fixture
def mock_whatsapp_service(monkeypatch):
    """Mock do serviço de WhatsApp (Evolution API)"""
    class MockWhatsAppService:
        sent_messages = []

        async def enviar_mensagem(self, numero: str, mensagem: str):
            self.sent_messages.append({
                "numero": numero,
                "mensagem": mensagem,
                "timestamp": datetime.now()
            })
            return {"success": True, "message_id": "mock_123"}

    mock_service = MockWhatsAppService()

    # Monkeypatch para substituir o serviço real
    monkeypatch.setattr(
        "app.services.whatsapp_service.WhatsAppService",
        lambda: mock_service
    )

    return mock_service


# ============================================================================
# FIXTURES DE PERFORMANCE MONITORING
# ============================================================================

@pytest.fixture(autouse=True)
def performance_monitor(request):
    """
    Monitor de performance automático para todos os testes
    Loga warnings se teste demorar > 1s
    """
    start_time = datetime.now()

    yield

    duration = (datetime.now() - start_time).total_seconds()

    if duration > 1.0:
        print(f"\n⚠️  SLOW TEST: {request.node.nodeid} took {duration:.2f}s")


# ============================================================================
# FIXTURES DE CLEANUP
# ============================================================================

@pytest.fixture(autouse=True, scope="function")
def reset_rate_limiter():
    """Reset do rate limiter entre testes"""
    yield
    # Aqui você pode adicionar lógica para resetar o rate limiter
    # Por enquanto apenas yield


# ============================================================================
# HOOKS DO PYTEST
# ============================================================================

def pytest_configure(config):
    """Configuração inicial do pytest"""
    # Criar diretório de logs se não existir
    os.makedirs("tests/logs", exist_ok=True)

    # Registrar markers customizados
    config.addinivalue_line(
        "markers", "smoke: Smoke tests for critical paths"
    )


def pytest_collection_modifyitems(config, items):
    """
    Modificar ordem de execução dos testes
    Priorizar testes críticos e smoke
    """
    critical_tests = []
    smoke_tests = []
    other_tests = []

    for item in items:
        if "critical" in item.keywords:
            critical_tests.append(item)
        elif "smoke" in item.keywords:
            smoke_tests.append(item)
        else:
            other_tests.append(item)

    # Executar na ordem: critical -> smoke -> outros
    items[:] = critical_tests + smoke_tests + other_tests


# ============================================================================
# UTILITIES PARA TESTES
# ============================================================================

@pytest.fixture
def assert_valid_response():
    """Helper para validar respostas da API"""
    def _assert(response, expected_status: int = 200, expected_keys: list = None):
        assert response.status_code == expected_status, \
            f"Expected {expected_status}, got {response.status_code}. Response: {response.text}"

        if expected_keys:
            data = response.json()
            for key in expected_keys:
                assert key in data, f"Key '{key}' not found in response. Keys: {data.keys()}"

        return response.json()

    return _assert


@pytest.fixture
def freeze_time(monkeypatch):
    """Congelar tempo para testes determinísticos"""
    def _freeze(frozen_datetime: datetime):
        class FrozenDatetime(datetime):
            @classmethod
            def now(cls, tz=None):
                return frozen_datetime

        monkeypatch.setattr("datetime.datetime", FrozenDatetime)

    return _freeze
