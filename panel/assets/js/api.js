// Far-Bot API Client v2.0.0
class APIClient {
  constructor(baseURL = "") {
    this.baseURL = baseURL || window.location.origin
    this.version = "2.0.0"
  }

  async request(endpoint, options = {}) {
    try {
      const url = endpoint.startsWith("http") ? endpoint : `${this.baseURL}${endpoint}`

      const response = await fetch(url, {
        headers: {
          "Content-Type": "application/json",
          ...options.headers,
        },
        ...options,
      })

      const contentType = response.headers.get("content-type")
      let data

      if (contentType && contentType.includes("application/json")) {
        data = await response.json()
      } else {
        data = await response.text()
      }

      if (!response.ok) {
        const errorMsg = typeof data === "object" ? data.error : data
        throw new Error(errorMsg || `HTTP ${response.status}`)
      }

      return data
    } catch (error) {
      console.error("[Far-Bot API Error]", error)
      throw error
    }
  }

  // ============ BOTS ============
  async getBots() {
    return this.request("/api/bots")
  }

  async getBot(botId) {
    return this.request(`/api/bots/${encodeURIComponent(botId)}`)
  }

  async createBot(botData) {
    return this.request("/api/bots", {
      method: "POST",
      body: JSON.stringify(botData),
    })
  }

  async updateBot(botId, updates) {
    return this.request(`/api/bots/${encodeURIComponent(botId)}`, {
      method: "PUT",
      body: JSON.stringify(updates),
    })
  }

  async deleteBot(botId) {
    return this.request(`/api/bots/${encodeURIComponent(botId)}`, {
      method: "DELETE",
    })
  }

  async startBot(botId, status = "online") {
    return this.request(`/api/bots/${encodeURIComponent(botId)}/start`, {
      method: "POST",
      body: JSON.stringify({ status }),
    })
  }

  async stopBot(botId) {
    return this.request(`/api/bots/${encodeURIComponent(botId)}/stop`, {
      method: "POST",
    })
  }

  async restartBot(botId) {
    return this.request(`/api/bots/${encodeURIComponent(botId)}/restart`, {
      method: "POST",
    })
  }

  // ============ COMMANDS ============
  async getCommands(botId) {
    return this.request(`/api/bots/${encodeURIComponent(botId)}/commands`)
  }

  async addCommand(botId, commandData) {
    return this.request(`/api/bots/${encodeURIComponent(botId)}/commands`, {
      method: "POST",
      body: JSON.stringify(commandData),
    })
  }

  // Alias para mantener compatibilidad
  async createCommand(botId, commandData) {
    return this.addCommand(botId, commandData)
  }

  async updateCommand(botId, commandId, updates) {
    return this.request(`/api/bots/${encodeURIComponent(botId)}/commands/${encodeURIComponent(commandId)}`, {
      method: "PUT",
      body: JSON.stringify(updates),
    })
  }

  async deleteCommand(botId, commandId) {
    return this.request(`/api/bots/${encodeURIComponent(botId)}/commands/${encodeURIComponent(commandId)}`, {
      method: "DELETE",
    })
  }

  async bulkAddCommands(botId, commands) {
    return this.request(`/api/bots/${encodeURIComponent(botId)}/commands/bulk`, {
      method: "POST",
      body: JSON.stringify({ commands }),
    })
  }

  async syncSlashCommands(botId) {
    return this.request(`/api/bots/${encodeURIComponent(botId)}/sync-commands`, {
      method: "POST",
    })
  }

  // ============ STATS ============
  async getStats(botId) {
    return this.request(`/api/bots/${encodeURIComponent(botId)}/stats`)
  }

  // ============ LOGS ============
  async getLogs(botId, limit = 100) {
    return this.request(`/api/bots/${encodeURIComponent(botId)}/logs?limit=${limit}`)
  }

  // ============ HEALTH ============
  async health() {
    return this.request("/api/health")
  }

  async getVersion() {
    return { version: this.version, api: "Far-Bot API" }
  }
}

// Create global API instance
const api = new APIClient()

// Export for module usage
if (typeof module !== "undefined" && module.exports) {
  module.exports = { APIClient, api }
}

