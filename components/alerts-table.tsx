"use client"

import { useEffect, useState } from "react"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Spinner } from "@/components/ui/spinner"

interface Alert {
  id: number
  client_name: string
  alert_type: string
  status: string
  created_at: string
}

export function AlertsTable() {
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const response = await fetch("/api/alerts")
        const data = await response.json()
        setAlerts(data.alerts || [])
      } catch (error) {
        console.error("Error fetching alerts:", error)
      } finally {
        setLoading(false)
      }
    }

    fetchAlerts()
  }, [])

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case "open":
        return "bg-error/10 text-error border-error/20"
      case "in_progress":
        return "bg-warning/10 text-warning border-warning/20"
      case "resolved":
        return "bg-success/10 text-success border-success/20"
      default:
        return "bg-muted text-muted-foreground"
    }
  }

  const formatTime = (dateString: string) => {
    const date = new Date(dateString)
    const now = new Date()
    const diff = Math.floor((now.getTime() - date.getTime()) / 1000 / 60)

    if (diff < 60) return `${diff} minutes ago`
    if (diff < 1440) return `${Math.floor(diff / 60)} hours ago`
    return `${Math.floor(diff / 1440)} days ago`
  }

  if (loading) {
    return (
      <Card className="p-8 bg-card border border-border">
        <div className="flex items-center justify-center">
          <Spinner className="w-8 h-8" />
        </div>
      </Card>
    )
  }

  return (
    <Card className="bg-card border border-border overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead className="bg-secondary/50 border-b border-border">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                Client
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                Type
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">
                Timestamp
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {alerts.slice(0, 4).map((alert) => (
              <tr key={alert.id} className="hover:bg-secondary/30 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-foreground">{alert.client_name}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">{alert.alert_type}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <Badge variant="outline" className={getStatusColor(alert.status)}>
                    {alert.status === "open" ? "Critical" : alert.status === "in_progress" ? "Unresolved" : "Resolved"}
                  </Badge>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">
                  {formatTime(alert.created_at)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  )
}
