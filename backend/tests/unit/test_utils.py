"""
Testes Unitários dos Utils
Enterprise-grade: Testes de funções auxiliares e autenticação
"""
import pytest
from datetime import datetime, timedelta, date
from decimal import Decimal

from app.utils.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token
)
from app.utils.helpers import (
    formatar_telefone_brasileiro,
    validar_telefone_brasileiro,
    formatar_moeda_brasileira,
    calcular_dias_atraso,
    calcular_proxima_data_vencimento
)


# ============================================================================
# TESTES DE AUTENTICAÇÃO (utils/auth.py)
# ============================================================================

@pytest.mark.unit
class TestAuthUtils:
    """Testes das funções de autenticação"""

    def test_hash_senha(self):
        """Teste: Hash de senha usando bcrypt"""
        senha = "senha123"
        hash_senha = get_password_hash(senha)

        # Hash deve ser diferente da senha
        assert hash_senha != senha

        # Hash bcrypt tem formato específico
        assert hash_senha.startswith("$2b$")
        assert len(hash_senha) > 50

    def test_verificar_senha_correta(self):
        """Teste: Verificar senha correta"""
        senha = "senha123"
        hash_senha = get_password_hash(senha)

        assert verify_password(senha, hash_senha) is True

    def test_verificar_senha_incorreta(self):
        """Teste: Verificar senha incorreta"""
        senha_correta = "senha123"
        senha_errada = "senha_errada"
        hash_senha = get_password_hash(senha_correta)

        assert verify_password(senha_errada, hash_senha) is False

    def test_criar_access_token(self):
        """Teste: Criar token JWT"""
        data = {
            "user_id": 1,
            "email": "test@example.com",
            "role": "admin"
        }

        token = create_access_token(data)

        # Token deve ser string não vazia
        assert isinstance(token, str)
        assert len(token) > 50

        # Token tem 3 partes separadas por ponto
        parts = token.split(".")
        assert len(parts) == 3

    def test_criar_token_com_expiracao_customizada(self):
        """Teste: Criar token com tempo de expiração customizado"""
        data = {"user_id": 1}
        expires_delta = timedelta(minutes=30)

        token = create_access_token(data, expires_delta=expires_delta)

        # Decodificar e verificar expiração
        payload = decode_access_token(token)

        assert payload is not None
        assert "exp" in payload
        assert "iat" in payload

    def test_decodificar_token_valido(self):
        """Teste: Decodificar token JWT válido"""
        original_data = {
            "user_id": 1,
            "email": "test@example.com",
            "role": "admin"
        }

        token = create_access_token(original_data)
        decoded_data = decode_access_token(token)

        assert decoded_data is not None
        assert decoded_data["user_id"] == 1
        assert decoded_data["email"] == "test@example.com"
        assert decoded_data["role"] == "admin"

    def test_decodificar_token_invalido(self):
        """Teste: Decodificar token inválido retorna None"""
        token_invalido = "token.invalido.fake"

        resultado = decode_access_token(token_invalido)

        assert resultado is None

    def test_decodificar_token_expirado(self):
        """Teste: Token expirado retorna None"""
        data = {"user_id": 1}
        # Criar token que já expirou
        expires_delta = timedelta(seconds=-10)  # Negativo = já expirado

        token = create_access_token(data, expires_delta=expires_delta)
        resultado = decode_access_token(token)

        # Token expirado deve retornar None
        assert resultado is None


# ============================================================================
# TESTES DE HELPERS (utils/helpers.py)
# ============================================================================

@pytest.mark.unit
class TestHelpersUtils:
    """Testes das funções auxiliares"""

    def test_formatar_telefone_com_11_digitos(self):
        """Teste: Formatar telefone com 11 dígitos (celular)"""
        telefone = "11999998888"
        formatado = formatar_telefone_brasileiro(telefone)

        assert formatado == "(11) 99999-8888"

    def test_formatar_telefone_com_10_digitos(self):
        """Teste: Formatar telefone com 10 dígitos (fixo)"""
        telefone = "1133334444"
        formatado = formatar_telefone_brasileiro(telefone)

        assert formatado == "(11) 3333-4444"

    def test_formatar_telefone_com_caracteres_especiais(self):
        """Teste: Formatar telefone removendo caracteres especiais"""
        telefone = "(11) 99999-8888"
        formatado = formatar_telefone_brasileiro(telefone)

        assert formatado == "(11) 99999-8888"

    def test_validar_telefone_brasileiro_valido_11_digitos(self):
        """Teste: Validar telefone brasileiro com 11 dígitos"""
        assert validar_telefone_brasileiro("11999998888") is True
        assert validar_telefone_brasileiro("(11) 99999-8888") is True

    def test_validar_telefone_brasileiro_valido_10_digitos(self):
        """Teste: Validar telefone brasileiro com 10 dígitos"""
        assert validar_telefone_brasileiro("1133334444") is True
        assert validar_telefone_brasileiro("(11) 3333-4444") is True

    def test_validar_telefone_brasileiro_invalido(self):
        """Teste: Validar telefone brasileiro inválido"""
        assert validar_telefone_brasileiro("123") is False
        assert validar_telefone_brasileiro("999999999") is False  # 9 dígitos
        assert validar_telefone_brasileiro("123456789012") is False  # 12 dígitos

    def test_formatar_valor_brl(self):
        """Teste: Formatar valor em BRL"""
        assert formatar_moeda_brasileira(150.00) == "R$ 150,00"
        assert formatar_moeda_brasileira(1234.56) == "R$ 1.234,56"
        assert formatar_moeda_brasileira(1000000.99) == "R$ 1.000.000,99"

    def test_formatar_valor_brl_com_centavos(self):
        """Teste: Formatar valor com centavos"""
        assert formatar_moeda_brasileira(10.50) == "R$ 10,50"
        assert formatar_moeda_brasileira(0.99) == "R$ 0,99"

    def test_calcular_dias_atraso_sem_pagamento(self, sample_aluno):
        """Teste: Calcular dias de atraso quando aluno nunca pagou"""
        # Aluno sem pagamentos
        dias = calcular_dias_atraso(sample_aluno, data_hoje=date(2025, 10, 16))

        # Deve calcular desde a data de início do contrato
        assert dias >= 0

    def test_calcular_dias_atraso_com_pagamento_recente(self, db_session, sample_aluno, pagamento_factory):
        """Teste: Aluno com pagamento recente não está em atraso"""
        # Criar pagamento de hoje
        pagamento_factory.create(
            db_session,
            aluno=sample_aluno,
            data_pagamento=date.today()
        )

        dias = calcular_dias_atraso(sample_aluno, data_hoje=date.today())

        assert dias == 0  # Não está em atraso

    def test_obter_proximo_vencimento_dia_10(self):
        """Teste: Obter próximo vencimento para aluno com dia 10"""
        # Se hoje é dia 5, próximo vencimento é dia 10 deste mês
        data_hoje = date(2025, 10, 5)
        proximo = calcular_proxima_data_vencimento(dia_vencimento=10, data_referencia=data_hoje)

        assert proximo == date(2025, 10, 10)

    def test_obter_proximo_vencimento_ja_passou(self):
        """Teste: Próximo vencimento quando dia já passou no mês"""
        # Se hoje é dia 15 e vencimento é dia 10, próximo é 10 do mês seguinte
        data_hoje = date(2025, 10, 15)
        proximo = calcular_proxima_data_vencimento(dia_vencimento=10, data_referencia=data_hoje)

        assert proximo == date(2025, 11, 10)


# ============================================================================
# TESTES DE EDGE CASES
# ============================================================================

@pytest.mark.unit
class TestEdgeCases:
    """Testes de casos extremos"""

    def test_hash_senha_vazia(self):
        """Teste: Hash de senha vazia"""
        hash_vazia = get_password_hash("")

        assert len(hash_vazia) > 0  # Deve gerar hash mesmo assim

    def test_telefone_vazio(self):
        """Teste: Validação de telefone vazio"""
        assert validar_telefone_brasileiro("") is False
        assert validar_telefone_brasileiro(None) is False

    def test_formatar_valor_zero(self):
        """Teste: Formatar valor zero"""
        assert formatar_moeda_brasileira(0.00) == "R$ 0,00"

    def test_formatar_valor_negativo(self):
        """Teste: Formatar valor negativo"""
        resultado = formatar_moeda_brasileira(-50.00)

        # Deve formatar mesmo sendo negativo
        assert "50" in resultado
        assert "-" in resultado
