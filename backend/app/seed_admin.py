"""
Script de Seed para Criar Usuário Admin Inicial
Execute: python -m app.seed_admin
"""
from app.database import SessionLocal
from app.models.user import User
from app.utils.auth import get_password_hash
import os


def create_admin_user():
    """Cria usuário admin padrão se não existir"""
    db = SessionLocal()

    try:
        # Verificar se já existe admin
        admin_exists = db.query(User).filter(User.role == "admin").first()

        if admin_exists:
            print("✅ Usuário admin já existe:")
            print(f"   Email: {admin_exists.email}")
            print(f"   Username: {admin_exists.username}")
            return

        # Obter credenciais do ambiente ou usar padrão
        admin_email = os.getenv("ADMIN_EMAIL", "admin@natacao.com")
        admin_password = os.getenv("ADMIN_PASSWORD", "admin123")  # MUDE EM PRODUÇÃO!
        admin_username = os.getenv("ADMIN_USERNAME", "admin")

        # Criar usuário admin
        admin_user = User(
            email=admin_email,
            username=admin_username,
            full_name="Administrador do Sistema",
            password_hash=get_password_hash(admin_password),
            role="admin",
            is_active=True,
            is_superuser=True
        )

        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        print("✅ Usuário admin criado com sucesso!")
        print(f"   Email: {admin_email}")
        print(f"   Username: {admin_username}")
        print(f"   Senha: {admin_password}")
        print("⚠️  IMPORTANTE: Altere a senha padrão após o primeiro login!")

    except Exception as e:
        print(f"❌ Erro ao criar usuário admin: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("🔧 Criando usuário admin inicial...")
    create_admin_user()
