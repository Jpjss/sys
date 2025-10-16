import { AlertDashboard } from "@/components/alert-dashboard"
import { DashboardHeader } from "@/components/dashboard-header"
import { StatsOverview } from "@/components/stats-overview"

export default async function Home() {
  return (
    <div className="min-h-screen bg-background">
      <DashboardHeader />

      <main className="container mx-auto px-4 py-6 space-y-6">
        <StatsOverview />
        <AlertDashboard />
      </main>
    </div>
  )
}
