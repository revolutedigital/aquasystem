"""
Página de Login - Sistema de Gestão de Natação
"""
import streamlit as st
import requests
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from styles import get_global_styles
from streamlit_hacks import get_improved_contrast_css

# Configuração da página
st.set_page_config(
    page_title="Login - Sistema de Natação",
    page_icon="🔐",
    layout="centered"
)

# Configuração da API
API_URL = os.getenv("API_URL", "http://backend:9000")

# Função de autenticação (precisa vir antes do CSS condicional)
def check_authentication():
    """Verifica se usuário está autenticado"""
    return "access_token" in st.session_state and st.session_state.access_token is not None

# Aplicar estilos globais
st.markdown(get_global_styles(), unsafe_allow_html=True)
st.markdown(get_improved_contrast_css(), unsafe_allow_html=True)

# CSS específico da página de login
# Apenas aplicar o CSS de esconder sidebar se NÃO estiver autenticado
if not check_authentication():
    st.markdown("""
    <style>
    /* ESCONDER COMPLETAMENTE O MENU LATERAL NA PÁGINA DE LOGIN */
    [data-testid="stSidebar"] {
        display: none !important;
    }

    section[data-testid="stSidebar"] {
        display: none !important;
    }

    /* Remover botão de abrir sidebar */
    button[kind="header"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
<style>
.login-container {
    background: var(--bg-card);
    backdrop-filter: blur(20px);
    padding: 3rem 2rem;
    border-radius: 16px;
    box-shadow: var(--shadow-lg);
    border: 1px solid var(--border-color);
    max-width: 450px;
    margin: 2rem auto;
}

.login-header {
    text-align: center;
    margin-bottom: 2rem;
}

.login-header h1 {
    color: var(--primary) !important;
    font-size: 2rem !important;
    margin-bottom: 0.5rem !important;
}

.login-header p {
    color: var(--text-secondary);
    font-size: 1rem;
}

.login-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
}

.info-box {
    background: var(--bg-card);
    backdrop-filter: blur(20px);
    border-left: 4px solid var(--primary);
    border: 1px solid var(--border-color);
    padding: 1rem;
    border-radius: 8px;
    margin-top: 1.5rem;
}

.info-box p {
    margin: 0;
    color: var(--text-secondary) !important;
    font-size: 0.9rem;
}

.success-box {
    background: var(--bg-card);
    backdrop-filter: blur(20px);
    border-left: 4px solid var(--secondary);
    border: 1px solid var(--border-color);
    padding: 1rem;
    border-radius: 8px;
    margin-top: 1rem;
}

.success-box p {
    color: var(--text-secondary) !important;
}

.footer-text {
    text-align: center;
    color: var(--text-secondary);
    font-size: 0.85rem;
    margin-top: 2rem;
}

/* Melhorar legibilidade geral */
h1, h2, h3, h4, h5, h6, p, label, span, div {
    color: var(--text-primary) !important;
}

.login-header p {
    color: var(--text-primary) !important;
    font-weight: 500;
}

/* Streamlit subheaders e headers */
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: var(--primary) !important;
}

/* Labels dos inputs */
label[data-baseweb="form-control-label"] {
    color: var(--text-primary) !important;
    font-weight: 500 !important;
}

/* Inputs de texto */
input[type="text"], input[type="password"], input[type="email"] {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
}

input::placeholder {
    color: var(--text-secondary) !important;
    opacity: 0.7;
}

/* Strong tags dentro de info-box */
.info-box strong {
    color: var(--primary) !important;
}

.success-box strong {
    color: var(--secondary) !important;
}
</style>
""", unsafe_allow_html=True)


def perform_login(email: str, password: str):
    """Realiza o login na API"""
    try:
        response = requests.post(
            f"{API_URL}/api/auth/login",
            json={"email": email, "password": password},
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            # Armazenar token e dados do usuário na sessão
            st.session_state.access_token = data["access_token"]
            st.session_state.token_type = data["token_type"]
            st.session_state.user = data["user"]
            st.session_state.logged_in = True
            return True, "Login realizado com sucesso!"
        elif response.status_code == 401:
            return False, "Email ou senha incorretos"
        elif response.status_code == 403:
            return False, "Usuário inativo. Contate o administrador."
        else:
            return False, f"Erro no servidor: {response.status_code}"

    except requests.exceptions.ConnectionError:
        return False, "Não foi possível conectar ao servidor. Verifique sua conexão."
    except Exception as e:
        return False, f"Erro inesperado: {str(e)}"


def logout():
    """Realiza logout limpando a sessão"""
    keys_to_remove = ["access_token", "token_type", "user", "logged_in"]
    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]


# Verificar se usuário já está logado
if check_authentication():
    # Usuário autenticado - mostrar tela limpa
    st.markdown("""
    <div style='text-align: center; padding: 4rem 2rem;'>
        <div style='font-size: 5rem; margin-bottom: 2rem;'>🏊‍♂️</div>
        <h1 style='color: var(--primary); margin-bottom: 1rem;'>Sistema de Natação</h1>
        <p style='color: var(--text-secondary); font-size: 1.1rem; margin-bottom: 2rem;'>
            Bem-vindo de volta! Você está autenticado.
        </p>
        <div style='background: var(--bg-card); padding: 2rem; border-radius: 12px; max-width: 600px; margin: 0 auto; border: 1px solid var(--border-color);'>
            <p style='color: var(--text-primary); font-size: 1rem; margin-bottom: 1rem;'>
                👈 Use o <strong>menu lateral</strong> para navegar:
            </p>
            <ul style='text-align: left; color: var(--text-secondary); list-style: none; padding: 0;'>
                <li style='padding: 0.5rem; margin: 0.5rem 0; background: var(--bg-secondary); border-radius: 8px;'>📊 <strong>Dashboard</strong> - Visão geral</li>
                <li style='padding: 0.5rem; margin: 0.5rem 0; background: var(--bg-secondary); border-radius: 8px;'>📝 <strong>Cadastro Alunos</strong> - Gerenciar alunos</li>
                <li style='padding: 0.5rem; margin: 0.5rem 0; background: var(--bg-secondary); border-radius: 8px;'>📅 <strong>Grade Horários</strong> - Aulas e horários</li>
                <li style='padding: 0.5rem; margin: 0.5rem 0; background: var(--bg-secondary); border-radius: 8px;'>💰 <strong>Financeiro</strong> - Pagamentos</li>
                <li style='padding: 0.5rem; margin: 0.5rem 0; background: var(--bg-secondary); border-radius: 8px;'>👥 <strong>Usuários</strong> - Gerenciar usuários</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

else:
    # Página de Login
    st.markdown("""
    <div class='login-container'>
        <div class='login-header'>
            <div style='text-align: center; margin-bottom: 1.5rem; font-size: 4rem;'>
                🏊‍♂️
            </div>
            <h1>Sistema de Natação</h1>
            <p>Faça login para acessar o sistema</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Formulário de Login
    with st.form("login_form", clear_on_submit=False):
        st.subheader("🔑 Credenciais de Acesso")

        email = st.text_input(
            "Email",
            placeholder="seu.email@exemplo.com",
            help="Digite seu email cadastrado"
        )

        password = st.text_input(
            "Senha",
            type="password",
            placeholder="••••••••",
            help="Digite sua senha"
        )

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button(
                "🔓 Entrar",
                use_container_width=True,
                type="primary"
            )

        if submit_button:
            if not email or not password:
                st.error("❌ Por favor, preencha todos os campos")
            else:
                with st.spinner("Autenticando..."):
                    success, message = perform_login(email, password)

                    if success:
                        st.success(f"✅ {message}")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")

    # Informações de credenciais padrão
    st.markdown("""
    <div class='info-box'>
        <p><strong>📝 Credenciais Padrão do Admin:</strong></p>
        <p>Email: <code>admin@natacao.com</code></p>
        <p>Senha: <code>admin123</code></p>
        <p><em>⚠️ Altere a senha após o primeiro login!</em></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='footer-text'>
        <p>Sistema de Gestão para Academia de Natação v2.0</p>
        <p>🔒 Conexão segura com autenticação JWT</p>
    </div>
    """, unsafe_allow_html=True)
