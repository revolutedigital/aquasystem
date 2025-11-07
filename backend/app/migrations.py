"""
Database migrations module
Automatically runs migrations on application startup
"""
from sqlalchemy import text
from app.database import engine
import logging

logger = logging.getLogger(__name__)


def run_migrations():
    """
    Run all pending migrations
    This function is idempotent - safe to run multiple times
    """
    logger.info("Starting database migrations...")

    try:
        with engine.connect() as conn:
            # Migration 1: Add contract management fields
            migrate_add_contract_fields(conn)

            # Commit all changes
            conn.commit()

        logger.info("All migrations completed successfully!")
        return True

    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        raise


def migrate_add_contract_fields(conn):
    """
    Migration: Add contract management fields to alunos table
    - data_fim_contrato (DATE)
    - duracao_contrato_meses (INTEGER, default 12)
    """
    logger.info("Running migration: add_contract_fields")

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
        logger.info("Adding column: data_fim_contrato")
        conn.execute(text("ALTER TABLE alunos ADD COLUMN data_fim_contrato DATE"))
    else:
        logger.info("Column data_fim_contrato already exists - skipping")

    # Add duracao_contrato_meses if it doesn't exist
    if 'duracao_contrato_meses' not in existing_columns:
        logger.info("Adding column: duracao_contrato_meses")
        conn.execute(text("ALTER TABLE alunos ADD COLUMN duracao_contrato_meses INTEGER DEFAULT 12"))
    else:
        logger.info("Column duracao_contrato_meses already exists - skipping")

    # Update existing records that have data_inicio but no data_fim
    logger.info("Calculating contract end dates for existing students...")
    result = conn.execute(text("""
        UPDATE alunos
        SET
            data_fim_contrato = data_inicio_contrato + INTERVAL '12 months',
            duracao_contrato_meses = 12
        WHERE
            data_inicio_contrato IS NOT NULL
            AND data_fim_contrato IS NULL
    """))

    rows_updated = result.rowcount
    logger.info(f"Updated {rows_updated} student records with contract end dates")

    logger.info("Migration add_contract_fields completed successfully!")
