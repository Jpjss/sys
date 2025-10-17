"""
API REST - FastAPI
Endpoints para o frontend consumir
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging

from database import db_manager
from notifiers import NotificationManager

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar app FastAPI
app = FastAPI(
    title="Sistema de Alertas API",
    description="API para gerenciamento de alertas e monitoramento",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========== MODELS ==========

class AlertUpdate(BaseModel):
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    resolved_by: Optional[str] = None


class AlertCreate(BaseModel):
    client_id: str
    client_name: str
    alert_type: str
    severity: str
    title: str
    description: str
    metadata: Optional[Dict] = None


class ResolveAlert(BaseModel):
    resolved_by: str


# ========== STARTUP/SHUTDOWN ==========

@app.on_event("startup")
async def startup_event():
    """Conecta ao MongoDB na inicialização"""
    if db_manager.connect():
        logger.info("✓ API iniciada e conectada ao MongoDB")
    else:
        logger.error("✗ Falha ao conectar ao MongoDB")


@app.on_event("shutdown")
async def shutdown_event():
    """Fecha conexão ao desligar"""
    db_manager.close()
    logger.info("✓ API desligada")


# ========== ENDPOINTS ==========

@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "online",
        "service": "Alerts System API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/alerts")
async def get_alerts(
    status: Optional[str] = Query(None, description="Filtrar por status"),
    severity: Optional[str] = Query(None, description="Filtrar por severidade"),
    client_id: Optional[str] = Query(None, description="Filtrar por cliente"),
    limit: int = Query(100, ge=1, le=1000, description="Limite de resultados")
):
    """Lista alertas com filtros opcionais"""
    try:
        filters = {}
        
        if status and status != "all":
            filters['status'] = status
        
        if severity and severity != "all":
            filters['severity'] = severity
        
        if client_id:
            filters['client_id'] = client_id
        
        alerts = db_manager.get_alerts(filters, limit)
        
        return {
            "success": True,
            "alerts": alerts,
            "total": len(alerts)
        }
    
    except Exception as e:
        logger.error(f"Erro ao buscar alertas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/alerts/{alert_id}")
async def get_alert(alert_id: str):
    """Retorna um alerta específico"""
    try:
        from bson.objectid import ObjectId
        
        collection = db_manager.get_collection('alerts')
        alert = collection.find_one({'_id': ObjectId(alert_id)})
        
        if not alert:
            raise HTTPException(status_code=404, detail="Alerta não encontrado")
        
        alert['_id'] = str(alert['_id'])
        
        return {
            "success": True,
            "alert": alert
        }
    
    except Exception as e:
        logger.error(f"Erro ao buscar alerta: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/alerts")
async def create_alert(alert: AlertCreate):
    """Cria um novo alerta"""
    try:
        alert_data = alert.dict()
        alert_id = db_manager.insert_alert(alert_data)
        
        if not alert_id:
            raise HTTPException(status_code=500, detail="Falha ao criar alerta")
        
        return {
            "success": True,
            "alert_id": alert_id,
            "message": "Alerta criado com sucesso"
        }
    
    except Exception as e:
        logger.error(f"Erro ao criar alerta: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/alerts/{alert_id}")
async def update_alert(alert_id: str, update: AlertUpdate):
    """Atualiza um alerta"""
    try:
        update_data = {k: v for k, v in update.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum dado para atualizar")
        
        success = db_manager.update_alert(alert_id, update_data)
        
        if not success:
            raise HTTPException(status_code=404, detail="Alerta não encontrado")
        
        return {
            "success": True,
            "message": "Alerta atualizado com sucesso"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar alerta: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/alerts/{alert_id}/resolve")
async def resolve_alert(alert_id: str, data: ResolveAlert):
    """Marca um alerta como resolvido"""
    try:
        success = db_manager.resolve_alert(alert_id, data.resolved_by)
        
        if not success:
            raise HTTPException(status_code=404, detail="Alerta não encontrado")
        
        # Registrar no log
        db_manager.insert_log({
            'origin': 'API',
            'level': 'INFO',
            'message': f'Alerta {alert_id} resolvido por {data.resolved_by}'
        })
        
        return {
            "success": True,
            "message": "Alerta resolvido com sucesso"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao resolver alerta: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/alerts/{alert_id}")
async def delete_alert(alert_id: str):
    """Deleta um alerta"""
    try:
        from bson.objectid import ObjectId
        
        collection = db_manager.get_collection('alerts')
        result = collection.delete_one({'_id': ObjectId(alert_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Alerta não encontrado")
        
        return {
            "success": True,
            "message": "Alerta deletado com sucesso"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao deletar alerta: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def get_stats():
    """Retorna estatísticas dos alertas"""
    try:
        stats = db_manager.get_alert_stats()
        
        return {
            "success": True,
            **stats
        }
    
    except Exception as e:
        logger.error(f"Erro ao buscar estatísticas: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/logs")
async def get_logs(
    level: Optional[str] = Query(None, description="Filtrar por nível"),
    origin: Optional[str] = Query(None, description="Filtrar por origem"),
    limit: int = Query(1000, ge=1, le=5000, description="Limite de resultados")
):
    """Lista logs do sistema"""
    try:
        filters = {}
        
        if level:
            filters['level'] = level.upper()
        
        if origin:
            filters['origin'] = origin
        
        logs = db_manager.get_logs(filters, limit)
        
        return {
            "success": True,
            "logs": logs,
            "total": len(logs)
        }
    
    except Exception as e:
        logger.error(f"Erro ao buscar logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ========== EXECUTAR API ==========

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
