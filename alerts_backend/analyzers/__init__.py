"""
Analisadores de Logs e Banco de Dados
Detectam problemas específicos
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class BaseAnalyzer:
    """Classe base para todos os analisadores"""
    
    def __init__(self, db_manager):
        self.db = db_manager
        self.alert_type = "unknown"
        self.severity = "medium"
    
    def analyze(self) -> List[Dict]:
        """Método abstrato - deve ser implementado pelas subclasses"""
        raise NotImplementedError("Subclasses devem implementar analyze()")
    
    def create_alert(self, client_id: str, client_name: str, 
                    title: str, description: str, 
                    metadata: Optional[Dict] = None) -> Dict:
        """Cria estrutura de alerta padronizada"""
        return {
            'client_id': client_id,
            'client_name': client_name,
            'alert_type': self.alert_type,
            'severity': self.severity,
            'title': title,
            'description': description,
            'source': self.__class__.__name__,
            'metadata': metadata or {},
            'status': 'open'
        }


class BackupAnalyzer(BaseAnalyzer):
    """Analisa falhas em backups"""
    
    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.alert_type = "backup_failed"
        self.severity = "critical"
    
    def analyze(self) -> List[Dict]:
        """Verifica falhas de backup nas últimas 24h"""
        alerts = []
        
        try:
            # Simular consulta a logs de backup
            # Em produção, isso consultaria logs reais ou tabela de backups
            
            # Exemplo: buscar clientes que não tiveram backup nas últimas 24h
            clients = [
                {'id': 'CLI001', 'name': 'Empresa ABC Ltda'},
                {'id': 'CLI002', 'name': 'Comércio XYZ'},
            ]
            
            for client in clients:
                # Verificar se já existe alerta recente
                if self.db.check_duplicate_alert(client['id'], self.alert_type, hours=24):
                    continue
                
                # Criar alerta de backup falho
                alert = self.create_alert(
                    client_id=client['id'],
                    client_name=client['name'],
                    title=f"Falha no Backup Automático - {client['name']}",
                    description="O backup automático não foi concluído com sucesso nas últimas 24 horas.",
                    metadata={
                        'last_attempt': datetime.now().isoformat(),
                        'error': 'Timeout na conexão com servidor de backup'
                    }
                )
                alerts.append(alert)
                logger.info(f"✓ Alerta de backup criado: {client['name']}")
        
        except Exception as e:
            logger.error(f"✗ Erro no BackupAnalyzer: {e}")
        
        return alerts


class StockAnalyzer(BaseAnalyzer):
    """Analisa produtos com estoque zerado"""
    
    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.alert_type = "stock_zero"
        self.severity = "high"
    
    def analyze(self) -> List[Dict]:
        """Verifica produtos sem estoque"""
        alerts = []
        
        try:
            # Simular consulta a inventário
            # Em produção, consultar banco de dados de estoque real
            
            zero_stock_items = [
                {
                    'client_id': 'CLI002',
                    'client_name': 'Comércio XYZ',
                    'product_id': 'PROD12345',
                    'product_name': 'Notebook Dell Inspiron 15',
                    'sku': 'NB-DELL-I15'
                }
            ]
            
            for item in zero_stock_items:
                if self.db.check_duplicate_alert(item['client_id'], 
                                                 self.alert_type, hours=6):
                    continue
                
                alert = self.create_alert(
                    client_id=item['client_id'],
                    client_name=item['client_name'],
                    title=f"Estoque Zerado - {item['product_name']}",
                    description=f"O produto '{item['product_name']}' (SKU: {item['sku']}) está sem estoque disponível.",
                    metadata={
                        'product_id': item['product_id'],
                        'product_name': item['product_name'],
                        'sku': item['sku']
                    }
                )
                alerts.append(alert)
                logger.info(f"✓ Alerta de estoque criado: {item['product_name']}")
        
        except Exception as e:
            logger.error(f"✗ Erro no StockAnalyzer: {e}")
        
        return alerts


class NFeAnalyzer(BaseAnalyzer):
    """Analisa erros no envio de NF-e"""
    
    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.alert_type = "nfe_error"
        self.severity = "critical"
    
    def analyze(self) -> List[Dict]:
        """Verifica erros em envios de NF-e"""
        alerts = []
        
        try:
            # Simular consulta a logs de NF-e
            nfe_errors = [
                {
                    'client_id': 'CLI003',
                    'client_name': 'Indústria Beta',
                    'nfe_number': '45678',
                    'error_code': '218',
                    'error_message': 'Certificado digital expirado'
                }
            ]
            
            for error in nfe_errors:
                if self.db.check_duplicate_alert(error['client_id'], 
                                                 self.alert_type, hours=2):
                    continue
                
                alert = self.create_alert(
                    client_id=error['client_id'],
                    client_name=error['client_name'],
                    title=f"Erro no Envio de NF-e #{error['nfe_number']}",
                    description=f"Falha ao enviar NF-e para SEFAZ. Código: {error['error_code']} - {error['error_message']}",
                    metadata={
                        'nfe_number': error['nfe_number'],
                        'error_code': error['error_code'],
                        'error_message': error['error_message']
                    }
                )
                alerts.append(alert)
                logger.info(f"✓ Alerta de NF-e criado: {error['nfe_number']}")
        
        except Exception as e:
            logger.error(f"✗ Erro no NFeAnalyzer: {e}")
        
        return alerts


class DatabaseAnalyzer(BaseAnalyzer):
    """Analisa conexões e performance do banco de dados"""
    
    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.alert_type = "db_connection_error"
        self.severity = "critical"
    
    def analyze(self) -> List[Dict]:
        """Verifica problemas de conexão com banco"""
        alerts = []
        
        try:
            # Simular verificação de conexões
            db_issues = [
                {
                    'client_id': 'CLI001',
                    'client_name': 'Empresa ABC Ltda',
                    'error': 'Connection timeout após 30 segundos',
                    'database': 'production_db'
                }
            ]
            
            for issue in db_issues:
                if self.db.check_duplicate_alert(issue['client_id'], 
                                                 self.alert_type, hours=1):
                    continue
                
                alert = self.create_alert(
                    client_id=issue['client_id'],
                    client_name=issue['client_name'],
                    title="Falha na Conexão com Banco de Dados",
                    description=f"Não foi possível conectar ao banco '{issue['database']}'. Erro: {issue['error']}",
                    metadata={
                        'database': issue['database'],
                        'error': issue['error']
                    }
                )
                alerts.append(alert)
                logger.info(f"✓ Alerta de BD criado: {issue['client_name']}")
        
        except Exception as e:
            logger.error(f"✗ Erro no DatabaseAnalyzer: {e}")
        
        return alerts


class ErrorRateAnalyzer(BaseAnalyzer):
    """Analisa taxa de erros em APIs e aplicações"""
    
    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.alert_type = "high_error_rate"
        self.severity = "high"
    
    def analyze(self) -> List[Dict]:
        """Verifica taxas elevadas de erro"""
        alerts = []
        
        try:
            # Simular análise de logs de erro
            high_error_clients = [
                {
                    'client_id': 'CLI004',
                    'client_name': 'Loja Virtual Gama',
                    'error_count': 127,
                    'timeframe': '1 hora',
                    'api_endpoint': '/api/payments'
                }
            ]
            
            for client in high_error_clients:
                if self.db.check_duplicate_alert(client['client_id'], 
                                                 self.alert_type, hours=1):
                    continue
                
                alert = self.create_alert(
                    client_id=client['client_id'],
                    client_name=client['client_name'],
                    title=f"Taxa de Erro Elevada - {client['api_endpoint']}",
                    description=f"Detectados {client['error_count']} erros na última {client['timeframe']} no endpoint {client['api_endpoint']}.",
                    metadata={
                        'error_count': client['error_count'],
                        'timeframe': client['timeframe'],
                        'endpoint': client['api_endpoint']
                    }
                )
                alerts.append(alert)
                logger.info(f"✓ Alerta de erro elevado criado: {client['client_name']}")
        
        except Exception as e:
            logger.error(f"✗ Erro no ErrorRateAnalyzer: {e}")
        
        return alerts


class DiskSpaceAnalyzer(BaseAnalyzer):
    """Analisa espaço em disco"""
    
    def __init__(self, db_manager):
        super().__init__(db_manager)
        self.alert_type = "disk_space_low"
        self.severity = "high"
    
    def analyze(self) -> List[Dict]:
        """Verifica espaço em disco baixo"""
        alerts = []
        
        try:
            low_disk_servers = [
                {
                    'client_id': 'CLI005',
                    'client_name': 'Sistema Delta',
                    'server': 'srv-prod-01',
                    'free_space_percent': 8,
                    'free_space_gb': 45
                }
            ]
            
            for server in low_disk_servers:
                if self.db.check_duplicate_alert(server['client_id'], 
                                                 self.alert_type, hours=6):
                    continue
                
                alert = self.create_alert(
                    client_id=server['client_id'],
                    client_name=server['client_name'],
                    title=f"Espaço em Disco Baixo - {server['server']}",
                    description=f"Servidor '{server['server']}' com apenas {server['free_space_percent']}% de espaço livre ({server['free_space_gb']}GB).",
                    metadata={
                        'server': server['server'],
                        'free_space_percent': server['free_space_percent'],
                        'free_space_gb': server['free_space_gb']
                    }
                )
                alerts.append(alert)
                logger.info(f"✓ Alerta de disco criado: {server['server']}")
        
        except Exception as e:
            logger.error(f"✗ Erro no DiskSpaceAnalyzer: {e}")
        
        return alerts


# Factory para facilitar criação de analisadores
def get_all_analyzers(db_manager) -> List[BaseAnalyzer]:
    """Retorna lista de todos os analisadores"""
    return [
        BackupAnalyzer(db_manager),
        StockAnalyzer(db_manager),
        NFeAnalyzer(db_manager),
        DatabaseAnalyzer(db_manager),
        ErrorRateAnalyzer(db_manager),
        DiskSpaceAnalyzer(db_manager)
    ]
