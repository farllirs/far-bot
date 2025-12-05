# Far-Bot v2.0.0 Documentation (English)

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Web Panel](#web-panel)
5. [Command Builder](#command-builder)
6. [AutoMod System](#automod-system)
7. [Slash Commands](#slash-commands)
8. [Variables Reference](#variables-reference)
9. [Advanced Commands](#advanced-commands)
10. [API Reference](#api-reference)
11. [Troubleshooting](#troubleshooting)

---

## Introduction

Far-Bot v2.0.0 is a complete Discord bot management platform. It includes a visual command builder, automatic message system (welcome/goodbye), slash commands support, and much more.

### Repository

- GitHub: [https://github.com/farllirs/farllirs-bots](https://github.com/farllirs/farllirs-bots)

### Key Concepts

- **Bot**: A Discord application that connects to your server
- **Command**: An action triggered by a message (e.g., `!hello`)
- **Trigger**: The word that activates a command
- **Response**: What the bot sends back
- **Variable**: Dynamic placeholders replaced with real data

---

## Installation

### Prerequisites

1. **Python 3.8+**: Download from [python.org](https://python.org)
2. **pip**: Usually included with Python
3. **Discord Bot Token**: Create at [Discord Developer Portal](https://discord.com/developers/applications)

### Step-by-Step Installation

```bash
# 1. Download Far-Bot
git clone https://github.com/farllirs/farllirs-bots.git
cd farllirs-bots

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the installer for first-time setup
python installer.py

# 5. Launch Far-Bot
python launcher.py
```

### Creating a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to "Bot" section and click "Add Bot"
4. Copy the Token (keep it secret!)
5. Enable these Intents:
   - Presence Intent
   - Server Members Intent
   - Message Content Intent
6. Go to OAuth2 > URL Generator
7. Select scopes: `bot`, `applications.commands`
8. Select permissions your bot needs
9. Copy the URL and invite bot to your server

---

## Configuration

### Bot Configuration

Each bot can be configured with:

| Option | Description | Default |
|--------|-------------|---------|
| Token | Your Discord bot token | Required |
| Prefix | Command prefix | `!` |
| Name | Display name in panel | Bot username |
| Auto-start | Start when Far-Bot launches | `false` |

---

## Web Panel

### Dashboard

The main dashboard shows:
- Active bots and their status
- Total commands across all bots
- Server count
- Recent activity

### Bot Management

- **Add Bot**: Click "New Bot" button
- **Start/Stop**: Use the play/stop buttons
- **Edit**: Click on a bot card to modify settings
- **Delete**: Remove a bot and all its commands

### Command Management

- **View Commands**: Click on a bot to see its commands
- **Add Command**: Choose Simple or Advanced mode
- **Edit Command**: Click on a command to modify it
- **Delete Command**: Remove individual commands
- **Import/Export**: Backup and restore commands

---

## Command Builder

### Simple Mode

The Simple Command Builder is perfect for:
- Text responses
- Welcome messages
- Information commands
- FAQ responses

#### Example Simple Commands

**Greeting Command**
```
Trigger: hello
Response: Hello $username! 👋 Welcome to **$servername**!
```

**Server Info**
```
Trigger: serverinfo
Response: 📊 **$servername**
Members: $membercount
Channel: $channel
```

### Advanced Mode

The Advanced Command Builder allows full Python code:

#### Example Advanced Commands

**Dice Roll with Custom Sides**
```python
@bot.command(name='dice')
async def dice_cmd(ctx, sides: int = 6):
    """Roll a dice with custom sides"""
    import random
    if sides < 2:
        await ctx.send("Dice must have at least 2 sides!")
        return
    result = random.randint(1, sides)
    await ctx.send(f"🎲 You rolled a **{result}** (d{sides})")
```

---

## AutoMod System

### Access

Click on "AutoMod" in the sidebar or access `/automod.html`

### Features

1. **Welcome Messages**
   - Message when someone joins
   - Embed option with colors
   - Optional DM message

2. **Goodbye Messages**
   - Message when someone leaves
   - Customizable with variables

3. **Auto-Roles**
   - Automatically assign roles to new members

4. **Activity Logging**
   - Log joins/leaves
   - Log deleted/edited messages

---

## Slash Commands

### Create a Slash Command

In the advanced editor, use this structure:

```python
@bot.tree.command(name='ping', description='Shows latency')
async def ping_slash(interaction: discord.Interaction):
    await interaction.response.send_message(f'Pong! {round(bot.latency * 1000)}ms')
```

### With Parameters

```python
@bot.tree.command(name='avatar', description='Shows user avatar')
@app_commands.describe(user='The user to get avatar from')
async def avatar_slash(interaction: discord.Interaction, user: discord.Member = None):
    user = user or interaction.user
    embed = discord.Embed(title=f'Avatar of {user.display_name}')
    embed.set_image(url=user.display_avatar.url)
    await interaction.response.send_message(embed=embed)
```

### Syncing

Slash commands are automatically synced when the bot starts.

---

## Variables Reference

### User Variables

| Variable | Description | Example Output |
|----------|-------------|----------------|
| `$username` | User's name | `John` |
| `$userid` | User's ID | `123456789012345678` |
| `$mention` | Mentions the user | `@John` |
| `$displayname` | User's display name | `Johnny` |
| `$avatar` | User's avatar URL | `https://cdn.discord...` |

### Server Variables

| Variable | Description | Example Output |
|----------|-------------|----------------|
| `$servername` | Server name | `My Server` |
| `$serverid` | Server ID | `987654321098765432` |
| `$membercount` | Member count | `150` |
| `$servericon` | Server icon URL | `https://cdn.discord...` |

### Bot Variables

| Variable | Description | Example Output |
|----------|-------------|----------------|
| `$botname` | Bot's name | `Far-Bot` |
| `$botid` | Bot's ID | `999888777666555444` |
| `$prefix` | Command prefix | `!` |

### Special Variables

| Variable | Description | Example Output |
|----------|-------------|----------------|
| `$random` | Random 1-100 | `42` |
| `$coin` | Heads/Tails | `Heads` |
| `$8ball` | Magic answer | `Yes` |
| `$time` | Current time | `14:30:45` |
| `$date` | Current date | `2025-12-04` |

---

## Advanced Commands

### Allowed Imports

For security, only these modules are allowed:
- `discord`
- `asyncio`
- `random`
- `datetime`
- `time`
- `math`
- `json`
- `re`
- `typing`
- `collections`

### Decorators

```python
# Basic command
@bot.command(name='cmd')
async def my_cmd(ctx):
    pass

# With aliases
@bot.command(name='cmd', aliases=['c', 'command'])
async def my_cmd(ctx):
    pass

# Require permissions
@bot.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban_cmd(ctx, member: discord.Member):
    pass
```

---

## API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/bots` | List all bots |
| POST | `/api/bots` | Create new bot |
| POST | `/api/bots/{id}/start` | Start bot |
| POST | `/api/bots/{id}/stop` | Stop bot |
| GET | `/api/bots/{id}/commands` | List commands |
| POST | `/api/bots/{id}/commands` | Add command |
| DELETE | `/api/bots/{id}/commands/{cmd}` | Delete command |
| GET | `/api/bots/{id}/automod/{guild}` | Get automod config |
| PUT | `/api/bots/{id}/automod/{guild}` | Update automod config |

---

## Troubleshooting

### Common Issues

**Bot not responding to commands**
- Check if Message Content Intent is enabled
- Verify the prefix is correct
- Ensure the command is enabled

**Slash commands don't appear**
- Wait a few minutes (Discord may take time to sync)
- Restart the bot from the panel
- Verify the bot has the `applications.commands` scope

**"Response is required" error**
- Simple commands MUST have a response
- Don't leave the response field empty

### Getting Help

- GitHub Issues: [https://github.com/farllirs/farllirs-bots/issues](https://github.com/farllirs/farllirs-bots/issues)
