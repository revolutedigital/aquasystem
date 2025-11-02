"""
Script de migração para adicionar coluna plano_id à tabela alunos
Executar: python -m app.migrate_add_plano_id
"""
from sqlalchemy import text
from app.database import engine, SessionLocal

def migrate():
    """Adiciona coluna plano_id à tabela alunos"""
    print("🔄 Iniciando migração: adicionar plano_id à tabela alunos")

    with engine.connect() as conn:
        # Verificar se a coluna já existe
        result = conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='alunos' AND column_name='plano_id'
        """))

        if result.fetchone():
            print("✅ Coluna plano_id já existe na tabela alunos")
            return

        # Adicionar a coluna
        print("➕ Adicionando coluna plano_id...")
        conn.execute(text("""
            ALTER TABLE alunos
            ADD COLUMN plano_id INTEGER REFERENCES planos(id)
        """))
        conn.commit()

        print("✅ Migração concluída com sucesso!")
        print("📊 Coluna plano_id adicionada à tabela alunos")

if __name__ == "__main__":
    migrate()
