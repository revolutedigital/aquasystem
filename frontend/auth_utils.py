"""
Utilitários de autenticação reutilizáveis
"""
import streamlit as st


def require_authentication():
    """
    Verifica se o usuário está autenticado.
    Se não estiver, mostra mensagem e redireciona para login.
    Use no início de cada página protegida.
    """
    if "access_token" not in st.session_state or st.session_state.access_token is None:
        st.error("🔒 Acesso negado")
        st.warning("⚠️ Você precisa fazer login para acessar esta página.")

        # Botão para voltar ao login
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔓 Fazer Login", type="primary", use_container_width=True):
                st.switch_page("streamlit_app.py")

        st.info("💡 **Dica:** Use a página inicial (Home) no menu lateral para fazer login")
        st.stop()


def get_auth_headers():
    """
    Retorna headers com token de autenticação para requisições à API
    """
    if "access_token" not in st.session_state:
        return {}

    return {
        "Authorization": f"Bearer {st.session_state.access_token}",
        "Content-Type": "application/json"
    }


def is_authenticated():
    """
    Verifica se o usuário está autenticado
    Retorna True se estiver, False caso contrário
    """
    return "access_token" in st.session_state and st.session_state.access_token is not None


def logout():
    """
    Realiza logout limpando a sessão
    """
    keys_to_remove = ["access_token", "token_type", "user", "logged_in", "form_data_aluno"]
    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()


def get_current_user():
    """
    Retorna os dados do usuário autenticado
    """
    if "user" in st.session_state:
        return st.session_state.user
    return None


def hide_streamlit_app_from_sidebar():
    """
    Esconde o item 'streamlit app' do menu lateral
    Deve ser chamado em todas as páginas
    """
    st.markdown("""
        <style>
        /* Esconder primeiro item da lista de navegação (streamlit app) */
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
