"""
Script para Simular Falhas e Testar o Sistema de Alertas
"""

from database import db_manager
from notifiers import NotificationManager
from datetime import datetime
import time

def simulate_backup_failure():
    """Simula falha crítica de backup"""
    print("\n🔴 Simulando FALHA DE BACKUP CRÍTICA...")
    
    alert = {
        "title": "CRÍTICO: Falha total no sistema de backup",
        "description": "O servidor de backup principal não responde há 48 horas. Todos os backups programados falharam.",
        "severity": "critical",
        "status": "open",
        "type": "backup_failure",
        "source": "BackupAnalyzer",
        "created_at": datetime.now(),
        "details": {
            "last_successful_backup": "2025-01-15 22:00:00",
            "hours_since_backup": 48,
            "backup_server": "srv-backup-01",
            "error_code": "BKP_TIMEOUT_9999",
            "affected_databases": ["production_db", "users_db", "transactions_db"],
            "storage_path": "/mnt/backup/daily",
            "attempted_retries": 12,
            "last_error": "Connection timeout - Server not responding"
        }
    }
    
    alert_id = db_manager.insert_alert(alert)
    if alert_id:
        print(f"   ✅ Alerta criado: {alert_id}")
        
        # Log da falha
        db_manager.insert_log({
            "level": "CRITICAL",
            "message": "Sistema de backup completamente offline - Situação crítica",
            "origin": "BackupAnalyzer",
            "metadata": {
                "alert_id": alert_id,
                "server": "srv-backup-01",
                "downtime_hours": 48
            }
        })
        print("   ✅ Log registrado")
    
    return alert_id


def simulate_stock_critical():
    """Simula produtos com estoque crítico"""
    print("\n🟠 Simulando ESTOQUE CRÍTICO...")
    
    products = [
        {"id": 10523, "name": "Notebook Dell Inspiron 15", "stock": 0, "min": 50},
        {"id": 10891, "name": "Mouse Logitech MX Master", "stock": 3, "min": 100},
        {"id": 11247, "name": "Teclado Mecânico RGB", "stock": 8, "min": 75}
    ]
    
    alert_ids = []
    for product in products:
        severity = "critical" if product["stock"] == 0 else "high"
        
        alert = {
            "title": f"Produto #{product['id']} com estoque {'ZERADO' if product['stock'] == 0 else 'crítico'}",
            "description": f"{product['name']} - Estoque atual: {product['stock']} unidades (mínimo: {product['min']})",
            "severity": severity,
            "status": "open",
            "type": "low_stock",
            "source": "StockAnalyzer",
            "created_at": datetime.now(),
            "details": {
                "product_id": product["id"],
                "product_name": product["name"],
                "current_stock": product["stock"],
                "minimum_stock": product["min"],
                "deficit": product["min"] - product["stock"],
                "warehouse": "CD-Principal",
                "last_entry": "2025-01-10",
                "pending_orders": 45 if product["stock"] < 10 else 0
            }
        }
        
        alert_id = db_manager.insert_alert(alert)
        if alert_id:
            alert_ids.append(alert_id)
            print(f"   ✅ Alerta produto #{product['id']}: {alert_id}")
    
    # Log consolidado
    db_manager.insert_log({
        "level": "ERROR",
        "message": f"Detectados {len(products)} produtos com estoque crítico",
        "origin": "StockAnalyzer",
        "metadata": {
            "products_affected": len(products),
            "alerts_created": len(alert_ids)
        }
    })
    print(f"   ✅ {len(alert_ids)} alertas criados")
    
    return alert_ids


def simulate_database_slow():
    """Simula queries lentas no banco de dados"""
    print("\n🟡 Simulando QUERIES LENTAS...")
    
    alert = {
        "title": "Performance degradada - Queries extremamente lentas",
        "description": "Múltiplas consultas SQL excedendo 5 segundos de tempo de resposta",
        "severity": "high",
        "status": "open",
        "type": "database_slow",
        "source": "DatabaseAnalyzer",
        "created_at": datetime.now(),
        "details": {
            "avg_query_time": "8.5s",
            "slowest_query_time": "15.2s",
            "affected_tables": ["orders", "customers", "products"],
            "slow_queries_count": 127,
            "database": "production_db",
            "server": "db-primary-01",
            "cpu_usage": "92%",
            "memory_usage": "88%",
            "active_connections": 450,
            "max_connections": 500,
            "slowest_query": "SELECT o.*, c.*, p.* FROM orders o JOIN customers c ON..."
        }
    }
    
    alert_id = db_manager.insert_alert(alert)
    if alert_id:
        print(f"   ✅ Alerta criado: {alert_id}")
        
        # Vários logs de queries lentas
        queries = [
            "SELECT * FROM orders WHERE created_at > '2025-01-01' - 12.5s",
            "UPDATE customers SET last_login = NOW() - 8.3s",
            "SELECT COUNT(*) FROM products p JOIN inventory i - 15.2s"
        ]
        
        for query in queries:
            db_manager.insert_log({
                "level": "WARNING",
                "message": f"Query lenta detectada: {query}",
                "origin": "DatabaseAnalyzer",
                "metadata": {
                    "alert_id": alert_id,
                    "query": query.split(' - ')[0],
                    "execution_time": query.split(' - ')[1]
                }
            })
        
        print(f"   ✅ {len(queries)} logs de queries registrados")
    
    return alert_id


def simulate_disk_space_critical():
    """Simula disco cheio"""
    print("\n🔴 Simulando DISCO CHEIO...")
    
    alert = {
        "title": "CRÍTICO: Espaço em disco esgotado - Sistema em risco",
        "description": "Partição principal com 98% de uso. Apenas 2.1GB disponíveis.",
        "severity": "critical",
        "status": "open",
        "type": "disk_space",
        "source": "DiskSpaceAnalyzer",
        "created_at": datetime.now(),
        "details": {
            "disk_path": "C:",
            "disk_usage": 98,
            "total_space": "500GB",
            "used_space": "490GB",
            "free_space": "2.1GB",
            "largest_folders": [
                {"path": "C:\\Logs", "size": "180GB"},
                {"path": "C:\\Temp", "size": "95GB"},
                {"path": "C:\\Database\\Backup", "size": "120GB"}
            ],
            "growth_rate": "2.5GB/dia",
            "estimated_full_in": "1 dia"
        }
    }
    
    alert_id = db_manager.insert_alert(alert)
    if alert_id:
        print(f"   ✅ Alerta criado: {alert_id}")
        
        db_manager.insert_log({
            "level": "CRITICAL",
            "message": "Espaço em disco C: atingiu 98% - Ação imediata necessária",
            "origin": "DiskSpaceAnalyzer",
            "metadata": {
                "alert_id": alert_id,
                "disk": "C:",
                "free_space_gb": 2.1,
                "usage_percent": 98
            }
        })
        print("   ✅ Log registrado")
    
    return alert_id


def simulate_high_error_rate():
    """Simula taxa de erro elevada"""
    print("\n🟠 Simulando ALTA TAXA DE ERROS...")
    
    alert = {
        "title": "Taxa de erros crítica - 15.3% de falhas",
        "description": "Sistema apresentando taxa anormal de erros nas últimas 2 horas",
        "severity": "high",
        "status": "open",
        "type": "high_error_rate",
        "source": "ErrorRateAnalyzer",
        "created_at": datetime.now(),
        "details": {
            "error_rate": 15.3,
            "total_requests": 8540,
            "error_count": 1307,
            "time_window": "2 horas",
            "top_errors": [
                {"code": "500", "count": 487, "message": "Internal Server Error"},
                {"code": "503", "count": 356, "message": "Service Unavailable"},
                {"code": "504", "count": 289, "message": "Gateway Timeout"},
                {"code": "400", "count": 175, "message": "Bad Request"}
            ],
            "affected_endpoints": [
                "/api/orders/create",
                "/api/payments/process",
                "/api/inventory/update"
            ]
        }
    }
    
    alert_id = db_manager.insert_alert(alert)
    if alert_id:
        print(f"   ✅ Alerta criado: {alert_id}")
        
        # Logs de erros específicos
        for error in alert["details"]["top_errors"][:3]:
            db_manager.insert_log({
                "level": "ERROR",
                "message": f"Erro {error['code']}: {error['message']} ({error['count']} ocorrências)",
                "origin": "ErrorRateAnalyzer",
                "metadata": {
                    "alert_id": alert_id,
                    "error_code": error["code"],
                    "count": error["count"]
                }
            })
        
        print("   ✅ Logs de erros registrados")
    
    return alert_id


def simulate_nfe_errors():
    """Simula erros no processamento de NFe"""
    print("\n🟡 Simulando ERROS DE NFe...")
    
    nfes = [45678, 45892, 46103, 46215, 46334]
    alert_ids = []
    
    for nfe in nfes:
        alert = {
            "title": f"Erro ao processar NFe #{nfe}",
            "description": f"Falha no processamento da Nota Fiscal Eletrônica {nfe}",
            "severity": "medium",
            "status": "open",
            "type": "nfe_error",
            "source": "NFeAnalyzer",
            "created_at": datetime.now(),
            "details": {
                "nfe_number": nfe,
                "error_type": "XML_VALIDATION_ERROR",
                "xml_file": f"NFe{nfe}.xml",
                "file_size": f"{156 + (nfe % 100)}KB",
                "validation_errors": [
                    "Campo 'destinatario/IE' inválido",
                    "Valor total divergente",
                    "Assinatura digital ausente"
                ],
                "attempted_at": datetime.now().isoformat(),
                "retry_count": 3,
                "sefaz_status": "Rejeitada"
            }
        }
        
        alert_id = db_manager.insert_alert(alert)
        if alert_id:
            alert_ids.append(alert_id)
    
    print(f"   ✅ {len(alert_ids)} alertas de NFe criados")
    
    db_manager.insert_log({
        "level": "WARNING",
        "message": f"Lote de {len(nfes)} NFes rejeitadas pela SEFAZ",
        "origin": "NFeAnalyzer",
        "metadata": {
            "nfes_affected": len(nfes),
            "alerts_created": len(alert_ids)
        }
    })
    
    return alert_ids


def send_notifications(alert_ids):
    """Envia notificações para os alertas criados"""
    print("\n📧 Enviando notificações...")
    
    try:
        notifier = NotificationManager()
        
        # Buscar alertas do banco
        alerts = []
        for alert_id in alert_ids[:3]:  # Enviar apenas os 3 primeiros para teste
            alert = db_manager.get_alert_by_id(alert_id)
            if alert:
                alerts.append(alert)
        
        if alerts:
            # Tentar enviar (vai falhar se SMTP não configurado, mas é esperado)
            try:
                notifier.send_alert_notification(alerts[0])
                print("   ✅ Notificação enviada (se SMTP configurado)")
            except Exception as e:
                print(f"   ⚠️  Notificação não enviada: {e}")
                print("   💡 Configure SMTP no .env para enviar emails reais")
        
    except Exception as e:
        print(f"   ⚠️  Erro ao enviar notificações: {e}")


def main():
    """Executa simulação completa de falhas"""
    
    print("=" * 70)
    print("🧪 SIMULADOR DE FALHAS - SISTEMA DE ALERTAS")
    print("=" * 70)
    
    try:
        # Conectar ao banco
        print("\n🔌 Conectando ao MongoDB...")
        db_manager.connect()
        print("   ✅ Conectado")
        
        all_alert_ids = []
        
        # Simular todas as falhas
        all_alert_ids.append(simulate_backup_failure())
        all_alert_ids.extend(simulate_stock_critical())
        all_alert_ids.append(simulate_database_slow())
        all_alert_ids.append(simulate_disk_space_critical())
        all_alert_ids.append(simulate_high_error_rate())
        all_alert_ids.extend(simulate_nfe_errors())
        
        # Filtrar None
        all_alert_ids = [aid for aid in all_alert_ids if aid]
        
        print("\n" + "=" * 70)
        print(f"✅ SIMULAÇÃO CONCLUÍDA!")
        print(f"   📊 Total de alertas criados: {len(all_alert_ids)}")
        print(f"   🔴 Críticos: {2}")
        print(f"   🟠 High: {4}")
        print(f"   🟡 Medium: {5}")
        print("=" * 70)
        
        # Enviar notificações
        send_notifications(all_alert_ids)
        
        print("\n🌐 Acesse o Dashboard:")
        print("   👉 http://localhost:3000")
        print("\n💡 Dicas:")
        print("   • Vá para a aba 'Alerts' para ver todos os alertas")
        print("   • Vá para 'Logs' para ver os logs gerados")
        print("   • Dashboard mostrará as estatísticas atualizadas")
        print("   • Use os filtros para encontrar alertas específicos")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        db_manager.close()
        print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
