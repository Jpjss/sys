"""
Script de teste de conexão MongoDB
"""

import os
from dotenv import load_dotenv
from database import db_manager

# Carregar variáveis de ambiente
load_dotenv()

def test_connection():
    """Testa conexão e mostra informações do MongoDB"""
    
    print("=" * 60)
    print("🔍 TESTE DE CONEXÃO MONGODB")
    print("=" * 60)
    
    # Mostrar configurações
    print("\n📋 Configurações:")
    print(f"   URI: {os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')}")
    print(f"   Database: {os.getenv('MONGODB_DB', 'alerts_system')}")
    
    # Tentar conectar
    print("\n🔌 Conectando ao MongoDB...")
    if db_manager.connect():
        print("   ✅ Conexão estabelecida com sucesso!")
        
        # Mostrar estatísticas do banco
        print("\n📊 Estatísticas do Banco:")
        
        # Contar documentos em cada coleção
        try:
            alerts_count = db_manager.get_collection('alerts').count_documents({})
            logs_count = db_manager.get_collection('logs').count_documents({})
            
            print(f"   • Alertas: {alerts_count}")
            print(f"   • Logs: {logs_count}")
            
            # Mostrar alguns logs recentes
            if logs_count > 0:
                print("\n📝 Últimos 5 Logs:")
                logs = db_manager.get_logs(limit=5)
                for i, log in enumerate(logs, 1):
                    print(f"   {i}. [{log['level']}] {log['origin']}: {log['message'][:50]}...")
            
            # Mostrar estatísticas de alertas
            print("\n🚨 Estatísticas de Alertas:")
            stats = db_manager.get_alert_stats()
            print(f"   • Alertas Abertos: {stats['openAlerts']}")
            print(f"   • Em Progresso: {stats['inProgress']}")
            print(f"   • Resolvidos Hoje: {stats['resolvedToday']}")
            print(f"   • Total: {stats['total']}")
            
        except Exception as e:
            print(f"   ⚠️  Erro ao buscar estatísticas: {e}")
        
        # Listar todos os bancos de dados
        print("\n🗄️  Bancos de Dados Disponíveis:")
        try:
            dbs = db_manager.client.list_database_names()
            for db_name in dbs:
                print(f"   • {db_name}")
        except Exception as e:
            print(f"   ⚠️  Erro ao listar bancos: {e}")
        
        # Fechar conexão
        db_manager.close()
        print("\n✅ Teste concluído com sucesso!")
        
    else:
        print("   ❌ Falha na conexão!")
        print("\n💡 Dicas:")
        print("   1. Verifique se o MongoDB está rodando: mongod --version")
        print("   2. Verifique a string de conexão no arquivo .env")
        print("   3. Tente conectar manualmente: mongo")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_connection()
