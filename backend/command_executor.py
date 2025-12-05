import asyncio
import re
from typing import Dict, Optional, Any
from discord.ext import commands
from discord import app_commands
import discord
from datetime import datetime

VERSION = "2.0.0"

class CommandExecutor:
    """Executes and manages bot commands - v2.0.0"""
    
    def __init__(self):
        self.custom_commands = {}
        self.execution_history = []
    
    async def execute_simple_command(self, ctx, response: str) -> str:
        """Execute a simple command with variable replacement"""
        try:
            result = response
            
            # User variables
            result = result.replace('$username', ctx.author.name)
            result = result.replace('$user', ctx.author.name)
            result = result.replace('$userid', str(ctx.author.id))
            result = result.replace('$mention', ctx.author.mention)
            result = result.replace('$usermention', ctx.author.mention)
            result = result.replace('$discriminator', ctx.author.discriminator)
            result = result.replace('$avatar', str(ctx.author.avatar.url if ctx.author.avatar else ''))
            result = result.replace('$displayname', ctx.author.display_name)
            
            # Server variables
            if ctx.guild:
                result = result.replace('$servername', ctx.guild.name)
                result = result.replace('$server', ctx.guild.name)
                result = result.replace('$serverid', str(ctx.guild.id))
                result = result.replace('$membercount', str(ctx.guild.member_count))
                result = result.replace('$members', str(ctx.guild.member_count))
                result = result.replace('$servericon', str(ctx.guild.icon.url if ctx.guild.icon else ''))
            else:
                result = result.replace('$servername', 'DM')
                result = result.replace('$server', 'DM')
                result = result.replace('$serverid', 'DM')
                result = result.replace('$membercount', '1')
                result = result.replace('$members', '1')
                result = result.replace('$servericon', '')
            
            # Channel variables
            result = result.replace('$channel', ctx.channel.name if hasattr(ctx.channel, 'name') else 'DM')
            result = result.replace('$channelid', str(ctx.channel.id))
            result = result.replace('$channelmention', ctx.channel.mention if hasattr(ctx.channel, 'mention') else 'DM')
            
            # Bot variables
            result = result.replace('$botname', ctx.bot.user.name)
            result = result.replace('$bot', ctx.bot.user.name)
            result = result.replace('$botmention', ctx.bot.user.mention)
            result = result.replace('$botid', str(ctx.bot.user.id))
            result = result.replace('$prefix', ctx.prefix)
            
            # Time variables
            now = datetime.now()
            result = result.replace('$time', now.strftime('%H:%M:%S'))
            result = result.replace('$date', now.strftime('%Y-%m-%d'))
            result = result.replace('$datetime', now.strftime('%Y-%m-%d %H:%M:%S'))
            result = result.replace('$day', now.strftime('%A'))
            result = result.replace('$month', now.strftime('%B'))
            result = result.replace('$year', str(now.year))
            
            # Random number (for fun commands)
            import random
            result = re.sub(r'\$random$$(\d+),(\d+)$$', 
                          lambda m: str(random.randint(int(m.group(1)), int(m.group(2)))), 
                          result)
            result = result.replace('$random', str(random.randint(1, 100)))
            
            # Arguments (if any)
            args = ctx.message.content.split()[1:]  # Skip the command itself
            result = result.replace('$args', ' '.join(args))
            for i, arg in enumerate(args):
                result = result.replace(f'$arg{i+1}', arg)
            
            await ctx.send(result)
            return result
        except Exception as e:
            print(f"[CommandExecutor] Error executing simple command: {e}")
            raise
    
    async def execute_advanced_command(self, bot: commands.Bot, code: str) -> bool:
        """Execute advanced Python command"""
        try:
            # Create execution context
            exec_globals = {
                'bot': bot,
                'commands': commands,
                'discord': discord,
                'asyncio': asyncio,
            }
            
            # Execute the code
            exec(code, exec_globals)
            return True
        except Exception as e:
            print(f"[CommandExecutor] Error executing advanced command: {e}")
            raise
    
    @staticmethod
    def _get_formatted_time() -> str:
        """Get current formatted time"""
        return datetime.now().strftime('%H:%M:%S')
    
    def validate_command_syntax(self, code: str) -> tuple[bool, str]:
        """Validate Python command syntax"""
        try:
            compile(code, '<string>', 'exec')
            return True, "Valid syntax"
        except SyntaxError as e:
            return False, f"Syntax error: {str(e)}"


class CommandBuilder:
    """Builds and registers commands dynamically - v2.0.0"""
    
    def __init__(self, bot: commands.Bot, executor: CommandExecutor):
        self.bot = bot
        self.executor = executor
        self.registered_commands = {}
        self.registered_slash_commands = {}
    
    def build_simple_command(self, trigger: str, response: str) -> bool:
        """Build a simple command"""
        try:
            # Remove existing command if it exists
            if trigger in self.registered_commands:
                self.bot.remove_command(trigger)
            
            # Create the command function
            async def simple_cmd(ctx, response=response):
                await self.executor.execute_simple_command(ctx, response)
            
            # Set function name for discord.py
            simple_cmd.__name__ = trigger
            
            # Create and add the command
            cmd = commands.Command(simple_cmd, name=trigger)
            self.bot.add_command(cmd)
            self.registered_commands[trigger] = cmd
            
            print(f"[CommandBuilder] Simple command '{trigger}' registered successfully")
            return True
        except Exception as e:
            print(f"[CommandBuilder] Error building simple command '{trigger}': {e}")
            return False
    
    def build_advanced_command(self, code: str) -> bool:
        """Build an advanced command from Python code"""
        try:
            # Validate first
            valid, msg = self.executor.validate_command_syntax(code)
            if not valid:
                print(f"[CommandBuilder] Invalid code: {msg}")
                return False
            
            # Execute in bot's context
            exec_globals = {
                'bot': self.bot,
                'commands': commands,
                'discord': discord,
                'asyncio': asyncio,
                'datetime': datetime,
            }
            exec(code, exec_globals)
            print(f"[CommandBuilder] Advanced command registered successfully")
            return True
        except Exception as e:
            print(f"[CommandBuilder] Error building advanced command: {e}")
            return False
    
    def build_slash_command(self, name: str, description: str, code: str) -> bool:
        """Build a slash command from Python code"""
        try:
            # Validate first
            valid, msg = self.executor.validate_command_syntax(code)
            if not valid:
                print(f"[CommandBuilder] Invalid slash code: {msg}")
                return False
            
            # Execute in bot's context
            exec_globals = {
                'bot': self.bot,
                'commands': commands,
                'discord': discord,
                'asyncio': asyncio,
                'datetime': datetime,
                'app_commands': app_commands,
            }
            exec(code, exec_globals)
            
            self.registered_slash_commands[name] = True
            print(f"[CommandBuilder] Slash command '{name}' registered successfully")
            return True
        except Exception as e:
            print(f"[CommandBuilder] Error building slash command '{name}': {e}")
            return False
    
    async def sync_slash_commands(self):
        """Sync slash commands with Discord"""
        try:
            synced = await self.bot.tree.sync()
            print(f"[CommandBuilder] Synced {len(synced)} slash commands")
            return True
        except Exception as e:
            print(f"[CommandBuilder] Error syncing slash commands: {e}")
            return False
    
    def remove_command(self, trigger: str) -> bool:
        """Remove a command"""
        try:
            if trigger in self.registered_commands:
                self.bot.remove_command(trigger)
                del self.registered_commands[trigger]
                print(f"[CommandBuilder] Command '{trigger}' removed")
            return True
        except Exception as e:
            print(f"[CommandBuilder] Error removing command '{trigger}': {e}")
            return False
    
    def clear_commands(self):
        """Clear all registered custom commands"""
        for trigger in list(self.registered_commands.keys()):
            self.remove_command(trigger)


class BotInstance:
    """Wrapper for a Discord bot instance with command management - v2.0.0"""
    
    def __init__(self, bot_id: str, token: str, prefix: str = "!"):
        self.bot_id = bot_id
        self.token = token
        self.prefix = prefix
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.intents.members = True
        self.intents.guilds = True
        self.bot = commands.Bot(command_prefix=prefix, intents=self.intents)
        self.executor = CommandExecutor()
        self.builder = CommandBuilder(self.bot, self.executor)
        self.is_running = False
        self.is_ready = False
        self.last_error = None
        self.guilds_info = []
        self._setup_events()
    
    def _setup_events(self):
        """Setup bot events"""
        @self.bot.event
        async def on_ready():
            print(f"[Bot] {self.bot.user} is ready!")
            self.is_running = True
            self.is_ready = True
            
            # Collect guild info
            self.guilds_info = []
            for guild in self.bot.guilds:
                self.guilds_info.append({
                    'id': str(guild.id),
                    'name': guild.name,
                    'icon': str(guild.icon.url) if guild.icon else None,
                    'member_count': guild.member_count
                })
            
            print(f"[Bot] Connected to {len(self.guilds_info)} servers")
            
            # Sync slash commands
            try:
                await self.builder.sync_slash_commands()
            except Exception as e:
                print(f"[Bot] Error syncing slash commands: {e}")
        
        @self.bot.event
        async def on_command_error(ctx, error):
            error_msg = str(error)
            print(f"[Bot] Command error: {error_msg}")
            self.last_error = error_msg
            
            if isinstance(error, commands.CommandNotFound):
                # Don't send message for unknown commands
                pass
            elif isinstance(error, commands.MissingRequiredArgument):
                await ctx.send(f"Missing argument: {error.param.name}")
            elif isinstance(error, commands.BadArgument):
                await ctx.send(f"Invalid argument: {error}")
            elif isinstance(error, commands.MissingPermissions):
                await ctx.send("You don't have permission to use this command.")
            elif isinstance(error, commands.BotMissingPermissions):
                await ctx.send("I don't have permission to do that.")
            elif isinstance(error, commands.CommandOnCooldown):
                await ctx.send(f"Command on cooldown. Try again in {error.retry_after:.1f}s")
            else:
                try:
                    await ctx.send(f"Error: {error_msg}")
                except:
                    pass
        
        @self.bot.event
        async def on_disconnect():
            print(f"[Bot] {self.bot_id} disconnected")
            self.is_running = False
        
        @self.bot.event
        async def on_resumed():
            print(f"[Bot] {self.bot_id} resumed")
            self.is_running = True
    
    async def start(self) -> bool:
        """Start the bot"""
        try:
            print(f"[BotInstance] Starting bot {self.bot_id}...")
            await self.bot.start(self.token)
            return True
        except discord.LoginFailure as e:
            self.last_error = "Invalid token"
            print(f"[BotInstance] Invalid token for bot {self.bot_id}")
            return False
        except Exception as e:
            self.last_error = str(e)
            print(f"[BotInstance] Failed to start bot {self.bot_id}: {e}")
            return False
    
    async def stop(self) -> bool:
        """Stop the bot"""
        try:
            await self.bot.close()
            self.is_running = False
            self.is_ready = False
            return True
        except Exception as e:
            print(f"[BotInstance] Failed to stop bot {self.bot_id}: {e}")
            return False
    
    def add_command(self, cmd_id: str, cmd_data: Dict[str, Any]) -> bool:
        """Add a command to the bot"""
        try:
            cmd_type = cmd_data.get('type', 'simple')
            trigger = cmd_data.get('trigger', cmd_id)
            
            if not cmd_data.get('enabled', True):
                print(f"[BotInstance] Command {cmd_id} is disabled, skipping")
                return True
            
            if cmd_type == 'simple':
                response = cmd_data.get('response', '')
                if response:
                    return self.builder.build_simple_command(trigger, response)
                else:
                    print(f"[BotInstance] Empty response for command {cmd_id}")
                    return False
            elif cmd_type == 'slash':
                code = cmd_data.get('code', '')
                description = cmd_data.get('description', 'Un comando slash')
                if code:
                    return self.builder.build_slash_command(trigger, description, code)
                else:
                    print(f"[BotInstance] Empty code for slash command {cmd_id}")
                    return False
            else:
                code = cmd_data.get('code', '')
                if code:
                    return self.builder.build_advanced_command(code)
                else:
                    print(f"[BotInstance] Empty code for advanced command {cmd_id}")
                    return False
        except Exception as e:
            print(f"[BotInstance] Error adding command {cmd_id}: {e}")
            return False
    
    def reload_commands(self, commands_data: Dict[str, Any]):
        """Reload all commands"""
        self.builder.clear_commands()
        for cmd_id, cmd_data in commands_data.items():
            self.add_command(cmd_id, cmd_data)
