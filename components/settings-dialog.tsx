"use client"

import { Moon, Sun, Monitor } from "lucide-react"
import { useTheme } from "next-themes"
import { useEffect, useState } from "react"

interface SettingsDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function SettingsDialog({ open, onOpenChange }: SettingsDialogProps) {
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!open) return null

  const themes = [
    { value: "light", label: "Claro", icon: Sun },
    { value: "dark", label: "Escuro", icon: Moon },
    { value: "system", label: "Sistema", icon: Monitor },
  ]

  return (
    <>
      {/* Backdrop */}
      <div className="fixed inset-0 bg-black/50 z-50" onClick={() => onOpenChange(false)} />

      {/* Dialog */}
      <div className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-full max-w-md">
        <div className="bg-card border border-border rounded-lg shadow-lg">
          {/* Header */}
          <div className="px-6 py-4 border-b border-border">
            <h2 className="text-lg font-semibold text-foreground">Configurações</h2>
            <p className="text-sm text-muted-foreground mt-1">Personalize as preferências do seu dashboard</p>
          </div>

          {/* Content */}
          <div className="px-6 py-4">
            <div className="space-y-4">
              <div>
                <label className="text-sm font-medium text-foreground">Tema</label>
                <p className="text-xs text-muted-foreground mt-1 mb-3">Selecione seu tema preferido</p>

                <div className="grid grid-cols-3 gap-3">
                  {themes.map((themeOption) => {
                    const Icon = themeOption.icon
                    const isActive = mounted && theme === themeOption.value

                    return (
                      <button
                        key={themeOption.value}
                        onClick={() => setTheme(themeOption.value)}
                        className={`
                          flex flex-col items-center gap-2 p-4 rounded-lg border-2 transition-all
                          ${isActive ? "border-primary bg-primary/10" : "border-border bg-card hover:bg-secondary"}
                        `}
                      >
                        <Icon className={`w-5 h-5 ${isActive ? "text-primary" : "text-muted-foreground"}`} />
                        <span className={`text-sm font-medium ${isActive ? "text-primary" : "text-foreground"}`}>
                          {themeOption.label}
                        </span>
                      </button>
                    )
                  })}
                </div>
              </div>

              <div className="pt-2">
                <label className="text-sm font-medium text-foreground">Notificações</label>
                <p className="text-xs text-muted-foreground mt-1 mb-3">Configure as notificações de alertas</p>

                <div className="space-y-2">
                  <label className="flex items-center justify-between p-3 rounded-lg border border-border bg-card hover:bg-secondary cursor-pointer transition-colors">
                    <span className="text-sm text-foreground">Notificações por email</span>
                    <input
                      type="checkbox"
                      defaultChecked
                      className="w-4 h-4 rounded border-border text-primary focus:ring-primary"
                    />
                  </label>

                  <label className="flex items-center justify-between p-3 rounded-lg border border-border bg-card hover:bg-secondary cursor-pointer transition-colors">
                    <span className="text-sm text-foreground">Notificações por WhatsApp</span>
                    <input
                      type="checkbox"
                      defaultChecked
                      className="w-4 h-4 rounded border-border text-primary focus:ring-primary"
                    />
                  </label>
                </div>
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="px-6 py-4 border-t border-border flex justify-end gap-3">
            <button
              onClick={() => onOpenChange(false)}
              className="px-4 py-2 text-sm font-medium text-foreground bg-secondary hover:bg-secondary/80 rounded-lg transition-colors"
            >
              Cancelar
            </button>
            <button
              onClick={() => onOpenChange(false)}
              className="px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 rounded-lg transition-colors bg-secondary"
            >
              Salvar Alterações
            </button>
          </div>
        </div>
      </div>
    </>
  )
}
