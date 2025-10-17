"use client"

import { useEffect, useState } from "react"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Spinner } from "@/components/ui/spinner"
import { Terminal, Filter, RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

interface Log {
  _id: string
  timestamp: string
  origin: string
  level: string
  message: string
  metadata?: Record<string, any>
}

export function LogsView() {
  const [logs, setLogs] = useState<Log[]>([])
  const [loading, setLoading] = useState(true)
  const [levelFilter, setLevelFilter] = useState<string>("all")
  const [originFilter, setOriginFilter] = useState<string>("all")

  const fetchLogs = async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      if (levelFilter !== "all") params.set("level", levelFilter)
      if (originFilter !== "all") params.set("origin", originFilter)
      params.set("limit", "1000")

      const response = await fetch(`http://localhost:8000/logs?${params}`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      const data = await response.json()
      
      // A API retorna { success, logs, total } ou pode retornar array direto
      if (Array.isArray(data)) {
        setLogs(data)
      } else if (data.logs && Array.isArray(data.logs)) {
        setLogs(data.logs)
      } else {
        console.error("Formato de dados inesperado:", data)
        setLogs([])
      }
    } catch (error) {
      console.error("Erro ao buscar logs:", error)
      setLogs([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchLogs()
  }, [levelFilter, originFilter])

  const getLevelColor = (level: string) => {
    switch (level.toUpperCase()) {
      case "ERROR":
        return "bg-red-500/10 text-red-500 border-red-500/20"
      case "WARN":
      case "WARNING":
        return "bg-yellow-500/10 text-yellow-500 border-yellow-500/20"
      case "INFO":
        return "bg-blue-500/10 text-blue-500 border-blue-500/20"
      default:
        return "bg-gray-500/10 text-gray-500 border-gray-500/20"
    }
  }

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    })
  }

  return (
    <div className="flex flex-col h-screen">
      <header className="bg-card border-b border-border px-8 py-4">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <Terminal className="w-6 h-6 text-foreground" />
            <div>
              <h1 className="text-2xl font-semibold text-foreground">Logs do Sistema</h1>
              <p className="text-sm text-muted-foreground">
                {logs.length} entrada{logs.length !== 1 ? "s" : ""} de log
              </p>
            </div>
          </div>
          <Button onClick={fetchLogs} variant="outline" size="sm">
            <RefreshCw className="w-4 h-4 mr-2" />
            Atualizar
          </Button>
        </div>

        <div className="flex gap-4">
          <Select value={levelFilter} onValueChange={setLevelFilter}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Nível" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todos os Níveis</SelectItem>
              <SelectItem value="INFO">INFO</SelectItem>
              <SelectItem value="WARN">WARN</SelectItem>
              <SelectItem value="ERROR">ERROR</SelectItem>
            </SelectContent>
          </Select>

          <Select value={originFilter} onValueChange={setOriginFilter}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Origem" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todas as Origens</SelectItem>
              <SelectItem value="API">API</SelectItem>
              <SelectItem value="MainScript">MainScript</SelectItem>
              <SelectItem value="NotificationManager">NotificationManager</SelectItem>
              <SelectItem value="Analyzer">Analyzer</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </header>

      <div className="flex-1 overflow-auto p-8">
        {loading ? (
          <div className="flex items-center justify-center h-full">
            <Spinner className="w-8 h-8" />
          </div>
        ) : logs.length === 0 ? (
          <Card className="p-12 text-center">
            <Terminal className="w-12 h-12 mx-auto mb-4 text-muted-foreground" />
            <h3 className="text-lg font-semibold text-foreground mb-2">
              Nenhum log encontrado
            </h3>
            <p className="text-sm text-muted-foreground">
              Os logs do sistema aparecerão aqui
            </p>
          </Card>
        ) : (
          <Card className="bg-black/95 p-4 font-mono text-sm">
            <div className="space-y-2">
              {logs.map((log) => (
                <div
                  key={log._id}
                  className="flex items-start gap-3 p-3 rounded hover:bg-white/5 transition-colors"
                >
                  <Badge variant="outline" className={getLevelColor(log.level)}>
                    {log.level}
                  </Badge>
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-1">
                      <span className="text-gray-400 text-xs" suppressHydrationWarning>
                        {formatTimestamp(log.timestamp)}
                      </span>
                      <span className="text-cyan-400 text-xs">[{log.origin}]</span>
                    </div>
                    <p className="text-green-400">{log.message}</p>
                    {log.metadata && Object.keys(log.metadata).length > 0 && (
                      <details className="mt-2 text-xs text-gray-500">
                        <summary className="cursor-pointer hover:text-gray-400">
                          Metadados
                        </summary>
                        <pre className="mt-1 ml-4 text-gray-600">
                          {JSON.stringify(log.metadata, null, 2)}
                        </pre>
                      </details>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </Card>
        )}
      </div>
    </div>
  )
}
