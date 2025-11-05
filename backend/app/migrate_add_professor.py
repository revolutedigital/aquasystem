"""
Script de migração para adicionar tabela professores e colunas professor_id e fila_espera
Executar: python -m app.migrate_add_professor
"""
from sqlalchemy import text
from app.database import engine, SessionLocal


def migrate():
    """Adiciona tabela professores e atualiza tabela horarios"""
    print("🔄 Iniciando migração: adicionar tabela professores e atualizar horarios")

    with engine.connect() as conn:
        # 1. Criar tabela professores se não existir
        print("➕ Verificando tabela professores...")
        result = conn.execute(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_name='professores'
        """))

        if not result.fetchone():
            print("➕ Criando tabela professores...")
            conn.execute(text("""
                CREATE TABLE professores (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    cpf VARCHAR(14) NOT NULL UNIQUE,
                    telefone VARCHAR(20),
                    especialidade VARCHAR(100),
                    is_active BOOLEAN NOT NULL DEFAULT TRUE
                )
            """))

            # Criar índices
            conn.execute(text("CREATE INDEX ix_professores_nome ON professores(nome)"))
            conn.execute(text("CREATE INDEX ix_professores_email ON professores(email)"))
            conn.execute(text("CREATE INDEX ix_professores_cpf ON professores(cpf)"))

            conn.commit()
            print("✅ Tabela professores criada com sucesso!")
        else:
            print("✅ Tabela professores já existe")

        # 2. Adicionar coluna professor_id à tabela horarios
        print("➕ Verificando coluna professor_id em horarios...")
        result = conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='horarios' AND column_name='professor_id'
        """))

        if not result.fetchone():
            print("➕ Adicionando coluna professor_id...")
            conn.execute(text("""
                ALTER TABLE horarios
                ADD COLUMN professor_id INTEGER REFERENCES professores(id)
            """))
            conn.commit()
            print("✅ Coluna professor_id adicionada!")
        else:
            print("✅ Coluna professor_id já existe")

        # 3. Adicionar coluna fila_espera à tabela horarios
        print("➕ Verificando coluna fila_espera em horarios...")
        result = conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='horarios' AND column_name='fila_espera'
        """))

        if not result.fetchone():
            print("➕ Adicionando coluna fila_espera...")
            conn.execute(text("""
                ALTER TABLE horarios
                ADD COLUMN fila_espera INTEGER NOT NULL DEFAULT 0
            """))
            conn.commit()
            print("✅ Coluna fila_espera adicionada!")
        else:
            print("✅ Coluna fila_espera já existe")

        print("✅ Migração concluída com sucesso!")
        print("📊 Resumo:")
        print("   - Tabela professores criada/verificada")
        print("   - Coluna professor_id adicionada/verificada em horarios")
        print("   - Coluna fila_espera adicionada/verificada em horarios")


if __name__ == "__main__":
    migrate()
