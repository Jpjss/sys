import { NextResponse } from "next/server"

// Mock data - em produção, conectar ao banco de dados real
const mockAlerts = [
  {
    id: 1,
    client_id: "CLI001",
    client_name: "Empresa ABC Ltda",
    alert_type: "backup_failed",
    severity: "critical",
    title: "Falha no Backup Diário",
    description: "O backup automático falhou às 03:00. Erro: Timeout na conexão com o servidor de backup.",
    status: "open",
    created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    assigned_to: null,
    resolved_by: null,
    resolved_at: null,
  },
  {
    id: 2,
    client_id: "CLI002",
    client_name: "Comércio XYZ",
    alert_type: "stock_zero",
    severity: "high",
    title: "Estoque Zerado - Produto #1234",
    description: 'O produto "Notebook Dell Inspiron 15" está com estoque zerado.',
    status: "open",
    created_at: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(),
    assigned_to: "João Silva",
    resolved_by: null,
    resolved_at: null,
  },
  {
    id: 3,
    client_id: "CLI003",
    client_name: "Indústria Beta",
    alert_type: "nfe_error",
    severity: "critical",
    title: "Erro no Envio de NF-e #45678",
    description: "Falha ao enviar NF-e para SEFAZ. Erro: Certificado digital expirado.",
    status: "in_progress",
    created_at: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
    assigned_to: "Maria Santos",
    resolved_by: null,
    resolved_at: null,
  },
  {
    id: 4,
    client_id: "CLI001",
    client_name: "Empresa ABC Ltda",
    alert_type: "db_connection_error",
    severity: "critical",
    title: "Falha na Conexão com Banco de Dados",
    description: "Não foi possível conectar ao banco de dados principal.",
    status: "resolved",
    created_at: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
    assigned_to: "Admin",
    resolved_by: "Admin",
    resolved_at: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 5,
    client_id: "CLI004",
    client_name: "Loja Virtual Gama",
    alert_type: "high_error_rate",
    severity: "high",
    title: "Taxa de Erro Elevada na API",
    description: "Detectados 127 erros na última hora na API de pagamentos.",
    status: "open",
    created_at: new Date(Date.now() - 15 * 60 * 1000).toISOString(),
    assigned_to: null,
    resolved_by: null,
    resolved_at: null,
  },
  {
    id: 6,
    client_id: "CLI005",
    client_name: "Sistema Delta",
    alert_type: "disk_space_low",
    severity: "medium",
    title: "Espaço em Disco Baixo",
    description: "Servidor com apenas 8% de espaço livre.",
    status: "resolved",
    created_at: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(),
    assigned_to: "Pedro Costa",
    resolved_by: "Pedro Costa",
    resolved_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 7,
    client_id: "CLI002",
    client_name: "Comércio XYZ",
    alert_type: "api_slow",
    severity: "medium",
    title: "API com Resposta Lenta",
    description: "Tempo médio de resposta acima de 3 segundos.",
    status: "resolved",
    created_at: new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString(),
    assigned_to: "Ana Lima",
    resolved_by: "Ana Lima",
    resolved_at: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
  },
]

export async function GET() {
  const now = new Date()
  const startOfToday = new Date(now.getFullYear(), now.getMonth(), now.getDate())

  // Calcular estatísticas
  const openAlerts = mockAlerts.filter((a) => a.status === "open").length
  const inProgress = mockAlerts.filter((a) => a.status === "in_progress").length
  
  // Resolvidos hoje
  const resolvedToday = mockAlerts.filter((a) => {
    if (a.status !== "resolved" || !a.resolved_at) return false
    const resolvedDate = new Date(a.resolved_at)
    return resolvedDate >= startOfToday
  }).length

  // Tempo médio de resolução (em minutos)
  const resolvedAlerts = mockAlerts.filter((a) => a.status === "resolved" && a.resolved_at)
  let avgResponseTime = "N/A"
  
  if (resolvedAlerts.length > 0) {
    const totalMinutes = resolvedAlerts.reduce((sum, alert) => {
      const created = new Date(alert.created_at).getTime()
      const resolved = new Date(alert.resolved_at!).getTime()
      return sum + (resolved - created) / (1000 * 60)
    }, 0)
    
    const avgMinutes = Math.round(totalMinutes / resolvedAlerts.length)
    
    if (avgMinutes < 60) {
      avgResponseTime = `${avgMinutes}min`
    } else {
      const hours = Math.floor(avgMinutes / 60)
      const minutes = avgMinutes % 60
      avgResponseTime = `${hours}h ${minutes}min`
    }
  }

  return NextResponse.json({
    openAlerts,
    inProgress,
    resolvedToday,
    avgResponseTime,
  })
}
