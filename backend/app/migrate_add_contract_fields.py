"""
Migration to add contract management fields to alunos table
"""
from sqlalchemy import text
from app.database import engine

def migrate():
    """Add contract fields to alunos table"""
    with engine.connect() as conn:
        try:
            # Check if columns already exist
            result = conn.execute(text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='alunos'
                AND column_name IN ('data_fim_contrato', 'duracao_contrato_meses')
            """))
            existing_columns = [row[0] for row in result]

            # Add data_fim_contrato if it doesn't exist
            if 'data_fim_contrato' not in existing_columns:
                print("Adding data_fim_contrato column...")
                conn.execute(text("""
                    ALTER TABLE alunos
                    ADD COLUMN data_fim_contrato DATE
                """))
                conn.commit()
                print("✓ data_fim_contrato column added successfully")
            else:
                print("✓ data_fim_contrato column already exists")

            # Add duracao_contrato_meses if it doesn't exist
            if 'duracao_contrato_meses' not in existing_columns:
                print("Adding duracao_contrato_meses column...")
                conn.execute(text("""
                    ALTER TABLE alunos
                    ADD COLUMN duracao_contrato_meses INTEGER DEFAULT 12
                """))
                conn.commit()
                print("✓ duracao_contrato_meses column added successfully")
            else:
                print("✓ duracao_contrato_meses column already exists")

            # Update existing records: calculate data_fim_contrato based on data_inicio_contrato
            print("Calculating contract end dates for existing students...")
            conn.execute(text("""
                UPDATE alunos
                SET data_fim_contrato = data_inicio_contrato + INTERVAL '12 months',
                    duracao_contrato_meses = 12
                WHERE data_inicio_contrato IS NOT NULL
                AND data_fim_contrato IS NULL
            """))
            conn.commit()
            print("✓ Contract end dates calculated successfully")

            print("\n✅ Migration completed successfully!")

        except Exception as e:
            print(f"❌ Error during migration: {e}")
            conn.rollback()
            raise

if __name__ == "__main__":
    print("Starting contract fields migration...")
    migrate()
