# 🚀 Guia de Execução da Migration - Gestão de Contratos

## ✅ Status do Deploy
- ✅ **Código Frontend**: Deployado via Git Push
- ✅ **Código Backend**: Deployado via Git Push
- ⏳ **Migration do Banco**: PENDENTE (executar agora)

---

## 📋 Pré-requisitos
- Acesso ao Railway Dashboard
- Projeto: **AQUAFLOWPRO**
- Serviços: backend (PostgreSQL)

---

## 🎯 Opção 1: Executar via Railway Dashboard (RECOMENDADO)

### Passo 1: Acessar o Railway Dashboard
1. Acesse: https://railway.app/dashboard
2. Faça login com: **igorrevolute@gmail.com**
3. Selecione o projeto: **AQUAFLOWPRO**
4. Clique no serviço: **PostgreSQL** (banco de dados)

### Passo 2: Abrir Query Editor
1. Na tela do PostgreSQL, vá em **"Data"** ou **"Connect"**
2. Clique em **"Query"** ou **"psql"**
3. Isso abrirá um terminal SQL ou query editor

### Passo 3: Executar a Migration SQL
Copie e cole o conteúdo do arquivo `migration_contract_fields.sql` no query editor:

```sql
-- Migration: Add contract management fields to alunos table

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
```

### Passo 4: Verificar os Resultados
Após executar, você deve ver:
```
✅ Added data_fim_contrato column (ou "already exists" se já existir)
✅ Added duracao_contrato_meses column (ou "already exists" se já existir)
✅ Atualização de X linhas (alunos existentes)
✅ Tabela mostrando os campos criados
```

### Passo 5: Validar Dados
Execute esta query para ver os dados atualizados:
```sql
SELECT
    id,
    nome_completo,
    data_inicio_contrato,
    data_fim_contrato,
    duracao_contrato_meses,
    ativo
FROM alunos
LIMIT 10;
```

---

## 🎯 Opção 2: Executar via Railway CLI (Terminal)

### Se conseguir fazer o link do projeto:

```bash
# 1. Ir para o diretório do projeto
cd /Users/yourapple/aquasystem/natacao-manager

# 2. Fazer link com o projeto (vai abrir navegador)
railway link

# 3. Selecionar:
#    - Workspace: revolutedigital's Projects
#    - Project: AQUAFLOWPRO
#    - Environment: production

# 4. Executar a migration
cd backend
railway run python app/migrate_add_contract_fields.py
```

---

## 🎯 Opção 3: Executar via psql (se tiver connection string)

Se você tiver a connection string do PostgreSQL:

```bash
# 1. Obter a connection string no Railway Dashboard:
#    PostgreSQL > Connect > Copy DATABASE_URL

# 2. Executar migration via psql
psql "postgresql://user:pass@host:port/db" < migration_contract_fields.sql
```

---

## ✅ Como Saber se Funcionou?

### No Backend (Railway Logs):
1. Vá em **Backend Service > Deployments**
2. Clique no último deploy
3. Verifique se não há erros relacionados a campos faltando

### No Frontend (Testar):
1. Acesse o sistema: https://seu-dominio.railway.app
2. Faça login
3. Vá em **Alunos > Novo Aluno**
4. Você deve ver os novos campos:
   - ✅ **Duração (meses)** - dropdown com 3, 6, 12, 18, 24 meses
   - ✅ **Data Fim (calculado)** - campo desabilitado que calcula automaticamente

### No Dashboard:
1. Acesse o **Dashboard** principal
2. Você deve ver a nova seção: **"Contratos Expirando"**
3. Se houver alunos com contratos nos próximos 30 dias, aparecerão listados

---

## 🐛 Troubleshooting

### Erro: "column data_fim_contrato already exists"
**Solução**: Tudo bem! Significa que a migration já foi executada antes. Ignore e continue.

### Erro: "permission denied"
**Solução**: Verifique se está usando o usuário correto do banco. No Railway, use o query editor integrado.

### Erro: "relation alunos does not exist"
**Solução**: Verifique se está conectado no banco de dados correto. O nome deve ser o mesmo do backend.

### Frontend mostra erro 500 ao criar aluno
**Solução**: A migration ainda não foi executada. Execute os comandos SQL acima.

---

## 📊 O Que Foi Modificado no Banco?

### Tabela: `alunos`

**Colunas Adicionadas:**
```sql
data_fim_contrato        DATE         NULL
duracao_contrato_meses   INTEGER      DEFAULT 12
```

**Dados Atualizados:**
- Todos os alunos com `data_inicio_contrato` preenchida receberam:
  - `data_fim_contrato` = `data_inicio_contrato` + 12 meses
  - `duracao_contrato_meses` = 12

---

## 🎉 Próximos Passos Após a Migration

1. **Testar o cadastro de alunos** com os novos campos
2. **Ver o dashboard** com contratos expirando
3. **Enviar propostas de renovação** via WhatsApp
4. **Filtrar alunos** por "Contratos Expirando"

---

## 📞 Suporte

Se tiver qualquer problema, me avise e eu ajudo a resolver!

**Arquivos Criados:**
- ✅ `migration_contract_fields.sql` - Script SQL pronto para executar
- ✅ `MIGRATION_GUIDE.md` - Este guia (você está aqui)
- ✅ `backend/app/migrate_add_contract_fields.py` - Script Python (alternativa)
