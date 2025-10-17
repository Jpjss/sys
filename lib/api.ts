/**
 * Funções para integração com a API Python
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Alert {
  _id: string
  client_id: string
  client_name: string
  alert_type: string
  severity: string
  title: string
  description: string
  status: string
  created_at: string
  updated_at?: string
  assigned_to?: string
  resolved_by?: string
  resolved_at?: string
  metadata?: Record<string, any>
}

interface ApiResponse<T> {
  success: boolean
  data?: T
  message?: string
  error?: string
}

/**
 * Busca lista de alertas
 */
export async function getAlerts(params?: {
  status?: string
  severity?: string
  client_id?: string
  limit?: number
}): Promise<{ alerts: Alert[]; total: number }> {
  const queryParams = new URLSearchParams()
  
  if (params?.status) queryParams.set('status', params.status)
  if (params?.severity) queryParams.set('severity', params.severity)
  if (params?.client_id) queryParams.set('client_id', params.client_id)
  if (params?.limit) queryParams.set('limit', params.limit.toString())

  const response = await fetch(`${API_BASE_URL}/alerts?${queryParams}`, {
    cache: 'no-store',
  })

  if (!response.ok) {
    throw new Error('Falha ao buscar alertas')
  }

  return response.json()
}

/**
 * Busca um alerta específico
 */
export async function getAlert(alertId: string): Promise<Alert> {
  const response = await fetch(`${API_BASE_URL}/alerts/${alertId}`, {
    cache: 'no-store',
  })

  if (!response.ok) {
    throw new Error('Alerta não encontrado')
  }

  const data = await response.json()
  return data.alert
}

/**
 * Cria novo alerta
 */
export async function createAlert(alertData: Partial<Alert>): Promise<string> {
  const response = await fetch(`${API_BASE_URL}/alerts`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(alertData),
  })

  if (!response.ok) {
    throw new Error('Falha ao criar alerta')
  }

  const data = await response.json()
  return data.alert_id
}

/**
 * Atualiza um alerta
 */
export async function updateAlert(
  alertId: string,
  updates: Partial<Alert>
): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/alerts/${alertId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(updates),
  })

  if (!response.ok) {
    throw new Error('Falha ao atualizar alerta')
  }
}

/**
 * Marca alerta como resolvido
 */
export async function resolveAlert(
  alertId: string,
  resolvedBy: string
): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/alerts/${alertId}/resolve`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ resolved_by: resolvedBy }),
  })

  if (!response.ok) {
    throw new Error('Falha ao resolver alerta')
  }
}

/**
 * Deleta um alerta
 */
export async function deleteAlert(alertId: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/alerts/${alertId}`, {
    method: 'DELETE',
  })

  if (!response.ok) {
    throw new Error('Falha ao deletar alerta')
  }
}

/**
 * Busca estatísticas
 */
export async function getStats(): Promise<{
  openAlerts: number
  inProgress: number
  resolvedToday: number
  avgResponseTime: string
  total: number
}> {
  const response = await fetch(`${API_BASE_URL}/stats`, {
    cache: 'no-store',
  })

  if (!response.ok) {
    throw new Error('Falha ao buscar estatísticas')
  }

  return response.json()
}

/**
 * Busca logs do sistema
 */
export async function getLogs(params?: {
  level?: string
  origin?: string
  limit?: number
}): Promise<{ logs: any[]; total: number }> {
  const queryParams = new URLSearchParams()
  
  if (params?.level) queryParams.set('level', params.level)
  if (params?.origin) queryParams.set('origin', params.origin)
  if (params?.limit) queryParams.set('limit', params.limit.toString())

  const response = await fetch(`${API_BASE_URL}/logs?${queryParams}`, {
    cache: 'no-store',
  })

  if (!response.ok) {
    throw new Error('Falha ao buscar logs')
  }

  return response.json()
}
