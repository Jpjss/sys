"use client"

import { useState } from "react"
import { Search, Filter } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { AlertList } from "@/components/alert-list"
import { AlertFilters } from "@/components/alert-filters"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

export function AlertsView() {
  const [filters, setFilters] = useState({
    status: "all",
    severity: "all",
    search: "",
  })
  const [showFilters, setShowFilters] = useState(false)

  return (
    <div className="flex flex-col h-screen">
      <header className="bg-card border-b border-border px-8 py-4">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h1 className="text-2xl font-semibold text-foreground">Alertas</h1>
            <p className="text-sm text-muted-foreground">Gerencie todos os alertas do sistema</p>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowFilters(!showFilters)}
          >
            <Filter className="w-4 h-4 mr-2" />
            Filtros
          </Button>
        </div>

        <div className="flex gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              type="search"
              placeholder="Buscar alertas por título, cliente ou descrição..."
              className="pl-9"
              value={filters.search}
              onChange={(e) => setFilters({ ...filters, search: e.target.value })}
            />
          </div>
          <Select
            value={filters.status}
            onValueChange={(value) => setFilters({ ...filters, status: value })}
          >
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todos os Status</SelectItem>
              <SelectItem value="open">Abertos</SelectItem>
              <SelectItem value="in_progress">Em Progresso</SelectItem>
              <SelectItem value="resolved">Resolvidos</SelectItem>
            </SelectContent>
          </Select>
          <Select
            value={filters.severity}
            onValueChange={(value) => setFilters({ ...filters, severity: value })}
          >
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Severidade" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todas as Severidades</SelectItem>
              <SelectItem value="critical">Crítico</SelectItem>
              <SelectItem value="high">Alto</SelectItem>
              <SelectItem value="medium">Médio</SelectItem>
              <SelectItem value="low">Baixo</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {showFilters && (
          <div className="mt-4">
            <AlertFilters filters={filters} onFiltersChange={setFilters} />
          </div>
        )}
      </header>

      <div className="flex-1 overflow-auto p-8">
        <AlertList filters={filters} />
      </div>
    </div>
  )
}
