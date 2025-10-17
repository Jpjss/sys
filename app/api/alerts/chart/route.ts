import { NextResponse } from "next/server"

// Mock data - em produção, conectar ao banco de dados real
const mockAlerts = [
  {
    id: 1,
    severity: "critical",
    status: "open",
    created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 2,
    severity: "high",
    status: "open",
    created_at: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 3,
    severity: "critical",
    status: "in_progress",
    created_at: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
  },
  {
    id: 4,
    severity: "critical",
    status: "resolved",
    created_at: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 5,
    severity: "high",
    status: "open",
    created_at: new Date(Date.now() - 15 * 60 * 1000).toISOString(),
  },
  {
    id: 6,
    severity: "medium",
    status: "resolved",
    created_at: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 7,
    severity: "medium",
    status: "resolved",
    created_at: new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString(),
  },
  // Alertas dos últimos 7 dias
  {
    id: 8,
    severity: "critical",
    status: "resolved",
    created_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 9,
    severity: "high",
    status: "resolved",
    created_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 10,
    severity: "critical",
    status: "resolved",
    created_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 11,
    severity: "high",
    status: "resolved",
    created_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 12,
    severity: "critical",
    status: "resolved",
    created_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 13,
    severity: "high",
    status: "resolved",
    created_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 14,
    severity: "medium",
    status: "resolved",
    created_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 15,
    severity: "critical",
    status: "resolved",
    created_at: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 16,
    severity: "high",
    status: "resolved",
    created_at: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 17,
    severity: "critical",
    status: "resolved",
    created_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 18,
    severity: "high",
    status: "resolved",
    created_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 19,
    severity: "medium",
    status: "resolved",
    created_at: new Date(Date.now() - 6 * 24 * 60 * 60 * 1000).toISOString(),
  },
]

export async function GET() {
  const now = new Date()
  const last7Days: string[] = []
  
  // Gerar últimos 7 dias
  for (let i = 6; i >= 0; i--) {
    const date = new Date(now)
    date.setDate(date.getDate() - i)
    last7Days.push(date.toLocaleDateString("pt-BR", { weekday: "short" }))
  }

  // Contar alertas por dia e severidade
  const chartData = last7Days.map((day, index) => {
    const daysAgo = 6 - index
    const startOfDay = new Date(now)
    startOfDay.setDate(startOfDay.getDate() - daysAgo)
    startOfDay.setHours(0, 0, 0, 0)
    
    const endOfDay = new Date(startOfDay)
    endOfDay.setHours(23, 59, 59, 999)

    const alertsOnDay = mockAlerts.filter((alert) => {
      const alertDate = new Date(alert.created_at)
      return alertDate >= startOfDay && alertDate <= endOfDay
    })

    const critical = alertsOnDay.filter((a) => a.severity === "critical").length
    const high = alertsOnDay.filter((a) => a.severity === "high").length
    const medium = alertsOnDay.filter((a) => a.severity === "medium").length

    return {
      day: day.charAt(0).toUpperCase() + day.slice(1),
      critical,
      high,
      medium,
      total: critical + high + medium,
    }
  })

  return NextResponse.json({
    data: chartData,
  })
}
