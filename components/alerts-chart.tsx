"use client"

import { useEffect, useState } from "react"
import { Card } from "@/components/ui/card"
import { ChartContainer } from "@/components/ui/chart"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts"
import { Spinner } from "@/components/ui/spinner"

interface ChartData {
  day: string
  critical: number
  high: number
  medium: number
  total: number
}

const chartConfig = {
  critical: {
    label: "Crítico",
    color: "#ef4444",
  },
  high: {
    label: "Alto",
    color: "#f97316",
  },
  medium: {
    label: "Médio",
    color: "#fbbf24",
  },
}

export function AlertsChart() {
  const [data, setData] = useState<ChartData[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchChartData = async () => {
      try {
        const response = await fetch("/api/alerts/chart")
        const result = await response.json()
        setData(result.data)
      } catch (error) {
        console.error("Erro ao buscar dados do gráfico:", error)
      } finally {
        setLoading(false)
      }
    }

    fetchChartData()
    
    // Atualizar a cada 5 minutos
    const interval = setInterval(fetchChartData, 5 * 60 * 1000)
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return (
      <Card className="p-6 bg-card border border-border">
        <h2 className="text-lg font-semibold text-foreground mb-6">Alertas dos Últimos 7 Dias</h2>
        <div className="flex items-center justify-center h-[200px]">
          <Spinner className="w-8 h-8" />
        </div>
      </Card>
    )
  }

  return (
    <Card className="p-6 bg-card border border-border">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold text-foreground">Alertas dos Últimos 7 Dias</h2>
        <div className="flex gap-4 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-[#ef4444]"></div>
            <span className="text-muted-foreground">Crítico</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-[#f97316]"></div>
            <span className="text-muted-foreground">Alto</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-[#fbbf24]"></div>
            <span className="text-muted-foreground">Médio</span>
          </div>
        </div>
      </div>
      <ChartContainer config={chartConfig} className="h-[300px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
            <XAxis 
              dataKey="day" 
              tick={{ fill: "#6b7280", fontSize: 12 }} 
              stroke="#d1d5db"
            />
            <YAxis 
              tick={{ fill: "#6b7280", fontSize: 12 }} 
              stroke="#d1d5db"
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: "#1f2937", 
                border: "1px solid #374151",
                borderRadius: "8px",
                color: "#fff"
              }}
            />
            <Line 
              type="monotone" 
              dataKey="critical" 
              stroke="#ef4444" 
              strokeWidth={2} 
              dot={{ fill: "#ef4444", r: 4 }}
              activeDot={{ r: 6 }}
            />
            <Line 
              type="monotone" 
              dataKey="high" 
              stroke="#f97316" 
              strokeWidth={2} 
              dot={{ fill: "#f97316", r: 4 }}
              activeDot={{ r: 6 }}
            />
            <Line 
              type="monotone" 
              dataKey="medium" 
              stroke="#fbbf24" 
              strokeWidth={2} 
              dot={{ fill: "#fbbf24", r: 4 }}
              activeDot={{ r: 6 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </ChartContainer>
    </Card>
  )
}
