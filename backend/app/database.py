"""
Configuração do banco de dados PostgreSQL usando SQLAlchemy
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Obter URL do banco de dados
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://natacao_user:natacao_password@postgres:5432/natacao_db"
)

# Railway fix: Converter postgres:// para postgresql://
# Railway às vezes retorna formato antigo que não funciona com SQLAlchemy
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    print(f"✅ DATABASE_URL convertida para formato correto")

print(f"🔗 Conectando ao banco de dados...")
print(f"📍 Host: {DATABASE_URL.split('@')[1].split('/')[0] if '@' in DATABASE_URL else 'localhost'}")

# Criar engine do SQLAlchemy
try:
    engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)
    print("✅ Engine do banco de dados criada com sucesso!")
except Exception as e:
    print(f"❌ Erro ao criar engine do banco: {str(e)}")
    raise

# Criar SessionLocal para gerenciar sessões do banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

def get_db():
    """
    Dependency injection para obter sessão do banco de dados.
    Utilizado nos endpoints do FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Inicializa o banco de dados criando todas as tabelas.
    Esta função é chamada no startup da aplicação.
    """
    from app.models import aluno, pagamento, horario, turma, user

    # Criar todas as tabelas no banco
    Base.metadata.create_all(bind=engine)
    print("✅ Banco de dados inicializado com sucesso!")

    # Criar usuário admin inicial (se não existir)
    try:
        from app.seed_admin import create_admin_user
        create_admin_user()
    except Exception as e:
        print(f"⚠️  Aviso: Não foi possível criar usuário admin: {str(e)}")
