"use client"

import { useEffect, useState } from "react"
import { AlertCircle, CheckCircle, AlertTriangle, Clock } from "lucide-react"
import { Card } from "@/components/ui/card"
import { Spinner } from "@/components/ui/spinner"

interface Stats {
  openAlerts: number
  inProgress: number
  resolvedToday: number
  avgResponseTime: string
}

export function StatsCards() {
  const [stats, setStats] = useState<Stats | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch("/api/alerts/stats")
        const data = await response.json()
        setStats(data)
      } catch (error) {
        console.error("Erro ao buscar estatísticas:", error)
      } finally {
        setLoading(false)
      }
    }

    fetchStats()
    
    // Atualizar a cada 30 segundos
    const interval = setInterval(fetchStats, 30 * 1000)
    return () => clearInterval(interval)
  }, [])

  if (loading || !stats) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {[1, 2, 3, 4].map((i) => (
          <Card key={i} className="p-6 bg-card border border-border">
            <div className="flex items-center justify-center h-20">
              <Spinner className="w-6 h-6" />
            </div>
          </Card>
        ))}
      </div>
    )
  }

  const cards = [
    {
      label: "Alertas Críticos Abertos",
      value: stats.openAlerts,
      icon: AlertCircle,
      color: "text-error",
      bgColor: "bg-error/10",
      trend: stats.openAlerts > 5 ? "high" : "normal",
    },
    {
      label: "Em Progresso",
      value: stats.inProgress,
      icon: Clock,
      color: "text-warning",
      bgColor: "bg-warning/10",
      trend: "normal",
    },
    {
      label: "Resolvidos Hoje",
      value: stats.resolvedToday,
      icon: CheckCircle,
      color: "text-success",
      bgColor: "bg-success/10",
      trend: "positive",
    },
    {
      label: "Tempo Médio de Resolução",
      value: stats.avgResponseTime,
      icon: AlertTriangle,
      color: "text-primary",
      bgColor: "bg-primary/10",
      trend: "normal",
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card) => (
        <Card key={card.label} className="p-6 bg-card border border-border hover:shadow-lg transition-shadow">
          <div className="flex items-start justify-between">
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">{card.label}</p>
              <p className="text-3xl font-bold text-foreground">{card.value}</p>
              {card.trend === "high" && (
                <p className="text-xs text-error">⚠️ Acima do normal</p>
              )}
              {card.trend === "positive" && card.value > 0 && (
                <p className="text-xs text-success">✓ Bom desempenho</p>
              )}
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
