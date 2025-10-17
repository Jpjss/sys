import { AlertTriangle, CheckCircle2, Clock, TrendingUp } from "lucide-react"
import { Card } from "@/components/ui/card"

async function getStats() {
  try {
    const response = await fetch("http://localhost:3000/api/alerts/stats", {
      cache: "no-store", // Sempre buscar dados atualizados
    })
    
    if (!response.ok) {
      throw new Error("Falha ao buscar estatísticas")
    }
    
    return await response.json()
  } catch (error) {
    console.error("Erro ao buscar estatísticas:", error)
    // Fallback em caso de erro
    return {
      openAlerts: 0,
      inProgress: 0,
      resolvedToday: 0,
      avgResponseTime: "N/A",
    }
  }
}

export async function StatsOverview() {
  const stats = await getStats()

  const cards = [
    {
      title: "Alertas Abertos",
      value: stats.openAlerts,
      icon: AlertTriangle,
      color: "text-error",
      bgColor: "bg-error/10",
    },
    {
      title: "Em Progresso",
      value: stats.inProgress,
      icon: Clock,
      color: "text-warning",
      bgColor: "bg-warning/10",
    },
    {
      title: "Resolvidos Hoje",
      value: stats.resolvedToday,
      icon: CheckCircle2,
      color: "text-success",
      bgColor: "bg-success/10",
    },
    {
      title: "Tempo Médio",
      value: stats.avgResponseTime,
      icon: TrendingUp,
      color: "text-primary",
      bgColor: "bg-primary/10",
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card) => (
        <Card key={card.title} className="p-6 bg-card border-border">
          <div className="flex items-start justify-between">
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">{card.title}</p>
              <p className="text-3xl font-bold text-foreground">{card.value}</p>
            </div>
            <div className={`p-3 rounded-lg ${card.bgColor}`}>
              <card.icon className={`w-5 h-5 ${card.color}`} />
            </div>
          </div>
        </Card>
      ))}
    </div>
  )
}
