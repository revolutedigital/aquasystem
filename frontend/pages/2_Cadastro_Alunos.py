"""
Página de Cadastro de Alunos - Sistema de Gestão de Natação
"""
import streamlit as st
import requests
import os
from datetime import date
import re
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import get_global_styles, get_custom_components, create_pagination, render_pagination_controls
from streamlit_hacks import get_improved_contrast_css
from auth_utils import require_authentication, get_auth_headers, hide_streamlit_app_from_sidebar

# Configuração da página
st.set_page_config(
    page_title="Cadastro de Alunos",
    page_icon="📝",
    layout="wide"
)

# Verificar autenticação PRIMEIRO
require_authentication()

# Aplicar estilos globais otimizados
st.markdown(get_global_styles(), unsafe_allow_html=True)
st.markdown(get_improved_contrast_css(), unsafe_allow_html=True)

# Esconder 'streamlit app' do menu
hide_streamlit_app_from_sidebar()

# Obter componentes customizados
components = get_custom_components()

# CSS adicional específico desta página
st.markdown("""
<style>
.info-card {
    background: var(--bg-card);
    backdrop-filter: blur(20px);
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: var(--shadow-lg);
    border: 1px solid var(--border-color);
    border-left: 5px solid var(--secondary);
    margin: 1rem 0;
    transition: all 0.25s ease;
}

.info-card:hover {
    box-shadow: var(--shadow-2xl);
    transform: translateX(4px);
}

.info-card h2, .info-card h3, .info-card p {
    color: var(--text-secondary) !important;
}
</style>
""", unsafe_allow_html=True)

API_URL = os.getenv("API_URL", "http://backend:9000")

# Função para validar telefone brasileiro
def validar_telefone(telefone: str) -> bool:
    """Valida formato de telefone brasileiro"""
    if not telefone:
        return True  # Telefone é opcional
    # Remove caracteres não numéricos
    numeros = re.sub(r'\D', '', telefone)
    # Verifica se tem 10 ou 11 dígitos
    return len(numeros) in [10, 11]

# Função para formatar telefone automaticamente
def formatar_telefone(telefone: str) -> str:
    """Formata telefone para padrão brasileiro automaticamente"""
    if not telefone:
        return ""
    # Remove tudo que não é número
    numeros = re.sub(r'\D', '', telefone)

    # Formata automaticamente conforme digita
    if len(numeros) == 0:
        return ""
    elif len(numeros) <= 2:
        return f"({numeros}"
    elif len(numeros) <= 6:
        return f"({numeros[:2]}) {numeros[2:]}"
    elif len(numeros) <= 10:
        return f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}"
    else:
        # Celular com 11 dígitos
        return f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:11]}"

# Função para aplicar máscara ao telefone (apenas números)
def aplicar_mascara_telefone(telefone: str) -> str:
    """Remove formatação e retorna apenas números"""
    if not telefone:
        return ""
    return re.sub(r'\D', '', telefone)

# Header
st.title("📝 Gestão de Alunos")

# Breadcrumb
st.markdown(components["breadcrumb"](["Home", "Gestão de Alunos"]), unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["➕ Novo Aluno", "📋 Listar Alunos", "✏️ Buscar/Editar"])

# TAB 1 - NOVO ALUNO
with tab1:
    st.header("Cadastrar Novo Aluno")

    # Inicializar session_state para preservar dados
    if 'form_data_aluno' not in st.session_state:
        st.session_state.form_data_aluno = {}

    with st.form("form_novo_aluno", clear_on_submit=False):
        # Dados pessoais
        st.subheader("👤 Dados Pessoais")
        col1, col2 = st.columns(2)

        with col1:
            nome_completo = st.text_input(
                "Nome Completo *",
                value=st.session_state.form_data_aluno.get('nome_completo', ''),
                placeholder="Ex: João Silva Santos",
                help="Nome completo do aluno"
            )
            telefone_whatsapp_raw = st.text_input(
                "Telefone/WhatsApp (apenas números)",
                value=st.session_state.form_data_aluno.get('telefone_whatsapp', ''),
                placeholder="11999999999",
                help="Digite apenas os números (DDD + telefone). A formatação é automática!",
                max_chars=11
            )
            # Aplicar formatação automática
            telefone_whatsapp = formatar_telefone(telefone_whatsapp_raw)
            if telefone_whatsapp_raw:
                st.caption(f"📱 Formato: {telefone_whatsapp}")

            responsavel = st.text_input(
                "Nome do Responsável",
                value=st.session_state.form_data_aluno.get('responsavel', ''),
                placeholder="Para menores de idade",
                help="Deixe em branco se o aluno for maior de idade"
            )

        with col2:
            tipo_aula_index = 0 if st.session_state.form_data_aluno.get('tipo_aula', 'natacao') == 'natacao' else 1
            tipo_aula = st.selectbox(
                "Tipo de Aula *",
                options=["natacao", "hidroginastica"],
                index=tipo_aula_index,
                format_func=lambda x: "Natação" if x == "natacao" else "Hidroginástica",
                help="Modalidade que o aluno irá praticar"
            )
            data_inicio_contrato = st.date_input(
                "Data de Início do Contrato",
                value=st.session_state.form_data_aluno.get('data_inicio_contrato', date.today()),
                help="Data de início das aulas"
            )
            ativo = st.checkbox(
                "Aluno Ativo",
                value=st.session_state.form_data_aluno.get('ativo', True)
            )

        # Dados financeiros
        st.subheader("💰 Dados Financeiros")
        col3, col4 = st.columns(2)

        with col3:
            valor_mensalidade = st.number_input(
                "Valor da Mensalidade (R$) *",
                min_value=0.0,
                value=float(st.session_state.form_data_aluno.get('valor_mensalidade', 150.0)),
                step=10.0,
                format="%.2f",
                help="Valor mensal a ser pago pelo aluno"
            )

        with col4:
            dia_vencimento = st.number_input(
                "Dia do Vencimento *",
                min_value=1,
                max_value=31,
                value=int(st.session_state.form_data_aluno.get('dia_vencimento', 10)),
                help="Dia do mês em que a mensalidade vence"
            )

        # Observações
        observacoes = st.text_area(
            "Observações",
            value=st.session_state.form_data_aluno.get('observacoes', ''),
            placeholder="Informações adicionais sobre o aluno (opcional)",
            help="Restrições médicas, observações importantes, etc."
        )

        # Botão de submissão
        submitted = st.form_submit_button("✅ Cadastrar Aluno", type="primary", use_container_width=True)

        if submitted:
            # Salvar dados no session_state para preservar em caso de erro
            st.session_state.form_data_aluno = {
                'nome_completo': nome_completo,
                'telefone_whatsapp': telefone_whatsapp_raw,
                'responsavel': responsavel,
                'tipo_aula': tipo_aula,
                'data_inicio_contrato': data_inicio_contrato,
                'ativo': ativo,
                'valor_mensalidade': valor_mensalidade,
                'dia_vencimento': dia_vencimento,
                'observacoes': observacoes
            }

            # Validações
            erros = []

            if not nome_completo or len(nome_completo.strip()) == 0:
                erros.append("Nome completo é obrigatório")

            if telefone_whatsapp_raw and not validar_telefone(telefone_whatsapp_raw):
                erros.append("Telefone inválido. Digite 10 ou 11 números (DDD + telefone)")

            if erros:
                for erro in erros:
                    st.error(f"❌ {erro}")
                st.warning("⚠️ Corrija os erros acima. Seus dados foram preservados!")
            else:
                # Preparar dados
                aluno_data = {
                    "nome_completo": nome_completo.strip(),
                    "responsavel": responsavel.strip() if responsavel else None,
                    "tipo_aula": tipo_aula,
                    "valor_mensalidade": float(valor_mensalidade),
                    "dia_vencimento": int(dia_vencimento),
                    "data_inicio_contrato": str(data_inicio_contrato),
                    "ativo": ativo,
                    "telefone_whatsapp": telefone_whatsapp if telefone_whatsapp_raw else None,
                    "observacoes": observacoes.strip() if observacoes else None
                }

                # Enviar para a plataforma
                try:
                    response = requests.post(f"{API_URL}/api/alunos", json=aluno_data, headers=get_auth_headers(), timeout=10)

                    if response.status_code == 200:
                        st.success(f"✅ Aluno {nome_completo} cadastrado com sucesso!")
                        st.balloons()
                        # Limpar dados apenas em caso de sucesso
                        st.session_state.form_data_aluno = {}
                        st.rerun()
                    else:
                        st.error(f"❌ Não foi possível salvar os dados. Tente novamente.")
                        st.warning("⚠️ Seus dados foram preservados. Corrija e tente novamente!")

                except requests.exceptions.ConnectionError:
                    st.error("❌ Sistema temporariamente indisponível. Tente novamente em alguns instantes.")
                    st.warning("⚠️ Seus dados foram preservados!")
                except Exception as e:
                    st.error(f"❌ Erro inesperado ao processar solicitação.")
                    st.warning("⚠️ Seus dados foram preservados!")

# TAB 2 - LISTAR ALUNOS
with tab2:
    st.header("Lista de Alunos Cadastrados")

    # Filtros
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        filtro_tipo = st.selectbox(
            "Filtrar por Tipo de Aula",
            options=["Todos", "natacao", "hidroginastica"],
            format_func=lambda x: {"Todos": "Todos", "natacao": "Natação", "hidroginastica": "Hidroginástica"}[x]
        )

    with col2:
        filtro_status = st.selectbox(
            "Filtrar por Status",
            options=["Todos", "Ativos", "Inativos"]
        )

    with col3:
        if st.button("🔄 Atualizar", use_container_width=True):
            st.rerun()

    # Adicionar campo de busca por nome
    busca_nome = st.text_input("🔍 Buscar por nome", placeholder="Digite o nome do aluno...")

    # Buscar alunos
    try:
        params = {}

        if filtro_tipo != "Todos":
            params["tipo_aula"] = filtro_tipo

        if filtro_status == "Ativos":
            params["ativo"] = "true"
        elif filtro_status == "Inativos":
            params["ativo"] = "false"

        response = requests.get(f"{API_URL}/api/alunos", params=params, headers=get_auth_headers(), timeout=10)

        if response.status_code == 200:
            alunos = response.json()

            # Aplicar filtro de busca por nome
            if busca_nome:
                alunos = [a for a in alunos if busca_nome.lower() in a.get('nome_completo', '').lower()]

            if alunos:
                # Aplicar paginação
                alunos_paginados, pagina_atual, total_paginas, total_itens = create_pagination(alunos, items_per_page=10)

                st.info(f"📊 Mostrando {len(alunos_paginados)} de {total_itens} alunos encontrados")
                st.markdown("---")

                for aluno in alunos_paginados:
                    # Criar expander para cada aluno
                    status_emoji = "🟢" if aluno.get('ativo', False) else "🔴"
                    tipo_emoji = "🏊" if aluno.get('tipo_aula') == 'natacao' else "💧"

                    with st.expander(
                        f"{status_emoji} {tipo_emoji} {aluno.get('nome_completo', 'Sem nome')} - ID: {aluno.get('id')}"
                    ):
                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown("**📋 Informações Básicas**")
                            st.write(f"**ID:** {aluno.get('id')}")
                            st.write(f"**Nome:** {aluno.get('nome_completo', 'N/A')}")
                            st.write(f"**Responsável:** {aluno.get('responsavel') or 'Não informado'}")
                            st.write(f"**Telefone:** {aluno.get('telefone_whatsapp') or 'Não informado'}")
                            st.write(f"**Status:** {'Ativo ✅' if aluno.get('ativo') else 'Inativo ❌'}")

                        with col2:
                            st.markdown("**💰 Informações Financeiras**")
                            st.write(f"**Tipo de Aula:** {'Natação 🏊' if aluno.get('tipo_aula') == 'natacao' else 'Hidroginástica 💧'}")

                            valor = aluno.get('valor_mensalidade', 0)
                            valor_formatado = f"R$ {float(valor):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                            st.write(f"**Mensalidade:** {valor_formatado}")

                            st.write(f"**Dia Vencimento:** {aluno.get('dia_vencimento', 'N/A')}")
                            st.write(f"**Data Início:** {aluno.get('data_inicio_contrato') or 'N/A'}")

                        if aluno.get('observacoes'):
                            st.info(f"**📝 Observações:** {aluno['observacoes']}")

                # Renderizar controles de paginação
                render_pagination_controls(pagina_atual, total_paginas, total_itens)
            else:
                st.markdown(components["empty_state"]("👥", "Nenhum aluno encontrado", "Tente ajustar os filtros ou cadastre um novo aluno"), unsafe_allow_html=True)
        else:
            st.error(f"❌ Não foi possível carregar os dados. Tente novamente.")

    except requests.exceptions.ConnectionError:
        st.error("❌ Sistema temporariamente indisponível. Tente novamente em alguns instantes.")
    except Exception as e:
        st.error(f"❌ Erro ao processar solicitação.")

# TAB 3 - BUSCAR/EDITAR
with tab3:
    st.header("Buscar e Editar Aluno")

    # Busca por ID
    col1, col2 = st.columns([3, 1])

    with col1:
        aluno_id = st.number_input("ID do Aluno", min_value=1, step=1, help="Digite o ID do aluno para buscar")

    with col2:
        buscar_btn = st.button("🔍 Buscar", type="primary", use_container_width=True)

    if buscar_btn:
        try:
            response = requests.get(f"{API_URL}/api/alunos/{aluno_id}", headers=get_auth_headers(), timeout=10)

            if response.status_code == 200:
                aluno = response.json()

                st.success(f"✅ Aluno encontrado: **{aluno.get('nome_completo')}**")
                st.markdown("---")

                # Formulário de edição
                with st.form("form_editar_aluno"):
                    st.subheader("✏️ Editar Informações")

                    # Dados pessoais
                    col1, col2 = st.columns(2)

                    with col1:
                        nome_completo = st.text_input("Nome Completo *", value=aluno.get('nome_completo', ''))
                        # Extrair apenas números do telefone salvo
                        telefone_salvo = aluno.get('telefone_whatsapp', '') or ''
                        telefone_numeros = aplicar_mascara_telefone(telefone_salvo)

                        telefone_whatsapp_raw = st.text_input(
                            "Telefone/WhatsApp (apenas números)",
                            value=telefone_numeros,
                            placeholder="11999999999",
                            help="Digite apenas os números (DDD + telefone). A formatação é automática!",
                            max_chars=11
                        )
                        # Mostrar formatação
                        telefone_whatsapp = formatar_telefone(telefone_whatsapp_raw)
                        if telefone_whatsapp_raw:
                            st.caption(f"📱 Formato: {telefone_whatsapp}")

                        responsavel = st.text_input(
                            "Nome do Responsável",
                            value=aluno.get('responsavel', '') or ''
                        )

                    with col2:
                        tipo_aula = st.selectbox(
                            "Tipo de Aula *",
                            options=["natacao", "hidroginastica"],
                            index=0 if aluno.get('tipo_aula') == 'natacao' else 1,
                            format_func=lambda x: "Natação" if x == "natacao" else "Hidroginástica"
                        )

                        # Data de início
                        data_inicio_str = aluno.get('data_inicio_contrato')
                        if data_inicio_str:
                            from datetime import datetime
                            data_inicio_value = datetime.fromisoformat(data_inicio_str).date()
                        else:
                            data_inicio_value = date.today()

                        data_inicio_contrato = st.date_input(
                            "Data de Início do Contrato",
                            value=data_inicio_value
                        )

                        ativo = st.checkbox("Aluno Ativo", value=aluno.get('ativo', True))

                    # Dados financeiros
                    col3, col4 = st.columns(2)

                    with col3:
                        valor_mensalidade = st.number_input(
                            "Valor da Mensalidade (R$) *",
                            min_value=0.0,
                            value=float(aluno.get('valor_mensalidade', 150.0)),
                            step=10.0,
                            format="%.2f"
                        )

                    with col4:
                        dia_vencimento = st.number_input(
                            "Dia do Vencimento *",
                            min_value=1,
                            max_value=31,
                            value=int(aluno.get('dia_vencimento', 10))
                        )

                    # Observações
                    observacoes = st.text_area(
                        "Observações",
                        value=aluno.get('observacoes', '') or ''
                    )

                    # Botões
                    col_btn1, col_btn2 = st.columns(2)

                    with col_btn1:
                        update_btn = st.form_submit_button("✅ Atualizar", type="primary", use_container_width=True)

                    with col_btn2:
                        delete_btn = st.form_submit_button("🗑️ Inativar", type="secondary", use_container_width=True)

                    # Processar atualização
                    if update_btn:
                        if telefone_whatsapp_raw and not validar_telefone(telefone_whatsapp_raw):
                            st.error("❌ Telefone inválido. Digite 10 ou 11 números (DDD + telefone)")
                            st.warning("⚠️ Corrija o telefone e tente novamente. Os dados estão preservados!")
                        else:
                            aluno_data = {
                                "nome_completo": nome_completo.strip(),
                                "responsavel": responsavel.strip() if responsavel else None,
                                "tipo_aula": tipo_aula,
                                "valor_mensalidade": float(valor_mensalidade),
                                "dia_vencimento": int(dia_vencimento),
                                "data_inicio_contrato": str(data_inicio_contrato),
                                "ativo": ativo,
                                "telefone_whatsapp": telefone_whatsapp if telefone_whatsapp_raw else None,
                                "observacoes": observacoes.strip() if observacoes else None
                            }

                            try:
                                response = requests.put(
                                    f"{API_URL}/api/alunos/{aluno_id}",
                                    json=aluno_data,
                                    headers=get_auth_headers(),
                                    timeout=10
                                )

                                if response.status_code == 200:
                                    st.success("✅ Aluno atualizado com sucesso!")
                                    st.rerun()
                                else:
                                    st.error(f"❌ Não foi possível atualizar os dados.")
                                    st.warning("⚠️ Seus dados estão preservados. Tente novamente!")

                            except Exception as e:
                                st.error(f"❌ Sistema temporariamente indisponível.")
                                st.warning("⚠️ Seus dados estão preservados!")

                    # Processar inativação (soft delete)
                    if delete_btn:
                        try:
                            response = requests.delete(f"{API_URL}/api/alunos/{aluno_id}", headers=get_auth_headers(), timeout=10)

                            if response.status_code == 200:
                                st.success("✅ Aluno inativado com sucesso!")
                                st.rerun()
                            else:
                                st.error(f"❌ Não foi possível inativar o aluno.")

                        except Exception as e:
                            st.error(f"❌ Sistema temporariamente indisponível.")

            elif response.status_code == 404:
                st.error("❌ Aluno não encontrado.")
            else:
                st.error(f"❌ Não foi possível localizar o aluno.")

        except requests.exceptions.ConnectionError:
            st.error("❌ Sistema temporariamente indisponível. Tente novamente em alguns instantes.")
        except Exception as e:
            st.error(f"❌ Erro ao processar solicitação.")

# Dark Mode Toggle
st.markdown(components["dark_mode_toggle"], unsafe_allow_html=True)

# Indicador de página ativa
st.markdown(components["page_indicator"]("Cadastro"), unsafe_allow_html=True)
