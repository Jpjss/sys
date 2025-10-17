"""
Script para gerar alertas de exemplo
"""

from database import db_manager
from datetime import datetime, timedelta
import random

def generate_sample_alerts():
    """Gera alertas de exemplo para teste"""
    
    severities = ["critical", "high", "medium", "low"]
    statuses = ["open", "in_progress", "resolved"]
    types = [
        "backup_failure",
        "low_stock",
        "nfe_error", 
        "database_slow",
        "high_error_rate",
        "disk_space"
    ]
    
    alerts = []
    now = datetime.now()
    
    # Gerar 30 alertas variados
    for i in range(30):
        # Timestamp aleatório nos últimos 7 dias
        days_ago = random.uniform(0, 7)
        created_at = now - timedelta(days=days_ago)
        
        # Escolher severidade (mais medium e high)
        severity = random.choices(
            severities,
            weights=[10, 30, 40, 20],
            k=1
        )[0]
        
        # Escolher status (70% open, 20% in_progress, 10% resolved)
        status = random.choices(
            statuses,
            weights=[70, 20, 10],
            k=1
        )[0]
        
        # Escolher tipo
        alert_type = random.choice(types)
        
        # Criar mensagem baseada no tipo
        messages = {
            "backup_failure": "Falha no backup automático - último backup há {} horas",
            "low_stock": "Produto {} com estoque crítico: {} unidades restantes",
            "nfe_error": "Erro ao processar NFe {} - arquivo corrompido",
            "database_slow": "Consulta lenta detectada - tempo de resposta: {}ms",
            "high_error_rate": "Taxa de erros elevada: {}% no último período",
            "disk_space": "Espaço em disco crítico: {}% utilizado em {}"
        }
        
        # Gerar detalhes específicos
        if alert_type == "backup_failure":
            hours = random.randint(24, 72)
            message = messages[alert_type].format(hours)
            details = {
                "last_backup": (now - timedelta(hours=hours)).isoformat(),
                "backup_server": f"srv-backup-{random.randint(1,3)}",
                "error_code": f"BKP_{random.randint(1000, 9999)}"
            }
        
        elif alert_type == "low_stock":
            product_id = random.randint(1000, 9999)
            quantity = random.randint(0, 10)
            message = messages[alert_type].format(product_id, quantity)
            details = {
                "product_id": product_id,
                "current_stock": quantity,
                "minimum_stock": 50,
                "warehouse": f"CD-{random.randint(1,5)}"
            }
        
        elif alert_type == "nfe_error":
            nfe_number = random.randint(10000, 99999)
            message = messages[alert_type].format(nfe_number)
            details = {
                "nfe_number": nfe_number,
                "error_type": "XML_MALFORMED",
                "file_size": f"{random.randint(10, 500)}KB"
            }
        
        elif alert_type == "database_slow":
            response_time = random.randint(1000, 5000)
            message = messages[alert_type].format(response_time)
            details = {
                "query_time": response_time,
                "database": "production_db",
                "query": "SELECT * FROM orders WHERE..."[:50]
            }
        
        elif alert_type == "high_error_rate":
            error_rate = random.uniform(5, 25)
            message = messages[alert_type].format(f"{error_rate:.1f}")
            details = {
                "error_rate": error_rate,
                "total_requests": random.randint(1000, 10000),
                "error_count": int(random.randint(50, 500))
            }
        
        else:  # disk_space
            usage = random.randint(80, 98)
            disk = random.choice(["C:", "D:", "/var", "/home"])
            message = messages[alert_type].format(usage, disk)
            details = {
                "disk_usage": usage,
                "disk_path": disk,
                "free_space": f"{random.uniform(1, 50):.1f}GB",
                "total_space": f"{random.randint(100, 1000)}GB"
            }
        
        # Criar alerta
        alert = {
            "title": message,
            "description": f"Alerta automático gerado pelo monitoramento",
            "severity": severity,
            "status": status,
            "type": alert_type,
            "source": f"{alert_type.split('_')[0].title()}Analyzer",
            "created_at": created_at,
            "details": details
        }
        
        # Se resolvido, adicionar dados de resolução
        if status == "resolved":
            resolved_hours = random.uniform(0.5, 24)
            alert["resolved_at"] = created_at + timedelta(hours=resolved_hours)
            alert["resolved_by"] = random.choice(["João Silva", "Maria Santos", "Pedro Costa", "Ana Oliveira"])
            alert["resolution"] = random.choice([
                "Problema corrigido automaticamente",
                "Backup executado manualmente",
                "Estoque reposto",
                "Arquivo reprocessado",
                "Cache limpo e otimizado",
                "Disco expandido"
            ])
        
        alerts.append(alert)
    
    # Inserir alertas no banco
    print(f"Gerando {len(alerts)} alertas de exemplo...")
    
    inserted_count = 0
    for alert in alerts:
        alert_id = db_manager.insert_alert(alert)
        if alert_id:
            inserted_count += 1
    
    print(f"✓ {inserted_count} alertas inseridos com sucesso!")
    
    # Estatísticas
    print("\n📊 Estatísticas dos alertas gerados:")
    print(f"\n  Por Severidade:")
    for severity in severities:
        count = sum(1 for a in alerts if a["severity"] == severity)
        print(f"    • {severity.upper()}: {count}")
    
    print(f"\n  Por Status:")
    for status in statuses:
        count = sum(1 for a in alerts if a["status"] == status)
        print(f"    • {status.replace('_', ' ').title()}: {count}")
    
    print(f"\n  Por Tipo:")
    for alert_type in types:
        count = sum(1 for a in alerts if a["type"] == alert_type)
        if count > 0:
            print(f"    • {alert_type.replace('_', ' ').title()}: {count}")


if __name__ == "__main__":
    print("=" * 60)
    print("🚨 GERADOR DE ALERTAS DE EXEMPLO")
    print("=" * 60)
    print()
    
    try:
        # Conectar ao banco
        print("Conectando ao MongoDB...")
        db_manager.connect()
        
        # Gerar alertas
        generate_sample_alerts()
        
        print("\n✅ Processo concluído!")
        print("Acesse http://localhost:3000 para visualizar os alertas")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Desconectar
        db_manager.close()
    
    print("\n" + "=" * 60)
