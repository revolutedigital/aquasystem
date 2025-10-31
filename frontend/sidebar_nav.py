"""
Componente de navegação e logout para sidebar
"""
import streamlit as st


def add_logout_button():
    """
    Adiciona botão de logout na sidebar
    """
    if "access_token" in st.session_state and st.session_state.access_token:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 👤 Usuário")

        # Mostrar nome do usuário se disponível
        if "user" in st.session_state and st.session_state.user:
            user = st.session_state.user
            st.sidebar.write(f"**{user.get('name', user.get('email', 'Usuário'))}**")
            st.sidebar.caption(f"Role: {user.get('role', 'N/A')}")

        st.sidebar.markdown("---")

        # Botão de logout
        if st.sidebar.button("🚪 Sair / Logout", use_container_width=True, type="secondary"):
            # Limpar toda a sessão
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


def show_navigation_helper():
    """
    Mostra helper de navegação quando não autenticado
    """
    st.sidebar.markdown("---")
    st.sidebar.info("🔐 **Faça login** na página inicial para acessar o sistema")
