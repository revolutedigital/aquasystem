"""
Página de Gerenciamento de Usuários (CRUD) - Apenas Admin
Sistema de Gestão de Natação
"""
import streamlit as st
import requests
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from styles import get_global_styles, get_custom_components
from streamlit_hacks import get_streamlit_ui_hacks, get_improved_contrast_css
from auth_utils import require_authentication, get_auth_headers, hide_streamlit_app_from_sidebar

# Configuração da página
st.set_page_config(
    page_title="Gerenciamento de Usuários",
    page_icon="👥",
    layout="wide"
)

# Aplicar estilos globais
st.markdown(get_global_styles(), unsafe_allow_html=True)
st.markdown(get_streamlit_ui_hacks(), unsafe_allow_html=True)
st.markdown(get_improved_contrast_css(), unsafe_allow_html=True)

# Esconder 'streamlit app' do menu
hide_streamlit_app_from_sidebar()

# Obter componentes customizados
components = get_custom_components()

# Configuração da API
API_URL = os.getenv("API_URL", "http://backend:9000")

# CSS específico da página
st.markdown("""
<style>
.user-card {
    background: var(--bg-card);
    backdrop-filter: blur(20px);
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: var(--shadow-lg);
    border: 1px solid var(--border-color);
    border-left: 5px solid var(--primary);
    margin: 1rem 0;
}

.user-card.admin {
    border-left-color: #EF4444;
}

.user-card.recepcionista {
    border-left-color: var(--primary);
}

.user-card.aluno {
    border-left-color: var(--secondary);
}

.user-card h2, .user-card h3, .user-card p {
    color: var(--text-secondary) !important;
}

.role-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
}

.role-admin {
    background: #FFEBEE;
    color: #D32F2F;
}

.role-recepcionista {
    background: #E3F2FD;
    color: #1565C0;
}

.role-aluno {
    background: #E8F5E9;
    color: #00952F;
}
</style>
""", unsafe_allow_html=True)


def check_authentication():
    """Verifica se usuário está autenticado"""
    return "access_token" in st.session_state and st.session_state.access_token is not None


def check_admin():
    """Verifica se usuário é admin"""
    if not check_authentication():
        return False
    return st.session_state.user.get("role") == "admin"


def get_auth_headers():
    """Retorna headers com token de autenticação"""
    return {
        "Authorization": f"Bearer {st.session_state.access_token}",
        "Content-Type": "application/json"
    }


# Verificar autenticação
if not check_authentication():
    st.error("🔒 Você precisa fazer login primeiro!")
    st.info("👈 Use o menu lateral para acessar a página de Login")
    st.stop()

# Verificar se é admin
if not check_admin():
    st.error("⛔ Acesso negado! Esta página é apenas para administradores.")
    st.info(f"Seu papel atual: **{st.session_state.user.get('role').title()}**")
    st.stop()

# Header
st.title("👥 Gerenciamento de Usuários")

# Breadcrumb
st.markdown(components["breadcrumb"](["Home", "Usuários"]), unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["➕ Novo Usuário", "📋 Listar Usuários", "✏️ Editar/Excluir"])

# TAB 1 - NOVO USUÁRIO
with tab1:
    st.header("Cadastrar Novo Usuário")

    with st.form("form_novo_usuario", clear_on_submit=True):
        st.subheader("👤 Dados do Usuário")
        col1, col2 = st.columns(2)

        with col1:
            full_name = st.text_input(
                "Nome Completo *",
                placeholder="Ex: João Silva Santos",
                help="Nome completo do usuário"
            )
            email = st.text_input(
                "Email *",
                placeholder="usuario@exemplo.com",
                help="Email único para login"
            )

        with col2:
            username = st.text_input(
                "Username *",
                placeholder="joaosilva",
                help="Username único (sem espaços)"
            )
            password = st.text_input(
                "Senha *",
                type="password",
                placeholder="Mínimo 6 caracteres",
                help="Senha para login (mínimo 6 caracteres)"
            )

        st.subheader("🔐 Permissões")
        role = st.selectbox(
            "Papel do Usuário *",
            options=["recepcionista", "admin", "aluno"],
            format_func=lambda x: {
                "admin": "🔴 Administrador (acesso total)",
                "recepcionista": "🔵 Recepcionista (gerencia alunos e pagamentos)",
                "aluno": "🟢 Aluno (acesso limitado)"
            }[x],
            help="Define as permissões do usuário no sistema"
        )

        # Botão de submissão
        submitted = st.form_submit_button("✅ Cadastrar Usuário", type="primary", use_container_width=True)

        if submitted:
            # Validações
            erros = []

            if not full_name or len(full_name.strip()) < 3:
                erros.append("Nome completo deve ter ao menos 3 caracteres")

            if not email or "@" not in email:
                erros.append("Email inválido")

            if not username or len(username.strip()) < 3:
                erros.append("Username deve ter ao menos 3 caracteres")

            if not password or len(password) < 6:
                erros.append("Senha deve ter ao menos 6 caracteres")

            if erros:
                for erro in erros:
                    st.error(f"❌ {erro}")
            else:
                # Preparar dados
                user_data = {
                    "full_name": full_name.strip(),
                    "email": email.strip().lower(),
                    "username": username.strip().lower(),
                    "password": password,
                    "role": role
                }

                # Enviar para a API
                try:
                    response = requests.post(
                        f"{API_URL}/api/users",
                        json=user_data,
                        headers=get_auth_headers(),
                        timeout=10
                    )

                    if response.status_code == 201:
                        st.success(f"✅ Usuário {full_name} cadastrado com sucesso!")
                        st.balloons()
                    elif response.status_code == 400:
                        error_detail = response.json().get("detail", "Erro desconhecido")
                        st.error(f"❌ {error_detail}")
                    else:
                        st.error(f"❌ Erro ao cadastrar usuário. Código: {response.status_code}")

                except requests.exceptions.ConnectionError:
                    st.error("❌ Não foi possível conectar ao servidor")
                except Exception as e:
                    st.error(f"❌ Erro inesperado: {str(e)}")

# TAB 2 - LISTAR USUÁRIOS
with tab2:
    st.header("Lista de Usuários Cadastrados")

    # Filtros
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        filtro_role = st.selectbox(
            "Filtrar por Papel",
            options=["Todos", "admin", "recepcionista", "aluno"],
            format_func=lambda x: {"Todos": "Todos", "admin": "Administradores", "recepcionista": "Recepcionistas", "aluno": "Alunos"}[x]
        )

    with col2:
        filtro_status = st.selectbox(
            "Filtrar por Status",
            options=["Todos", "Ativos", "Inativos"]
        )

    with col3:
        if st.button("🔄 Atualizar", use_container_width=True):
            st.rerun()

    # Buscar usuários
    try:
        params = {}

        if filtro_role != "Todos":
            params["role"] = filtro_role

        if filtro_status == "Ativos":
            params["is_active"] = "true"
        elif filtro_status == "Inativos":
            params["is_active"] = "false"

        response = requests.get(
            f"{API_URL}/api/users",
            params=params,
            headers=get_auth_headers(),
            timeout=10
        )

        if response.status_code == 200:
            usuarios = response.json()

            if usuarios:
                st.info(f"📊 Total de {len(usuarios)} usuário(s) encontrado(s)")
                st.markdown("---")

                for usuario in usuarios:
                    # Determinar classe CSS baseada no role
                    role_class = usuario.get('role', '')
                    status_emoji = "🟢" if usuario.get('is_active', False) else "🔴"

                    # Ícone por role
                    role_icon = {"admin": "🔴", "recepcionista": "🔵", "aluno": "🟢"}
                    icon = role_icon.get(role_class, "⚪")

                    with st.expander(
                        f"{status_emoji} {icon} {usuario.get('full_name', '')} - {usuario.get('email', '')}"
                    ):
                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown("**📋 Informações Básicas**")
                            st.write(f"**ID:** {usuario.get('id')}")
                            st.write(f"**Nome:** {usuario.get('full_name', 'N/A')}")
                            st.write(f"**Email:** {usuario.get('email', 'N/A')}")
                            st.write(f"**Username:** {usuario.get('username', 'N/A')}")

                        with col2:
                            st.markdown("**🔐 Permissões e Status**")

                            # Badge de role
                            role_label = usuario.get('role', '').title()
                            role_badge_class = f"role-{usuario.get('role', '')}"
                            st.markdown(f'<span class="role-badge {role_badge_class}">{role_label}</span>', unsafe_allow_html=True)

                            st.write(f"**Status:** {'Ativo ✅' if usuario.get('is_active') else 'Inativo ❌'}")
                            st.write(f"**Superusuário:** {'Sim 👑' if usuario.get('is_superuser') else 'Não'}")
                            st.write(f"**Criado em:** {usuario.get('created_at', 'N/A')[:10]}")

                            if usuario.get('last_login'):
                                st.write(f"**Último login:** {usuario.get('last_login', 'N/A')[:10]}")

            else:
                st.markdown(components["empty_state"]("👥", "Nenhum usuário encontrado", "Tente ajustar os filtros ou cadastre um novo usuário"), unsafe_allow_html=True)
        else:
            st.error(f"❌ Erro ao carregar usuários. Código: {response.status_code}")

    except requests.exceptions.ConnectionError:
        st.error("❌ Não foi possível conectar ao servidor")
    except Exception as e:
        st.error(f"❌ Erro ao processar solicitação: {str(e)}")

# TAB 3 - EDITAR/EXCLUIR
with tab3:
    st.header("Editar ou Excluir Usuário")

    # Busca por ID
    col1, col2 = st.columns([3, 1])

    with col1:
        user_id = st.number_input("ID do Usuário", min_value=1, step=1, help="Digite o ID do usuário")

    with col2:
        buscar_btn = st.button("🔍 Buscar", type="primary", use_container_width=True)

    if buscar_btn:
        try:
            response = requests.get(
                f"{API_URL}/api/users/{user_id}",
                headers=get_auth_headers(),
                timeout=10
            )

            if response.status_code == 200:
                usuario = response.json()

                st.success(f"✅ Usuário encontrado: **{usuario.get('full_name')}**")
                st.markdown("---")

                # Formulário de edição
                with st.form("form_editar_usuario"):
                    st.subheader("✏️ Editar Informações")

                    col1, col2 = st.columns(2)

                    with col1:
                        full_name = st.text_input("Nome Completo", value=usuario.get('full_name', ''))
                        email = st.text_input("Email", value=usuario.get('email', ''))

                    with col2:
                        username = st.text_input("Username", value=usuario.get('username', ''))
                        password = st.text_input(
                            "Nova Senha",
                            type="password",
                            placeholder="Deixe em branco para não alterar",
                            help="Preencha apenas se quiser alterar a senha"
                        )

                    col3, col4 = st.columns(2)

                    with col3:
                        role = st.selectbox(
                            "Papel do Usuário",
                            options=["admin", "recepcionista", "aluno"],
                            index=["admin", "recepcionista", "aluno"].index(usuario.get('role', 'recepcionista')),
                            format_func=lambda x: {
                                "admin": "🔴 Administrador",
                                "recepcionista": "🔵 Recepcionista",
                                "aluno": "🟢 Aluno"
                            }[x]
                        )

                    with col4:
                        is_active = st.checkbox("Usuário Ativo", value=usuario.get('is_active', True))

                    # Botões
                    col_btn1, col_btn2, col_btn3 = st.columns(3)

                    with col_btn1:
                        update_btn = st.form_submit_button("✅ Atualizar", type="primary", use_container_width=True)

                    with col_btn2:
                        deactivate_btn = st.form_submit_button("🚫 Desativar", type="secondary", use_container_width=True)

                    with col_btn3:
                        activate_btn = st.form_submit_button("✅ Ativar", type="secondary", use_container_width=True)

                    # Processar atualização
                    if update_btn:
                        user_data = {
                            "full_name": full_name.strip(),
                            "email": email.strip().lower(),
                            "username": username.strip().lower(),
                            "role": role,
                            "is_active": is_active
                        }

                        # Adicionar senha se fornecida
                        if password and len(password) >= 6:
                            user_data["password"] = password

                        try:
                            response = requests.put(
                                f"{API_URL}/api/users/{user_id}",
                                json=user_data,
                                headers=get_auth_headers(),
                                timeout=10
                            )

                            if response.status_code == 200:
                                st.success("✅ Usuário atualizado com sucesso!")
                                st.rerun()
                            elif response.status_code == 400:
                                error_detail = response.json().get("detail", "Erro desconhecido")
                                st.error(f"❌ {error_detail}")
                            else:
                                st.error(f"❌ Erro ao atualizar. Código: {response.status_code}")

                        except Exception as e:
                            st.error(f"❌ Erro: {str(e)}")

                    # Processar desativação
                    if deactivate_btn:
                        try:
                            response = requests.delete(
                                f"{API_URL}/api/users/{user_id}",
                                headers=get_auth_headers(),
                                timeout=10
                            )

                            if response.status_code == 200:
                                st.success("✅ Usuário desativado com sucesso!")
                                st.rerun()
                            elif response.status_code == 400:
                                error_detail = response.json().get("detail", "Erro desconhecido")
                                st.error(f"❌ {error_detail}")
                            else:
                                st.error(f"❌ Erro ao desativar. Código: {response.status_code}")

                        except Exception as e:
                            st.error(f"❌ Erro: {str(e)}")

                    # Processar ativação
                    if activate_btn:
                        try:
                            response = requests.post(
                                f"{API_URL}/api/users/{user_id}/activate",
                                headers=get_auth_headers(),
                                timeout=10
                            )

                            if response.status_code == 200:
                                st.success("✅ Usuário ativado com sucesso!")
                                st.rerun()
                            else:
                                st.error(f"❌ Erro ao ativar. Código: {response.status_code}")

                        except Exception as e:
                            st.error(f"❌ Erro: {str(e)}")

            elif response.status_code == 404:
                st.error("❌ Usuário não encontrado")
            else:
                st.error(f"❌ Erro ao buscar usuário. Código: {response.status_code}")

        except requests.exceptions.ConnectionError:
            st.error("❌ Não foi possível conectar ao servidor")
        except Exception as e:
            st.error(f"❌ Erro: {str(e)}")

# Dark Mode Toggle
st.markdown(components["dark_mode_toggle"], unsafe_allow_html=True)

# Indicador de página ativa
st.markdown(components["page_indicator"]("Usuários"), unsafe_allow_html=True)
