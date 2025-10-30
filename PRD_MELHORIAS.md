# PRD - Product Requirements Document
## Sistema de Gestão para Academia de Natação - Melhorias

**Versão:** 1.0
**Data:** 15 de Outubro de 2025
**Status:** Em Planejamento
**Responsável:** Equipe de Desenvolvimento

---

## 📋 Índice

1. [Resumo Executivo](#resumo-executivo)
2. [Contexto Atual](#contexto-atual)
3. [Objetivos das Melhorias](#objetivos-das-melhorias)
4. [Escopo das Melhorias](#escopo-das-melhorias)
5. [Requisitos Funcionais](#requisitos-funcionais)
6. [Requisitos Não-Funcionais](#requisitos-não-funcionais)
7. [Cronograma de Implementação](#cronograma-de-implementação)
8. [Métricas de Sucesso](#métricas-de-sucesso)
9. [Riscos e Mitigações](#riscos-e-mitigações)

---

## 1. Resumo Executivo

O sistema de gestão para academia de natação está **90% funcional**, com backend completo (FastAPI), frontend operacional (Streamlit), banco de dados PostgreSQL e integração WhatsApp via Evolution API. Este PRD documenta as melhorias necessárias para alcançar **100% de completude** e evoluir o produto para as versões 2.0 e 3.0.

### Fases de Melhorias

- **Fase 1 (Curto Prazo - 1-2 semanas)**: Completar features pendentes da v1.0
- **Fase 2 (Médio Prazo - 1-2 meses)**: Implementar funcionalidades v2.0
- **Fase 3 (Longo Prazo - 3-6 meses)**: Expansão para v3.0

---

## 2. Contexto Atual

### 2.1 O Que Já Funciona ✅

**Backend (100% completo)**
- 22 endpoints REST (Alunos, Pagamentos, Horários)
- 4 models SQLAlchemy com relacionamentos
- 13 schemas Pydantic validados
- Integração WhatsApp Evolution API
- Sistema de notificações automatizadas (APScheduler)
- 11 funções utilitárias (helpers.py)

**Frontend (70% completo)**
- 5 páginas Streamlit operacionais
- Integração com API backend
- Cards de estatísticas básicas
- CRUDs funcionais (com gaps)

**Infraestrutura (100% completo)**
- Docker Compose orquestrado
- PostgreSQL 15 Alpine
- Volumes persistentes
- Health checks

### 2.2 Gaps Identificados ⚠️

**Frontend (30% pendente)**
- Validações de telefone brasileiro incompletas
- Falta de gráficos Plotly interativos
- Indicadores visuais básicos (faltam 🟢🟡🔴)
- Botões WhatsApp não implementados
- Export CSV ausente

**Backend (Pontos de Melhoria)**
- Falta init_db.py com dados de exemplo
- Ausência de autenticação/autorização
- Sem testes automatizados
- Logging básico

**Documentação**
- README incompleto (falta troubleshooting detalhado)
- Falta docker-compose.test.yml

---

## 3. Objetivos das Melhorias

### 3.1 Objetivos de Negócio

1. **Aumentar produtividade da academia em 40%** através de automação completa
2. **Reduzir inadimplência em 30%** com notificações WhatsApp eficientes
3. **Facilitar onboarding de novos usuários** com dados de exemplo e documentação clara
4. **Preparar sistema para escala** (múltiplas academias)

### 3.2 Objetivos Técnicos

1. Alcançar **100% de cobertura de testes** nas funcionalidades críticas
2. Implementar **autenticação segura** (JWT)
3. Otimizar **performance** (tempo de resposta < 200ms)
4. Garantir **compatibilidade mobile** no frontend

---

## 4. Escopo das Melhorias

### FASE 1: Completude da v1.0 (ALTA PRIORIDADE)

#### 4.1 Frontend - Páginas Aprimoradas

**US-F01: Página de Cadastro de Alunos (1_Cadastro_Alunos.py)**

**Descrição:** Aprimorar validações e UX da página de cadastro

**Critérios de Aceitação:**
- [ ] Validação de telefone brasileiro em tempo real (10 ou 11 dígitos)
- [ ] Formatação automática: (11) 99999-9999
- [ ] Máscara de CPF com validação de dígitos verificadores
- [ ] Indicador visual 🟢 para aluno ativo, 🔴 para inativo
- [ ] Ícones 🏊 para natação, 💧 para hidroginástica
- [ ] Botão "Enviar WhatsApp" ao lado do telefone
- [ ] Campo de busca com autocomplete por nome
- [ ] Export da lista de alunos para CSV

**Protótipo de Código:**
```python
import re

def validar_telefone_brasileiro(telefone: str) -> bool:
    # Remove caracteres não numéricos
    numeros = re.sub(r'\D', '', telefone)
    # Valida se tem 10 ou 11 dígitos
    return len(numeros) in [10, 11]

def formatar_telefone(telefone: str) -> str:
    numeros = re.sub(r'\D', '', telefone)
    if len(numeros) == 11:
        return f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:]}"
    elif len(numeros) == 10:
        return f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}"
    return telefone
```

---

**US-F02: Página de Financeiro (2_Financeiro.py)**

**Descrição:** Adicionar gráficos interativos e melhorar relatórios

**Critérios de Aceitação:**
- [ ] Gráfico de barras: Receita mensal dos últimos 6 meses (Plotly)
- [ ] Gráfico de pizza: Distribuição por forma de pagamento
- [ ] Gráfico de linha: Evolução da taxa de inadimplência
- [ ] Cards com KPIs: Receita total, média por aluno, inadimplência %
- [ ] Filtros por período (data início/fim)
- [ ] Botão "Enviar Cobrança WhatsApp" para cada inadimplente
- [ ] Export de relatório financeiro em CSV
- [ ] Indicador de status: 🟢 em dia, 🟡 vence em 3 dias, 🔴 atrasado

**Exemplo de Gráfico Plotly:**
```python
import plotly.express as px

def criar_grafico_receita_mensal(dados):
    fig = px.bar(
        dados,
        x='mes',
        y='receita',
        title='Receita Mensal - Últimos 6 Meses',
        labels={'mes': 'Mês', 'receita': 'Receita (R$)'},
        color='receita',
        color_continuous_scale='Blues'
    )
    fig.update_layout(showlegend=False)
    return fig
```

---

**US-F03: Página de Grade de Horários (3_Grade_Horarios.py)**

**Descrição:** Melhorar visualização de capacidade e facilitar matrículas

**Critérios de Aceitação:**
- [ ] Indicadores de ocupação: 🟢 < 70%, 🟡 70-90%, 🔴 > 90%
- [ ] Visualização em grid (cards por dia da semana)
- [ ] Drag-and-drop para matricular aluno (opcional)
- [ ] Modal de confirmação ao remover aluno
- [ ] Filtro por tipo de aula (natação/hidroginástica)
- [ ] Badge com número de vagas restantes
- [ ] Busca de horários disponíveis por dia/período
- [ ] Export da grade completa em CSV

**Layout Proposto:**
```
SEGUNDA-FEIRA
┌─────────────────────────────────┐
│ 08:00 - Natação        🟢       │
│ Ocupação: 12/20 (60%)           │
│ Vagas restantes: 8              │
│ ▪ João Silva                    │
│ ▪ Maria Santos                  │
│ ... [ver todos]                 │
└─────────────────────────────────┘
```

---

**US-F04: Dashboard (4_Dashboard.py)**

**Descrição:** Criar dashboard executivo com métricas em tempo real

**Critérios de Aceitação:**
- [ ] 4 métricas principais em st.metric:
  - Total de alunos ativos (com delta % mês anterior)
  - Inadimplentes (com delta % mês anterior)
  - Receita últimos 30 dias (com delta % mês anterior)
  - Taxa de ocupação média (com delta % semana anterior)
- [ ] Gráfico de linha: Evolução de alunos ativos (6 meses)
- [ ] Gráfico de barras empilhadas: Natação vs Hidroginástica por mês
- [ ] Tabela Top 5 horários mais procurados
- [ ] Tabela de próximos vencimentos (7 dias)
- [ ] Filtro de período para todos os gráficos
- [ ] Auto-refresh a cada 5 minutos

---

#### 4.2 Backend - Dados de Exemplo

**US-B01: Script de Inicialização do Banco (init_db.py)**

**Descrição:** Criar script para popular banco com dados realistas

**Critérios de Aceitação:**
- [ ] Função `criar_dados_exemplo()` que cria:
  - 20 alunos (15 natação, 5 hidroginástica)
  - 12 horários (Segunda a Sábado, manhã e tarde)
  - 60 pagamentos (últimos 3 meses)
  - 30 matrículas aluno-horário
- [ ] Dados realistas (nomes brasileiros, telefones válidos, CPFs válidos)
- [ ] Relacionamentos consistentes (pagamentos de alunos existentes)
- [ ] Flag `--reset` para limpar banco antes de popular
- [ ] Executável via: `python -m app.init_db --seed`
- [ ] Integração com docker-compose (variável CREATE_SAMPLE_DATA=true)

**Estrutura do Script:**
```python
# backend/app/init_db.py

from app.database import SessionLocal
from app.models import Aluno, Pagamento, Horario, AlunoHorario
from faker import Faker
import random

fake = Faker('pt_BR')

def criar_alunos_exemplo(db, quantidade=20):
    """Cria alunos de exemplo com dados realistas"""
    alunos = []
    for i in range(quantidade):
        aluno = Aluno(
            nome_completo=fake.name(),
            responsavel=fake.name() if random.random() > 0.5 else None,
            tipo_aula=random.choice(['natacao', 'hidroginastica']),
            valor_mensalidade=random.choice([150.00, 180.00, 200.00]),
            dia_vencimento=random.randint(5, 25),
            data_inicio_contrato=fake.date_between(start_date='-1y', end_date='today'),
            ativo=True,
            telefone_whatsapp=fake.phone_number(),
            observacoes=None
        )
        db.add(aluno)
        alunos.append(aluno)
    db.commit()
    return alunos

# ... demais funções
```

---

#### 4.3 Documentação e Validação

**US-D01: Completar README.md**

**Critérios de Aceitação:**
- [ ] Seção "Troubleshooting" expandida com 10+ problemas comuns
- [ ] Seção "Evolution API" com passo-a-passo completo e screenshots
- [ ] Seção "FAQ" com 15 perguntas frequentes
- [ ] Exemplos de uso da API com curl completos
- [ ] Vídeo tutorial (opcional - link para YouTube)
- [ ] Badge de status: build passing, coverage, version

---

**US-D02: Testes Automatizados (docker-compose.test.yml)**

**Critérios de Aceitação:**
- [ ] docker-compose.test.yml configurado
- [ ] Testes de integração para os 22 endpoints
- [ ] Testes de models e schemas
- [ ] Cobertura mínima de 80%
- [ ] CI/CD com GitHub Actions (opcional)

**Exemplo de Teste:**
```python
# backend/tests/test_alunos.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_criar_aluno():
    payload = {
        "nome_completo": "João Silva",
        "tipo_aula": "natacao",
        "valor_mensalidade": 150.00,
        "dia_vencimento": 10,
        "data_inicio_contrato": "2025-01-15",
        "telefone_whatsapp": "(11) 99999-9999"
    }
    response = client.post("/api/alunos", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["nome_completo"] == "João Silva"
    assert data["id"] is not None
```

---

### FASE 2: Funcionalidades v2.0 (MÉDIA PRIORIDADE)

#### 4.4 Autenticação e Autorização

**US-A01: Sistema de Login JWT**

**Descrição:** Implementar autenticação segura para múltiplos usuários

**Critérios de Aceitação:**
- [ ] Model `User` com campos: id, email, password_hash, role, created_at
- [ ] 3 roles: admin, recepcionista, aluno
- [ ] Endpoint POST /api/auth/login (retorna JWT)
- [ ] Endpoint POST /api/auth/register (apenas admin pode criar users)
- [ ] Endpoint GET /api/auth/me (retorna dados do usuário logado)
- [ ] Middleware de validação de JWT em todas as rotas protegidas
- [ ] Passwords hasheados com bcrypt
- [ ] Token expira em 24h
- [ ] Refresh token (expira em 7 dias)

**Permissões por Role:**
| Funcionalidade | Admin | Recepcionista | Aluno |
|----------------|-------|---------------|-------|
| Criar aluno | ✅ | ✅ | ❌ |
| Editar aluno | ✅ | ✅ | ❌ (apenas próprio cadastro) |
| Ver financeiro | ✅ | ✅ | ❌ (apenas próprios pagamentos) |
| Criar horário | ✅ | ❌ | ❌ |
| Matricular aluno | ✅ | ✅ | ❌ |
| Dashboard completo | ✅ | ✅ | ❌ |

**Diagrama de Fluxo:**
```
┌──────────┐      POST /login       ┌──────────┐
│  Client  │─────────────────────▶  │  Backend │
└──────────┘                        └──────────┘
     │                                    │
     │        {access_token, refresh}     │
     │◀───────────────────────────────────┤
     │                                    │
     │   GET /api/alunos                  │
     │   Header: Authorization: Bearer... │
     ├───────────────────────────────────▶│
     │                                    │
     │        {alunos: [...]}             │
     │◀───────────────────────────────────┤
```

---

**US-A02: Página de Login no Frontend**

**Critérios de Aceitação:**
- [ ] Página `0_Login.py` (primeira da aplicação)
- [ ] Form com email e password
- [ ] Armazenamento do JWT em `st.session_state`
- [ ] Redirecionamento automático após login
- [ ] Botão "Sair" no sidebar
- [ ] Proteção de todas as páginas (verifica se está autenticado)
- [ ] Mensagens de erro amigáveis

---

#### 4.5 Check-in com QR Code

**US-C01: Sistema de Check-in/Check-out**

**Descrição:** Permitir registro de presença dos alunos via QR Code

**Critérios de Aceitação:**
- [ ] Model `Presenca` com campos: id, aluno_id, horario_id, data, hora_entrada, hora_saida
- [ ] Endpoint POST /api/checkin (registra entrada)
- [ ] Endpoint POST /api/checkout (registra saída)
- [ ] Geração de QR Code único por aluno (válido por 1 hora)
- [ ] Página no frontend para escanear QR Code (usando streamlit-webrtc ou similar)
- [ ] Dashboard com presença diária por horário
- [ ] Relatório de frequência mensal por aluno
- [ ] Alerta se aluno não comparece por 7 dias consecutivos

**Fluxo de Uso:**
1. Aluno recebe QR Code por email/WhatsApp ao se matricular
2. Ao chegar na academia, mostra QR Code na recepção
3. Recepcionista escaneia QR Code (ou aluno escaneia em totem)
4. Sistema registra entrada com timestamp
5. Ao sair, repete o processo (registra saída)

**Dados do QR Code:**
```json
{
  "aluno_id": 123,
  "token": "abc123...",
  "expires_at": "2025-10-15T10:00:00"
}
```

---

#### 4.6 Integração com Plataformas de Pagamento

**US-P01: Pagamento Online via Mercado Pago/Stripe**

**Descrição:** Permitir pagamento de mensalidades online

**Critérios de Aceitação:**
- [ ] Integração com Mercado Pago API ou Stripe API
- [ ] Botão "Pagar Online" no frontend (página Financeiro)
- [ ] Geração de link de pagamento único por aluno/mês
- [ ] Webhook para receber confirmação de pagamento
- [ ] Atualização automática de status de pagamento
- [ ] Envio de recibo por email/WhatsApp após pagamento
- [ ] Suporte a PIX, cartão de crédito, boleto
- [ ] Logs de tentativas de pagamento (sucesso/falha)

**Exemplo de Integração (Mercado Pago):**
```python
import mercadopago

sdk = mercadopago.SDK(os.getenv("MERCADOPAGO_ACCESS_TOKEN"))

def criar_link_pagamento(aluno: Aluno, valor: float, mes_ref: str):
    payment_data = {
        "items": [
            {
                "title": f"Mensalidade {mes_ref} - {aluno.nome_completo}",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": float(valor)
            }
        ],
        "payer": {
            "email": aluno.email,
            "phone": {"number": aluno.telefone_whatsapp}
        },
        "back_urls": {
            "success": f"{FRONTEND_URL}/pagamento/sucesso",
            "failure": f"{FRONTEND_URL}/pagamento/falha",
            "pending": f"{FRONTEND_URL}/pagamento/pendente"
        },
        "notification_url": f"{BACKEND_URL}/api/webhooks/mercadopago"
    }

    result = sdk.preference().create(payment_data)
    return result["response"]["init_point"]  # URL para pagamento
```

---

### FASE 3: Expansão v3.0 (BAIXA PRIORIDADE - FUTURO)

#### 4.7 App Mobile

**US-M01: Aplicativo React Native ou Flutter**

**Descrição:** App mobile para alunos e staff

**Funcionalidades:**
- Login de alunos
- Visualização de horários matriculados
- Histórico de pagamentos
- QR Code para check-in
- Notificações push (lembretes de aula, vencimentos)
- Chat com a academia

---

#### 4.8 Avaliação Física

**US-AF01: Sistema de Avaliação Física**

**Descrição:** Registro e acompanhamento de evolução dos alunos

**Critérios de Aceitação:**
- [ ] Model `AvaliacaoFisica` com campos: peso, altura, IMC, pressão, observações
- [ ] Gráfico de evolução de peso/IMC ao longo do tempo
- [ ] Metas de saúde por aluno
- [ ] Alertas se aluno não faz avaliação há 3 meses

---

#### 4.9 Controle de Equipamentos

**US-E01: Gestão de Materiais e Equipamentos**

**Descrição:** Inventário de equipamentos da piscina

**Critérios de Aceitação:**
- [ ] Model `Equipamento`: prancha, macarrão, boia, etc
- [ ] Controle de quantidade em estoque
- [ ] Registro de manutenção
- [ ] Alertas de reposição

---

#### 4.10 Relatórios em PDF

**US-R01: Exportação de Relatórios PDF**

**Descrição:** Geração de relatórios profissionais em PDF

**Tipos de Relatórios:**
- Relatório financeiro mensal (com gráficos)
- Relatório de frequência por aluno
- Comprovante de pagamento
- Contrato de matrícula

**Biblioteca:** ReportLab ou WeasyPrint

---

## 5. Requisitos Funcionais

### 5.1 Requisitos de Performance

| Métrica | Objetivo | Medição |
|---------|----------|---------|
| Tempo de resposta API | < 200ms (95th percentile) | New Relic/Prometheus |
| Tempo de carregamento frontend | < 3s | Lighthouse |
| Capacidade de usuários simultâneos | 100 usuários | Testes de carga (Locust) |
| Disponibilidade | 99.5% uptime | Monitoramento |

### 5.2 Requisitos de Segurança

- [ ] HTTPS obrigatório em produção
- [ ] Passwords hasheados com bcrypt (salt rounds ≥ 12)
- [ ] JWT com secret forte (256 bits)
- [ ] Rate limiting: 100 req/min por IP
- [ ] Validação de input em todos os endpoints (Pydantic)
- [ ] Logs de ações sensíveis (criação/exclusão de dados)
- [ ] Backup automático diário do banco de dados

### 5.3 Requisitos de Compatibilidade

- [ ] Navegadores: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- [ ] Dispositivos: Desktop, tablet, mobile (responsive)
- [ ] Sistema Operacional (Docker): Linux, macOS, Windows 10+

---

## 6. Requisitos Não-Funcionais

### 6.1 Escalabilidade

- Sistema deve suportar até 500 alunos por academia
- Preparar arquitetura para multi-tenancy (v3.0)

### 6.2 Manutenibilidade

- Cobertura de testes ≥ 80%
- Documentação inline (docstrings) em 100% das funções
- Logs estruturados (JSON) para facilitar debug

### 6.3 Usabilidade

- Tempo de onboarding de novo usuário < 10 minutos
- Interface em português brasileiro
- Mensagens de erro claras e acionáveis

---

## 7. Cronograma de Implementação

### Fase 1: Completude v1.0 (2 semanas)

| Task | Esforço | Responsável | Deadline |
|------|---------|-------------|----------|
| US-F01: Página Cadastro Alunos | 3 dias | Dev Frontend | 18/10/2025 |
| US-F02: Página Financeiro | 3 dias | Dev Frontend | 21/10/2025 |
| US-F03: Página Grade Horários | 2 dias | Dev Frontend | 23/10/2025 |
| US-F04: Dashboard | 2 dias | Dev Frontend | 25/10/2025 |
| US-B01: Script init_db.py | 1 dia | Dev Backend | 26/10/2025 |
| US-D01: Completar README | 1 dia | Dev Backend | 27/10/2025 |
| US-D02: Testes Automatizados | 2 dias | QA | 29/10/2025 |

**Total:** 14 dias corridos

### Fase 2: Funcionalidades v2.0 (6 semanas)

| Task | Esforço | Responsável | Deadline |
|------|---------|-------------|----------|
| US-A01: Sistema Login JWT | 5 dias | Dev Backend | 06/11/2025 |
| US-A02: Página Login Frontend | 2 dias | Dev Frontend | 08/11/2025 |
| US-C01: Check-in QR Code | 7 dias | Dev Fullstack | 18/11/2025 |
| US-P01: Pagamento Online | 10 dias | Dev Backend + Integração | 02/12/2025 |

**Total:** 24 dias corridos (6 semanas)

### Fase 3: Expansão v3.0 (6 meses)

A definir conforme priorização de stakeholders.

---

## 8. Métricas de Sucesso

### 8.1 KPIs de Produto

| Métrica | Baseline Atual | Meta Fase 1 | Meta Fase 2 |
|---------|---------------|-------------|-------------|
| Taxa de adoção (academias usando) | 1 | 5 | 20 |
| NPS (Net Promoter Score) | N/A | 50 | 70 |
| Tempo médio de cadastro de aluno | 5 min | 2 min | 1 min |
| Redução de inadimplência | N/A | 20% | 30% |
| Engajamento (logins/semana) | N/A | 15 | 30 |

### 8.2 KPIs Técnicos

| Métrica | Baseline Atual | Meta Fase 1 | Meta Fase 2 |
|---------|---------------|-------------|-------------|
| Cobertura de testes | 0% | 80% | 90% |
| Bugs críticos em produção | N/A | < 2/mês | < 1/mês |
| Tempo de deploy | Manual | 10 min | 5 min (CI/CD) |
| Uptime | N/A | 99% | 99.9% |

---

## 9. Riscos e Mitigações

### 9.1 Riscos Técnicos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| Integração WhatsApp Evolution API falha | Média | Alto | Implementar fallback para email/SMS |
| Performance degradada com > 500 alunos | Baixa | Médio | Testes de carga antecipados, otimização de queries |
| Segurança de JWT comprometida | Baixa | Alto | Rotação de secrets, testes de penetração |
| Bug em produção afeta faturamento | Média | Alto | Testes E2E completos antes de deploy |

### 9.2 Riscos de Negócio

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| Academias não adotam sistema | Média | Alto | Pilotos gratuitos, treinamento presencial |
| Concorrentes lançam produto similar | Alta | Médio | Acelerar roadmap v2.0, focar em diferenciais |
| Custo de infraestrutura alto | Baixa | Médio | Otimizar uso de recursos, planos de pricing |

### 9.3 Riscos de Equipe

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| Desenvolvedor chave sai do projeto | Baixa | Alto | Documentação detalhada, pair programming |
| Escopo creep (aumento de escopo) | Alta | Médio | Priorização rigorosa, sprints fixas |
| Estimativas otimistas | Média | Médio | Buffer de 20% em cronograma |

---

## 10. Definição de Pronto (DoD - Definition of Done)

Uma feature só é considerada "pronta" quando:

- [ ] Código implementado e revisado (code review)
- [ ] Testes unitários escritos (cobertura ≥ 80%)
- [ ] Testes de integração passando
- [ ] Documentação atualizada (README, docstrings)
- [ ] Deploy em ambiente de staging realizado
- [ ] Teste de aceitação pelo product owner
- [ ] Sem bugs críticos ou bloqueantes

---

## 11. Stakeholders

| Nome | Papel | Responsabilidade | Comunicação |
|------|-------|------------------|-------------|
| Dono da Academia | Product Owner | Aprovar features, priorizar roadmap | Reunião semanal |
| Gerente de TI | Tech Lead | Arquitetura, code reviews | Daily standup |
| Desenvolvedor Backend | Backend Engineer | APIs, banco de dados, integrações | Slack, GitHub |
| Desenvolvedor Frontend | Frontend Engineer | Streamlit UI, UX | Slack, GitHub |
| QA | Quality Assurance | Testes, validação | Email, Jira |

---

## 12. Anexos

### 12.1 Wireframes (Link para Figma)

*(A ser criado)*

### 12.2 Diagramas de Arquitetura

```
┌─────────────────────────────────────────────┐
│                  FRONTEND                   │
│          Streamlit (Python 3.11)            │
│  5 páginas: Home, Alunos, Financeiro,       │
│  Horários, Dashboard                        │
└──────────────┬──────────────────────────────┘
               │ HTTP (REST API)
               ▼
┌─────────────────────────────────────────────┐
│                  BACKEND                    │
│          FastAPI (Python 3.11)              │
│  - 22 endpoints REST                        │
│  - JWT authentication (v2.0)                │
│  - APScheduler (notificações)               │
│  - WhatsApp Service (Evolution API)         │
└──────────────┬──────────────────────────────┘
               │ SQLAlchemy ORM
               ▼
┌─────────────────────────────────────────────┐
│                 DATABASE                    │
│          PostgreSQL 15 Alpine               │
│  4 tabelas: alunos, pagamentos,             │
│  horarios, aluno_horario                    │
└─────────────────────────────────────────────┘
```

### 12.3 Modelo de Dados (ER Diagram)

```
┌─────────────┐         ┌──────────────┐
│   alunos    │─────────│  pagamentos  │
│             │ 1     N │              │
│ id (PK)     │         │ id (PK)      │
│ nome        │         │ aluno_id (FK)│
│ telefone    │         │ valor        │
│ tipo_aula   │         │ data_pag     │
│ ...         │         │ mes_ref      │
└─────┬───────┘         └──────────────┘
      │
      │ M:N
      ▼
┌─────────────────┐
│ aluno_horario   │
│                 │
│ id (PK)         │
│ aluno_id (FK)   │
│ horario_id (FK) │
└─────────────────┘
      ▲
      │ M:N
      │
┌─────┴───────┐
│  horarios   │
│             │
│ id (PK)     │
│ dia_semana  │
│ horario     │
│ capacidade  │
│ tipo_aula   │
└─────────────┘
```

---

## 13. Glossário

- **Soft Delete**: Marcar registro como inativo em vez de deletar fisicamente
- **JWT**: JSON Web Token, padrão de autenticação stateless
- **APScheduler**: Biblioteca Python para agendamento de tarefas
- **Evolution API**: API open-source para integração com WhatsApp
- **ORM**: Object-Relational Mapping (SQLAlchemy)
- **NPS**: Net Promoter Score, métrica de satisfação do cliente
- **DoD**: Definition of Done, critérios de conclusão de uma tarefa

---

## 14. Aprovações

| Nome | Cargo | Assinatura | Data |
|------|-------|------------|------|
| [Nome] | Product Owner | ___________ | ___/___/___ |
| [Nome] | Tech Lead | ___________ | ___/___/___ |
| [Nome] | Stakeholder | ___________ | ___/___/___ |

---

**Última atualização:** 15/10/2025
**Versão do documento:** 1.0
**Próxima revisão:** 01/11/2025
