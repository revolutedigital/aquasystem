"""
Testes de Integração - API de Alunos
Enterprise-grade: Testes completos de endpoints
"""
import pytest
from decimal import Decimal
from datetime import date


@pytest.mark.integration
@pytest.mark.api
class TestAlunosAPI:
    """Testes dos endpoints de alunos"""

    def test_criar_aluno_sucesso(self, client, auth_headers):
        """Teste: POST /api/alunos - Criar aluno com sucesso"""
        aluno_data = {
            "nome_completo": "João Silva Santos",
            "responsavel": "Maria Silva",
            "tipo_aula": "natacao",
            "valor_mensalidade": 150.00,
            "dia_vencimento": 10,
            "data_inicio_contrato": "2025-01-15",
            "ativo": True,
            "telefone_whatsapp": "(11) 99999-9999"
        }

        response = client.post("/api/alunos", json=aluno_data, headers=auth_headers)

        assert response.status_code == 201
        data = response.json()
        assert data["nome_completo"] == "João Silva Santos"
        assert data["tipo_aula"] == "natacao"
        assert "id" in data

    def test_criar_aluno_sem_autenticacao(self, client):
        """Teste: POST /api/alunos sem autenticação retorna 401/403"""
        aluno_data = {
            "nome_completo": "João Silva",
            "tipo_aula": "natacao",
            "valor_mensalidade": 150.00,
            "dia_vencimento": 10
        }

        response = client.post("/api/alunos", json=aluno_data)

        assert response.status_code in [401, 403]

    def test_criar_aluno_dados_invalidos(self, client, auth_headers):
        """Teste: POST /api/alunos com dados inválidos retorna 422"""
        aluno_data = {
            "nome_completo": "João",
            "tipo_aula": "futebol",  # Tipo inválido
            "valor_mensalidade": -50,  # Valor negativo
            "dia_vencimento": 35  # Dia inválido
        }

        response = client.post("/api/alunos", json=aluno_data, headers=auth_headers)

        assert response.status_code == 422

    def test_listar_alunos_vazio(self, client, auth_headers):
        """Teste: GET /api/alunos retorna lista vazia quando não há alunos"""
        response = client.get("/api/alunos", headers=auth_headers)

        assert response.status_code == 200
        assert response.json() == []

    def test_listar_alunos_com_dados(self, client, auth_headers, sample_alunos):
        """Teste: GET /api/alunos retorna lista de alunos"""
        response = client.get("/api/alunos", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10  # sample_alunos cria 10
        assert all("id" in aluno for aluno in data)

    def test_listar_alunos_filtro_ativo(self, client, auth_headers, db_session, aluno_factory):
        """Teste: GET /api/alunos?ativo=true filtra apenas ativos"""
        # Criar 3 ativos e 2 inativos
        for i in range(3):
            aluno_factory.create(db_session, ativo=True)
        for i in range(2):
            aluno_factory.create(db_session, ativo=False)

        response = client.get("/api/alunos?ativo=true", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all(aluno["ativo"] is True for aluno in data)

    def test_listar_alunos_filtro_tipo_aula(self, client, auth_headers, db_session, aluno_factory):
        """Teste: GET /api/alunos?tipo_aula=natacao filtra por tipo"""
        # Criar 4 natação e 3 hidroginástica
        for i in range(4):
            aluno_factory.create(db_session, tipo_aula="natacao")
        for i in range(3):
            aluno_factory.create(db_session, tipo_aula="hidroginastica")

        response = client.get("/api/alunos?tipo_aula=natacao", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 4
        assert all(aluno["tipo_aula"] == "natacao" for aluno in data)

    def test_buscar_aluno_por_id_sucesso(self, client, auth_headers, sample_aluno):
        """Teste: GET /api/alunos/{id} retorna aluno específico"""
        response = client.get(f"/api/alunos/{sample_aluno.id}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_aluno.id
        assert data["nome_completo"] == sample_aluno.nome_completo

    def test_buscar_aluno_inexistente(self, client, auth_headers):
        """Teste: GET /api/alunos/{id} com ID inexistente retorna 404"""
        response = client.get("/api/alunos/99999", headers=auth_headers)

        assert response.status_code == 404

    def test_atualizar_aluno_sucesso(self, client, auth_headers, sample_aluno):
        """Teste: PUT /api/alunos/{id} atualiza aluno"""
        update_data = {
            "valor_mensalidade": 200.00,
            "dia_vencimento": 15
        }

        response = client.put(
            f"/api/alunos/{sample_aluno.id}",
            json=update_data,
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["valor_mensalidade"] == "200.00"
        assert data["dia_vencimento"] == 15

    def test_deletar_aluno_soft_delete(self, client, auth_headers, sample_aluno):
        """Teste: DELETE /api/alunos/{id} faz soft delete"""
        response = client.delete(f"/api/alunos/{sample_aluno.id}", headers=auth_headers)

        assert response.status_code == 200

        # Verificar que aluno foi desativado (soft delete)
        response_get = client.get(f"/api/alunos/{sample_aluno.id}", headers=auth_headers)
        assert response_get.status_code == 200
        data = response_get.json()
        assert data["ativo"] is False

    def test_listar_inadimplentes(self, client, auth_headers, db_session, aluno_factory, pagamento_factory):
        """Teste: GET /api/alunos/inadimplentes retorna alunos sem pagamento"""
        from datetime import datetime, timedelta

        # Criar aluno com pagamento recente (não inadimplente)
        aluno1 = aluno_factory.create(db_session)
        pagamento_factory.create(
            db_session,
            aluno=aluno1,
            data_pagamento=datetime.now().date()
        )

        # Criar aluno sem pagamento (inadimplente)
        aluno2 = aluno_factory.create(db_session)

        # Criar aluno com pagamento antigo (inadimplente)
        aluno3 = aluno_factory.create(db_session)
        pagamento_factory.create(
            db_session,
            aluno=aluno3,
            data_pagamento=(datetime.now() - timedelta(days=60)).date()
        )

        response = client.get("/api/alunos/inadimplentes", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # Deve ter pelo menos 2 inadimplentes (aluno2 e aluno3)
        assert len(data) >= 2

    @pytest.mark.critical
    def test_criar_aluno_performance(self, client, auth_headers, assert_valid_response):
        """Teste CRÍTICO: Criar aluno deve ser rápido (< 500ms)"""
        import time

        aluno_data = {
            "nome_completo": "Performance Test",
            "tipo_aula": "natacao",
            "valor_mensalidade": 150.00,
            "dia_vencimento": 10
        }

        start = time.time()
        response = client.post("/api/alunos", json=aluno_data, headers=auth_headers)
        duration = time.time() - start

        assert response.status_code == 201
        assert duration < 0.5, f"Criação de aluno demorou {duration:.2f}s (limite: 0.5s)"


@pytest.mark.integration
@pytest.mark.api
class TestPermissoesAlunos:
    """Testes de permissões de acesso aos endpoints de alunos"""

    def test_recepcionista_pode_criar_aluno(self, client, recep_auth_headers):
        """Teste: Recepcionista tem permissão para criar aluno"""
        aluno_data = {
            "nome_completo": "Teste Recepcionista",
            "tipo_aula": "natacao",
            "valor_mensalidade": 150.00,
            "dia_vencimento": 10
        }

        response = client.post("/api/alunos", json=aluno_data, headers=recep_auth_headers)

        assert response.status_code == 201

    def test_aluno_nao_pode_criar_aluno(self, client, aluno_auth_headers):
        """Teste: Aluno comum NÃO tem permissão para criar aluno"""
        aluno_data = {
            "nome_completo": "Teste Sem Permissão",
            "tipo_aula": "natacao",
            "valor_mensalidade": 150.00,
            "dia_vencimento": 10
        }

        response = client.post("/api/alunos", json=aluno_data, headers=aluno_auth_headers)

        assert response.status_code == 403  # Forbidden
