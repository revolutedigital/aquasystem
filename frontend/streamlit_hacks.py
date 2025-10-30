"""
Hacks e Correções de CSS para Streamlit
Funções reutilizáveis para aplicar em todas as páginas
"""


def get_streamlit_ui_hacks() -> str:
    """
    Retorna CSS e JavaScript para corrigir/esconder elementos do Streamlit

    Returns:
        str: HTML com CSS e JS para aplicar com st.markdown(unsafe_allow_html=True)
    """
    return """
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

    /* Forçar dark mode quando a classe está presente */
    body.dark-mode {
        background-color: #121212 !important;
    }

    body.dark-mode [data-testid="stAppViewContainer"],
    body.dark-mode .main,
    body.dark-mode section[data-testid="stAppViewContainer"] {
        background-color: #121212 !important;
        background-image: linear-gradient(to bottom, #121212 0%, #1A1A1A 100%) !important;
        color: #E0E0E0 !important;
    }
    </style>
    """


def hide_streamlit_menu_footer() -> str:
    """
    Esconde menu hamburger e footer do Streamlit

    Returns:
        str: CSS para esconder elementos
    """
    return """
    <style>
    /* Esconder menu hamburger */
    #MainMenu {visibility: hidden;}

    /* Esconder footer "Made with Streamlit" */
    footer {visibility: hidden;}

    /* Esconder header */
    header {visibility: hidden;}
    </style>
    """


def get_improved_contrast_css() -> str:
    """
    Retorna CSS adicional para melhorar contraste e legibilidade em dark mode

    Returns:
        str: CSS para melhorar contraste de textos
    """
    return """
    <style>
    /* Melhorar legibilidade geral de TODOS os textos */
    body, html {
        color: var(--text-primary) !important;
    }

    /* Garantir que títulos sejam sempre legíveis */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
    }

    /* Streamlit headers */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: var(--primary) !important;
    }

    /* Parágrafos e textos */
    p, span, div, label {
        color: var(--text-secondary) !important;
    }

    /* Labels de formulários */
    label[data-baseweb="form-control-label"],
    [data-baseweb="form-control-label"] label {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }

    /* Inputs - Todos os tipos - Máxima especificidade */
    input, textarea, select,
    input[type="text"],
    input[type="password"],
    input[type="email"],
    input[type="number"],
    input[type="tel"],
    input[type="date"],
    input[type="time"],
    .stTextInput input,
    .stTextInput > div > div > input,
    .stTextInput div[data-baseweb="base-input"] input,
    .stTextArea textarea,
    .stTextArea > div > div > textarea,
    .stSelectbox select,
    .stNumberInput input,
    .stNumberInput > div > div > input,
    .stDateInput input,
    .stDateInput > div > div > input,
    .stTimeInput input,
    .stTimeInput > div > div > input,
    [data-baseweb="input"] input,
    [data-baseweb="textarea"] textarea,
    div[data-baseweb="base-input"] input,
    div[role="textbox"],
    input[role="spinbutton"] {
        background: var(--bg-card) !important;
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
    }

    /* Forçar background em todos os estados */
    input:focus,
    textarea:focus,
    select:focus {
        background: var(--bg-card) !important;
        background-color: var(--bg-card) !important;
    }

    /* Prevenir background branco do autofill */
    input:-webkit-autofill,
    input:-webkit-autofill:hover,
    input:-webkit-autofill:focus,
    textarea:-webkit-autofill,
    textarea:-webkit-autofill:hover,
    textarea:-webkit-autofill:focus,
    select:-webkit-autofill,
    select:-webkit-autofill:hover,
    select:-webkit-autofill:focus {
        -webkit-box-shadow: 0 0 0px 1000px var(--bg-secondary) inset !important;
        -webkit-text-fill-color: var(--text-primary) !important;
        box-shadow: 0 0 0px 1000px var(--bg-secondary) inset !important;
        background-color: var(--bg-secondary) !important;
        transition: background-color 5000s ease-in-out 0s !important;
    }

    /* Selectbox - Texto do valor selecionado */
    .stSelectbox > div > div > div,
    [data-baseweb="select"] > div,
    [data-baseweb="select"] span,
    [data-baseweb="select"] div {
        color: var(--text-primary) !important;
    }

    /* Dropdown aberto - opções */
    [role="listbox"] li,
    [role="option"],
    [data-baseweb="menu"] li {
        color: var(--text-primary) !important;
        background: var(--bg-card) !important;
    }

    [role="listbox"] li:hover,
    [role="option"]:hover,
    [data-baseweb="menu"] li:hover {
        background: var(--gradient-primary) !important;
        color: white !important;
    }

    /* Background escuro suave para inputs */
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stDateInput"] input,
    div[data-testid="stTimeInput"] input {
        background-color: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
    }

    /* DatePicker/Calendar - Fundo escuro */
    [data-baseweb="calendar"],
    [data-baseweb="calendar"] > div,
    div[data-baseweb="calendar"],
    .react-datepicker,
    .react-datepicker__header,
    .react-datepicker__month-container {
        background-color: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
    }

    /* Dias do calendário */
    .react-datepicker__day,
    .react-datepicker__day-name {
        color: var(--text-primary) !important;
    }

    .react-datepicker__day:hover {
        background-color: var(--primary) !important;
        color: white !important;
    }

    /* Selectbox/Dropdown - Forçar fundo escuro */
    [data-baseweb="select"],
    [data-baseweb="select"] > div,
    div[data-baseweb="select"] {
        background-color: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
    }

    /* Selectbox - valor selecionado */
    [data-baseweb="select"] div[role="button"],
    [data-baseweb="select"] [role="button"] {
        background-color: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
    }

    /* Highlight quando campo está focado */
    div[data-testid="stTextInput"]:focus-within,
    div[data-testid="stNumberInput"]:focus-within,
    div[data-testid="stSelectbox"]:focus-within,
    div[data-testid="stTextArea"]:focus-within {
        outline: 2px solid var(--primary) !important;
        outline-offset: 2px;
        border-radius: 8px;
    }

    /* Input com foco - borda destacada */
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stNumberInput"] input:focus,
    div[data-testid="stTextArea"] textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.2) !important;
    }

    /* Placeholders - Máxima especificidade */
    input::placeholder,
    textarea::placeholder,
    select::placeholder,
    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder,
    input[type="text"]::placeholder,
    input[type="password"]::placeholder,
    input[type="email"]::placeholder,
    input[type="number"]::placeholder,
    input[type="tel"]::placeholder {
        color: var(--text-secondary) !important;
        opacity: 0.9 !important;
    }

    /* Força contraste dos placeholders */
    ::placeholder {
        color: var(--text-secondary) !important;
        opacity: 0.9 !important;
    }

    ::-webkit-input-placeholder {
        color: var(--text-secondary) !important;
        opacity: 0.9 !important;
    }

    ::-moz-placeholder {
        color: var(--text-secondary) !important;
        opacity: 0.9 !important;
    }

    :-ms-input-placeholder {
        color: var(--text-secondary) !important;
        opacity: 0.9 !important;
    }

    :-moz-placeholder {
        color: var(--text-secondary) !important;
        opacity: 0.9 !important;
    }

    /* Sidebar - garantir legibilidade total */
    [data-testid="stSidebar"] * {
        color: var(--text-primary) !important;
    }

    [data-testid="stSidebar"] a {
        color: var(--text-primary) !important;
    }

    [data-testid="stSidebar"] a:hover {
        color: white !important;
    }

    /* Alertas e info boxes */
    .stAlert, .stInfo, .stSuccess, .stWarning, .stError {
        color: var(--text-primary) !important;
    }

    .stAlert p, .stInfo p, .stSuccess p, .stWarning p, .stError p {
        color: var(--text-primary) !important;
    }

    /* Code blocks */
    code {
        background: var(--bg-secondary) !important;
        color: var(--primary) !important;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
    }

    /* Strong e em */
    strong {
        color: var(--primary) !important;
        font-weight: 700 !important;
    }

    em {
        color: var(--secondary) !important;
    }
    </style>
    """
