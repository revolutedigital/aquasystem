-- Migration: Add contract management fields to alunos table
-- Date: 2025-01-06
-- Description: Adds data_fim_contrato and duracao_contrato_meses fields

-- Step 1: Add data_fim_contrato column
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name='alunos' AND column_name='data_fim_contrato'
    ) THEN
        ALTER TABLE alunos ADD COLUMN data_fim_contrato DATE;
        RAISE NOTICE 'Added data_fim_contrato column';
    ELSE
        RAISE NOTICE 'data_fim_contrato column already exists';
    END IF;
END $$;

-- Step 2: Add duracao_contrato_meses column
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name='alunos' AND column_name='duracao_contrato_meses'
    ) THEN
        ALTER TABLE alunos ADD COLUMN duracao_contrato_meses INTEGER DEFAULT 12;
        RAISE NOTICE 'Added duracao_contrato_meses column';
    ELSE
        RAISE NOTICE 'duracao_contrato_meses column already exists';
    END IF;
END $$;

-- Step 3: Calculate data_fim_contrato for existing students
-- This sets data_fim to data_inicio + 12 months for all students that have data_inicio but no data_fim
UPDATE alunos
SET
    data_fim_contrato = data_inicio_contrato + INTERVAL '12 months',
    duracao_contrato_meses = 12
WHERE
    data_inicio_contrato IS NOT NULL
    AND data_fim_contrato IS NULL;

-- Step 4: Verify the migration
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'alunos'
    AND column_name IN ('data_fim_contrato', 'duracao_contrato_meses')
ORDER BY column_name;

-- Step 5: Show sample of updated data
SELECT
    id,
    nome_completo,
    data_inicio_contrato,
    data_fim_contrato,
    duracao_contrato_meses,
    ativo
FROM alunos
WHERE data_fim_contrato IS NOT NULL
LIMIT 5;
