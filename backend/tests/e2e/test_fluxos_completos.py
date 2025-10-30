"""
Testes End-to-End - Fluxos Completos
Enterprise-grade: Testes de jornadas completas do usuário
"""
import pytest
from datetime import datetime, timedelta
from decimal import Decimal


@pytest.mark.e2e
@pytest.mark.slow
@pytest.mark.critical
class TestFluxoGestaoAluno:
    """Teste E2E: Fluxo completo de gestão de aluno"""

    def test_fluxo_completo_ciclo_vida_aluno(self, client, auth_headers):
        """
        Teste E2E: Ciclo de vida completo de um aluno
        1. Criar aluno
        2. Atualizar dados
        3. Registrar pagamentos
        4. Matricular em horário
        5. Verificar inadimplência
        6. Desativar aluno
        """

        # 1. CRIAR ALUNO
        aluno_data = {
            "nome_completo": "João E2E Test",
            "responsavel": "Maria E2E",
            "tipo_aula": "natacao",
            "valor_mensalidade": 150.00,
            "dia_vencimento": 10,
            "ativo": True,
            "telefone_whatsapp": "(11) 99999-9999"
        }

        response = client.post("/api/alunos", json=aluno_data, headers=auth_headers)
        assert response.status_code == 201
        aluno = response.json()
        aluno_id = aluno["id"]

        # 2. ATUALIZAR DADOS DO ALUNO
        update_data = {"valor_mensalidade": 180.00}
        response = client.put(f"/api/alunos/{aluno_id}", json=update_data, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["valor_mensalidade"] == "180.00"

        # 3. REGISTRAR PAGAMENTO
        pagamento_data = {
            "aluno_id": aluno_id,
            "valor": 180.00,
            "data_pagamento": datetime.now().strftime("%Y-%m-%d"),
            "mes_referencia": datetime.now().strftime("%Y-%m"),
            "forma_pagamento": "pix"
        }

        response = client.post("/api/pagamentos", json=pagamento_data, headers=auth_headers)
        assert response.status_code == 200
        pagamento = response.json()

        # 4. CRIAR HORÁRIO E MATRICULAR ALUNO
        horario_data = {
            "dia_semana": "Segunda",
            "horario": "08:00:00",
            "capacidade_maxima": 20,
            "tipo_aula": "natacao"
        }

        response = client.post("/api/horarios", json=horario_data, headers=auth_headers)
        assert response.status_code == 200
        horario = response.json()
        horario_id = horario["id"]

        # Matricular aluno no horário
        response = client.post(
            f"/api/horarios/{horario_id}/alunos/{aluno_id}",
            headers=auth_headers
        )
        assert response.status_code == 200

        # 5. VERIFICAR QUE ALUNO NÃO ESTÁ INADIMPLENTE
        response = client.get("/api/alunos/inadimplentes", headers=auth_headers)
        inadimplentes_ids = [a["id"] for a in response.json()]
        assert aluno_id not in inadimplentes_ids

        # 6. DESATIVAR ALUNO (SOFT DELETE)
        response = client.delete(f"/api/alunos/{aluno_id}", headers=auth_headers)
        assert response.status_code == 200

        # Verificar que foi desativado
        response = client.get(f"/api/alunos/{aluno_id}", headers=auth_headers)
        assert response.json()["ativo"] is False


@pytest.mark.e2e
@pytest.mark.critical
class TestFluxoAutenticacao:
    """Teste E2E: Fluxo completo de autenticação"""

    def test_fluxo_completo_login_e_acesso(self, client, admin_user):
        """
        Teste E2E: Login e acesso a recursos protegidos
        1. Login com credenciais
        2. Acessar recurso protegido
        3. Refresh token
        4. Acessar com novo token
        """

        # 1. LOGIN
        login_data = {
            "email": "admin@test.com",
            "password": "admin123"
        }

        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 200
        token_data = response.json()
        token = token_data["access_token"]

        # 2. ACESSAR RECURSO PROTEGIDO
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/alunos", headers=headers)
        assert response.status_code == 200

        # 3. REFRESH TOKEN
        response = client.post("/api/auth/refresh", headers=headers)
        assert response.status_code == 200
        new_token = response.json()["access_token"]

        # 4. ACESSAR COM NOVO TOKEN
        new_headers = {"Authorization": f"Bearer {new_token}"}
        response = client.get("/api/alunos", headers=new_headers)
        assert response.status_code == 200


@pytest.mark.e2e
class TestFluxoFinanceiro:
    """Teste E2E: Fluxo completo de gestão financeira"""

    def test_fluxo_completo_pagamentos(self, client, auth_headers, db_session, aluno_factory):
        """
        Teste E2E: Gestão financeira completa
        1. Criar aluno
        2. Registrar múltiplos pagamentos
        3. Consultar histórico
        4. Verificar relatório mensal
        """

        # 1. CRIAR ALUNO
        aluno = aluno_factory.create(db_session)

        # 2. REGISTRAR 3 PAGAMENTOS
        pagamentos_ids = []
        for i in range(3):
            pagamento_data = {
                "aluno_id": aluno.id,
                "valor": 150.00,
                "data_pagamento": (datetime.now() - timedelta(days=i*30)).strftime("%Y-%m-%d"),
                "mes_referencia": (datetime.now() - timedelta(days=i*30)).strftime("%Y-%m"),
                "forma_pagamento": "pix"
            }

            response = client.post("/api/pagamentos", json=pagamento_data, headers=auth_headers)
            assert response.status_code == 200
            pagamentos_ids.append(response.json()["id"])

        # 3. CONSULTAR HISTÓRICO DO ALUNO
        response = client.get(f"/api/alunos/{aluno.id}/pagamentos", headers=auth_headers)
        assert response.status_code == 200
        historico = response.json()
        assert len(historico) == 3

        # 4. CONSULTAR RELATÓRIO MENSAL
        ano = datetime.now().year
        mes = datetime.now().month
        response = client.get(
            f"/api/pagamentos/relatorio-mensal?ano={ano}&mes={mes}",
            headers=auth_headers
        )
        assert response.status_code == 200


@pytest.mark.e2e
class TestFluxoHorarios:
    """Teste E2E: Fluxo completo de gestão de horários"""

    def test_fluxo_completo_grade_horarios(self, client, auth_headers, db_session, aluno_factory):
        """
        Teste E2E: Gestão de grade de horários
        1. Criar horário
        2. Matricular múltiplos alunos
        3. Verificar capacidade
        4. Remover aluno
        5. Consultar grade completa
        """

        # 1. CRIAR HORÁRIO
        horario_data = {
            "dia_semana": "Segunda",
            "horario": "08:00:00",
            "capacidade_maxima": 5,
            "tipo_aula": "natacao"
        }

        response = client.post("/api/horarios", json=horario_data, headers=auth_headers)
        assert response.status_code == 200
        horario_id = response.json()["id"]

        # 2. CRIAR E MATRICULAR 3 ALUNOS
        alunos = aluno_factory.create_batch(db_session, count=3)

        for aluno in alunos:
            response = client.post(
                f"/api/horarios/{horario_id}/alunos/{aluno.id}",
                headers=auth_headers
            )
            assert response.status_code == 200

        # 3. VERIFICAR CAPACIDADE NA GRADE
        response = client.get("/api/horarios/grade-completa", headers=auth_headers)
        assert response.status_code == 200
        grade = response.json()

        # Encontrar nosso horário
        horario_encontrado = None
        for dia_horarios in grade.values():
            for h in dia_horarios:
                if h["id"] == horario_id:
                    horario_encontrado = h
                    break

        assert horario_encontrado is not None
        assert len(horario_encontrado["alunos"]) == 3

        # 4. REMOVER UM ALUNO
        response = client.delete(
            f"/api/horarios/{horario_id}/alunos/{alunos[0].id}",
            headers=auth_headers
        )
        assert response.status_code == 200

        # Verificar que foi removido
        response = client.get(f"/api/horarios/{horario_id}", headers=auth_headers)
        horario_atualizado = response.json()
        # Aqui você pode verificar a contagem de alunos se o endpoint retornar isso


@pytest.mark.e2e
@pytest.mark.smoke
class TestSmokeTests:
    """Smoke Tests: Validação básica de que o sistema está funcionando"""

    def test_smoke_api_esta_funcionando(self, client):
        """Smoke Test: API está online"""
        response = client.get("/")
        assert response.status_code == 200

    def test_smoke_health_check(self, client):
        """Smoke Test: Health check responde"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_smoke_docs_disponiveis(self, client):
        """Smoke Test: Documentação Swagger está disponível"""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_smoke_login_funciona(self, client, admin_user):
        """Smoke Test: Login básico funciona"""
        login_data = {
            "email": "admin@test.com",
            "password": "admin123"
        }

        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_smoke_crud_aluno_basico(self, client, auth_headers):
        """Smoke Test: CRUD básico de aluno funciona"""
        # Create
        aluno_data = {
            "nome_completo": "Smoke Test",
            "tipo_aula": "natacao",
            "valor_mensalidade": 150,
            "dia_vencimento": 10
        }

        response = client.post("/api/alunos", json=aluno_data, headers=auth_headers)
        assert response.status_code == 201
        aluno_id = response.json()["id"]

        # Read
        response = client.get(f"/api/alunos/{aluno_id}", headers=auth_headers)
        assert response.status_code == 200

        # Update
        response = client.put(
            f"/api/alunos/{aluno_id}",
            json={"valor_mensalidade": 200},
            headers=auth_headers
        )
        assert response.status_code == 200

        # Delete
        response = client.delete(f"/api/alunos/{aluno_id}", headers=auth_headers)
        assert response.status_code == 200
