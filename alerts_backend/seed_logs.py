"""
Script para gerar logs de exemplo
"""

from database import db_manager
from datetime import datetime, timedelta
import random

def generate_sample_logs():
    """Gera logs de exemplo para teste"""
    
    # Níveis de log
    levels = ["INFO", "WARNING", "ERROR", "DEBUG", "CRITICAL"]
    
    # Origens dos logs
    origins = [
        "BackupAnalyzer",
        "StockAnalyzer", 
        "NFeAnalyzer",
        "DatabaseAnalyzer",
        "ErrorRateAnalyzer",
        "DiskSpaceAnalyzer",
        "API",
        "NotificationManager",
        "System"
    ]
    
    # Mensagens de exemplo por tipo
    messages = {
        "INFO": [
            "Verificação de backup concluída com sucesso",
            "Sistema inicializado corretamente",
            "Análise de estoque finalizada",
            "Conexão com banco de dados estabelecida",
            "Notificação enviada com sucesso",
            "API iniciada na porta 8000",
            "Verificação automática executada",
            "Cache limpo com sucesso"
        ],
        "WARNING": [
            "Espaço em disco atingiu 75% de uso",
            "Backup com mais de 12 horas de atraso",
            "Taxa de erros acima do normal (3%)",
            "Conexão lenta com o banco de dados",
            "Produto com estoque baixo detectado",
            "Tentativa de reconexão com serviço externo",
            "Memória RAM acima de 80%",
            "CPU com uso elevado"
        ],
        "ERROR": [
            "Falha ao conectar com servidor de backup",
            "Erro ao processar NFe: arquivo corrompido",
            "Timeout na consulta ao banco de dados",
            "Falha no envio de email de notificação",
            "Erro ao ler arquivo de configuração",
            "Serviço de monitoramento não respondeu",
            "Falha na autenticação da API",
            "Erro ao gravar log no disco"
        ],
        "DEBUG": [
            "Query executada em 45ms",
            "Cache hit: 95%",
            "Memória utilizada: 2.5GB/8GB",
            "Threads ativas: 12",
            "Conexões abertas: 5",
            "Tamanho do banco: 156MB",
            "Requests por minuto: 234",
            "Tempo de resposta médio: 120ms"
        ],
        "CRITICAL": [
            "Banco de dados offline - impossível conectar",
            "Disco cheio - sistema crítico",
            "Serviço principal travado",
            "Falha total no sistema de backup",
            "Perda de conexão com todos os servidores",
            "Erro fatal na aplicação principal"
        ]
    }
    
    logs = []
    
    # Gerar logs das últimas 24 horas
    now = datetime.now()
    
    for i in range(150):  # Gerar 150 logs
        # Calcular timestamp aleatório nas últimas 24 horas
        hours_ago = random.uniform(0, 24)
        timestamp = now - timedelta(hours=hours_ago)
        
        # Escolher nível aleatório (mais INFO e WARNING, menos CRITICAL)
        level = random.choices(
            levels,
            weights=[40, 30, 20, 8, 2],  # Probabilidades
            k=1
        )[0]
        
        # Escolher origem aleatória
        origin = random.choice(origins)
        
        # Escolher mensagem apropriada ao nível
        message = random.choice(messages[level])
        
        # Metadados adicionais
        metadata = {}
        
        if level in ["ERROR", "CRITICAL"]:
            metadata["stack_trace"] = f"Error at line {random.randint(10, 500)}"
            metadata["error_code"] = f"ERR_{random.randint(1000, 9999)}"
        
        if "Banco" in message or "Database" in origin:
            metadata["query_time"] = f"{random.randint(10, 500)}ms"
            metadata["affected_rows"] = random.randint(0, 100)
        
        if "disk" in message.lower() or "Disco" in message:
            metadata["disk_usage"] = f"{random.randint(50, 95)}%"
            metadata["free_space"] = f"{random.uniform(1, 50):.1f}GB"
        
        # Criar log
        log = {
            "level": level,
            "message": message,
            "origin": origin,
            "timestamp": timestamp,
            "metadata": metadata
        }
        
        logs.append(log)
    
    # Inserir logs no banco
    print(f"Gerando {len(logs)} logs de exemplo...")
    
    for log in logs:
        log_data = {
            "level": log["level"],
            "message": log["message"],
            "origin": log["origin"],
            "metadata": log["metadata"]
        }
        db_manager.insert_log(log_data)
    
    print(f"✓ {len(logs)} logs inseridos com sucesso!")
    
    # Estatísticas
    stats = {}
    for level in levels:
        count = sum(1 for log in logs if log["level"] == level)
        stats[level] = count
    
    print("\nEstatísticas dos logs gerados:")
    for level, count in stats.items():
        print(f"  {level}: {count}")


if __name__ == "__main__":
    print("=== Gerador de Logs de Exemplo ===\n")
    
    try:
        # Conectar ao banco
        print("Conectando ao MongoDB...")
        db_manager.connect()
        
        # Gerar logs
        generate_sample_logs()
        
        print("\n✅ Processo concluído!")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Desconectar
        db_manager.close()
