// Far-Bot Frontend Application
const api = {
  // Declare api variable here
  getBots: async () => {
    // Mock implementation
    return {}
  },
  createBot: async (data) => {
    // Mock implementation
  },
  startBot: async (botId) => {
    // Mock implementation
  },
  stopBot: async (botId) => {
    // Mock implementation
  },
  deleteBot: async (botId) => {
    // Mock implementation
  },
  getCommands: async (botId) => {
    // Mock implementation
    return {}
  },
  createCommand: async (botId, data) => {
    // Mock implementation
  },
  deleteCommand: async (botId, cmdId) => {
    // Mock implementation
  },
}

class FarBotApp {
  constructor() {
    this.currentView = "dashboard"
    this.currentBot = null
    this.bots = {}
    this.logs = []
    this.startTime = Date.now()
    this.init()
  }

  init() {
    this.setupEventListeners()
    this.loadData()
    this.startAutoRefresh()
  }

  setupEventListeners() {
    // Navigation
    document.querySelectorAll(".nav-item").forEach((item) => {
      item.addEventListener("click", (e) => {
        e.preventDefault()
        const view = item.dataset.view
        this.switchView(view)
      })
    })

    // Bot Modal
    document.getElementById("addBotBtn")?.addEventListener("click", () => {
      this.showBotModal()
    })

    document.getElementById("closeBotModal")?.addEventListener("click", () => {
      this.hideBotModal()
    })

    document.getElementById("cancelBotBtn")?.addEventListener("click", () => {
      this.hideBotModal()
    })

    document.getElementById("botForm")?.addEventListener("submit", (e) => {
      e.preventDefault()
      this.addBot()
    })

    // Command Modal
    document.getElementById("createCommandBtn")?.addEventListener("click", () => {
      this.showCommandModal()
    })

    document.getElementById("closeCommandModal")?.addEventListener("click", () => {
      this.hideCommandModal()
    })

    document.getElementById("cancelCommandBtn")?.addEventListener("click", () => {
      this.hideCommandModal()
    })

    document.getElementById("commandForm")?.addEventListener("submit", (e) => {
      e.preventDefault()
      this.addCommand()
    })

    // Command type toggle
    document.querySelectorAll('input[name="cmdType"]')?.forEach((radio) => {
      radio.addEventListener("change", () => {
        this.toggleCommandFields()
      })
    })

    // Bot selector
    document.getElementById("commandBotSelect")?.addEventListener("change", (e) => {
      this.currentBot = e.target.value
      this.loadCommands()
    })

    // Refresh
    document.getElementById("refreshBtn")?.addEventListener("click", () => {
      this.loadData()
    })

    // Settings
    document.getElementById("saveSettingsBtn")?.addEventListener("click", () => {
      this.saveSettings()
    })

    // Clear logs
    document.getElementById("clearLogsBtn")?.addEventListener("click", () => {
      this.clearLogs()
    })

    // Close modals on outside click
    document.querySelectorAll(".modal").forEach((modal) => {
      modal.addEventListener("click", (e) => {
        if (e.target === modal) {
          modal.classList.remove("active")
        }
      })
    })
  }

  async loadData() {
    try {
      this.bots = await api.getBots()
      this.updateDashboard()
      this.updateBotsList()
      this.updateCommandBotSelect()
      this.addLog("info", "Data refreshed")
    } catch (error) {
      this.addLog("error", `Failed to load data: ${error.message}`)
    }
  }

  updateDashboard() {
    const activeBots = Object.values(this.bots).filter((b) => b.status === "running").length
    let totalCommands = 0

    for (const bot of Object.values(this.bots)) {
      // Placeholder until we fetch commands
      totalCommands += 0
    }

    document.getElementById("activeBotCount").textContent = activeBots
    document.getElementById("totalCommandCount").textContent = totalCommands

    const uptime = this.formatUptime(Date.now() - this.startTime)
    document.getElementById("uptime").textContent = uptime
  }

  updateBotsList() {
    const list = document.getElementById("botsList")

    if (Object.keys(this.bots).length === 0) {
      list.innerHTML = '<p class="empty-state">No bots added yet. Create your first bot!</p>'
      return
    }

    list.innerHTML = Object.entries(this.bots)
      .map(
        ([botId, bot]) => `
            <div class="bot-card">
                <div class="bot-card-header">
                    <div class="bot-card-title">🤖 ${bot.name}</div>
                    <span class="bot-card-status ${bot.status === "running" ? "running" : "stopped"}">
                        ${bot.status === "running" ? "● Running" : "● Stopped"}
                    </span>
                </div>
                <div class="bot-card-body">
                    <div class="bot-card-info">
                        <div class="bot-card-info-item">
                            <span>Prefix:</span>
                            <strong>${bot.prefix || "!"}</strong>
                        </div>
                        <div class="bot-card-info-item">
                            <span>Status:</span>
                            <strong>${bot.stats?.commands_run || 0} commands run</strong>
                        </div>
                    </div>
                    <div class="bot-card-actions">
                        ${
                          bot.status === "running"
                            ? `<button class="btn-secondary" onclick="app.stopBotAction('${botId}')">Stop</button>`
                            : `<button class="btn-primary" onclick="app.startBotAction('${botId}')">Start</button>`
                        }
                        <button class="btn-secondary" onclick="app.editBot('${botId}')">Edit</button>
                        <button class="btn-danger" onclick="app.deleteBot('${botId}')">Delete</button>
                    </div>
                </div>
            </div>
        `,
      )
      .join("")
  }

  updateCommandBotSelect() {
    const select = document.getElementById("commandBotSelect")
    if (!select) return

    const options = Object.entries(this.bots)
      .map(([id, bot]) => `<option value="${id}">${bot.name}</option>`)
      .join("")

    select.innerHTML = `<option value="">-- Select a Bot --</option>${options}`
  }

  async loadCommands() {
    if (!this.currentBot) {
      document.getElementById("commandsList").innerHTML = '<p class="empty-state">Select a bot to view its commands</p>'
      return
    }

    try {
      const commands = await api.getCommands(this.currentBot)
      const list = document.getElementById("commandsList")

      if (Object.keys(commands).length === 0) {
        list.innerHTML = '<p class="empty-state">No commands yet. Create your first command!</p>'
        return
      }

      list.innerHTML = Object.entries(commands)
        .map(
          ([cmdId, cmd]) => `
                <div class="command-item">
                    <div class="command-item-info">
                        <div class="command-item-name">/${cmd.trigger || cmdId}</div>
                        <div class="command-item-type">${cmd.type === "simple" ? "Simple Response" : "Advanced Python"}</div>
                    </div>
                    <div class="command-item-actions">
                        <button class="btn-secondary" onclick="app.editCommand('${this.currentBot}', '${cmdId}')">Edit</button>
                        <button class="btn-danger" onclick="app.deleteCommand('${this.currentBot}', '${cmdId}')">Delete</button>
                    </div>
                </div>
            `,
        )
        .join("")
    } catch (error) {
      this.addLog("error", `Failed to load commands: ${error.message}`)
    }
  }

  switchView(viewName) {
    document.querySelectorAll(".view").forEach((v) => v.classList.remove("active"))
    document.getElementById(`view-${viewName}`).classList.add("active")

    document.querySelectorAll(".nav-item").forEach((item) => {
      item.classList.remove("active")
      if (item.dataset.view === viewName) {
        item.classList.add("active")
      }
    })

    document.getElementById("pageTitle").textContent = viewName.charAt(0).toUpperCase() + viewName.slice(1)

    this.currentView = viewName
  }

  showBotModal() {
    document.getElementById("botForm").reset()
    document.getElementById("botModal").classList.add("active")
  }

  hideBotModal() {
    document.getElementById("botModal").classList.remove("active")
  }

  async addBot() {
    const data = {
      name: document.getElementById("botName").value,
      token: document.getElementById("botToken").value,
      prefix: document.getElementById("botPrefix").value || "!",
      client_id: document.getElementById("botClientId").value,
      description: document.getElementById("botDescription").value,
    }

    try {
      await api.createBot(data)
      this.addLog("success", `Bot "${data.name}" created successfully`)
      this.hideBotModal()
      this.loadData()
    } catch (error) {
      this.addLog("error", `Failed to create bot: ${error.message}`)
    }
  }

  async startBotAction(botId) {
    try {
      await api.startBot(botId)
      this.addLog("success", `Bot started successfully`)
      this.loadData()
    } catch (error) {
      this.addLog("error", `Failed to start bot: ${error.message}`)
    }
  }

  async stopBotAction(botId) {
    try {
      await api.stopBot(botId)
      this.addLog("success", `Bot stopped successfully`)
      this.loadData()
    } catch (error) {
      this.addLog("error", `Failed to stop bot: ${error.message}`)
    }
  }

  editBot(botId) {
    const bot = this.bots[botId]
    document.getElementById("botName").value = bot.name
    document.getElementById("botToken").value = bot.token
    document.getElementById("botPrefix").value = bot.prefix
    document.getElementById("botClientId").value = bot.client_id || ""
    document.getElementById("botDescription").value = bot.description || ""
    this.showBotModal()
  }

  async deleteBot(botId) {
    if (!confirm("Are you sure you want to delete this bot?")) return

    try {
      await api.deleteBot(botId)
      this.addLog("success", `Bot deleted successfully`)
      this.loadData()
    } catch (error) {
      this.addLog("error", `Failed to delete bot: ${error.message}`)
    }
  }

  showCommandModal() {
    document.getElementById("commandForm").reset()
    document.getElementById("commandModal").classList.add("active")
  }

  hideCommandModal() {
    document.getElementById("commandModal").classList.remove("active")
  }

  toggleCommandFields() {
    const type = document.querySelector('input[name="cmdType"]:checked').value
    document.getElementById("simpleCommandFields").style.display = type === "simple" ? "block" : "none"
    document.getElementById("advancedCommandFields").style.display = type === "advanced" ? "block" : "none"
  }

  async addCommand() {
    if (!this.currentBot) {
      alert("Please select a bot first")
      return
    }

    const type = document.querySelector('input[name="cmdType"]:checked').value
    const data = {
      id: document.getElementById("cmdName").value,
      type: type,
      trigger: document.getElementById("cmdName").value,
    }

    if (type === "simple") {
      data.response = document.getElementById("cmdResponse").value
    } else {
      data.code = document.getElementById("cmdCode").value
    }

    try {
      await api.createCommand(this.currentBot, data)
      this.addLog("success", `Command "${data.id}" created successfully`)
      this.hideCommandModal()
      this.loadCommands()
    } catch (error) {
      this.addLog("error", `Failed to create command: ${error.message}`)
    }
  }

  async deleteCommand(botId, cmdId) {
    if (!confirm("Are you sure you want to delete this command?")) return

    try {
      await api.deleteCommand(botId, cmdId)
      this.addLog("success", `Command deleted successfully`)
      this.loadCommands()
    } catch (error) {
      this.addLog("error", `Failed to delete command: ${error.message}`)
    }
  }

  editCommand(botId, cmdId) {
    // TODO: Implement edit command
    alert("Edit command feature coming soon")
  }

  saveSettings() {
    const prefix = document.getElementById("defaultPrefix").value || "!"
    const theme = document.getElementById("themeSelect").value

    localStorage.setItem("farbot-prefix", prefix)
    localStorage.setItem("farbot-theme", theme)

    this.addLog("success", "Settings saved")
  }

  clearLogs() {
    this.logs = []
    this.renderLogs()
  }

  addLog(level, message) {
    const timestamp = new Date().toLocaleTimeString()
    this.logs.push({ level, message, timestamp })

    // Keep only last 100 logs
    if (this.logs.length > 100) {
      this.logs.shift()
    }

    this.renderLogs()
  }

  renderLogs() {
    const container = document.getElementById("logsDisplay")
    const filter = document.getElementById("logLevelFilter")?.value || ""

    const filtered = filter ? this.logs.filter((log) => log.level === filter) : this.logs

    if (filtered.length === 0) {
      container.innerHTML = '<p class="empty-state">No logs yet</p>'
      return
    }

    container.innerHTML = filtered
      .map(
        (log) =>
          `<div class="log-entry ${log.level}">[${log.timestamp}] [${log.level.toUpperCase()}] ${log.message}</div>`,
      )
      .join("")

    container.scrollTop = container.scrollHeight
  }

  formatUptime(ms) {
    const seconds = Math.floor(ms / 1000) % 60
    const minutes = Math.floor(ms / 60000) % 60
    const hours = Math.floor(ms / 3600000)
    return `${hours}h ${minutes}m ${seconds}s`
  }

  startAutoRefresh() {
    const interval = localStorage.getItem("farbot-refresh-interval") || 10
    setInterval(() => {
      if (this.currentView === "dashboard") {
        this.loadData()
      }
    }, interval * 1000)
  }
}

// Initialize app when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  window.app = new FarBotApp()
  window.app.addLog("success", "Far-Bot panel initialized")
})
