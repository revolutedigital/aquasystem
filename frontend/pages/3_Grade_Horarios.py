import streamlit as st
import requests
import os
from datetime import time
import sys

st.set_page_config(page_title="Grade de Horários", page_icon="📅", layout="wide")

# Adicionar path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import get_global_styles, get_custom_components
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
</style>
""", unsafe_allow_html=True)

API_URL = os.getenv("API_URL", "http://backend:9000")

# Header
st.title("📅 Grade de Horários")

# Breadcrumb
st.markdown(components["breadcrumb"](["Home", "Grade de Horários"]), unsafe_allow_html=True)

DIAS_SEMANA = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]

def calcular_percentual_ocupacao(atual, maximo):
    """Calcula o percentual de ocupação"""
    if maximo == 0:
        return 0
    return (atual / maximo) * 100

def obter_indicador_capacidade(percentual):
    """Retorna emoji indicador baseado no percentual de ocupação"""
    if percentual < 70:
        return "🟢"
    elif percentual < 90:
        return "🟡"
    else:
        return "🔴"

def carregar_alunos_ativos():
    """Carrega lista de alunos ativos"""
    try:
        response = requests.get(
            f"{API_URL}/api/alunos",
            params={"ativo": True},
            headers=get_auth_headers(),
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados dos alunos.")
        return []

def carregar_horarios():
    """Carrega lista de horários"""
    try:
        response = requests.get(
            f"{API_URL}/api/horarios",
            headers=get_auth_headers(),
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados dos horários.")
        return []

def carregar_grade_completa():
    """Carrega grade completa com alunos matriculados"""
    try:
        response = requests.get(
            f"{API_URL}/api/horarios/grade-completa",
            headers=get_auth_headers(),
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"❌ Erro ao carregar grade completa.")
        return []

tab1, tab2, tab3 = st.tabs(["➕ Criar Horário", "📋 Grade Completa", "👥 Matricular Aluno"])

with tab1:
    st.markdown("""
    <div class="info-card">
        <h2 style="margin: 0;">➕ Criar Novo Horário</h2>
    </div>
    """, unsafe_allow_html=True)

    with st.form("form_horario"):
        col1, col2 = st.columns(2)

        with col1:
            dia_semana = st.selectbox(
                "📆 Dia da semana",
                options=DIAS_SEMANA
            )

            horario = st.time_input(
                "🕐 Horário",
                value=time(9, 0)
            )

        with col2:
            capacidade_maxima = st.number_input(
                "👥 Capacidade máxima",
                min_value=1,
                max_value=30,
                value=10,
                step=1
            )

            tipo_aula = st.selectbox(
                "🏊 Tipo de aula",
                options=["natacao", "hidroginastica"]
            )

        submitted = st.form_submit_button("✅ Criar Horário", use_container_width=True)

        if submitted:
            payload = {
                "dia_semana": dia_semana,
                "horario": horario.strftime("%H:%M:%S"),
                "capacidade_maxima": capacidade_maxima,
                "tipo_aula": tipo_aula
            }

            try:
                response = requests.post(
                    f"{API_URL}/api/horarios",
                    json=payload,
                    headers=get_auth_headers(),
                    timeout=10
                )

                if response.status_code == 201:
                    st.success(f"✅ Horário criado com sucesso! {dia_semana} às {horario.strftime('%H:%M')}")
                    st.rerun()
                else:
                    st.error(f"❌ Não foi possível criar o horário. Tente novamente.")
            except Exception as e:
                st.error(f"❌ Sistema temporariamente indisponível. Tente novamente em alguns instantes.")

with tab2:
    st.markdown("""
    <div class="info-card">
        <h2 style="margin: 0;">📋 Grade Completa de Horários</h2>
    </div>
    """, unsafe_allow_html=True)

    grade_completa = carregar_grade_completa()

    if not grade_completa:
        st.markdown(components["empty_state"]("📅", "Nenhum horário cadastrado", "Crie horários na aba 'Criar Horário' para começar"), unsafe_allow_html=True)
    else:
        grade_por_dia = {}
        for horario in grade_completa:
            dia = horario['dia_semana']
            if dia not in grade_por_dia:
                grade_por_dia[dia] = []
            grade_por_dia[dia].append(horario)

        for dia in DIAS_SEMANA:
            if dia in grade_por_dia:
                st.subheader(f"📆 {dia}")

                horarios_dia = sorted(grade_por_dia[dia], key=lambda x: x['horario'])

                for horario in horarios_dia:
                    alunos_matriculados = horario.get('alunos', [])
                    num_alunos = len(alunos_matriculados)
                    capacidade = horario['capacidade_maxima']
                    percentual = calcular_percentual_ocupacao(num_alunos, capacidade)
                    indicador = obter_indicador_capacidade(percentual)

                    tipo_emoji = "🏊" if horario['tipo_aula'] == "natacao" else "💧"

                    with st.expander(
                        f"{indicador} {tipo_emoji} {horario['horario'][:5]} - {horario['tipo_aula'].capitalize()} - {num_alunos}/{capacidade} alunos ({percentual:.0f}%)"
                    ):
                        col1, col2 = st.columns([2, 1])

                        with col1:
                            st.write(f"**🕐 Horário:** {horario['horario'][:5]}")
                            st.write(f"**🏊 Tipo:** {horario['tipo_aula'].capitalize()}")
                            st.write(f"**👥 Capacidade:** {num_alunos}/{capacidade}")

                            if percentual >= 90:
                                st.error(f"🔴 Capacidade crítica: {percentual:.0f}%")
                            elif percentual >= 70:
                                st.warning(f"🟡 Capacidade elevada: {percentual:.0f}%")
                            else:
                                st.success(f"🟢 Capacidade normal: {percentual:.0f}%")

                        with col2:
                            if st.button(f"🗑️ Deletar Horário", key=f"del_horario_{horario['id']}"):
                                try:
                                    del_response = requests.delete(
                                        f"{API_URL}/api/horarios/{horario['id']}",
                                        headers=get_auth_headers(),
                                        timeout=10
                                    )

                                    if del_response.status_code == 204:
                                        st.success("✅ Horário deletado com sucesso!")
                                        st.rerun()
                                    else:
                                        st.error(f"❌ Não foi possível deletar o horário.")
                                except Exception as e:
                                    st.error(f"❌ Sistema temporariamente indisponível.")

                        if alunos_matriculados:
                            st.markdown("---")
                            st.write("**👥 Alunos Matriculados:**")

                            for aluno in alunos_matriculados:
                                col_aluno1, col_aluno2 = st.columns([3, 1])

                                with col_aluno1:
                                    st.write(f"• {aluno['nome_completo']}")

                                with col_aluno2:
                                    if st.button(
                                        "❌ Remover",
                                        key=f"remove_{horario['id']}_{aluno['id']}"
                                    ):
                                        try:
                                            remove_response = requests.delete(
                                                f"{API_URL}/api/horarios/{horario['id']}/alunos/{aluno['id']}",
                                                headers=get_auth_headers(),
                                                timeout=10
                                            )

                                            if remove_response.status_code == 204:
                                                st.success(f"✅ {aluno['nome_completo']} removido do horário!")
                                                st.rerun()
                                            else:
                                                st.error(f"❌ Não foi possível remover o aluno.")
                                        except Exception as e:
                                            st.error(f"❌ Sistema temporariamente indisponível.")
                        else:
                            st.markdown(components["empty_state"]("👥", "Nenhum aluno matriculado", "Matricule alunos na aba 'Matricular Aluno'"), unsafe_allow_html=True)

                st.markdown("---")

with tab3:
    st.markdown("""
    <div class="info-card">
        <h2 style="margin: 0;">👥 Matricular Aluno em Horário</h2>
    </div>
    """, unsafe_allow_html=True)

    alunos = carregar_alunos_ativos()
    horarios = carregar_horarios()

    if not alunos:
        st.markdown(components["empty_state"]("👥", "Nenhum aluno ativo encontrado", "Cadastre alunos primeiro para poder matriculá-los"), unsafe_allow_html=True)
    elif not horarios:
        st.markdown(components["empty_state"]("📅", "Nenhum horário cadastrado", "Crie horários primeiro na aba 'Criar Horário'"), unsafe_allow_html=True)
    else:
        with st.form("form_matricula"):
            alunos_dict = {f"{a['nome_completo']} (ID: {a['id']})": a['id'] for a in alunos}
            aluno_selecionado = st.selectbox(
                "👤 Selecione o aluno",
                options=list(alunos_dict.keys())
            )

            horarios_info = []
            for h in horarios:
                tipo_emoji = "🏊" if h['tipo_aula'] == "natacao" else "💧"
                info = f"{h['dia_semana']} - {h['horario'][:5]} - {tipo_emoji} {h['tipo_aula'].capitalize()} - Cap: {h['capacidade_maxima']} (ID: {h['id']})"
                horarios_info.append(info)

            horarios_dict = {info: horarios[i]['id'] for i, info in enumerate(horarios_info)}

            horario_selecionado = st.selectbox(
                "📅 Selecione o horário",
                options=list(horarios_dict.keys())
            )

            submitted = st.form_submit_button("✅ Matricular Aluno", use_container_width=True)

            if submitted:
                aluno_id = alunos_dict[aluno_selecionado]
                horario_id = horarios_dict[horario_selecionado]

                try:
                    response = requests.post(
                        f"{API_URL}/api/horarios/{horario_id}/alunos/{aluno_id}",
                        headers=get_auth_headers(),
                        timeout=10
                    )

                    if response.status_code == 200:
                        st.success("✅ Aluno matriculado com sucesso!")
                        st.rerun()
                    elif response.status_code == 400:
                        st.error(f"❌ {response.json().get('detail', 'Não foi possível matricular o aluno.')}")
                    else:
                        st.error(f"❌ Não foi possível matricular o aluno. Tente novamente.")
                except Exception as e:
                    st.error(f"❌ Sistema temporariamente indisponível. Tente novamente em alguns instantes.")

# Dark Mode Toggle
st.markdown(components["dark_mode_toggle"], unsafe_allow_html=True)

# Indicador de página ativa
st.markdown(components["page_indicator"]("Grade"), unsafe_allow_html=True)
