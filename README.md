# 🚨 Sistema de Monitoramento e Gestão de Alertas

<div align="center">

![Next.js](https://img.shields.io/badge/Next.js-15.2.4-black?style=for-the-badge&logo=next.js)
![React](https://img.shields.io/badge/React-19-blue?style=for-the-badge&logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5-blue?style=for-the-badge&logo=typescript)
![TailwindCSS](https://img.shields.io/badge/Tailwind-4.1-38B2AC?style=for-the-badge&logo=tailwind-css)
![Python](https://img.shields.io/badge/Python-3.x-yellow?style=for-the-badge&logo=python)

**Sistema completo para monitoramento automático, detecção e gestão de alertas críticos em ambientes de produção**

[Demonstração](#-capturas-de-tela) • [Instalação](#-instalação) • [Documentação](#-documentação) • [Contribuir](#-contribuindo)

</div>

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Características](#-características)
- [Tecnologias](#-tecnologias)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Uso](#-uso)
- [Arquitetura](#-arquitetura)
- [API](#-api)
- [Monitoramento Automático](#-monitoramento-automático)
- [Tipos de Alertas](#-tipos-de-alertas)
- [Capturas de Tela](#-capturas-de-tela)
- [Roadmap](#-roadmap)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

---

## 🎯 Sobre o Projeto

O **Sistema de Monitoramento e Gestão de Alertas** é uma plataforma completa para detecção, gerenciamento e resposta a incidentes técnicos e operacionais em tempo real. Ideal para empresas que precisam monitorar múltiplos clientes e sistemas simultaneamente.

### Problema que Resolve

- ❌ **Antes**: Falhas críticas passam despercebidas até que clientes reclamem
- ❌ **Antes**: Informações de alertas espalhadas em múltiplos canais
- ❌ **Antes**: Sem priorização clara de incidentes
- ❌ **Antes**: Notificações atrasadas ou perdidas

- ✅ **Agora**: Detecção automática proativa de problemas
- ✅ **Agora**: Dashboard centralizado e organizado
- ✅ **Agora**: Sistema inteligente de severidade e priorização
- ✅ **Agora**: Notificações instantâneas multi-canal

---

## ✨ Características

### 🎨 Interface Web Moderna

- ⚡ **Dashboard em Tempo Real** - Visão consolidada de todos os alertas
- 📊 **Estatísticas e Métricas** - Acompanhe KPIs importantes
- 🔍 **Filtros Avançados** - Por status, severidade, cliente ou palavra-chave
- 🌓 **Tema Claro/Escuro** - Interface adaptável às preferências do usuário
- 📱 **Design Responsivo** - Funciona perfeitamente em todos os dispositivos
- ♿ **Acessibilidade** - Seguindo padrões WCAG

### 🤖 Monitoramento Automático

- ⏰ **Execução Programada** - Via cron jobs (5-15 minutos)
- 🔄 **Verificações Múltiplas** - 8+ tipos de monitoramento diferentes
- 🎯 **Detecção Inteligente** - Evita alertas duplicados
- 📝 **Logs Detalhados** - Registro completo de todas as operações
- 🔔 **Notificações Multi-canal** - Email, WhatsApp, SMS e mais

### 🛠️ Gestão de Alertas

- 📌 **Status Dinâmico** - Aberto, Em Progresso, Resolvido
- 👥 **Atribuição de Responsáveis** - Delegue alertas para sua equipe
- 📈 **Níveis de Severidade** - Crítico, Alto, Médio, Baixo
- 💬 **Histórico Completo** - Rastreie todas as ações e mudanças
- 📤 **Exportação de Dados** - Relatórios em PDF, CSV ou Excel

### 🔔 Sistema de Notificações

- 📧 **Email** - Notificações HTML formatadas
- 💬 **WhatsApp** - Integração via API
- 📱 **SMS** - Para alertas críticos (opcional)
- 🔗 **Webhooks** - Integre com outros sistemas
- ⚙️ **Regras Personalizadas** - Configure quando e como notificar

---

## 🚀 Tecnologias

### Frontend

- **[Next.js 15](https://nextjs.org/)** - Framework React com SSR/SSG
- **[React 19](https://react.dev/)** - Biblioteca UI com Server Components
- **[TypeScript](https://www.typescriptlang.org/)** - Tipagem estática
- **[Tailwind CSS 4](https://tailwindcss.com/)** - Framework CSS utilitário
- **[Radix UI](https://www.radix-ui.com/)** - Componentes acessíveis e customizáveis
- **[Lucide React](https://lucide.dev/)** - Ícones modernos e consistentes
- **[Recharts](https://recharts.org/)** - Gráficos e visualizações
- **[React Hook Form](https://react-hook-form.com/)** - Formulários performáticos
- **[Zod](https://zod.dev/)** - Validação de schemas

### Backend

- **[Python 3.x](https://www.python.org/)** - Sistema de monitoramento
- **[PostgreSQL](https://www.postgresql.org/)** - Banco de dados relacional
- **[psycopg2](https://www.psycopg.org/)** - Driver PostgreSQL para Python
- **[Next.js API Routes](https://nextjs.org/docs/api-routes/introduction)** - API REST

### DevOps & Ferramentas

- **[pnpm](https://pnpm.io/)** - Gerenciador de pacotes eficiente
- **[Cron](https://en.wikipedia.org/wiki/Cron)** - Agendamento de tarefas
- **[Git](https://git-scm.com/)** - Controle de versão
- **[ESLint](https://eslint.org/)** - Linting de código

---

## 📦 Instalação

### Pré-requisitos

Certifique-se de ter instalado:

- **Node.js** 18+ ([Download](https://nodejs.org/))
- **Python** 3.8+ ([Download](https://www.python.org/))
- **PostgreSQL** 14+ ([Download](https://www.postgresql.org/))
- **pnpm** (ou npm/yarn)

### 1. Clone o Repositório

```bash
git clone https://github.com/Jpjss/sys.git
cd sys
```

### 2. Instale as Dependências

#### Frontend (Next.js)

```bash
# Instalar pnpm globalmente (se ainda não tiver)
npm install -g pnpm

# Instalar dependências do projeto
pnpm install
```

#### Backend (Python)

```bash
cd scripts
pip install -r requirements.txt
```

### 3. Configure o Banco de Dados

```bash
# Criar banco de dados
createdb alerts_db

# Executar migrations
psql -U postgres -d alerts_db -f scripts/001_create_alerts_schema.sql
psql -U postgres -d alerts_db -f scripts/002_seed_alert_rules.sql
psql -U postgres -d alerts_db -f scripts/003_seed_sample_data.sql
```

---

## ⚙️ Configuração

### Variáveis de Ambiente

Crie um arquivo `.env.local` na raiz do projeto:

```env
# Banco de Dados
DB_HOST=localhost
DB_NAME=alerts_db
DB_USER=postgres
DB_PASSWORD=sua_senha
DB_PORT=5432

# Email (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=sua_senha_app
FROM_EMAIL=alertas@empresa.com

# WhatsApp API (opcional)
WHATSAPP_API_URL=https://api.whatsapp.com/send
WHATSAPP_API_TOKEN=seu_token_api

# Next.js
NEXT_PUBLIC_API_URL=http://localhost:3000
```

### Configuração do Monitor Python

Edite `scripts/monitor.py` se necessário e configure as credenciais no ambiente:

```bash
export DB_HOST=localhost
export DB_NAME=alerts_db
export DB_USER=postgres
export DB_PASSWORD=sua_senha
```

---

## 🎮 Uso

### Iniciar o Servidor de Desenvolvimento

```bash
pnpm dev
```

Acesse: **http://localhost:3000**

### Build para Produção

```bash
pnpm build
pnpm start
```

### Executar Monitor Manualmente

```bash
cd scripts
python3 monitor.py
```

### Configurar Monitoramento Automático (Cron)

```bash
cd scripts
chmod +x setup_cron.sh
./setup_cron.sh
```

Isso configurará o monitor para executar automaticamente a cada 15 minutos.

**Verificar Cron:**

```bash
crontab -l
```

**Logs do Monitor:**

```bash
tail -f /var/log/alert_monitor.log
```

---

## 🏗️ Arquitetura

### Estrutura de Diretórios

```
sys/
├── app/                          # Next.js App Router
│   ├── api/                      # API Routes
│   │   ├── alerts/              # Endpoints de alertas
│   │   │   ├── route.ts         # GET/POST alertas
│   │   │   └── [id]/            # Operações específicas
│   │   │       └── route.ts     # GET/PUT/DELETE por ID
│   │   └── notifications/       # Endpoints de notificações
│   │       ├── send/            # Enviar notificações
│   │       └── history/         # Histórico de envios
│   ├── layout.tsx               # Layout raiz
│   ├── page.tsx                 # Página inicial (Dashboard)
│   └── globals.css              # Estilos globais
│
├── components/                   # Componentes React
│   ├── ui/                      # Componentes base (Radix UI)
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── dialog.tsx
│   │   └── ...
│   ├── alert-card.tsx           # Card individual de alerta
│   ├── alert-list.tsx           # Lista de alertas
│   ├── alert-dashboard.tsx      # Dashboard principal
│   ├── alert-filters.tsx        # Filtros de busca
│   ├── stats-overview.tsx       # Estatísticas gerais
│   ├── dashboard-header.tsx     # Cabeçalho do dashboard
│   └── send-notification-dialog.tsx # Dialog de notificações
│
├── scripts/                      # Sistema de monitoramento Python
│   ├── monitor.py               # Script principal de monitoramento
│   ├── requirements.txt         # Dependências Python
│   ├── setup_cron.sh           # Configuração automática do cron
│   ├── 001_create_alerts_schema.sql    # Schema do banco
│   ├── 002_seed_alert_rules.sql        # Regras de alertas
│   ├── 003_seed_sample_data.sql        # Dados de exemplo
│   └── README.md                # Documentação do monitor
│
├── lib/                          # Utilitários
│   └── utils.ts                 # Funções auxiliares
│
├── hooks/                        # React Hooks customizados
│   ├── use-toast.ts            # Hook de notificações toast
│   └── use-mobile.ts           # Hook para detecção mobile
│
├── public/                       # Arquivos estáticos
├── styles/                       # Estilos adicionais
│
├── package.json                  # Dependências Node.js
├── tsconfig.json                # Configuração TypeScript
├── next.config.mjs              # Configuração Next.js
├── tailwind.config.js           # Configuração Tailwind
├── postcss.config.mjs           # Configuração PostCSS
└── components.json              # Configuração shadcn/ui
```

### Fluxo de Dados

```
┌─────────────────┐
│  Cron Job       │
│  (a cada 15min) │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  monitor.py             │
│  - Verifica sistemas    │
│  - Detecta problemas    │
│  - Cria alertas         │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  PostgreSQL Database    │
│  - Armazena alertas     │
│  - Armazena regras      │
│  - Histórico completo   │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Next.js API Routes     │
│  - REST API             │
│  - Validações           │
│  - Business Logic       │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  React Components       │
│  - Dashboard            │
│  - Alertas em tempo real│
│  - Filtros e ações      │
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Notificações           │
│  - Email (SMTP)         │
│  - WhatsApp (API)       │
│  - Webhooks             │
└─────────────────────────┘
```

---

## 🔌 API

### Endpoints Disponíveis

#### **GET /api/alerts**

Listar alertas com filtros opcionais

**Query Parameters:**
- `status` - Filtrar por status (open, in_progress, resolved)
- `severity` - Filtrar por severidade (critical, high, medium, low)
- `search` - Buscar por texto livre

**Resposta:**
```json
{
  "alerts": [
    {
      "id": 1,
      "client_id": "CLI001",
      "client_name": "Empresa ABC Ltda",
      "alert_type": "backup_failed",
      "severity": "critical",
      "title": "Falha no Backup Diário",
      "description": "O backup automático falhou...",
      "status": "open",
      "created_at": "2025-10-16T10:30:00Z",
      "assigned_to": null,
      "resolved_by": null,
      "resolved_at": null
    }
  ],
  "total": 1
}
```

#### **GET /api/alerts/[id]**

Obter detalhes de um alerta específico

**Resposta:**
```json
{
  "id": 1,
  "client_id": "CLI001",
  "client_name": "Empresa ABC Ltda",
  "alert_type": "backup_failed",
  "severity": "critical",
  "title": "Falha no Backup Diário",
  "description": "O backup automático falhou às 03:00...",
  "status": "open",
  "metadata": {
    "error": "Timeout na conexão"
  },
  "created_at": "2025-10-16T10:30:00Z"
}
```

#### **PUT /api/alerts/[id]**

Atualizar um alerta (status, atribuição, etc.)

**Body:**
```json
{
  "status": "in_progress",
  "assigned_to": "João Silva"
}
```

#### **DELETE /api/alerts/[id]**

Deletar um alerta

#### **POST /api/notifications/send**

Enviar notificação manual

**Body:**
```json
{
  "alert_id": 1,
  "channels": ["email", "whatsapp"],
  "recipients": ["email@example.com", "+5511999999999"]
}
```

#### **GET /api/notifications/history**

Obter histórico de notificações enviadas

---

## 🤖 Monitoramento Automático

### Como Funciona

O sistema de monitoramento é executado periodicamente via **cron job** e realiza as seguintes operações:

1. **Conexão com o Banco** - Estabelece conexão segura com PostgreSQL
2. **Carrega Regras Ativas** - Busca regras de monitoramento habilitadas
3. **Executa Verificações** - Roda cada tipo de check configurado
4. **Detecta Problemas** - Identifica anomalias e falhas
5. **Previne Duplicatas** - Verifica se alerta similar já existe
6. **Cria Alertas** - Insere novos alertas no banco
7. **Envia Notificações** - Notifica via canais configurados
8. **Registra Logs** - Salva log completo das operações

### Configuração de Regras

As regras de monitoramento são definidas na tabela `alert_rules`:

```sql
INSERT INTO alert_rules (
  rule_name, 
  alert_type, 
  check_interval_minutes, 
  severity, 
  notification_channels, 
  enabled
) VALUES (
  'Verificar Backups',
  'backup_failed',
  15,
  'critical',
  '["email", "whatsapp"]',
  true
);
```

### Personalizar Verificações

Para adicionar um novo tipo de verificação:

1. **Adicione a regra no banco:**

```sql
INSERT INTO alert_rules (rule_name, alert_type, check_interval_minutes, severity)
VALUES ('Minha Verificação', 'meu_tipo', 30, 'high');
```

2. **Crie o método no `monitor.py`:**

```python
def check_meu_tipo(self) -> List[Dict]:
    """Descrição da verificação"""
    query = """
        SELECT * FROM minha_tabela 
        WHERE condicao_problema = true
    """
    results = self.db.execute_query(query)
    
    alerts = []
    for row in results:
        alerts.append({
            'client_id': row['client_id'],
            'client_name': row['client_name'],
            'alert_type': 'meu_tipo',
            'severity': 'high',
            'title': 'Título do Alerta',
            'description': 'Descrição detalhada',
            'source': 'meu_monitor',
            'metadata': {}
        })
    
    return alerts
```

3. **Registre no `run_all_checks`:**

```python
checks = [
    # ... outros checks
    ('Minha Verificação', self.check_meu_tipo),
]
```

---

## 🎯 Tipos de Alertas

### Alertas Suportados

| Tipo | Descrição | Severidade Padrão | Intervalo |
|------|-----------|-------------------|-----------|
| `backup_failed` | Falhas em backups automáticos | Critical | 15 min |
| `stock_zero` | Produtos com estoque zerado | High | 30 min |
| `nfe_error` | Erros no envio de NF-e | Critical | 10 min |
| `db_connection_error` | Falhas de conexão com banco | Critical | 5 min |
| `high_error_rate` | Taxa elevada de erros na aplicação | High | 15 min |
| `disk_space_low` | Espaço em disco baixo (< 10%) | High | 60 min |
| `api_slow` | API com tempo de resposta alto | Medium | 30 min |
| `license_expiring` | Licenças próximas do vencimento | Medium | 1440 min |

### Níveis de Severidade

- 🔴 **Critical** - Requer ação imediata (ex: sistema fora do ar)
- 🟠 **High** - Importante mas não urgente (ex: estoque baixo)
- 🟡 **Medium** - Atenção necessária (ex: performance degradada)
- 🟢 **Low** - Informativo (ex: avisos gerais)

---

## 📸 Capturas de Tela

### Dashboard Principal
*Visão geral de todos os alertas com filtros e estatísticas*

### Card de Alerta
*Detalhes completos com ações disponíveis*

### Filtros Avançados
*Busque por status, severidade, cliente ou texto livre*

### Notificações
*Envie notificações manuais ou configure automáticas*

---

## 🗺️ Roadmap

### Em Desenvolvimento

- [ ] **Integração com Slack** - Notificações via Slack
- [ ] **Dashboard Analytics** - Gráficos e métricas avançadas
- [ ] **Relatórios Automatizados** - PDF/Excel agendados
- [ ] **API GraphQL** - Alternativa à REST API
- [ ] **Mobile App** - Aplicativo nativo iOS/Android

### Planejado

- [ ] **Inteligência Artificial** - Predição de falhas
- [ ] **Multi-tenancy** - Suporte a múltiplas empresas
- [ ] **SSO/SAML** - Login corporativo
- [ ] **Webhooks Bidirecionais** - Integração com ferramentas externas
- [ ] **Testes Automatizados** - Jest, Cypress, Pytest
- [ ] **Docker/Kubernetes** - Deploy containerizado
- [ ] **Internacionalização (i18n)** - Suporte a múltiplos idiomas

### Concluído ✅

- [x] Dashboard funcional com Next.js 15
- [x] Sistema de monitoramento Python
- [x] Notificações por Email
- [x] Filtros e busca avançada
- [x] CRUD completo de alertas
- [x] Tema claro/escuro
- [x] Design responsivo

---

## 🤝 Contribuindo

Contribuições são sempre bem-vindas! Veja como você pode ajudar:

### Como Contribuir

1. **Fork** o projeto
2. **Crie uma branch** para sua feature (`git checkout -b feature/MinhaFeature`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. **Push** para a branch (`git push origin feature/MinhaFeature`)
5. **Abra um Pull Request**

### Diretrizes

- Siga os padrões de código existentes
- Escreva mensagens de commit descritivas
- Adicione testes quando aplicável
- Atualize a documentação se necessário
- Seja respeitoso com outros colaboradores

### Reportar Bugs

Encontrou um bug? [Abra uma issue](https://github.com/Jpjss/sys/issues) com:

- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs atual
- Screenshots (se aplicável)
- Ambiente (SO, versão do Node, etc.)

---

## 📄 Licença

Este projeto está sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

**Jpjss**

- GitHub: [@Jpjss](https://github.com/Jpjss)
- LinkedIn: [Seu LinkedIn](https://linkedin.com/in/seu-perfil)

---

## 🙏 Agradecimentos

- [Vercel](https://vercel.com) - Por hospedar o projeto
- [Radix UI](https://www.radix-ui.com/) - Componentes acessíveis incríveis
- [shadcn/ui](https://ui.shadcn.com/) - Design system inspirador
- Comunidade Open Source - Por todas as ferramentas fantásticas

---

## 📞 Suporte

Precisa de ajuda? Entre em contato:

- 📧 Email: suporte@seudominio.com
- 💬 Discord: [Servidor da Comunidade](https://discord.gg/seu-servidor)
- 📖 Documentação: [Wiki](https://github.com/Jpjss/sys/wiki)

---

<div align="center">

**Feito com ❤️ e ☕ por [Jpjss](https://github.com/Jpjss)**

⭐ Se este projeto foi útil, considere dar uma estrela!

</div>
