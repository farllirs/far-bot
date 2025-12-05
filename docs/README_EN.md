<<<<<<< HEAD
# Far-Bot v2.0.0 Documentation (English)
=======
# Far-Bot Documentation (English)
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Web Panel](#web-panel)
5. [Command Builder](#command-builder)
<<<<<<< HEAD
6. [AutoMod System](#automod-system)
7. [Slash Commands](#slash-commands)
8. [Variables Reference](#variables-reference)
9. [Advanced Commands](#advanced-commands)
10. [API Reference](#api-reference)
11. [Troubleshooting](#troubleshooting)
=======
6. [Variables Reference](#variables-reference)
7. [Advanced Commands](#advanced-commands)
8. [API Reference](#api-reference)
9. [Troubleshooting](#troubleshooting)
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c

---

## Introduction

<<<<<<< HEAD
Far-Bot v2.0.0 is a complete Discord bot management platform. It includes a visual command builder, automatic message system (welcome/goodbye), slash commands support, and much more.

### Repository

- GitHub: [https://github.com/farllirs/farllirs-bots](https://github.com/farllirs/farllirs-bots)
=======
Far-Bot is a Discord bot management platform designed to make bot creation accessible to everyone. Whether you're a beginner who wants simple text responses or an advanced developer who needs full Python control, Far-Bot has you covered.
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c

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
<<<<<<< HEAD
git clone https://github.com/farllirs/farllirs-bots.git
cd farllirs-bots
=======
git clone https://github.com/farllirs/far-bot.git
cd far-bot
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Install dependencies
<<<<<<< HEAD
pip install -r requirements.txt
=======
python installer.py
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c

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

<<<<<<< HEAD
=======
### Server Configuration

Edit `config.json` or use the installer:

```json
{
  "host": "0.0.0.0",
  "port": 5000,
  "debug": false,
  "auto_save": true,
  "save_interval": 300
}
```

>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
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

<<<<<<< HEAD
=======
#### Creating a Simple Command

1. Enter the **Trigger** (command name without prefix)
2. Write the **Response** (use variables for dynamic content)
3. Add a **Description** (optional)
4. Click **Save**

>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
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

<<<<<<< HEAD
=======
**Random Response**
```
Trigger: roll
Response: 🎲 $username rolled a $random (1-100)!
```

>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
### Advanced Mode

The Advanced Command Builder allows full Python code:

<<<<<<< HEAD
=======
#### Creating an Advanced Command

1. Write your Python code using the `@bot.command` decorator
2. Use the templates panel for quick starts
3. Validate your code before saving
4. Click **Save**

>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
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

<<<<<<< HEAD
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

=======
**User Info with Embed**
```python
@bot.command(name='whois')
async def whois_cmd(ctx, member: discord.Member = None):
    """Show user information"""
    member = member or ctx.author
    embed = discord.Embed(
        title=f"About {member.name}",
        color=member.color
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Joined", value=member.joined_at.strftime("%Y-%m-%d"))
    embed.add_field(name="Roles", value=len(member.roles))
    await ctx.send(embed=embed)
```

>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
---

## Variables Reference

### User Variables

| Variable | Description | Example Output |
|----------|-------------|----------------|
| `$username` | User's name | `John` |
| `$userid` | User's ID | `123456789012345678` |
| `$mention` | Mentions the user | `@John` |
| `$displayname` | User's display name | `Johnny` |
<<<<<<< HEAD
=======
| `$discriminator` | User's discriminator | `1234` |
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
| `$avatar` | User's avatar URL | `https://cdn.discord...` |

### Server Variables

| Variable | Description | Example Output |
|----------|-------------|----------------|
| `$servername` | Server name | `My Server` |
| `$serverid` | Server ID | `987654321098765432` |
| `$membercount` | Member count | `150` |
| `$servericon` | Server icon URL | `https://cdn.discord...` |

<<<<<<< HEAD
=======
### Channel Variables

| Variable | Description | Example Output |
|----------|-------------|----------------|
| `$channel` | Channel name | `general` |
| `$channelid` | Channel ID | `111222333444555666` |
| `$channelmention` | Channel mention | `#general` |

>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
### Bot Variables

| Variable | Description | Example Output |
|----------|-------------|----------------|
| `$botname` | Bot's name | `Far-Bot` |
| `$botid` | Bot's ID | `999888777666555444` |
<<<<<<< HEAD
| `$prefix` | Command prefix | `!` |

=======
| `$botmention` | Bot mention | `@Far-Bot` |
| `$prefix` | Command prefix | `!` |

### Time Variables

| Variable | Description | Example Output |
|----------|-------------|----------------|
| `$time` | Current time | `14:30:45` |
| `$date` | Current date | `2025-12-04` |
| `$datetime` | Full datetime | `2025-12-04 14:30:45` |
| `$day` | Day name | `Thursday` |
| `$month` | Month name | `December` |
| `$year` | Year | `2025` |

>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
### Special Variables

| Variable | Description | Example Output |
|----------|-------------|----------------|
| `$random` | Random 1-100 | `42` |
<<<<<<< HEAD
| `$coin` | Heads/Tails | `Heads` |
| `$8ball` | Magic answer | `Yes` |
| `$time` | Current time | `14:30:45` |
| `$date` | Current date | `2025-12-04` |
=======
| `$random(min,max)` | Random in range | `$random(1,10)` → `7` |
| `$args` | All arguments | `hello world` |
| `$arg1`, `$arg2`... | Specific argument | `hello` |
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c

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
<<<<<<< HEAD
=======

# Cooldown
@bot.command(name='daily')
@commands.cooldown(1, 86400, commands.BucketType.user)
async def daily_cmd(ctx):
    pass
```

### Error Handling

```python
@bot.command(name='divide')
async def divide_cmd(ctx, a: int, b: int):
    try:
        result = a / b
        await ctx.send(f"Result: {result}")
    except ZeroDivisionError:
        await ctx.send("Cannot divide by zero!")
    except Exception as e:
        await ctx.send(f"Error: {e}")
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
```

---

## API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/bots` | List all bots |
| POST | `/api/bots` | Create new bot |
<<<<<<< HEAD
=======
| GET | `/api/bots/{id}` | Get bot details |
| PUT | `/api/bots/{id}` | Update bot |
| DELETE | `/api/bots/{id}` | Delete bot |
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
| POST | `/api/bots/{id}/start` | Start bot |
| POST | `/api/bots/{id}/stop` | Stop bot |
| GET | `/api/bots/{id}/commands` | List commands |
| POST | `/api/bots/{id}/commands` | Add command |
<<<<<<< HEAD
| DELETE | `/api/bots/{id}/commands/{cmd}` | Delete command |
| GET | `/api/bots/{id}/automod/{guild}` | Get automod config |
| PUT | `/api/bots/{id}/automod/{guild}` | Update automod config |
=======
| PUT | `/api/bots/{id}/commands/{cmd}` | Update command |
| DELETE | `/api/bots/{id}/commands/{cmd}` | Delete command |
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c

---

## Troubleshooting

### Common Issues

**Bot not responding to commands**
- Check if Message Content Intent is enabled
- Verify the prefix is correct
- Ensure the command is enabled

<<<<<<< HEAD
**Slash commands don't appear**
- Wait a few minutes (Discord may take time to sync)
- Restart the bot from the panel
- Verify the bot has the `applications.commands` scope

**"Response is required" error**
- Simple commands MUST have a response
- Don't leave the response field empty

### Getting Help

- GitHub Issues: [https://github.com/farllirs/farllirs-bots/issues](https://github.com/farllirs/farllirs-bots/issues)
=======
**"Token invalid" error**
- Regenerate your bot token
- Make sure there are no extra spaces

**Commands not saving**
- Check file permissions
- Verify the data directory exists

**Panel not loading**
- Check if port 5000 is available
- Try a different browser

### Getting Help

- Check [GitHub Issues](https://github.com/farllirs/far-bot/issues)
- Join our [Discord Server](https://discord.gg/farbot)
- Read the [FAQ](docs/FAQ_EN.md)
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
