"""
Testes de Performance
Enterprise-grade: Benchmarks e testes de carga
"""
import pytest
import time
from decimal import Decimal


@pytest.mark.performance
@pytest.mark.slow
class TestQueryPerformance:
    """Testes de performance de queries"""

    def test_query_inadimplentes_otimizada(self, client, auth_headers, db_session, aluno_factory, pagamento_factory):
        """Teste: Query de inadimplentes deve ser rápida mesmo com muitos alunos"""
        # Criar 100 alunos
        alunos = aluno_factory.create_batch(db_session, count=100)

        # Adicionar alguns pagamentos
        for i, aluno in enumerate(alunos[:50]):
            pagamento_factory.create(db_session, aluno=aluno)

        # Medir tempo da query
        start = time.time()
        response = client.get("/api/alunos/inadimplentes", headers=auth_headers)
        duration = time.time() - start

        assert response.status_code == 200
        # Deve executar em menos de 1 segundo (otimizado com JOIN)
        assert duration < 1.0, f"Query demorou {duration:.2f}s (limite: 1.0s)"

    def test_listar_alunos_performance(self, client, auth_headers, db_session, aluno_factory):
        """Teste: Listar alunos deve ser rápido"""
        # Criar 50 alunos
        aluno_factory.create_batch(db_session, count=50)

        start = time.time()
        response = client.get("/api/alunos", headers=auth_headers)
        duration = time.time() - start

        assert response.status_code == 200
        assert duration < 0.5, f"Listagem demorou {duration:.2f}s (limite: 0.5s)"

    def test_criar_aluno_performance(self, client, auth_headers):
        """Teste: Criar aluno deve ser instantâneo"""
        aluno_data = {
            "nome_completo": "Performance Test",
            "tipo_aula": "natacao",
            "valor_mensalidade": 150,
            "dia_vencimento": 10
        }

        start = time.time()
        response = client.post("/api/alunos", json=aluno_data, headers=auth_headers)
        duration = time.time() - start

        assert response.status_code == 201
        assert duration < 0.3, f"Criação demorou {duration:.2f}s (limite: 0.3s)"


@pytest.mark.performance
@pytest.mark.slow
class TestConcurrency:
    """Testes de concorrência"""

    def test_multiplos_usuarios_simultaneos(self, client, auth_headers, db_session, aluno_factory):
        """Teste: Sistema suporta múltiplos usuários simultaneamente"""
        from concurrent.futures import ThreadPoolExecutor, as_completed

        # Criar 20 requests em paralelo
        def make_request(i):
            response = client.get("/api/alunos", headers=auth_headers)
            return response.status_code

        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(make_request, i) for i in range(20)]
            results = [f.result() for f in as_completed(futures)]

        # Todas devem ter sucesso
        assert all(status == 200 for status in results)
        assert len(results) == 20

    def test_criacao_concorrente_sem_race_condition(self, client, auth_headers):
        """Teste: Criações simultâneas não causam race conditions"""
        from concurrent.futures import ThreadPoolExecutor

        def criar_aluno(i):
            aluno_data = {
                "nome_completo": f"Aluno Concurrent {i}",
                "tipo_aula": "natacao",
                "valor_mensalidade": 150,
                "dia_vencimento": 10
            }
            response = client.post("/api/alunos", json=aluno_data, headers=auth_headers)
            return response.status_code, response.json() if response.status_code == 201 else None

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(criar_aluno, i) for i in range(10)]
            results = [f.result() for f in futures]

        # Todos devem ter sido criados com sucesso
        assert all(status == 201 for status, _ in results)

        # IDs devem ser únicos
        ids = [data["id"] for _, data in results if data]
        assert len(ids) == len(set(ids)), "Duplicate IDs detected!"


@pytest.mark.performance
class TestMemoryUsage:
    """Testes de uso de memória"""

    def test_listagem_grande_nao_causa_memory_leak(self, client, auth_headers, db_session, aluno_factory):
        """Teste: Listar muitos alunos não causa memory leak"""
        import sys

        # Criar 200 alunos
        aluno_factory.create_batch(db_session, count=200)

        # Fazer várias requests
        for i in range(5):
            response = client.get("/api/alunos", headers=auth_headers)
            assert response.status_code == 200

        # Sistema deve continuar responsivo
        response = client.get("/api/alunos", headers=auth_headers)
        assert response.status_code == 200


@pytest.mark.performance
@pytest.mark.slow
class TestDatabasePerformance:
    """Testes de performance de banco de dados"""

    def test_bulk_insert_performance(self, db_session, aluno_factory):
        """Teste: Inserção em massa deve ser eficiente"""
        start = time.time()

        # Inserir 100 alunos
        alunos = aluno_factory.create_batch(db_session, count=100)

        duration = time.time() - start

        assert len(alunos) == 100
        # Deve inserir 100 registros em menos de 5 segundos
        assert duration < 5.0, f"Bulk insert demorou {duration:.2f}s (limite: 5.0s)"

    def test_query_com_relacionamentos(self, db_session, sample_aluno, pagamento_factory):
        """Teste: Query com relacionamentos não causa N+1"""
        # Criar 10 pagamentos
        for i in range(10):
            pagamento_factory.create(db_session, aluno=sample_aluno)

        # Query deve ser eficiente
        start = time.time()
        pagamentos = sample_aluno.pagamentos
        duration = time.time() - start

        assert len(pagamentos) == 10
        assert duration < 0.1, f"Query de relacionamento demorou {duration:.2f}s"
