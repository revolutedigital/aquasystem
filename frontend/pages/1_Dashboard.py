import streamlit as st
import requests
import os
from datetime import datetime, date, timedelta
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import sys

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# Adicionar path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import get_global_styles, get_custom_components
from streamlit_hacks import get_improved_contrast_css

# Aplicar estilos globais otimizados
st.markdown(get_global_styles(), unsafe_allow_html=True)
st.markdown(get_improved_contrast_css(), unsafe_allow_html=True)

# Obter componentes customizados
components = get_custom_components()

# CSS para esconder "streamlit app"
st.markdown("""
    <style>
    /* Esconder primeiro item da lista de navegação */
    [data-testid="stSidebarNav"] ul li:first-child,
    [data-testid="stSidebarNav"] > div > ul > li:first-child {
        display: none !important;
    }

    /* Ajustar espaçamento */
    [data-testid="stSidebarNav"] {
        padding-top: 1rem !important;
        margin-top: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# CSS específico da página
st.markdown("""
<style>
.info-card {
    background: var(--bg-card);
    backdrop-filter: blur(20px);
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: var(--shadow-lg);
    border: 1px solid var(--border-color);
    border-left: 5px solid var(--secondary);
    margin: 1rem 0;
}

.info-card h2, .info-card h3, .info-card p {
    color: var(--text-secondary) !important;
}
</style>
""", unsafe_allow_html=True)

API_URL = os.getenv("API_URL", "http://backend:9000")

# Verificar autenticação - Redirecionar para login se necessário
if "access_token" not in st.session_state or st.session_state.access_token is None:
    st.error("🔒 Acesso negado. Por favor, faça login primeiro.")
    st.info("👉 Clique em 'streamlit app' no menu lateral para fazer login")
    st.stop()

# Função auxiliar para headers autenticados
def get_auth_headers():
    """Retorna headers com token de autenticação"""
    return {
        "Authorization": f"Bearer {st.session_state.access_token}",
        "Content-Type": "application/json"
    }

# Header
st.title("📊 Dashboard Executivo")

# Breadcrumb
st.markdown(components["breadcrumb"](["Home", "Dashboard"]), unsafe_allow_html=True)

def formatar_moeda(valor):
    """Formata valor para padrão BR"""
    if valor is None:
        return "R$ 0,00"
    valor_float = float(valor)
    return f"R$ {valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def carregar_alunos():
    """Carrega todos os alunos"""
    try:
        response = requests.get(f"{API_URL}/api/alunos", headers=get_auth_headers(), timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados dos alunos.")
        return []

def carregar_alunos_ativos():
    """Carrega alunos ativos"""
    try:
        response = requests.get(f"{API_URL}/api/alunos", params={"ativo": True}, headers=get_auth_headers(), timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        return []

def carregar_inadimplentes():
    """Carrega alunos inadimplentes"""
    try:
        response = requests.get(f"{API_URL}/api/alunos/inadimplentes", headers=get_auth_headers(), timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        return []

def carregar_pagamentos():
    """Carrega todos os pagamentos"""
    try:
        response = requests.get(f"{API_URL}/api/pagamentos", headers=get_auth_headers(), timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados de pagamentos.")
        return []

def carregar_relatorio_mensal(ano, mes):
    """Carrega relatório mensal de pagamentos"""
    try:
        response = requests.get(
            f"{API_URL}/api/pagamentos/relatorio-mensal",
            params={"ano": ano, "mes": mes},
            headers=get_auth_headers(),
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        return []

def carregar_grade_completa():
    """Carrega grade completa com alunos"""
    try:
        response = requests.get(f"{API_URL}/api/horarios/grade-completa", headers=get_auth_headers(), timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        return []

st.header("📈 Métricas Principais")

col1, col2, col3, col4 = st.columns(4)

alunos_ativos = carregar_alunos_ativos()
inadimplentes = carregar_inadimplentes()
pagamentos = carregar_pagamentos()
grade_completa = carregar_grade_completa()

total_alunos_ativos = len(alunos_ativos)
total_inadimplentes = len(inadimplentes)

data_30_dias_atras = (date.today() - timedelta(days=30)).isoformat()
pagamentos_30_dias = [p for p in pagamentos if p['data_pagamento'] >= data_30_dias_atras]
receita_mensal = sum(float(p['valor']) for p in pagamentos_30_dias)

if grade_completa:
    ocupacoes = []
    for horario in grade_completa:
        num_alunos = len(horario.get('alunos', []))
        capacidade = horario['capacidade_maxima']
        if capacidade > 0:
            ocupacoes.append((num_alunos / capacidade) * 100)
    taxa_ocupacao_media = sum(ocupacoes) / len(ocupacoes) if ocupacoes else 0
else:
    taxa_ocupacao_media = 0

with col1:
    st.metric(
        label="👥 Alunos Ativos",
        value=total_alunos_ativos
    )

with col2:
    st.metric(
        label="⚠️ Inadimplentes",
        value=total_inadimplentes,
        delta=f"-{total_inadimplentes}" if total_inadimplentes > 0 else "0",
        delta_color="inverse"
    )

with col3:
    st.metric(
        label="💰 Receita (30 dias)",
        value=formatar_moeda(receita_mensal)
    )

with col4:
    st.metric(
        label="📊 Taxa de Ocupação",
        value=f"{taxa_ocupacao_media:.1f}%"
    )

st.markdown("---")

st.header("📊 Gráficos e Análises")

col_grafico1, col_grafico2 = st.columns(2)

with col_grafico1:
    st.subheader("💵 Receita Mensal (Últimos 6 Meses)")

    hoje = date.today()
    meses_dados = []

    for i in range(5, -1, -1):
        mes_data = hoje - timedelta(days=30 * i)
        ano = mes_data.year
        mes = mes_data.month

        relatorio = carregar_relatorio_mensal(ano, mes)

        total_mes = sum(float(item['total']) for item in relatorio)

        meses_dados.append({
            "mes": f"{mes:02d}/{ano}",
            "receita": total_mes
        })

    if meses_dados:
        fig_receita = go.Figure(data=[
            go.Bar(
                x=[m['mes'] for m in meses_dados],
                y=[m['receita'] for m in meses_dados],
                marker=dict(
                    color=[m['receita'] for m in meses_dados],
                    colorscale=[[0, '#1565C0'], [1, '#00952F']],
                    line=dict(color='white', width=2)
                ),
                text=[formatar_moeda(m['receita']) for m in meses_dados],
                textposition='auto'
            )
        ])

        fig_receita.update_layout(
            xaxis_title="Mês",
            yaxis_title="Receita (R$)",
            height=400,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(fig_receita, use_container_width=True)
    else:
        st.markdown(components["empty_state"]("💵", "Nenhum dado de receita", "Registre pagamentos para visualizar o gráfico"), unsafe_allow_html=True)

with col_grafico2:
    st.subheader("🏊 Distribuição por Tipo de Aula")

    if alunos_ativos:
        tipos_count = Counter(a['tipo_aula'] for a in alunos_ativos)

        fig_tipos = go.Figure(data=[
            go.Pie(
                labels=[t.capitalize() for t in tipos_count.keys()],
                values=list(tipos_count.values()),
                marker=dict(
                    colors=['#1565C0', '#00952F'],
                    line=dict(color='white', width=2)
                ),
                hole=0.3
            )
        ])

        fig_tipos.update_layout(
            height=400,
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(fig_tipos, use_container_width=True)
    else:
        st.markdown(components["empty_state"]("🏊", "Nenhum aluno cadastrado", "Cadastre alunos para visualizar a distribuição"), unsafe_allow_html=True)

st.markdown("---")

st.subheader("💳 Formas de Pagamento Mais Usadas")

if pagamentos:
    formas_pagamento = Counter(p['forma_pagamento'] for p in pagamentos)

    fig_formas = go.Figure(data=[
        go.Bar(
            y=list(formas_pagamento.keys()),
            x=list(formas_pagamento.values()),
            orientation='h',
            marker=dict(
                color=list(formas_pagamento.values()),
                colorscale=[[0, '#1565C0'], [1, '#00952F']],
                line=dict(color='white', width=2)
            ),
            text=list(formas_pagamento.values()),
            textposition='auto'
        )
    ])

    fig_formas.update_layout(
        xaxis_title="Quantidade de Pagamentos",
        yaxis_title="Forma de Pagamento",
        height=300,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig_formas, use_container_width=True)
else:
    st.markdown(components["empty_state"]("💳", "Nenhum pagamento registrado", "Registre pagamentos para visualizar as formas mais usadas"), unsafe_allow_html=True)

st.markdown("---")

col_tabela1, col_tabela2 = st.columns(2)

with col_tabela1:
    st.markdown("""
    <div class="info-card">
        <h3 style="margin: 0;">🏆 Top 5 Horários Mais Ocupados</h3>
    </div>
    """, unsafe_allow_html=True)

    if grade_completa:
        horarios_ocupacao = []
        for horario in grade_completa:
            num_alunos = len(horario.get('alunos', []))
            capacidade = horario['capacidade_maxima']
            tipo_emoji = "🏊" if horario['tipo_aula'] == "natacao" else "💧"

            horarios_ocupacao.append({
                "horario": f"{horario['dia_semana']} - {horario['horario'][:5]}",
                "tipo": f"{tipo_emoji} {horario['tipo_aula'].capitalize()}",
                "alunos": num_alunos,
                "capacidade": capacidade,
                "ocupacao": f"{(num_alunos/capacidade*100):.0f}%" if capacidade > 0 else "0%"
            })

        horarios_ordenados = sorted(horarios_ocupacao, key=lambda x: x['alunos'], reverse=True)[:5]

        if horarios_ordenados:
            for idx, h in enumerate(horarios_ordenados, 1):
                st.write(f"**{idx}. {h['horario']}** - {h['tipo']}")
                st.write(f"   👥 {h['alunos']}/{h['capacidade']} alunos ({h['ocupacao']})")
                st.write("")
        else:
            st.markdown(components["empty_state"]("📅", "Nenhum horário ocupado", "Matricule alunos nos horários criados"), unsafe_allow_html=True)
    else:
        st.markdown(components["empty_state"]("📅", "Nenhum horário cadastrado", "Crie horários para começar"), unsafe_allow_html=True)

with col_tabela2:
    st.markdown("""
    <div class="info-card">
        <h3 style="margin: 0;">📅 Próximos Vencimentos (7 dias)</h3>
    </div>
    """, unsafe_allow_html=True)

    if alunos_ativos:
        hoje = date.today()
        dia_hoje = hoje.day

        proximos_vencimentos = []

        for aluno in alunos_ativos:
            dia_vencimento = aluno.get('dia_vencimento')
            if dia_vencimento:
                if dia_vencimento >= dia_hoje and dia_vencimento <= dia_hoje + 7:
                    dias_restantes = dia_vencimento - dia_hoje
                    proximos_vencimentos.append({
                        "nome": aluno['nome_completo'],
                        "dia": dia_vencimento,
                        "valor": aluno.get('valor_mensalidade', 0),
                        "dias_restantes": dias_restantes
                    })
                elif dia_hoje > 23 and dia_vencimento <= 7:
                    dias_ate_fim_mes = 30 - dia_hoje
                    dias_restantes = dias_ate_fim_mes + dia_vencimento
                    if dias_restantes <= 7:
                        proximos_vencimentos.append({
                            "nome": aluno['nome_completo'],
                            "dia": dia_vencimento,
                            "valor": aluno.get('valor_mensalidade', 0),
                            "dias_restantes": dias_restantes
                        })

        proximos_vencimentos_ordenados = sorted(proximos_vencimentos, key=lambda x: x['dias_restantes'])

        if proximos_vencimentos_ordenados:
            for v in proximos_vencimentos_ordenados[:5]:
                st.write(f"**{v['nome']}**")
                st.write(f"   📅 Vence dia {v['dia']} (em {v['dias_restantes']} dias)")
                st.write(f"   💰 {formatar_moeda(v['valor'])}")
                st.write("")
        else:
            st.success("✅ Nenhum vencimento nos próximos 7 dias.")
    else:
        st.info("ℹ️ Nenhum aluno ativo cadastrado.")

st.markdown("---")

st.caption("📊 Dashboard atualizado automaticamente com dados em tempo real da plataforma")

# Dark Mode Toggle
st.markdown(components["dark_mode_toggle"], unsafe_allow_html=True)

# Indicador de página ativa
st.markdown(components["page_indicator"]("Dashboard"), unsafe_allow_html=True)
