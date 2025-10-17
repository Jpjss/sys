# Backend Python - Sistema de Alertas

## 📁 Estrutura

```
alerts_backend/
├── __init__.py              # Inicialização do módulo
├── database.py              # Gerenciador de conexão MongoDB
├── api.py                   # API REST com FastAPI
├── main.py                  # Script principal de monitoramento
├── requirements.txt         # Dependências Python
├── .env.example            # Exemplo de variáveis de ambiente
├── analyzers/
│   └── __init__.py         # Analisadores de problemas
│       ├── BackupAnalyzer
│       ├── StockAnalyzer
│       ├── NFeAnalyzer
│       ├── DatabaseAnalyzer
│       ├── ErrorRateAnalyzer
│       └── DiskSpaceAnalyzer
└── notifiers/
    └── __init__.py         # Serviços de notificação
        ├── EmailNotifier
        ├── WhatsAppNotifier
        └── NotificationManager
```

## 🚀 Instalação

### 1. Instalar MongoDB

**Windows:**
```powershell
# Baixe e instale de https://www.mongodb.com/try/download/community
# Ou use Chocolatey:
choco install mongodb
```

**Iniciar MongoDB:**
```powershell
mongod --dbpath C:\data\db
```

### 2. Instalar Dependências Python

```bash
cd alerts_backend
pip install -r requirements.txt
```

### 3. Configurar Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e configure:

```bash
cp .env.example .env
```

Edite o `.env`:
```env
MONGODB_URI=mongodb://localhost:27017/
DB_NAME=alerts_system

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=sua_senha_app
FROM_EMAIL=alertas@sistema.com
```

## 📡 Executar API

### Desenvolvimento

```bash
cd alerts_backend
python api.py
```

Ou com uvicorn:
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em: **http://localhost:8000**

### Documentação Interativa

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔄 Executar Monitor Manual

Para rodar as verificações uma vez:

```bash
cd alerts_backend
python main.py
```

## ⏰ Configurar Execução Automática

### Windows (Task Scheduler)

1. Abra o **Agendador de Tarefas**
2. Criar Tarefa Básica
3. Configurar para executar a cada 15 minutos
4. Ação: Iniciar um programa
5. Programa: `python`
6. Argumentos: `C:\path\to\alerts_backend\main.py`

### Linux/Mac (Cron)

```bash
# Editar crontab
crontab -e

# Adicionar linha (executar a cada 15 minutos)
*/15 * * * * cd /path/to/alerts_backend && python main.py >> monitor.log 2>&1
```

## 📚 Endpoints da API

### Alertas

- `GET /alerts` - Lista alertas
  - Query params: `status`, `severity`, `client_id`, `limit`
- `GET /alerts/{id}` - Busca alerta específico
- `POST /alerts` - Cria novo alerta
- `PUT /alerts/{id}` - Atualiza alerta
- `POST /alerts/{id}/resolve` - Marca como resolvido
- `DELETE /alerts/{id}` - Deleta alerta

### Estatísticas

- `GET /stats` - Retorna estatísticas
  - `openAlerts`
  - `inProgress`
  - `resolvedToday`
  - `avgResponseTime`

### Logs

- `GET /logs` - Lista logs do sistema
  - Query params: `level`, `origin`, `limit`

## 🔧 Personalizar Analisadores

Para adicionar um novo tipo de verificação:

1. Edite `alerts_backend/analyzers/__init__.py`
2. Crie uma nova classe herdando de `BaseAnalyzer`:

```python
class CustomAnalyzer(BaseAnalyzer):
    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.alert_type = "custom_type"
        self.severity = "high"
    
    def analyze(self) -> List[Dict]:
        alerts = []
        # Sua lógica aqui
        return alerts
```

3. Adicione ao factory `get_all_analyzers()`:

```python
def get_all_analyzers(db_manager) -> List[BaseAnalyzer]:
    return [
        # ... existentes
        CustomAnalyzer(db_manager)
    ]
```

## 📧 Configurar E-mail

### Gmail

1. Ative a verificação em 2 etapas
2. Gere uma "Senha de app" em: https://myaccount.google.com/apppasswords
3. Use essa senha no `.env`:

```env
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=senha_de_app_gerada
```

### Outros Provedores

```env
# Outlook
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587

# Yahoo
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
```

## 📱 Integrar WhatsApp

Use uma API de WhatsApp Business como:
- **Twilio**: https://www.twilio.com/whatsapp
- **WhatsApp Business API**: https://business.whatsapp.com

Configure no `.env`:
```env
WHATSAPP_API_URL=https://api.twilio.com/...
WHATSAPP_API_TOKEN=seu_token
```

## 🐳 Docker (Opcional)

Crie `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Executar:
```bash
docker build -t alerts-backend .
docker run -p 8000:8000 --env-file .env alerts-backend
```

## 🧪 Testes

```bash
# Testar conexão MongoDB
python -c "from database import db_manager; db_manager.connect()"

# Testar API
curl http://localhost:8000/

# Testar endpoint de alertas
curl http://localhost:8000/alerts
```

## 📊 Monitoramento

Os logs são salvos em:
- **Console**: Saída padrão
- **Arquivo**: `alerts_backend.log`

Para visualizar logs em tempo real:
```bash
tail -f alerts_backend.log
```

## 🔒 Segurança

Para produção:
1. Use HTTPS
2. Configure autenticação (JWT, OAuth)
3. Limite rate limiting
4. Use variáveis de ambiente seguras
5. Configure firewall do MongoDB

## 🆘 Troubleshooting

### Erro de conexão MongoDB
```bash
# Verificar se MongoDB está rodando
mongosh --eval "db.runCommand({ ping: 1 })"
```

### Erro de importação
```bash
# Reinstalar dependências
pip install --upgrade -r requirements.txt
```

### Porta 8000 já em uso
```bash
# Usar outra porta
uvicorn api:app --port 8001
```

## 📝 Logs e Debug

Ativar modo debug:
```python
# Em api.py ou main.py
logging.basicConfig(level=logging.DEBUG)
```

## 🔗 Links Úteis

- **MongoDB**: https://www.mongodb.com/docs/
- **FastAPI**: https://fastapi.tiangolo.com/
- **Python-dotenv**: https://pypi.org/project/python-dotenv/
