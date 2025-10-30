"""
Serviço de integração com Evolution API para WhatsApp
"""
import os
import requests
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EvolutionWhatsAppService:
    """Serviço para envio de mensagens via Evolution API"""

    def __init__(self, api_url: Optional[str] = None, api_key: Optional[str] = None, instance_name: Optional[str] = None):
        """
        Inicializa o serviço WhatsApp com configurações da Evolution API

        Args:
            api_url: URL da API Evolution (carrega de .env se não fornecido)
            api_key: Chave API (carrega de .env se não fornecido)
            instance_name: Nome da instância (carrega de .env se não fornecido)
        """
        self.api_url = api_url or os.getenv("EVOLUTION_API_URL", "")
        self.api_key = api_key or os.getenv("EVOLUTION_API_KEY", "")
        self.instance_name = instance_name or os.getenv("EVOLUTION_INSTANCE_NAME", "")

        if not self.api_url or not self.api_key or not self.instance_name:
            logger.warning("Evolution API não está completamente configurada. Verifique as variáveis de ambiente.")

    def send_text_message(self, numero: str, mensagem: str) -> bool:
        """
        Envia mensagem de texto via Evolution API

        Args:
            numero: Número do telefone (será formatado automaticamente)
            mensagem: Texto da mensagem

        Returns:
            bool: True se enviado com sucesso, False caso contrário
        """
        if not self.api_url or not self.api_key or not self.instance_name:
            logger.error("Evolution API não configurada corretamente")
            return False

        try:
            # Formatar número para padrão internacional
            numero_formatado = self.format_phone_number(numero)

            # Endpoint da Evolution API
            url = f"{self.api_url}/message/sendText/{self.instance_name}"

            # Headers com apikey
            headers = {
                "apikey": self.api_key,
                "Content-Type": "application/json"
            }

            # Payload
            payload = {
                "number": numero_formatado,
                "text": mensagem
            }

            # Fazer requisição POST
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=30
            )

            if response.status_code == 200 or response.status_code == 201:
                logger.info(f"Mensagem enviada com sucesso para {numero_formatado}")
                return True
            else:
                logger.error(f"Erro ao enviar mensagem. Status: {response.status_code}, Resposta: {response.text}")
                return False

        except requests.exceptions.Timeout:
            logger.error(f"Timeout ao enviar mensagem para {numero}")
            return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro de conexão ao enviar mensagem: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Erro inesperado ao enviar mensagem: {str(e)}")
            return False

    def format_phone_number(self, numero: str) -> str:
        """
        Formata número de telefone para padrão brasileiro internacional (55DDDNUMBER)

        Args:
            numero: Número de telefone em qualquer formato

        Returns:
            str: Número formatado (ex: 5511999999999)
        """
        # Remover caracteres não numéricos
        numero_limpo = ''.join(filter(str.isdigit, numero))

        # Se já tem código do país (55), retornar
        if numero_limpo.startswith('55') and len(numero_limpo) >= 12:
            return numero_limpo

        # Se não tem código do país, adicionar 55
        if len(numero_limpo) == 11 or len(numero_limpo) == 10:
            return f"55{numero_limpo}"

        # Se ainda não está no formato esperado, retornar como está
        logger.warning(f"Número {numero} pode estar em formato inválido: {numero_limpo}")
        return numero_limpo

    def send_aviso_vencimento(self, aluno: Any, dias_antes: int = 3) -> bool:
        """
        Envia aviso de vencimento próximo para o aluno

        Args:
            aluno: Objeto do modelo Aluno com dados necessários
            dias_antes: Quantos dias antes do vencimento está sendo enviado

        Returns:
            bool: True se enviado com sucesso
        """
        try:
            # Calcular data de vencimento
            hoje = datetime.now().date()
            data_vencimento = hoje + timedelta(days=dias_antes)

            # Template de mensagem em PT-BR
            mensagem = f"""
Olá, {aluno.nome_completo}! 👋

Este é um lembrete amigável sobre sua mensalidade de natação.

💰 *Valor:* R$ {float(aluno.valor_mensalidade):.2f}
📅 *Vencimento:* {aluno.dia_vencimento:02d}/{data_vencimento.month:02d}/{data_vencimento.year}
⏰ *Faltam {dias_antes} dias para o vencimento*

Para manter suas aulas em dia, por favor realize o pagamento até a data de vencimento.

Caso já tenha efetuado o pagamento, desconsidere esta mensagem.

Obrigado! 🏊‍♂️
Academia de Natação
""".strip()

            # Usar telefone do aluno
            telefone = aluno.telefone_whatsapp
            if not telefone:
                logger.warning(f"Aluno {aluno.nome_completo} não possui telefone cadastrado")
                return False

            return self.send_text_message(telefone, mensagem)

        except Exception as e:
            logger.error(f"Erro ao enviar aviso de vencimento para aluno {aluno.id}: {str(e)}")
            return False

    def send_aviso_atraso(self, aluno: Any, dias_atraso: int) -> bool:
        """
        Envia aviso de pagamento atrasado para o aluno

        Args:
            aluno: Objeto do modelo Aluno com dados necessários
            dias_atraso: Quantos dias de atraso

        Returns:
            bool: True se enviado com sucesso
        """
        try:
            # Template de cobrança em PT-BR
            mensagem = f"""
Olá, {aluno.nome_completo}! 👋

Identificamos que sua mensalidade de natação está em atraso.

💰 *Valor:* R$ {float(aluno.valor_mensalidade):.2f}
📅 *Vencimento:* {aluno.dia_vencimento:02d}
⚠️ *Dias em atraso:* {dias_atraso} dia(s)

Para regularizar sua situação e continuar aproveitando as aulas, por favor realize o pagamento o quanto antes.

Em caso de dúvidas ou dificuldades, entre em contato conosco.

Contamos com sua compreensão! 🏊‍♂️
Academia de Natação
""".strip()

            # Usar telefone do aluno
            telefone = aluno.telefone_whatsapp
            if not telefone:
                logger.warning(f"Aluno {aluno.nome_completo} não possui telefone cadastrado")
                return False

            return self.send_text_message(telefone, mensagem)

        except Exception as e:
            logger.error(f"Erro ao enviar aviso de atraso para aluno {aluno.id}: {str(e)}")
            return False
