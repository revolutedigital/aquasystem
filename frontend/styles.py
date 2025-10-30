"""
Design System Enterprise-Grade - Sistema de Gestão de Natação
Paleta Vibrante Aquática com Dark Mode Padrão
Inspirado em Stripe, Linear, Vercel e Notion
"""

def get_global_styles():
    """Retorna CSS global com design system vibrante e dark mode padrão"""
    return """
    <style>
    /* ============================================
       IMPORTAÇÕES E DESIGN TOKENS
    ============================================ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    :root {
        /* ===== PALETA AQUÁTICA VIBRANTE ===== */
        /* Primary - Aqua Blue */
        --primary: #0EA5E9;
        --primary-hover: #0284C7;
        --primary-light: #38BDF8;
        --primary-lighter: #7DD3FC;
        --primary-dark: #0369A1;
        --primary-darker: #075985;

        /* Secondary - Turquoise */
        --secondary: #14B8A6;
        --secondary-hover: #0D9488;
        --secondary-light: #2DD4BF;
        --secondary-lighter: #5EEAD4;
        --secondary-dark: #0F766E;

        /* Accent - Electric Blue */
        --accent: #3B82F6;
        --accent-hover: #2563EB;
        --accent-light: #60A5FA;

        /* Semantic Colors */
        --success: #10B981;
        --success-bg: #ECFDF5;
        --warning: #F59E0B;
        --warning-bg: #FFFBEB;
        --error: #EF4444;
        --error-bg: #FEF2F2;
        --info: #06B6D4;
        --info-bg: #CFFAFE;

        /* Backgrounds - Com cor sutil */
        --bg-primary: #F0F9FF;           /* sky-50 */
        --bg-secondary: #E0F2FE;         /* sky-100 */
        --bg-tertiary: #BAE6FD;          /* sky-200 */
        --bg-card: rgba(255, 255, 255, 0.9);
        --bg-card-hover: rgba(255, 255, 255, 0.95);

        /* Gradients */
        --gradient-primary: linear-gradient(135deg, #0EA5E9 0%, #14B8A6 100%);
        --gradient-secondary: linear-gradient(135deg, #14B8A6 0%, #10B981 100%);
        --gradient-accent: linear-gradient(135deg, #3B82F6 0%, #0EA5E9 100%);
        --gradient-bg: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 50%, #CCFBF1 100%);

        /* Text Colors */
        --text-primary: #0F172A;
        --text-secondary: #475569;
        --text-tertiary: #64748B;
        --text-disabled: #94A3B8;
        --text-inverse: #FFFFFF;
        --text-on-primary: #FFFFFF;

        /* Borders */
        --border-color: #BAE6FD;
        --border-hover: #7DD3FC;
        --border-focus: #0EA5E9;

        /* Shadows */
        --shadow-xs: 0 1px 2px 0 rgba(14, 165, 233, 0.05);
        --shadow-sm: 0 1px 3px 0 rgba(14, 165, 233, 0.1), 0 1px 2px -1px rgba(14, 165, 233, 0.1);
        --shadow-md: 0 4px 6px -1px rgba(14, 165, 233, 0.15), 0 2px 4px -2px rgba(14, 165, 233, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(14, 165, 233, 0.2), 0 4px 6px -4px rgba(14, 165, 233, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(14, 165, 233, 0.25), 0 8px 10px -6px rgba(14, 165, 233, 0.1);
        --shadow-2xl: 0 25px 50px -12px rgba(14, 165, 233, 0.35);

        /* Transitions */
        --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-base: 250ms cubic-bezier(0.4, 0, 0.2, 1);
        --transition-slow: 350ms cubic-bezier(0.4, 0, 0.2, 1);

        /* Spacing */
        --space-1: 0.25rem;
        --space-2: 0.5rem;
        --space-3: 0.75rem;
        --space-4: 1rem;
        --space-5: 1.25rem;
        --space-6: 1.5rem;
        --space-8: 2rem;
        --space-10: 2.5rem;
        --space-12: 3rem;
        --space-16: 4rem;

        /* Border Radius */
        --radius-sm: 0.375rem;
        --radius-md: 0.5rem;
        --radius-lg: 0.75rem;
        --radius-xl: 1rem;
        --radius-2xl: 1.5rem;
        --radius-full: 9999px;

        /* Z-index */
        --z-base: 0;
        --z-dropdown: 1000;
        --z-sticky: 1100;
        --z-fixed: 1200;
        --z-modal-backdrop: 1300;
        --z-modal: 1400;
        --z-popover: 1500;
        --z-tooltip: 1600;
    }

    /* ============================================
       DARK MODE (PADRÃO)
    ============================================ */
    body.dark-mode,
    body {
        /* Dark mode é o padrão */
        --primary: #38BDF8 !important;
        --primary-hover: #0EA5E9 !important;
        --primary-light: #7DD3FC !important;
        --primary-lighter: #1E3A5F !important;
        --primary-dark: #0C4A6E !important;

        --secondary: #2DD4BF !important;
        --secondary-hover: #14B8A6 !important;
        --secondary-light: #5EEAD4 !important;
        --secondary-lighter: #134E4A !important;

        --accent: #60A5FA !important;
        --accent-hover: #3B82F6 !important;

        --success: #34D399 !important;
        --success-bg: #064E3B !important;
        --warning: #FBBF24 !important;
        --warning-bg: #451A03 !important;
        --error: #F87171 !important;
        --error-bg: #450A0A !important;
        --info: #22D3EE !important;
        --info-bg: #164E63 !important;

        /* Dark Backgrounds */
        --bg-primary: #0F172A !important;           /* slate-900 */
        --bg-secondary: #1E293B !important;         /* slate-800 */
        --bg-tertiary: #334155 !important;          /* slate-700 */
        --bg-card: rgba(30, 41, 59, 0.8) !important;
        --bg-card-hover: rgba(30, 41, 59, 0.95) !important;

        /* Gradients Dark */
        --gradient-primary: linear-gradient(135deg, #38BDF8 0%, #2DD4BF 100%) !important;
        --gradient-secondary: linear-gradient(135deg, #2DD4BF 0%, #34D399 100%) !important;
        --gradient-accent: linear-gradient(135deg, #60A5FA 0%, #38BDF8 100%) !important;
        --gradient-bg: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #134E4A 100%) !important;

        /* Text Dark */
        --text-primary: #F8FAFC !important;
        --text-secondary: #CBD5E1 !important;
        --text-tertiary: #94A3B8 !important;
        --text-disabled: #64748B !important;

        /* Borders Dark */
        --border-color: #334155 !important;
        --border-hover: #475569 !important;
        --border-focus: #38BDF8 !important;

        /* Shadows Dark */
        --shadow-xs: 0 1px 2px 0 rgba(0, 0, 0, 0.3) !important;
        --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.4), 0 1px 2px -1px rgba(0, 0, 0, 0.4) !important;
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.5), 0 2px 4px -2px rgba(0, 0, 0, 0.4) !important;
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.6), 0 4px 6px -4px rgba(0, 0, 0, 0.5) !important;
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.7), 0 8px 10px -6px rgba(0, 0, 0, 0.6) !important;

        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }

    /* Light Mode (quando ativado) */
    body.light-mode {
        --primary: #0EA5E9 !important;
        --primary-hover: #0284C7 !important;
        --primary-light: #38BDF8 !important;
        --primary-lighter: #E0F2FE !important;

        --secondary: #14B8A6 !important;
        --secondary-hover: #0D9488 !important;
        --secondary-light: #2DD4BF !important;
        --secondary-lighter: #CCFBF1 !important;

        --accent: #3B82F6 !important;
        --accent-hover: #2563EB !important;

        --success: #10B981 !important;
        --success-bg: #ECFDF5 !important;

        /* Light Backgrounds */
        --bg-primary: #F0F9FF !important;
        --bg-secondary: #E0F2FE !important;
        --bg-tertiary: #BAE6FD !important;
        --bg-card: rgba(255, 255, 255, 0.9) !important;

        /* Gradients Light */
        --gradient-bg: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 50%, #CCFBF1 100%) !important;

        /* Text Light */
        --text-primary: #0F172A !important;
        --text-secondary: #475569 !important;
        --text-tertiary: #64748B !important;

        /* Borders Light */
        --border-color: #BAE6FD !important;
        --border-hover: #7DD3FC !important;

        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }

    /* Reset */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        box-sizing: border-box;
    }

    /* ============================================
       LAYOUT PRINCIPAL
    ============================================ */
    body,
    .main,
    [data-testid="stAppViewContainer"],
    section[data-testid="stAppViewContainer"] {
        background: var(--gradient-bg) !important;
        color: var(--text-primary) !important;
        transition: all var(--transition-base);
    }

    .main {
        padding: var(--space-6);
        min-height: 100vh;
    }

    .block-container {
        max-width: 1400px;
        padding: var(--space-8) var(--space-6);
    }

    /* ============================================
       SIDEBAR - Com Cor
    ============================================ */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div:first-child {
        background: var(--bg-card) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid var(--border-color) !important;
        box-shadow: var(--shadow-lg);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: var(--space-6);
    }

    /* Links da sidebar */
    [data-testid="stSidebar"] a {
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
        text-decoration: none !important;
        padding: var(--space-3) var(--space-4) !important;
        border-radius: var(--radius-lg) !important;
        display: block !important;
        transition: all var(--transition-fast) !important;
        margin: var(--space-1) var(--space-2) !important;
        font-size: 0.9375rem !important;
    }

    [data-testid="stSidebar"] a:hover {
        background: var(--gradient-primary) !important;
        color: var(--text-on-primary) !important;
        transform: translateX(4px);
        box-shadow: var(--shadow-md);
    }

    /* Página ativa */
    [data-testid="stSidebar"] a.active,
    [data-testid="stSidebar"] .element-container:has(a[aria-current="page"]) a {
        background: var(--gradient-primary) !important;
        color: white !important;
        font-weight: 600 !important;
        box-shadow: var(--shadow-lg);
    }

    /* Garantir legibilidade de todos os elementos do sidebar */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] h5,
    [data-testid="stSidebar"] h6,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] label {
        color: var(--text-primary) !important;
    }

    [data-testid="stSidebar"] button {
        color: var(--text-primary) !important;
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
    }

    [data-testid="stSidebar"] button:hover {
        background: var(--gradient-primary) !important;
        color: white !important;
    }

    /* ============================================
       TIPOGRAFIA
    ============================================ */
    h1 {
        color: var(--text-primary) !important;
        font-weight: 800 !important;
        font-size: 2.25rem !important;
        line-height: 1.2 !important;
        letter-spacing: -0.025em !important;
        margin-bottom: var(--space-6) !important;
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    h2 {
        color: var(--primary) !important;
        font-weight: 700 !important;
        font-size: 1.875rem !important;
        line-height: 1.25 !important;
        letter-spacing: -0.0125em !important;
        margin-top: var(--space-12) !important;
        margin-bottom: var(--space-6) !important;
    }

    h3 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 1.5rem !important;
        line-height: 1.33 !important;
        margin-bottom: var(--space-4) !important;
    }

    h4 {
        color: var(--text-secondary) !important;
        font-weight: 600 !important;
        font-size: 1.125rem !important;
        line-height: 1.5 !important;
        margin-bottom: var(--space-3) !important;
    }

    p, li, span {
        color: var(--text-secondary);
        font-size: 1rem;
        line-height: 1.625;
        font-weight: 400;
    }

    /* ============================================
       CARDS - Vibrantes
    ============================================ */
    div[data-testid="metric-container"] {
        background: var(--bg-card) !important;
        backdrop-filter: blur(20px);
        padding: var(--space-6) !important;
        border-radius: var(--radius-2xl) !important;
        box-shadow: var(--shadow-lg) !important;
        border: 1px solid var(--border-color) !important;
        transition: all var(--transition-base) !important;
        position: relative;
        overflow: hidden;
    }

    div[data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: var(--gradient-primary);
    }

    div[data-testid="metric-container"]::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(14, 165, 233, 0.1) 0%, transparent 70%);
        pointer-events: none;
    }

    div[data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-2xl) !important;
        border-color: var(--primary) !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        color: var(--primary) !important;
        line-height: 1 !important;
        letter-spacing: -0.025em !important;
    }

    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: var(--space-2) !important;
    }

    [data-testid="stMetricDelta"] {
        font-size: 0.875rem !important;
        font-weight: 500 !important;
    }

    /* ============================================
       BOTÕES - Vibrantes
    ============================================ */
    .stButton > button {
        background: var(--gradient-primary) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-xl) !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.9375rem !important;
        box-shadow: var(--shadow-lg) !important;
        transition: all var(--transition-base) !important;
        letter-spacing: 0.0125em;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255,255,255,0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }

    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-2xl) !important;
    }

    .stButton > button:active {
        transform: translateY(0) !important;
    }

    .stButton > button:focus {
        outline: 2px solid var(--primary);
        outline-offset: 2px;
    }

    /* ============================================
       FORMULÁRIOS
    ============================================ */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input,
    .stTimeInput > div > div > input {
        background-color: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
    }

    /* Selectbox/Dropdown - Fundo escuro completo */
    .stSelectbox [data-baseweb="select"],
    .stSelectbox [data-baseweb="select"] > div,
    .stSelectbox div[role="button"],
    [data-baseweb="select"],
    [data-baseweb="select"] > div,
    [data-baseweb="select"] div {
        background-color: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
    }

    /* Selectbox - texto dentro */
    [data-baseweb="select"] span,
    .stSelectbox span {
        color: var(--text-primary) !important;
    }

    /* Dropdown aberto - opções */
    [role="listbox"],
    [role="listbox"] li {
        background-color: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
    }

    [role="listbox"] li:hover {
        background-color: var(--primary) !important;
        color: white !important;
    }

    .stTextInput > div > div > input:hover,
    .stTextArea > div > div > textarea:hover,
    .stNumberInput > div > div > input:hover {
        border-color: var(--border-hover) !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.2) !important;
        outline: none !important;
    }

    label {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        margin-bottom: var(--space-2) !important;
        letter-spacing: 0.0125em;
    }

    /* ============================================
       ALERTS
    ============================================ */
    .stAlert {
        background: var(--bg-card) !important;
        border-radius: var(--radius-xl) !important;
        border-left: 4px solid var(--primary) !important;
        box-shadow: var(--shadow-md) !important;
        padding: var(--space-4) !important;
        backdrop-filter: blur(20px);
        animation: slideIn var(--transition-base);
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-12px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    .stSuccess {
        border-left-color: var(--success) !important;
        background: var(--success-bg) !important;
    }

    .stError {
        border-left-color: var(--error) !important;
        background: var(--error-bg) !important;
    }

    .stWarning {
        border-left-color: var(--warning) !important;
        background: var(--warning-bg) !important;
    }

    .stInfo {
        border-left-color: var(--info) !important;
        background: var(--info-bg) !important;
    }

    /* ============================================
       TABS
    ============================================ */
    .stTabs [data-baseweb="tab-list"] {
        gap: var(--space-2);
        background: transparent;
        border-bottom: 2px solid var(--border-color);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border: none !important;
        color: var(--text-secondary) !important;
        padding: var(--space-3) var(--space-5) !important;
        font-weight: 600 !important;
        transition: all var(--transition-fast) !important;
        border-radius: var(--radius-lg) var(--radius-lg) 0 0 !important;
        position: relative;
    }

    .stTabs [data-baseweb="tab"]::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        right: 0;
        height: 2px;
        background: transparent;
        transition: background var(--transition-fast);
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(14, 165, 233, 0.1) !important;
        color: var(--primary) !important;
    }

    .stTabs [aria-selected="true"] {
        color: var(--primary) !important;
    }

    .stTabs [aria-selected="true"]::after {
        background: var(--gradient-primary);
    }

    /* ============================================
       EXPANDERS
    ============================================ */
    .stExpander {
        background: var(--bg-card);
        backdrop-filter: blur(20px);
        border-radius: var(--radius-xl);
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-md);
        margin: var(--space-2) 0;
        transition: all var(--transition-base);
    }

    .stExpander:hover {
        box-shadow: var(--shadow-lg);
        border-color: var(--primary);
    }

    /* ============================================
       LOADING
    ============================================ */
    .stSpinner > div {
        border-color: var(--primary) transparent transparent transparent !important;
    }

    /* ============================================
       DIVISORES
    ============================================ */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent 0%, var(--border-color) 20%, var(--border-color) 80%, transparent 100%);
        margin: var(--space-8) 0;
        opacity: 1;
    }

    /* ============================================
       SCROLLBAR
    ============================================ */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
        border-radius: var(--radius-full);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--gradient-primary);
        border-radius: var(--radius-full);
        border: 3px solid var(--bg-secondary);
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary);
    }

    /* ============================================
       RESPONSIVIDADE
    ============================================ */
    @media (max-width: 768px) {
        .main {
            padding: var(--space-4);
        }

        .block-container {
            padding: var(--space-6) var(--space-4);
        }

        h1 {
            font-size: 1.875rem !important;
        }

        h2 {
            font-size: 1.5rem !important;
        }

        [data-testid="stMetricValue"] {
            font-size: 2rem !important;
        }

        .stButton > button {
            width: 100%;
            padding: var(--space-4) !important;
        }
    }

    /* ============================================
       ACESSIBILIDADE
    ============================================ */
    *:focus-visible {
        outline: 2px solid var(--primary);
        outline-offset: 2px;
        border-radius: var(--radius-sm);
    }

    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
        }
    }

    /* ============================================
       UTILITÁRIOS
    ============================================ */
    .fade-in {
        animation: fadeIn var(--transition-slow);
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    .slide-up {
        animation: slideUp var(--transition-base);
    }

    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(12px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .skeleton {
        background: linear-gradient(90deg, var(--bg-secondary) 25%, var(--bg-tertiary) 50%, var(--bg-secondary) 75%);
        background-size: 200% 100%;
        animation: loading 1.5s ease-in-out infinite;
        border-radius: var(--radius-lg);
    }

    @keyframes loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    </style>
    """

def get_aquasystem_logo():
    """Retorna o logo SVG do AquaSystem"""
    return """
    <svg width="200" height="60" viewBox="0 0 200 60" xmlns="http://www.w3.org/2000/svg">
        <!-- Ondas de água -->
        <defs>
            <linearGradient id="waveGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#0EA5E9;stop-opacity:1" />
                <stop offset="50%" style="stop-color:#14B8A6;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#10B981;stop-opacity:1" />
            </linearGradient>
        </defs>

        <!-- Onda superior -->
        <path d="M 5 20 Q 15 15, 25 20 T 45 20" stroke="url(#waveGradient)" stroke-width="2.5" fill="none" opacity="0.8"/>

        <!-- Onda do meio -->
        <path d="M 5 28 Q 15 23, 25 28 T 45 28" stroke="url(#waveGradient)" stroke-width="2.5" fill="none" opacity="0.6"/>

        <!-- Onda inferior -->
        <path d="M 5 36 Q 15 31, 25 36 T 45 36" stroke="url(#waveGradient)" stroke-width="2.5" fill="none" opacity="0.4"/>

        <!-- Texto AQUA -->
        <text x="55" y="28" font-family="Inter, sans-serif" font-size="18" font-weight="800" fill="#0EA5E9">AQUA</text>

        <!-- Texto SYSTEM -->
        <text x="55" y="44" font-family="Inter, sans-serif" font-size="14" font-weight="600" fill="#14B8A6">SYSTEM</text>
    </svg>
    """

def get_custom_components():
    """Retorna componentes HTML customizados reutilizáveis"""
    return {
        "logo": get_aquasystem_logo(),

        "breadcrumb": lambda items: f"""
            <nav aria-label="breadcrumb" style="margin-bottom: var(--space-6); animation: fadeIn 0.3s ease;">
                <ol style="display: flex; gap: var(--space-2); padding: 0; list-style: none; color: var(--text-secondary); font-size: 0.875rem;">
                    {" ".join([f'<li style="display: flex; align-items: center;">{item}</li><li style="margin: 0 var(--space-2); color: var(--text-tertiary);">›</li>' if i < len(items)-1 else f'<li style="color: var(--primary); font-weight: 600;">{item}</li>' for i, item in enumerate(items)])}
                </ol>
            </nav>
        """,

        "loading": """
            <div style="text-align: center; padding: var(--space-8);">
                <div class="skeleton" style="height: 100px; margin-bottom: var(--space-4);"></div>
                <p style="color: var(--text-secondary);">Carregando dados...</p>
            </div>
        """,

        "empty_state": lambda icon, title, message, action_button=None: f"""
            <div style="text-align: center; padding: var(--space-16) var(--space-8); color: var(--text-secondary); animation: fadeIn 0.5s ease;">
                <div style="font-size: 4rem; margin-bottom: var(--space-6); opacity: 0.7;">{icon}</div>
                <h3 style="color: var(--primary); margin-bottom: var(--space-4); font-size: 1.5rem;">{title}</h3>
                <p style="font-size: 1rem; max-width: 500px; margin: 0 auto var(--space-8);">{message}</p>
                {f'<div style="margin-top: var(--space-8);">{action_button}</div>' if action_button else ''}
            </div>
        """,

        "dark_mode_toggle": """
            <style>
            #darkModeToggle {
                position: fixed;
                bottom: var(--space-8);
                right: var(--space-8);
                z-index: var(--z-fixed);
                background: var(--gradient-primary);
                color: white;
                border: none;
                border-radius: var(--radius-full);
                width: 56px;
                height: 56px;
                font-size: 1.5rem;
                cursor: pointer;
                box-shadow: var(--shadow-2xl);
                transition: all var(--transition-base);
                display: flex;
                align-items: center;
                justify-content: center;
            }

            #darkModeToggle:hover {
                transform: scale(1.1) rotate(90deg);
                box-shadow: 0 30px 60px -15px rgba(14, 165, 233, 0.5);
            }

            #darkModeToggle:active {
                transform: scale(0.95);
            }
            </style>

            <div id="darkModeToggle" title="Toggle Light Mode (Ctrl/Cmd + D)" role="button" tabindex="0" aria-label="Toggle light mode">
                <span id="themeIcon">☀️</span>
            </div>

            <script>
                function toggleLightMode() {
                    const body = document.body;
                    const icon = document.getElementById('themeIcon');

                    // Toggle entre dark-mode (padrão) e light-mode
                    const isLightMode = body.classList.toggle('light-mode');

                    localStorage.setItem('theme', isLightMode ? 'light' : 'dark');
                    if (icon) icon.textContent = isLightMode ? '🌙' : '☀️';

                    const btn = document.getElementById('darkModeToggle');
                    if (btn) {
                        btn.style.transform = 'rotate(360deg) scale(1.1)';
                        setTimeout(() => {
                            btn.style.transform = 'rotate(0deg) scale(1)';
                        }, 300);
                    }
                }

                function applyTheme() {
                    const savedTheme = localStorage.getItem('theme');
                    const body = document.body;
                    const icon = document.getElementById('themeIcon');

                    // Dark mode é o padrão
                    if (savedTheme === 'light') {
                        body.classList.add('light-mode');
                        if (icon) icon.textContent = '🌙';
                    } else {
                        body.classList.remove('light-mode');
                        if (icon) icon.textContent = '☀️';
                    }
                }

                applyTheme();
                document.addEventListener('DOMContentLoaded', applyTheme);

                const btn = document.getElementById('darkModeToggle');
                if (btn) {
                    btn.addEventListener('click', toggleLightMode);
                    btn.addEventListener('keypress', (e) => {
                        if (e.key === 'Enter' || e.key === ' ') {
                            e.preventDefault();
                            toggleLightMode();
                        }
                    });
                }

                document.addEventListener('keydown', function(e) {
                    if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
                        e.preventDefault();
                        toggleLightMode();
                    }
                });
            </script>
        """,

        "page_indicator": lambda current_page: f"""
            <script>
                document.addEventListener('DOMContentLoaded', function() {{
                    const links = document.querySelectorAll('[data-testid="stSidebar"] a');
                    links.forEach(link => {{
                        if (link.textContent.includes('{current_page}')) {{
                            link.classList.add('active');
                            link.setAttribute('aria-current', 'page');
                        }}
                    }});
                }});
            </script>
        """
    }

def create_pagination(items, items_per_page=10):
    """Cria paginação para uma lista de itens"""
    import streamlit as st

    total_items = len(items)
    total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)

    if 'current_page' not in st.session_state:
        st.session_state.current_page = 1

    if st.session_state.current_page > total_pages:
        st.session_state.current_page = total_pages

    current_page = st.session_state.current_page
    start_idx = (current_page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_items)
    items_paginated = items[start_idx:end_idx]

    return items_paginated, current_page, total_pages, total_items

def render_pagination_controls(current_page, total_pages, total_items):
    """Renderiza os controles de paginação"""
    import streamlit as st

    if total_pages <= 1:
        return

    st.markdown("---")
    col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])

    with col1:
        if st.button("⏮️ Primeira", disabled=(current_page == 1), use_container_width=True):
            st.session_state.current_page = 1
            st.rerun()

    with col2:
        if st.button("◀️ Anterior", disabled=(current_page == 1), use_container_width=True):
            st.session_state.current_page = current_page - 1
            st.rerun()

    with col3:
        st.markdown(f"""
            <div style="text-align: center; padding: var(--space-3); background: var(--bg-card); backdrop-filter: blur(20px); border-radius: var(--radius-lg); border: 1px solid var(--border-color);">
                <strong style="color: var(--primary);">Página {current_page} de {total_pages}</strong>
                <br>
                <span style="font-size: 0.875rem; color: var(--text-secondary);">({total_items} itens no total)</span>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        if st.button("Próxima ▶️", disabled=(current_page == total_pages), use_container_width=True):
            st.session_state.current_page = current_page + 1
            st.rerun()

    with col5:
        if st.button("Última ⏭️", disabled=(current_page == total_pages), use_container_width=True):
            st.session_state.current_page = total_pages
            st.rerun()
