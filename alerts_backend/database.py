"""
Gerenciador de Conexão com MongoDB
"""

import os
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from typing import Optional, Dict, List, Any
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Gerencia conexões e operações com MongoDB"""
    
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
        self.connection_string = os.getenv(
            'MONGODB_URI', 
            'mongodb://localhost:27017/'
        )
        self.database_name = os.getenv('DB_NAME', 'alerts_system')
        
    def connect(self) -> bool:
        """Estabelece conexão com MongoDB"""
        try:
            self.client = MongoClient(
                self.connection_string,
                serverSelectionTimeoutMS=5000
            )
            # Testa a conexão
            self.client.server_info()
            self.db = self.client[self.database_name]
            logger.info(f"✓ Conectado ao MongoDB: {self.database_name}")
            return True
        except Exception as e:
            logger.error(f"✗ Erro ao conectar MongoDB: {e}")
            return False
    
    def close(self):
        """Fecha conexão com MongoDB"""
        if self.client:
            self.client.close()
            logger.info("✓ Conexão MongoDB fechada")
    
    def get_collection(self, name: str) -> Collection:
        """Retorna uma collection do banco"""
        if self.db is None:
            raise Exception("Banco de dados não conectado")
        return self.db[name]
    
    # ========== ALERTS ==========
    
    def insert_alert(self, alert_data: Dict) -> Optional[str]:
        """Insere novo alerta"""
        try:
            collection = self.get_collection('alerts')
            alert_data['created_at'] = datetime.now()
            alert_data['updated_at'] = datetime.now()
            alert_data['status'] = alert_data.get('status', 'open')
            
            result = collection.insert_one(alert_data)
            logger.info(f"✓ Alerta criado: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"✗ Erro ao inserir alerta: {e}")
            return None
    
    def get_alerts(self, filters: Optional[Dict] = None, 
                   limit: int = 100) -> List[Dict]:
        """Busca alertas com filtros opcionais"""
        try:
            collection = self.get_collection('alerts')
            query = filters or {}
            
            alerts = list(collection.find(query)
                         .sort('created_at', -1)
                         .limit(limit))
            
            # Converter ObjectId para string
            for alert in alerts:
                alert['_id'] = str(alert['_id'])
            
            return alerts
        except Exception as e:
            logger.error(f"✗ Erro ao buscar alertas: {e}")
            return []
    
    def update_alert(self, alert_id: str, update_data: Dict) -> bool:
        """Atualiza um alerta"""
        try:
            from bson.objectid import ObjectId
            collection = self.get_collection('alerts')
            
            update_data['updated_at'] = datetime.now()
            
            result = collection.update_one(
                {'_id': ObjectId(alert_id)},
                {'$set': update_data}
            )
            
            if result.modified_count > 0:
                logger.info(f"✓ Alerta atualizado: {alert_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"✗ Erro ao atualizar alerta: {e}")
            return False
    
    def resolve_alert(self, alert_id: str, resolved_by: str) -> bool:
        """Marca alerta como resolvido"""
        return self.update_alert(alert_id, {
            'status': 'resolved',
            'resolved_by': resolved_by,
            'resolved_at': datetime.now()
        })
    
    def check_duplicate_alert(self, client_id: str, alert_type: str, 
                             hours: int = 1) -> bool:
        """Verifica se já existe alerta similar recente"""
        try:
            from datetime import timedelta
            collection = self.get_collection('alerts')
            
            time_threshold = datetime.now() - timedelta(hours=hours)
            
            existing = collection.find_one({
                'client_id': client_id,
                'alert_type': alert_type,
                'status': {'$in': ['open', 'in_progress']},
                'created_at': {'$gte': time_threshold}
            })
            
            return existing is not None
        except Exception as e:
            logger.error(f"✗ Erro ao verificar duplicata: {e}")
            return False
    
    # ========== LOGS ==========
    
    def insert_log(self, log_data: Dict) -> bool:
        """Insere log no banco"""
        try:
            collection = self.get_collection('logs')
            log_data['timestamp'] = datetime.now()
            collection.insert_one(log_data)
            return True
        except Exception as e:
            logger.error(f"✗ Erro ao inserir log: {e}")
            return False
    
    def get_logs(self, filters: Optional[Dict] = None, 
                 limit: int = 1000) -> List[Dict]:
        """Busca logs do sistema"""
        try:
            collection = self.get_collection('logs')
            query = filters or {}
            
            logs = list(collection.find(query)
                       .sort('timestamp', -1)
                       .limit(limit))
            
            for log in logs:
                log['_id'] = str(log['_id'])
            
            return logs
        except Exception as e:
            logger.error(f"✗ Erro ao buscar logs: {e}")
            return []
    
    # ========== STATS ==========
    
    def get_alert_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas dos alertas"""
        try:
            collection = self.get_collection('alerts')
            
            # Alertas abertos
            open_count = collection.count_documents({'status': 'open'})
            
            # Em progresso
            in_progress = collection.count_documents({'status': 'in_progress'})
            
            # Resolvidos hoje
            from datetime import date
            today_start = datetime.combine(date.today(), datetime.min.time())
            resolved_today = collection.count_documents({
                'status': 'resolved',
                'resolved_at': {'$gte': today_start}
            })
            
            # Tempo médio de resolução
            resolved_alerts = list(collection.find({
                'status': 'resolved',
                'resolved_at': {'$exists': True}
            }).limit(100))
            
            avg_time = "N/A"
            if resolved_alerts:
                total_minutes = sum([
                    (alert['resolved_at'] - alert['created_at']).total_seconds() / 60
                    for alert in resolved_alerts
                ])
                avg_minutes = int(total_minutes / len(resolved_alerts))
                
                if avg_minutes < 60:
                    avg_time = f"{avg_minutes}min"
                else:
                    hours = avg_minutes // 60
                    minutes = avg_minutes % 60
                    avg_time = f"{hours}h {minutes}min"
            
            return {
                'openAlerts': open_count,
                'inProgress': in_progress,
                'resolvedToday': resolved_today,
                'avgResponseTime': avg_time,
                'total': collection.count_documents({})
            }
        except Exception as e:
            logger.error(f"✗ Erro ao calcular estatísticas: {e}")
            return {
                'openAlerts': 0,
                'inProgress': 0,
                'resolvedToday': 0,
                'avgResponseTime': 'N/A',
                'total': 0
            }


# Singleton instance
db_manager = DatabaseManager()
