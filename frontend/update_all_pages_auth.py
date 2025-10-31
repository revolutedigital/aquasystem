#!/usr/bin/env python3
"""
Script para atualizar todas as páginas com o novo sistema de autenticação
"""
import os
import re

# Páginas para atualizar
pages = [
    'pages/2_Cadastro_Alunos.py',
    'pages/3_Grade_Horarios.py',
    'pages/4_Financeiro.py',
    'pages/5_Usuarios.py'
]

# Padrão antigo a ser removido
old_pattern = r"""# CSS para esconder "streamlit app"
st\.markdown\(\"\"\"
    <style>
    /\* Esconder primeiro item da lista de navegação \*/
    \[data-testid="stSidebarNav"\] ul li:first-child,
    \[data-testid="stSidebarNav"\] > div > ul > li:first-child \{
        display: none !important;
    \}

    /\* Ajustar espaçamento \*/
    \[data-testid="stSidebarNav"\] \{
        padding-top: 1rem !important;
        margin-top: 0 !important;
    \}
    </style>
\"\"\", unsafe_allow_html=True\)"""

# Padrão antigo de autenticação
old_auth_pattern = r"""# Verificar autenticação - Redirecionar para login se necessário
if "access_token" not in st\.session_state or st\.session_state\.access_token is None:
    st\.error\("🔒 Acesso negado\. Por favor, faça login primeiro\."\)
    st\.info\("👉 Clique em 'streamlit app' no menu lateral para fazer login"\)
    st\.stop\(\)

# Função auxiliar para headers autenticados
def get_auth_headers\(\):
    \"\"\"Retorna headers com token de autenticação\"\"\"
    return \{
        "Authorization": f"Bearer \{st\.session_state\.access_token\}",
        "Content-Type": "application/json"
    \}"""

def update_imports(content):
    """Adiciona o import do auth_utils se não existir"""
    if 'from auth_utils import' in content:
        return content  # Já tem o import

    # Procurar pela linha de imports existentes
    import_pattern = r'(from styles import.*?\n)(from streamlit_hacks import.*?\n)'

    def add_auth_import(match):
        return match.group(0) + 'from auth_utils import require_authentication, get_auth_headers, hide_streamlit_app_from_sidebar\n'

    content = re.sub(import_pattern, add_auth_import, content)
    return content

def add_auth_check(content):
    """Adiciona verificação de autenticação após imports"""
    # Procurar por onde adicionar a checagem
    pattern = r'(# Aplicar estilos globais otimizados\n)'

    replacement = r'''# Verificar autenticação PRIMEIRO
require_authentication()

\1'''

    content = re.sub(pattern, replacement, content)
    return content

def add_hide_streamlit(content):
    """Adiciona função para esconder streamlit app do menu"""
    pattern = r'(# Obter componentes customizados\n)'

    replacement = r'''# Esconder 'streamlit app' do menu
hide_streamlit_app_from_sidebar()

\1'''

    content = re.sub(pattern, replacement, content)
    return content

def remove_old_css(content):
    """Remove o CSS antigo de esconder streamlit app"""
    # Remover o bloco de CSS antigo
    content = re.sub(
        r'# CSS para esconder "streamlit app"\nst\.markdown\(""".*?</style>\n""", unsafe_allow_html=True\)\n\n',
        '',
        content,
        flags=re.DOTALL
    )
    return content

def remove_old_auth(content):
    """Remove o código antigo de autenticação"""
    # Remover verificação antiga
    content = re.sub(
        r'# Verificar autenticação - Redirecionar para login se necessário\nif "access_token".*?st\.stop\(\)\n\n',
        '',
        content,
        flags=re.DOTALL
    )

    # Remover função antiga get_auth_headers
    content = re.sub(
        r'# Função auxiliar para headers autenticados\ndef get_auth_headers\(\):.*?\}\n\n',
        '',
        content,
        flags=re.DOTALL
    )

    return content

# Processar cada página
for page_path in pages:
    full_path = os.path.join(os.path.dirname(__file__), page_path)

    if not os.path.exists(full_path):
        print(f"❌ Arquivo não encontrado: {full_path}")
        continue

    print(f"📝 Processando: {page_path}")

    # Ler conteúdo
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Aplicar transformações
    content = update_imports(content)
    content = remove_old_css(content)
    content = remove_old_auth(content)
    content = add_auth_check(content)
    content = add_hide_streamlit(content)

    # Salvar
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Atualizado: {page_path}")

print("\n🎉 Todas as páginas foram atualizadas!")
print("📋 Alterações aplicadas:")
print("  - Adicionado import de auth_utils")
print("  - Adicionado require_authentication() no início")
print("  - Adicionado hide_streamlit_app_from_sidebar()")
print("  - Removido CSS antigo de esconder menu")
print("  - Removido código antigo de verificação de auth")
