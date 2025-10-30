"""
Testes de Segurança - Autenticação e Autorização
Enterprise-grade: Testes de segurança no nível dos top 10 players
"""
import pytest
from datetime import timedelta


@pytest.mark.security
@pytest.mark.auth
@pytest.mark.critical
class TestAuthenticationSecurity:
    """Testes de segurança de autenticação"""

    def test_login_com_credenciais_validas(self, client, admin_user):
        """Teste: Login com credenciais válidas retorna token"""
        login_data = {
            "email": "admin@test.com",
            "password": "admin123"
        }

        response = client.post("/api/auth/login", json=login_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data

    def test_login_com_senha_incorreta(self, client, admin_user):
        """Teste: Login com senha incorreta retorna 401"""
        login_data = {
            "email": "admin@test.com",
            "password": "senha_errada"
        }

        response = client.post("/api/auth/login", json=login_data)

        assert response.status_code == 401
        assert "incorretos" in response.json()["detail"].lower()

    def test_login_com_email_inexistente(self, client):
        """Teste: Login com email que não existe retorna 401"""
        login_data = {
            "email": "naoexiste@test.com",
            "password": "qualquersenha"
        }

        response = client.post("/api/auth/login", json=login_data)

        assert response.status_code == 401

    def test_login_usuario_inativo(self, client, db_session, admin_user):
        """Teste: Login de usuário inativo retorna 403"""
        # Desativar usuário
        admin_user.is_active = False
        db_session.commit()

        login_data = {
            "email": "admin@test.com",
            "password": "admin123"
        }

        response = client.post("/api/auth/login", json=login_data)

        assert response.status_code == 403
        assert "inativo" in response.json()["detail"].lower()

    def test_acesso_endpoint_protegido_sem_token(self, client):
        """Teste: Acessar endpoint protegido sem token retorna 401/403"""
        response = client.get("/api/alunos")

        assert response.status_code in [401, 403]

    def test_acesso_endpoint_protegido_com_token_invalido(self, client):
        """Teste: Token inválido retorna 401"""
        headers = {"Authorization": "Bearer token_invalido_fake"}

        response = client.get("/api/alunos", headers=headers)

        assert response.status_code == 401

    def test_acesso_endpoint_protegido_com_token_valido(self, client, auth_headers):
        """Teste: Token válido permite acesso"""
        response = client.get("/api/alunos", headers=auth_headers)

        assert response.status_code == 200

    def test_token_expira_corretamente(self, client, db_session, admin_user):
        """Teste: Token expirado não permite acesso"""
        from app.utils.auth import create_access_token

        # Criar token já expirado
        expired_token = create_access_token(
            data={"user_id": admin_user.id},
            expires_delta=timedelta(seconds=-10)
        )

        headers = {"Authorization": f"Bearer {expired_token}"}
        response = client.get("/api/alunos", headers=headers)

        assert response.status_code == 401

    def test_refresh_token_sucesso(self, client, auth_headers):
        """Teste: Refresh token gera novo token"""
        response = client.post("/api/auth/refresh", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert len(data["access_token"]) > 50

    def test_get_me_retorna_usuario_logado(self, client, auth_headers, admin_user):
        """Teste: GET /api/auth/me retorna dados do usuário autenticado"""
        response = client.get("/api/auth/me", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == admin_user.email
        assert data["role"] == admin_user.role


@pytest.mark.security
@pytest.mark.critical
class TestAuthorizationSecurity:
    """Testes de segurança de autorização (roles)"""

    def test_admin_pode_acessar_endpoints_admin(self, client, auth_headers):
        """Teste: Admin tem acesso total"""
        # Deve conseguir listar usuários
        response = client.get("/api/users", headers=auth_headers)
        assert response.status_code == 200

    def test_recepcionista_nao_pode_acessar_users(self, client, recep_auth_headers):
        """Teste: Recepcionista NÃO pode acessar /api/users"""
        response = client.get("/api/users", headers=recep_auth_headers)
        assert response.status_code == 403

    def test_aluno_nao_pode_criar_alunos(self, client, aluno_auth_headers):
        """Teste: Aluno comum não pode criar alunos"""
        aluno_data = {
            "nome_completo": "Teste",
            "tipo_aula": "natacao",
            "valor_mensalidade": 150,
            "dia_vencimento": 10
        }

        response = client.post("/api/alunos", json=aluno_data, headers=aluno_auth_headers)
        assert response.status_code == 403

    def test_roles_validas_apenas(self, client, auth_headers):
        """Teste: Apenas roles válidas são aceitas"""
        user_data = {
            "email": "teste@test.com",
            "username": "teste",
            "full_name": "Teste",
            "password": "senha123",
            "role": "super_admin"  # Role inválida
        }

        response = client.post("/api/users", json=user_data, headers=auth_headers)
        assert response.status_code == 422


@pytest.mark.security
class TestPasswordSecurity:
    """Testes de segurança de senhas"""

    def test_senha_nunca_retornada_na_api(self, client, auth_headers, admin_user):
        """Teste: Hash de senha nunca é exposto na API"""
        response = client.get(f"/api/users/{admin_user.id}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # Não deve conter password_hash ou password
        assert "password" not in data
        assert "password_hash" not in data

    def test_senha_minima_6_caracteres(self, client, auth_headers):
        """Teste: Senha deve ter no mínimo 6 caracteres"""
        user_data = {
            "email": "teste@test.com",
            "username": "teste",
            "full_name": "Teste",
            "password": "123",  # Muito curta
            "role": "aluno"
        }

        response = client.post("/api/users", json=user_data, headers=auth_headers)
        assert response.status_code == 422

    def test_hash_bcrypt_usado(self, db_session, admin_user):
        """Teste: Senhas são hasheadas com bcrypt"""
        # Hash bcrypt começa com $2b$
        assert admin_user.password_hash.startswith("$2b$")
        assert len(admin_user.password_hash) > 50
