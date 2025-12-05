"""
Auto Moderation Module for Far-Bot v2.0.0
Handles welcome/goodbye messages, auto-roles, and server configurations
"""

import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
import discord


class AutoModManager:
    """Manages auto-moderation features like welcome/goodbye messages"""
    
    DEFAULT_CONFIG = {
        "welcome": {
            "enabled": False,
            "channel_id": None,
            "message": "Bienvenido $mention a **$servername**! 🎉",
            "embed": False,
            "embed_color": "#5865F2",
            "embed_title": "Nuevo Miembro!",
            "embed_thumbnail": True,
            "dm_enabled": False,
            "dm_message": "Bienvenido a $servername! Lee las reglas y disfruta tu estancia."
        },
        "goodbye": {
            "enabled": False,
            "channel_id": None,
            "message": "$username ha dejado el servidor. Hasta pronto! 👋",
            "embed": False,
            "embed_color": "#FF6B6B",
            "embed_title": "Usuario se fue"
        },
        "autorole": {
            "enabled": False,
            "role_ids": []
        },
        "logging": {
            "enabled": False,
            "channel_id": None,
            "log_joins": True,
            "log_leaves": True,
            "log_messages": False,
            "log_edits": False,
            "log_deletes": False
        }
    }
    
    WELCOME_TEMPLATES = [
        {
            "id": "simple",
            "name": "Simple",
            "message": "Bienvenido $mention a **$servername**! 🎉"
        },
        {
            "id": "friendly",
            "name": "Amigable",
            "message": "Hey $username! 👋 Bienvenido a **$servername**! Esperamos que la pases genial con nosotros. Somos $membercount miembros!"
        },
        {
            "id": "formal",
            "name": "Formal",
            "message": "Bienvenido/a $mention al servidor **$servername**. Te invitamos a leer las reglas y presentarte en el canal correspondiente."
        },
        {
            "id": "gaming",
            "name": "Gaming",
            "message": "🎮 **$username ha entrado al server!** 🎮\nBienvenido a **$servername**! Eres el miembro #$membercount\nPrepara tu setup y unete a la partida! 🕹️"
        },
        {
            "id": "community",
            "name": "Comunidad",
            "message": "✨ **Nuevo miembro!** ✨\n$mention se ha unido a nuestra comunidad **$servername**!\n\n👥 Ahora somos $membercount miembros\n📜 No olvides leer las reglas\n💬 Presentate en el canal de presentaciones"
        }
    ]
    
    GOODBYE_TEMPLATES = [
        {
            "id": "simple",
            "name": "Simple",
            "message": "$username ha dejado el servidor. Hasta pronto! 👋"
        },
        {
            "id": "sad",
            "name": "Triste",
            "message": "😢 **$username** nos ha dejado... Esperamos verte pronto de nuevo!"
        },
        {
            "id": "neutral",
            "name": "Neutral",
            "message": "**$username** ha salido del servidor."
        },
        {
            "id": "fun",
            "name": "Divertido",
            "message": "🚪 **$username** ha huido del servidor! (Ahora somos $membercount)"
        }
    ]
    
    VARIABLES = {
        "$username": "Nombre del usuario",
        "$mention": "Mencion del usuario",
        "$userid": "ID del usuario",
        "$usertag": "Tag completo (Usuario#1234)",
        "$avatar": "URL del avatar",
        "$servername": "Nombre del servidor",
        "$serverid": "ID del servidor",
        "$membercount": "Cantidad de miembros",
        "$servericon": "URL del icono del servidor",
        "$date": "Fecha actual",
        "$time": "Hora actual"
    }
    
    def __init__(self, data_path: str = "data"):
        self.data_path = data_path
        self.configs_path = os.path.join(data_path, "automod")
        os.makedirs(self.configs_path, exist_ok=True)
    
    def _get_config_file(self, bot_id: str, guild_id: str) -> str:
        """Get config file path for a bot and guild"""
        bot_path = os.path.join(self.configs_path, bot_id)
        os.makedirs(bot_path, exist_ok=True)
        return os.path.join(bot_path, f"{guild_id}.json")
    
    def get_config(self, bot_id: str, guild_id: str) -> Dict[str, Any]:
        """Get automod config for a guild"""
        config_file = self._get_config_file(bot_id, guild_id)
        
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Merge with defaults for any missing keys
                    for key, value in self.DEFAULT_CONFIG.items():
                        if key not in config:
                            config[key] = value
                        elif isinstance(value, dict):
                            for subkey, subvalue in value.items():
                                if subkey not in config[key]:
                                    config[key][subkey] = subvalue
                    return config
            except Exception as e:
                print(f"[AutoMod] Error loading config: {e}")
        
        return self.DEFAULT_CONFIG.copy()
    
    def save_config(self, bot_id: str, guild_id: str, config: Dict[str, Any]) -> bool:
        """Save automod config for a guild"""
        config_file = self._get_config_file(bot_id, guild_id)
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"[AutoMod] Error saving config: {e}")
            return False
    
    def update_config(self, bot_id: str, guild_id: str, section: str, data: Dict[str, Any]) -> bool:
        """Update a specific section of the config"""
        config = self.get_config(bot_id, guild_id)
        
        if section in config:
            config[section].update(data)
        else:
            config[section] = data
        
        return self.save_config(bot_id, guild_id, config)
    
    def get_all_configs(self, bot_id: str) -> Dict[str, Dict[str, Any]]:
        """Get all guild configs for a bot"""
        bot_path = os.path.join(self.configs_path, bot_id)
        configs = {}
        
        if os.path.exists(bot_path):
            for filename in os.listdir(bot_path):
                if filename.endswith('.json'):
                    guild_id = filename[:-5]
                    configs[guild_id] = self.get_config(bot_id, guild_id)
        
        return configs
    
    def process_variables(self, message: str, member: discord.Member, guild: discord.Guild) -> str:
        """Replace variables in message with actual values"""
        replacements = {
            "$username": member.name,
            "$mention": member.mention,
            "$userid": str(member.id),
            "$usertag": str(member),
            "$avatar": str(member.avatar.url if member.avatar else member.default_avatar.url),
            "$servername": guild.name,
            "$serverid": str(guild.id),
            "$membercount": str(guild.member_count),
            "$servericon": str(guild.icon.url if guild.icon else ""),
            "$date": datetime.now().strftime("%Y-%m-%d"),
            "$time": datetime.now().strftime("%H:%M:%S")
        }
        
        result = message
        for var, value in replacements.items():
            result = result.replace(var, value)
        
        return result
    
    async def send_welcome(self, bot_id: str, member: discord.Member) -> bool:
        """Send welcome message for a new member"""
        config = self.get_config(bot_id, str(member.guild.id))
        welcome_config = config.get("welcome", {})
        
        if not welcome_config.get("enabled"):
            return False
        
        channel_id = welcome_config.get("channel_id")
        if not channel_id:
            return False
        
        channel = member.guild.get_channel(int(channel_id))
        if not channel:
            return False
        
        message = self.process_variables(
            welcome_config.get("message", "Bienvenido $mention!"),
            member,
            member.guild
        )
        
        try:
            if welcome_config.get("embed"):
                embed = discord.Embed(
                    title=welcome_config.get("embed_title", "Nuevo Miembro!"),
                    description=message,
                    color=discord.Color.from_str(welcome_config.get("embed_color", "#5865F2"))
                )
                if welcome_config.get("embed_thumbnail"):
                    embed.set_thumbnail(url=member.display_avatar.url)
                embed.set_footer(text=f"ID: {member.id}")
                await channel.send(embed=embed)
            else:
                await channel.send(message)
            
            # Send DM if enabled
            if welcome_config.get("dm_enabled"):
                dm_message = self.process_variables(
                    welcome_config.get("dm_message", "Bienvenido a $servername!"),
                    member,
                    member.guild
                )
                try:
                    await member.send(dm_message)
                except discord.Forbidden:
                    pass
            
            return True
        except Exception as e:
            print(f"[AutoMod] Error sending welcome: {e}")
            return False
    
    async def send_goodbye(self, bot_id: str, member: discord.Member) -> bool:
        """Send goodbye message for a leaving member"""
        config = self.get_config(bot_id, str(member.guild.id))
        goodbye_config = config.get("goodbye", {})
        
        if not goodbye_config.get("enabled"):
            return False
        
        channel_id = goodbye_config.get("channel_id")
        if not channel_id:
            return False
        
        channel = member.guild.get_channel(int(channel_id))
        if not channel:
            return False
        
        message = self.process_variables(
            goodbye_config.get("message", "$username ha dejado el servidor."),
            member,
            member.guild
        )
        
        try:
            if goodbye_config.get("embed"):
                embed = discord.Embed(
                    title=goodbye_config.get("embed_title", "Usuario se fue"),
                    description=message,
                    color=discord.Color.from_str(goodbye_config.get("embed_color", "#FF6B6B"))
                )
                await channel.send(embed=embed)
            else:
                await channel.send(message)
            
            return True
        except Exception as e:
            print(f"[AutoMod] Error sending goodbye: {e}")
            return False
    
    async def apply_autorole(self, bot_id: str, member: discord.Member) -> bool:
        """Apply auto-roles to a new member"""
        config = self.get_config(bot_id, str(member.guild.id))
        autorole_config = config.get("autorole", {})
        
        if not autorole_config.get("enabled"):
            return False
        
        role_ids = autorole_config.get("role_ids", [])
        if not role_ids:
            return False
        
        try:
            roles_to_add = []
            for role_id in role_ids:
                role = member.guild.get_role(int(role_id))
                if role:
                    roles_to_add.append(role)
            
            if roles_to_add:
                await member.add_roles(*roles_to_add, reason="Auto-role by Far-Bot")
                return True
            return False
        except Exception as e:
            print(f"[AutoMod] Error applying autorole: {e}")
            return False
    
    def get_templates(self) -> Dict[str, List[Dict]]:
        """Get all message templates"""
        return {
            "welcome": self.WELCOME_TEMPLATES,
            "goodbye": self.GOODBYE_TEMPLATES
        }
    
    def get_variables(self) -> Dict[str, str]:
        """Get available variables"""
        return self.VARIABLES
