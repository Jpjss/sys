import { type NextRequest, NextResponse } from "next/server"

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
]

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const status = searchParams.get("status")
  const severity = searchParams.get("severity")
  const search = searchParams.get("search")

  let filtered = [...mockAlerts]

  // Filter by status
  if (status && status !== "all") {
    filtered = filtered.filter((alert) => alert.status === status)
  }

  // Filter by severity
  if (severity && severity !== "all") {
    filtered = filtered.filter((alert) => alert.severity === severity)
  }

  // Filter by search
  if (search) {
    const searchLower = search.toLowerCase()
    filtered = filtered.filter(
      (alert) =>
        alert.title.toLowerCase().includes(searchLower) ||
        alert.client_name.toLowerCase().includes(searchLower) ||
        alert.description.toLowerCase().includes(searchLower),
    )
  }

  return NextResponse.json({
    alerts: filtered,
    total: filtered.length,
  })
}
