"use client"

import { useEffect, useState } from "react"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Spinner } from "@/components/ui/spinner"
import { CheckCircle2, Clock, User, Calendar } from "lucide-react"

interface Alert {
  id: number
  client_id: string
  client_name: string
  alert_type: string
  severity: "critical" | "high" | "medium" | "low"
  title: string
  description: string
  status: string
  created_at: string
  assigned_to?: string
  resolved_by?: string
  resolved_at?: string
}

export function HistoryView() {
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch("/api/alerts?status=resolved")
        const data = await response.json()
        setAlerts(data.alerts || [])
      } catch (error) {
        console.error("Erro ao buscar histórico:", error)
      } finally {
        setLoading(false)
      }
    }

    fetchHistory()
  }, [])

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "critical":
        return "bg-red-500/10 text-red-500 border-red-500/20"
      case "high":
        return "bg-orange-500/10 text-orange-500 border-orange-500/20"
      case "medium":
        return "bg-yellow-500/10 text-yellow-500 border-yellow-500/20"
      case "low":
        return "bg-blue-500/10 text-blue-500 border-blue-500/20"
      default:
        return "bg-muted text-muted-foreground"
    }
  }

  const calculateResolutionTime = (createdAt: string, resolvedAt: string) => {
    const created = new Date(createdAt).getTime()
    const resolved = new Date(resolvedAt).getTime()
    const diffMinutes = Math.floor((resolved - created) / (1000 * 60))

    if (diffMinutes < 60) {
      return `${diffMinutes} min`
    } else if (diffMinutes < 1440) {
      const hours = Math.floor(diffMinutes / 60)
      const minutes = diffMinutes % 60
      return `${hours}h ${minutes}min`
    } else {
      const days = Math.floor(diffMinutes / 1440)
      return `${days} dia${days > 1 ? 's' : ''}`
    }
  }

  const formatDate = (dateString: string) => {
    const date = new Date(dateString)
    return date.toLocaleDateString("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })
  }

  if (loading) {
    return (
      <div className="flex flex-col h-screen">
        <header className="bg-card border-b border-border px-8 py-4">
          <h1 className="text-2xl font-semibold text-foreground">Histórico</h1>
          <p className="text-sm text-muted-foreground">Alertas resolvidos</p>
        </header>
        <div className="flex-1 flex items-center justify-center">
          <Spinner className="w-8 h-8" />
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-screen">
      <header className="bg-card border-b border-border px-8 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-foreground">Histórico</h1>
            <p className="text-sm text-muted-foreground">
              {alerts.length} alerta{alerts.length !== 1 ? 's' : ''} resolvido{alerts.length !== 1 ? 's' : ''}
            </p>
          </div>
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <CheckCircle2 className="w-4 h-4 text-green-500" />
            <span>Todos resolvidos</span>
          </div>
        </div>
      </header>

      <div className="flex-1 overflow-auto p-8">
        {alerts.length === 0 ? (
          <Card className="p-12 text-center">
            <CheckCircle2 className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
            <h3 className="text-lg font-semibold text-foreground mb-2">
              Nenhum alerta resolvido
            </h3>
            <p className="text-sm text-muted-foreground">
              Os alertas resolvidos aparecerão aqui
            </p>
          </Card>
        ) : (
          <div className="space-y-4">
            {alerts.map((alert) => (
              <Card key={alert.id} className="p-6 hover:shadow-lg transition-shadow">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-lg font-semibold text-foreground">
                        {alert.title}
                      </h3>
                      <Badge variant="outline" className={getSeverityColor(alert.severity)}>
                        {alert.severity === "critical" && "Crítico"}
                        {alert.severity === "high" && "Alto"}
                        {alert.severity === "medium" && "Médio"}
                        {alert.severity === "low" && "Baixo"}
                      </Badge>
                      <Badge variant="outline" className="bg-green-500/10 text-green-500 border-green-500/20">
                        <CheckCircle2 className="w-3 h-3 mr-1" />
                        Resolvido
                      </Badge>
                    </div>
                    <p className="text-sm text-muted-foreground mb-3">
                      {alert.description}
                    </p>
                    <div className="flex items-center gap-4 text-xs text-muted-foreground">
                      <span className="font-medium">{alert.client_name}</span>
                      <span>•</span>
                      <span>{alert.alert_type.replace(/_/g, " ")}</span>
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t border-border">
                  <div className="flex items-center gap-2 text-sm">
                    <Calendar className="w-4 h-4 text-muted-foreground" />
                    <div>
                      <p className="text-xs text-muted-foreground">Criado em</p>
                      <p className="text-foreground">
                        {formatDate(alert.created_at)}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 text-sm">
                    <Clock className="w-4 h-4 text-muted-foreground" />
                    <div>
                      <p className="text-xs text-muted-foreground">Tempo de resolução</p>
                      <p className="text-foreground">
                        {alert.resolved_at
                          ? calculateResolutionTime(alert.created_at, alert.resolved_at)
                          : "N/A"}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 text-sm">
                    <User className="w-4 h-4 text-muted-foreground" />
                    <div>
                      <p className="text-xs text-muted-foreground">Resolvido por</p>
                      <p className="text-foreground">{alert.resolved_by || "N/A"}</p>
                    </div>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
