"""
Funções auxiliares para o sistema de gestão de natação
"""
from datetime import date, datetime, timedelta
from typing import Optional, List, Dict, Any
import calendar
import re


def calcular_dias_atraso(aluno: Any, data_hoje: Optional[date] = None) -> int:
    """
    Calcula quantos dias de atraso um aluno tem no pagamento

    Args:
        aluno: Objeto do modelo Aluno
        data_hoje: Data de referência (padrão: hoje)

    Returns:
        int: Número de dias de atraso (0 se não houver atraso)
    """
    if data_hoje is None:
        data_hoje = date.today()

    try:
        # Tentar criar data de vencimento com o dia do aluno
        data_vencimento = date(data_hoje.year, data_hoje.month, aluno.dia_vencimento)
    except ValueError:
        # Caso o dia não exista no mês (ex: 31 de fevereiro)
        ultimo_dia = calendar.monthrange(data_hoje.year, data_hoje.month)[1]
        data_vencimento = date(data_hoje.year, data_hoje.month, min(aluno.dia_vencimento, ultimo_dia))

    # Calcular diferença em dias
    dias_atraso = (data_hoje - data_vencimento).days

    # Retornar 0 se não houver atraso
    return max(0, dias_atraso)


def gerar_mes_referencia(data: Optional[date] = None) -> str:
    """
    Gera string de mês de referência no formato YYYY-MM

    Args:
        data: Data de referência (padrão: hoje)

    Returns:
        str: Mês de referência (ex: "2024-03")
    """
    if data is None:
        data = date.today()

    return f"{data.year}-{data.month:02d}"


def formatar_telefone_brasileiro(numero: str) -> str:
    """
    Formata número de telefone brasileiro para padrão (XX) XXXXX-XXXX ou (XX) XXXX-XXXX

    Args:
        numero: Número de telefone em qualquer formato

    Returns:
        str: Telefone formatado
    """
    # Remover caracteres não numéricos
    numero_limpo = ''.join(filter(str.isdigit, numero))

    # Remover código do país se existir
    if numero_limpo.startswith('55') and len(numero_limpo) >= 12:
        numero_limpo = numero_limpo[2:]

    # Formatar conforme tamanho
    if len(numero_limpo) == 11:  # Celular com 9 dígitos
        return f"({numero_limpo[:2]}) {numero_limpo[2:7]}-{numero_limpo[7:]}"
    elif len(numero_limpo) == 10:  # Fixo com 8 dígitos
        return f"({numero_limpo[:2]}) {numero_limpo[2:6]}-{numero_limpo[6:]}"
    else:
        # Retornar como está se não estiver em formato válido
        return numero


def validar_telefone_brasileiro(numero: str) -> bool:
    """
    Valida se o número de telefone brasileiro é válido

    Args:
        numero: Número de telefone

    Returns:
        bool: True se válido, False caso contrário
    """
    # Verificar se o número é None ou vazio
    if numero is None or numero == "":
        return False

    # Remover caracteres não numéricos
    numero_limpo = ''.join(filter(str.isdigit, numero))

    # Remover código do país se existir
    if numero_limpo.startswith('55'):
        numero_limpo = numero_limpo[2:]

    # Validar tamanho (10 ou 11 dígitos)
    if len(numero_limpo) not in [10, 11]:
        return False

    # Validar DDD (11 a 99)
    ddd = int(numero_limpo[:2])
    if ddd < 11 or ddd > 99:
        return False

    # Validar se não é número repetido
    if len(set(numero_limpo)) == 1:
        return False

    return True


def calcular_proxima_data_vencimento(dia_vencimento: int, data_referencia: Optional[date] = None) -> date:
    """
    Calcula a próxima data de vencimento a partir de um dia específico

    Args:
        dia_vencimento: Dia do mês para vencimento (1-31)
        data_referencia: Data de referência (padrão: hoje)

    Returns:
        date: Próxima data de vencimento
    """
    if data_referencia is None:
        data_referencia = date.today()

    # Tentar criar data de vencimento no mês atual
    try:
        data_vencimento = date(data_referencia.year, data_referencia.month, dia_vencimento)
    except ValueError:
        # Dia não existe no mês atual, usar último dia do mês
        ultimo_dia = calendar.monthrange(data_referencia.year, data_referencia.month)[1]
        data_vencimento = date(data_referencia.year, data_referencia.month, ultimo_dia)

    # Se a data já passou, calcular para o próximo mês
    if data_vencimento <= data_referencia:
        # Avançar para o próximo mês
        if data_referencia.month == 12:
            proximo_mes = 1
            proximo_ano = data_referencia.year + 1
        else:
            proximo_mes = data_referencia.month + 1
            proximo_ano = data_referencia.year

        # Tentar criar data no próximo mês
        try:
            data_vencimento = date(proximo_ano, proximo_mes, dia_vencimento)
        except ValueError:
            # Dia não existe no próximo mês, usar último dia
            ultimo_dia = calendar.monthrange(proximo_ano, proximo_mes)[1]
            data_vencimento = date(proximo_ano, proximo_mes, ultimo_dia)

    return data_vencimento


def calcular_estatisticas_periodo(pagamentos: List[Any], inicio: date, fim: date) -> Dict[str, Any]:
    """
    Calcula estatísticas de pagamentos para um período específico

    Args:
        pagamentos: Lista de objetos Pagamento
        inicio: Data de início do período
        fim: Data de fim do período

    Returns:
        Dict: Dicionário com estatísticas
    """
    # Filtrar pagamentos do período
    pagamentos_periodo = [
        p for p in pagamentos
        if inicio <= p.data_vencimento <= fim
    ]

    # Calcular estatísticas
    total_pagamentos = len(pagamentos_periodo)
    pagamentos_realizados = [p for p in pagamentos_periodo if p.pago]
    pagamentos_pendentes = [p for p in pagamentos_periodo if not p.pago]

    total_recebido = sum(float(p.valor) for p in pagamentos_realizados)
    total_pendente = sum(float(p.valor) for p in pagamentos_pendentes)
    total_esperado = total_recebido + total_pendente

    taxa_recebimento = (len(pagamentos_realizados) / total_pagamentos * 100) if total_pagamentos > 0 else 0

    return {
        "total_pagamentos": total_pagamentos,
        "pagamentos_realizados": len(pagamentos_realizados),
        "pagamentos_pendentes": len(pagamentos_pendentes),
        "total_recebido": total_recebido,
        "total_pendente": total_pendente,
        "total_esperado": total_esperado,
        "taxa_recebimento": round(taxa_recebimento, 2),
        "periodo_inicio": inicio.isoformat(),
        "periodo_fim": fim.isoformat()
    }


def formatar_moeda_brasileira(valor: float) -> str:
    """
    Formata valor monetário para padrão brasileiro (R$ 1.234,56)

    Args:
        valor: Valor em float

    Returns:
        str: Valor formatado
    """
    # Formatar com 2 casas decimais
    valor_formatado = f"{valor:,.2f}"

    # Trocar separadores (. para vírgula e , para ponto)
    valor_formatado = valor_formatado.replace(',', 'TEMP')
    valor_formatado = valor_formatado.replace('.', ',')
    valor_formatado = valor_formatado.replace('TEMP', '.')

    return f"R$ {valor_formatado}"


def calcular_taxa_inadimplencia(total_alunos: int, inadimplentes: int) -> float:
    """
    Calcula a taxa de inadimplência em percentual

    Args:
        total_alunos: Número total de alunos ativos
        inadimplentes: Número de alunos inadimplentes

    Returns:
        float: Taxa de inadimplência em percentual (0-100)
    """
    if total_alunos == 0:
        return 0.0

    taxa = (inadimplentes / total_alunos) * 100
    return round(taxa, 2)


# Funções auxiliares adicionais para formatação de CPF (mantidas do código original)

def formatar_cpf(cpf: str) -> str:
    """
    Formata CPF para o padrão XXX.XXX.XXX-XX

    Args:
        cpf: CPF sem formatação

    Returns:
        str: CPF formatado
    """
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11:
        return cpf
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def validar_cpf(cpf: str) -> bool:
    """
    Valida CPF

    Args:
        cpf: CPF a ser validado

    Returns:
        bool: True se válido, False caso contrário
    """
    cpf = ''.join(filter(str.isdigit, cpf))

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    # Validar primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10 % 11) % 10

    if digito1 != int(cpf[9]):
        return False

    # Validar segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10 % 11) % 10

    return digito2 == int(cpf[10])


def calcular_idade(data_nascimento: date) -> int:
    """
    Calcula idade a partir da data de nascimento

    Args:
        data_nascimento: Data de nascimento

    Returns:
        int: Idade em anos
    """
    hoje = date.today()
    idade = hoje.year - data_nascimento.year

    if (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day):
        idade -= 1

    return idade
