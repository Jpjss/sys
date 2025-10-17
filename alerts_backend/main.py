"""
Script Principal - Coordena verificações e notificações
"""

import sys
import os
from datetime import datetime
import logging

from database import db_manager
from analyzers import get_all_analyzers
from notifiers import NotificationManager

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('alerts_backend.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def run_all_checks():
    """Executa todas as verificações de monitoramento"""
    logger.info("=" * 60)
    logger.info(f"🚀 Iniciando verificações - {datetime.now()}")
    logger.info("=" * 60)
    
    # Conectar ao banco
    if not db_manager.connect():
        logger.error("✗ Falha ao conectar ao banco de dados")
        return
    
    try:
        # Obter todos os analisadores
        analyzers = get_all_analyzers(db_manager)
        notification_manager = NotificationManager(db_manager)
        
        total_alerts = 0
        created_alerts = 0
        
        # Executar cada analisador
        for analyzer in analyzers:
            analyzer_name = analyzer.__class__.__name__
            logger.info(f"\n📊 Executando {analyzer_name}...")
            
            try:
                # Detectar problemas
                detected_alerts = analyzer.analyze()
                total_alerts += len(detected_alerts)
                
                logger.info(f"  ✓ {len(detected_alerts)} alerta(s) detectado(s)")
                
                # Criar alertas no banco e enviar notificações
                for alert_data in detected_alerts:
                    # Inserir no banco
                    alert_id = db_manager.insert_alert(alert_data)
                    
                    if alert_id:
                        created_alerts += 1
                        alert_data['_id'] = alert_id
                        
                        # Enviar notificações
                        logger.info(f"  📧 Enviando notificações...")
                        results = notification_manager.send_alert_notification(
                            alert_data,
                            channels=['email']  # Pode adicionar 'whatsapp' aqui
                        )
                        
                        for channel, success in results.items():
                            status = "✓" if success else "✗"
                            logger.info(f"    {status} {channel}")
                
            except Exception as e:
                logger.error(f"  ✗ Erro no {analyzer_name}: {e}")
        
        # Resumo final
        logger.info("\n" + "=" * 60)
        logger.info(f"📈 RESUMO:")
        logger.info(f"  • Alertas detectados: {total_alerts}")
        logger.info(f"  • Alertas criados: {created_alerts}")
        logger.info(f"  • Timestamp: {datetime.now()}")
        logger.info("=" * 60)
        
        # Registrar execução no log
        db_manager.insert_log({
            'origin': 'MainScript',
            'level': 'INFO',
            'message': f'Verificações concluídas: {created_alerts} alertas criados',
            'metadata': {
                'detected': total_alerts,
                'created': created_alerts
            }
        })
        
    except Exception as e:
        logger.error(f"✗ Erro durante execução: {e}")
        db_manager.insert_log({
            'origin': 'MainScript',
            'level': 'ERROR',
            'message': f'Erro durante verificações: {str(e)}'
        })
    
    finally:
        db_manager.close()


if __name__ == "__main__":
    run_all_checks()
