"use client"

import { useState } from "react"
import { Sidebar } from "@/components/sidebar"
import { DashboardContent } from "@/components/dashboard-content"
import { AlertsView } from "@/components/alerts-view"
import { HistoryView } from "@/components/history-view"
import { SettingsDialog } from "@/components/settings-dialog"

export default function Home() {
  const [activeView, setActiveView] = useState("dashboard")
  const [settingsOpen, setSettingsOpen] = useState(false)

  const handleViewChange = (view: string) => {
    if (view === "settings") {
      setSettingsOpen(true)
    } else {
      setActiveView(view)
    }
  }

  const renderContent = () => {
    switch (activeView) {
      case "dashboard":
        return <DashboardContent />
      case "alerts":
        return <AlertsView />
      case "history":
        return <HistoryView />
      default:
        return <DashboardContent />
    }
  }

  return (
    <div className="flex min-h-screen bg-background">
      <Sidebar activeView={activeView} onViewChange={handleViewChange} />
      <main className="flex-1">
        {renderContent()}
      </main>
      <SettingsDialog open={settingsOpen} onOpenChange={setSettingsOpen} />
    </div>
  )
}
