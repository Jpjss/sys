import { Settings, User } from "lucide-react"
import { Button } from "@/components/ui/button"
import { StatsCards } from "@/components/stats-cards"
import { AlertsChart } from "@/components/alerts-chart"
import { AlertsTable } from "@/components/alerts-table"

export function DashboardContent() {
  return (
    <div className="flex flex-col h-screen">
      <header className="bg-card border-b border-border px-8 py-4 flex items-center justify-between">
        <h1 className="text-xl font-semibold text-foreground">Dashboard</h1>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="icon">
            <Settings className="w-5 h-5 text-muted-foreground" />
          </Button>
          <Button variant="ghost" size="icon">
            <User className="w-5 h-5 text-muted-foreground" />
          </Button>
        </div>
      </header>

      <div className="flex-1 overflow-auto p-8 space-y-6">
        <StatsCards />
        <AlertsChart />
        <AlertsTable />
      </div>
    </div>
  )
}
