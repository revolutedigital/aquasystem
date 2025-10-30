# 🛠️ Scripts de Deploy

Scripts úteis para deploy e manutenção do sistema.

## 📜 Scripts Disponíveis

### `deploy-railway.sh`

Script automatizado para deploy no Railway.

**Uso:**
```bash
./scripts/deploy-railway.sh
```

**O que faz:**
1. ✅ Verifica Railway CLI
2. ✅ Faz login (se necessário)
3. ✅ Cria/verifica projeto
4. ✅ Adiciona PostgreSQL
5. ✅ Deploy backend com variáveis
6. ✅ Deploy frontend com variáveis
7. ✅ Configura CORS automaticamente
8. ✅ Exibe URLs finais

**Pré-requisitos:**
- Railway CLI instalado (`npm i -g @railway/cli`)
- Git configurado
- Estar no diretório raiz do projeto

**Tempo estimado:** 5-10 minutos

---

## 🔧 Adicionar Novos Scripts

Para adicionar um novo script:

1. Crie o arquivo na pasta `scripts/`
2. Adicione shebang: `#!/bin/bash`
3. Torne executável: `chmod +x scripts/seu-script.sh`
4. Documente aqui no README

---

## 📚 Scripts Futuros (Planejados)

- `backup-railway.sh` - Backup do banco Railway
- `rollback.sh` - Rollback para versão anterior
- `monitor.sh` - Monitoramento de health checks
- `seed-data.sh` - Popular banco com dados de teste

---

**Sistema de Gestão de Natação**
*Scripts v1.0*
