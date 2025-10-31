import streamlit as st
import requests
import os
from datetime import datetime, date, timedelta
from decimal import Decimal
import sys

st.set_page_config(page_title="Financeiro", page_icon="💰", layout="wide")

# Adicionar path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import get_global_styles, get_custom_components, create_pagination, render_pagination_controls
from streamlit_hacks import get_improved_contrast_css
from auth_utils import require_authentication, get_auth_headers, hide_streamlit_app_from_sidebar

# Verificar autenticação PRIMEIRO
require_authentication()

# Aplicar estilos globais otimizados
st.markdown(get_global_styles(), unsafe_allow_html=True)
st.markdown(get_improved_contrast_css(), unsafe_allow_html=True)

# Esconder 'streamlit app' do menu
hide_streamlit_app_from_sidebar()

# Obter componentes customizados
components = get_custom_components()

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

.whatsapp-button > button {
    background: linear-gradient(135deg, #00952F 0%, #00C853 100%) !important;
}
</style>
""", unsafe_allow_html=True)

API_URL = os.getenv("API_URL", "http://backend:9000")

# Header
st.title("💰 Controle Financeiro")

# Breadcrumb
st.markdown(components["breadcrumb"](["Home", "Financeiro"]), unsafe_allow_html=True)

def formatar_moeda(valor):
    """Formata valor para padrão BR"""
    if valor is None:
        return "R$ 0,00"
    valor_float = float(valor)
    return f"R$ {valor_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def validar_telefone(telefone):
    """Valida se o telefone tem 10 ou 11 dígitos"""
    if not telefone:
        return False
    apenas_numeros = ''.join(filter(str.isdigit, telefone))
    return len(apenas_numeros) in [10, 11]

def formatar_telefone(telefone):
    """Formata telefone para padrão brasileiro"""
    if not telefone:
        return ""
    apenas_numeros = ''.join(filter(str.isdigit, telefone))
    if len(apenas_numeros) == 11:
        return f"({apenas_numeros[:2]}) {apenas_numeros[2:7]}-{apenas_numeros[7:]}"
    elif len(apenas_numeros) == 10:
        return f"({apenas_numeros[:2]}) {apenas_numeros[2:6]}-{apenas_numeros[6:]}"
    return telefone

def carregar_alunos_ativos():
    """Carrega lista de alunos ativos"""
    try:
        response = requests.get(f"{API_URL}/api/alunos", params={"ativo": True}, headers=get_auth_headers(), timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados dos alunos.")
        return []

def carregar_todos_alunos():
    """Carrega todos os alunos"""
    try:
        response = requests.get(f"{API_URL}/api/alunos", headers=get_auth_headers(), timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados dos alunos.")
        return []

tab1, tab2, tab3 = st.tabs(["📝 Registrar Pagamento", "📜 Histórico de Pagamentos", "⚠️ Inadimplentes"])

with tab1:
    st.markdown("""
    <div class="info-card">
        <h2 style="margin: 0;">📝 Registrar Novo Pagamento</h2>
    </div>
    """, unsafe_allow_html=True)

    alunos = carregar_alunos_ativos()

    if not alunos:
        st.markdown(components["empty_state"]("👥", "Nenhum aluno ativo encontrado", "Cadastre alunos primeiro para registrar pagamentos"), unsafe_allow_html=True)
    else:
        with st.form("form_pagamento"):
            alunos_dict = {f"{a['nome_completo']} (ID: {a['id']})": a['id'] for a in alunos}
            aluno_selecionado = st.selectbox(
                "👤 Selecione o aluno",
                options=list(alunos_dict.keys())
            )

            col1, col2 = st.columns(2)

            with col1:
                valor = st.number_input(
                    "💵 Valor do pagamento",
                    min_value=0.0,
                    format="%.2f",
                    step=10.0
                )

                data_pagamento = st.date_input(
                    "📅 Data do pagamento",
                    value=date.today()
                )

            with col2:
                mes_referencia_date = st.date_input(
                    "📆 Mês de referência",
                    value=date.today()
                )

                forma_pagamento = st.selectbox(
                    "💳 Forma de pagamento",
                    options=["dinheiro", "pix", "cartao", "transferencia"]
                )

            observacoes = st.text_area(
                "📝 Observações (opcional)",
                height=100
            )

            submitted = st.form_submit_button("✅ Registrar Pagamento", use_container_width=True)

            if submitted:
                if valor <= 0:
                    st.error("❌ O valor deve ser maior que zero.")
                else:
                    mes_referencia_str = mes_referencia_date.strftime("%Y-%m")
                    aluno_id = alunos_dict[aluno_selecionado]

                    payload = {
                        "aluno_id": aluno_id,
                        "valor": float(valor),
                        "data_pagamento": data_pagamento.isoformat(),
                        "mes_referencia": mes_referencia_str,
                        "forma_pagamento": forma_pagamento,
                        "observacoes": observacoes if observacoes else None
                    }

                    try:
                        response = requests.post(
                            f"{API_URL}/api/pagamentos",
                            json=payload,
                            headers=get_auth_headers(),
                            timeout=10
                        )

                        if response.status_code == 201:
                            st.success(f"✅ Pagamento de {formatar_moeda(valor)} registrado com sucesso!")
                            st.rerun()
                        else:
                            st.error(f"❌ Não foi possível registrar o pagamento. Tente novamente.")
                    except Exception as e:
                        st.error(f"❌ Sistema temporariamente indisponível. Tente novamente em alguns instantes.")

with tab2:
    st.markdown("""
    <div class="info-card">
        <h2 style="margin: 0;">📜 Histórico de Pagamentos</h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    todos_alunos = carregar_todos_alunos()

    with col1:
        alunos_filtro = {"Todos": None}
        alunos_filtro.update({f"{a['nome_completo']} (ID: {a['id']})": a['id'] for a in todos_alunos})

        filtro_aluno = st.selectbox(
            "👤 Filtrar por aluno",
            options=list(alunos_filtro.keys())
        )

    with col2:
        filtro_mes = st.date_input(
            "📆 Filtrar por mês de referência (opcional)",
            value=None
        )

    try:
        aluno_id_filtro = alunos_filtro[filtro_aluno]

        if aluno_id_filtro:
            response = requests.get(
                f"{API_URL}/api/pagamentos/aluno/{aluno_id_filtro}",
                headers=get_auth_headers(),
                timeout=10
            )
        else:
            response = requests.get(
                f"{API_URL}/api/pagamentos",
                headers=get_auth_headers(),
                timeout=10
            )

        if response.status_code == 200:
            pagamentos = response.json()

            if filtro_mes:
                mes_filtro_str = filtro_mes.strftime("%Y-%m")
                pagamentos = [p for p in pagamentos if p['mes_referencia'] == mes_filtro_str]

            if not pagamentos:
                st.markdown(components["empty_state"]("💳", "Nenhum pagamento encontrado", "Tente ajustar os filtros ou registre um novo pagamento"), unsafe_allow_html=True)
            else:
                pagamentos_ordenados = sorted(pagamentos, key=lambda x: x['data_pagamento'], reverse=True)

                # Aplicar paginação
                pagamentos_paginados, pagina_atual, total_paginas, total_itens = create_pagination(pagamentos_ordenados, items_per_page=15)

                st.info(f"💰 Mostrando {len(pagamentos_paginados)} de {total_itens} pagamentos")
                st.markdown("---")

                for pagamento in pagamentos_paginados:
                    aluno_nome = "Desconhecido"
                    for aluno in todos_alunos:
                        if aluno['id'] == pagamento['aluno_id']:
                            aluno_nome = aluno['nome_completo']
                            break

                    with st.expander(
                        f"💵 {aluno_nome} - {formatar_moeda(pagamento['valor'])} - {pagamento['data_pagamento']}"
                    ):
                        col1, col2, col3 = st.columns(3)

                        with col1:
                            st.write(f"**👤 Aluno:** {aluno_nome}")
                            st.write(f"**💰 Valor:** {formatar_moeda(pagamento['valor'])}")

                        with col2:
                            st.write(f"**📅 Data:** {pagamento['data_pagamento']}")
                            st.write(f"**📆 Mês Ref.:** {pagamento['mes_referencia']}")

                        with col3:
                            st.write(f"**💳 Forma:** {pagamento['forma_pagamento']}")
                            if pagamento.get('observacoes'):
                                st.write(f"**📝 Obs.:** {pagamento['observacoes']}")

                        if st.button(f"🗑️ Deletar Pagamento", key=f"del_{pagamento['id']}"):
                            try:
                                del_response = requests.delete(
                                    f"{API_URL}/api/pagamentos/{pagamento['id']}",
                                    headers=get_auth_headers(),
                                    timeout=10
                                )

                                if del_response.status_code == 204:
                                    st.success("✅ Pagamento deletado com sucesso!")
                                    st.rerun()
                                else:
                                    st.error(f"❌ Não foi possível deletar o pagamento.")
                            except Exception as e:
                                st.error(f"❌ Sistema temporariamente indisponível.")

                # Renderizar controles de paginação
                render_pagination_controls(pagina_atual, total_paginas, total_itens)
        else:
            st.error(f"❌ Não foi possível carregar os pagamentos.")

    except Exception as e:
        st.error(f"❌ Sistema temporariamente indisponível. Tente novamente em alguns instantes.")

with tab3:
    st.markdown("""
    <div class="info-card">
        <h2 style="margin: 0;">⚠️ Alunos Inadimplentes</h2>
    </div>
    """, unsafe_allow_html=True)

    try:
        response = requests.get(f"{API_URL}/api/alunos/inadimplentes", headers=get_auth_headers(), timeout=10)

        if response.status_code == 200:
            inadimplentes = response.json()

            if not inadimplentes:
                st.success("✅ Nenhum aluno inadimplente no momento!")
            else:
                st.warning(f"⚠️ **Total de inadimplentes:** {len(inadimplentes)}")

                st.markdown("---")

                for aluno in inadimplentes:
                    with st.container():
                        col1, col2, col3 = st.columns([3, 2, 1])

                        with col1:
                            st.write(f"### 👤 {aluno['nome_completo']}")
                            if aluno.get('responsavel'):
                                st.write(f"**Responsável:** {aluno['responsavel']}")

                        with col2:
                            telefone = aluno.get('telefone_whatsapp', '')
                            if validar_telefone(telefone):
                                st.write(f"**📱 Telefone:** {formatar_telefone(telefone)}")
                            else:
                                st.write("**📱 Telefone:** Não cadastrado")

                            st.write(f"**💰 Mensalidade:** {formatar_moeda(aluno.get('valor_mensalidade', 0))}")

                        with col3:
                            dias_atraso = aluno.get('dias_desde_ultimo_pagamento', 0)
                            st.metric("⏰ Dias de Atraso", f"{dias_atraso}")

                            telefone = aluno.get('telefone_whatsapp', '')
                            if validar_telefone(telefone):
                                apenas_numeros = ''.join(filter(str.isdigit, telefone))
                                whatsapp_url = f"https://wa.me/55{apenas_numeros}"
                                st.markdown(
                                    f'<div class="whatsapp-button">'
                                    f'<a href="{whatsapp_url}" target="_blank">'
                                    f'<button style="background: linear-gradient(135deg, #00952F 0%, #00C853 100%) !important; '
                                    f'color: white; border-radius: 25px; padding: 0.5rem 2rem; font-weight: 600; '
                                    f'box-shadow: 0 4px 6px rgba(0, 149, 47, 0.3); border: none; cursor: pointer; width: 100%;">'
                                    f'💬 WhatsApp</button></a></div>',
                                    unsafe_allow_html=True
                                )
                            else:
                                st.button(
                                    "💬 WhatsApp",
                                    disabled=True,
                                    use_container_width=True,
                                    help="Telefone não cadastrado"
                                )

                        if aluno.get('observacoes'):
                            st.info(f"📝 **Observações:** {aluno['observacoes']}")

                        st.markdown("---")
        else:
            st.error(f"❌ Não foi possível carregar os dados de inadimplentes.")

    except Exception as e:
        st.error(f"❌ Sistema temporariamente indisponível. Tente novamente em alguns instantes.")

# Dark Mode Toggle
st.markdown(components["dark_mode_toggle"], unsafe_allow_html=True)

# Indicador de página ativa
st.markdown(components["page_indicator"]("Financeiro"), unsafe_allow_html=True)
