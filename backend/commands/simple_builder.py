from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
import re
import random


class SimpleCommandBuilder:
    """Build and manage simple response commands with advanced variable handling and variations - v2.0.0"""
    
    TEMPLATES = {
        "greeting": {
            "trigger": "hola",
            "response": "Hola $mention! 👋 Bienvenido a **$servername**!",
            "variations": [
                "Hey $username! 👋 Que bueno verte por aqui!",
                "Hola $mention! 🎉 Bienvenido a **$servername**!",
                "Saludos $username! ✨ Esperamos que disfrutes tu estancia!",
            ],
            "description": "Saluda a los usuarios",
            "category": "basicos"
        },
        "goodbye": {
            "trigger": "adios",
            "response": "Adios $username! 👋 Hasta pronto!",
            "variations": [
                "Nos vemos $username! 👋",
                "Hasta luego $mention! 🌙",
                "Chao $username! Vuelve pronto! ✨",
            ],
            "description": "Despide a los usuarios",
            "category": "basicos"
        },
        "info": {
            "trigger": "info",
            "response": "🤖 **Info del Bot**\n\n• Bot: $botname\n• Servidor: $servername\n• Hora: $time\n• Fecha: $date",
            "description": "Muestra informacion del bot",
            "category": "utilidades"
        },
        "ping": {
            "trigger": "ping",
            "response": "🏓 Pong! El bot esta funcionando correctamente.",
            "variations": [
                "🏓 Pong! Latencia: ~50ms",
                "✅ Bot activo y funcionando!",
            ],
            "description": "Verifica el estado del bot",
            "category": "utilidades"
        },
        "server": {
            "trigger": "servidor",
            "response": "🏠 **$servername**\n\n• Miembros: $membercount\n• Canal: $channel",
            "description": "Info del servidor",
            "category": "informacion"
        },
        "roll": {
            "trigger": "dado",
            "response": "🎲 $username ha tirado el dado y obtuvo: **$random**",
            "variations": [
                "🎲 Resultado del dado: **$random** | Tirado por $mention",
                "🎯 $username saco un **$random** en el dado!",
            ],
            "description": "Tira un dado aleatorio",
            "category": "diversion"
        },
        "coinflip": {
            "trigger": "moneda",
            "response": "🪙 $username lanzo una moneda: **$coin**!",
            "description": "Lanza una moneda",
            "category": "diversion"
        },
        "8ball": {
            "trigger": "8ball",
            "response": "🎱 La bola magica dice: **$8ball**",
            "description": "Pregunta a la bola 8 magica",
            "category": "diversion"
        },
        "joke": {
            "trigger": "chiste",
            "response": "😂 $joke",
            "description": "Cuenta un chiste aleatorio",
            "category": "diversion"
        },
        "hug": {
            "trigger": "abrazo",
            "response": "🤗 $username envia un calido abrazo!",
            "description": "Envia un abrazo virtual",
            "category": "social"
        },
        "help": {
            "trigger": "ayuda",
            "response": "📚 **Comandos Disponibles**\n\n• `$prefix hola` - Saludo\n• `$prefix info` - Info del bot\n• `$prefix ayuda` - Este mensaje",
            "description": "Lista de comandos",
            "category": "basicos"
        },
    }
    
    VARIABLES = {
        "$username": "Nombre del usuario",
        "$user": "Alias de $username",
        "$userid": "ID del usuario",
        "$mention": "Mencion al usuario (@usuario)",
        "$displayname": "Nombre mostrado del usuario",
        "$avatar": "URL del avatar del usuario",
        "$servername": "Nombre del servidor",
        "$server": "Alias de $servername",
        "$serverid": "ID del servidor",
        "$membercount": "Cantidad de miembros",
        "$servericon": "URL del icono del servidor",
        "$channel": "Nombre del canal",
        "$channelid": "ID del canal",
        "$channelmention": "Mencion del canal (#canal)",
        "$botname": "Nombre del bot",
        "$bot": "Alias de $botname",
        "$botid": "ID del bot",
        "$botmention": "Mencion del bot",
        "$prefix": "Prefijo de comandos",
        "$time": "Hora actual (HH:MM:SS)",
        "$date": "Fecha actual (YYYY-MM-DD)",
        "$datetime": "Fecha y hora completa",
        "$random": "Numero aleatorio (1-100)",
        "$coin": "Lanzar moneda (Cara/Cruz)",
        "$8ball": "Respuesta de bola 8 magica",
        "$joke": "Chiste aleatorio",
        "$args": "Todos los argumentos del comando",
        "$arg1": "Primer argumento",
        "$arg2": "Segundo argumento",
    }
    
    EIGHTBALL_RESPONSES = [
        "Si, definitivamente",
        "Sin duda alguna",
        "Probablemente si",
        "Las senales apuntan a si",
        "Si",
        "Pregunta de nuevo mas tarde",
        "Mejor no te lo digo ahora",
        "No puedo predecirlo ahora",
        "Concentrate y pregunta de nuevo",
        "No cuentes con ello",
        "Mi respuesta es no",
        "Mis fuentes dicen que no",
        "Muy dudoso",
    ]
    
    JOKES = [
        "Por que los programadores prefieren el modo oscuro? Porque la luz atrae bugs!",
        "Que le dice un bit al otro? Nos vemos en el bus!",
        "Por que el libro de matematicas esta triste? Porque tiene muchos problemas.",
        "Que hace una abeja en el gimnasio? Zum-ba!",
        "Por que los pajaros no usan Facebook? Porque ya tienen Twitter.",
        "Que hace un pez en el agua? Nada!",
    ]
    
    @staticmethod
    def create_command(trigger: str, response: str, description: str = "", 
                       variations: List[str] = None, use_variations: bool = False) -> Dict[str, Any]:
        """Create a simple command with metadata"""
        if not response or not response.strip():
            response = f"Comando {trigger} ejecutado!"
        
        return {
            "id": trigger.lower().strip(),
            "type": "simple",
            "trigger": trigger.lower().strip(),
            "response": response.strip(),
            "variations": variations or [],
            "use_variations": use_variations,
            "description": description or f"Comando {trigger}",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "enabled": True,
            "usage_count": 0
        }
    
    @staticmethod
    def get_available_variables() -> Dict[str, str]:
        """Get list of available variables"""
        return SimpleCommandBuilder.VARIABLES
    
    @staticmethod
    def get_templates() -> Dict[str, Any]:
        """Get all available templates"""
        return SimpleCommandBuilder.TEMPLATES
    
    @staticmethod
    def get_templates_by_category() -> Dict[str, List[Dict]]:
        """Get templates organized by category"""
        categories = {}
        for key, template in SimpleCommandBuilder.TEMPLATES.items():
            cat = template.get('category', 'otros')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append({
                'id': key,
                **template
            })
        return categories
    
    @staticmethod
    def preview_command(response: str, context: Dict[str, str] = None) -> str:
        """Preview command output with sample data"""
        context = context or {}
        
        defaults = {
            "$username": "Usuario",
            "$user": "Usuario",
            "$userid": "123456789012345678",
            "$mention": "@Usuario",
            "$displayname": "Usuario Cool",
            "$avatar": "https://cdn.discordapp.com/avatars/...",
            "$servername": "Mi Servidor",
            "$server": "Mi Servidor",
            "$serverid": "987654321098765432",
            "$membercount": "150",
            "$servericon": "https://cdn.discordapp.com/icons/...",
            "$channel": "general",
            "$channelid": "111222333444555666",
            "$channelmention": "#general",
            "$botname": "Far-Bot",
            "$bot": "Far-Bot",
            "$botid": "999888777666555444",
            "$botmention": "@Far-Bot",
            "$prefix": "!",
            "$time": datetime.now().strftime("%H:%M:%S"),
            "$date": datetime.now().strftime("%Y-%m-%d"),
            "$datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "$random": str(random.randint(1, 100)),
            "$coin": random.choice(["Cara", "Cruz"]),
            "$8ball": random.choice(SimpleCommandBuilder.EIGHTBALL_RESPONSES),
            "$joke": random.choice(SimpleCommandBuilder.JOKES),
            "$args": "argumento1 argumento2",
            "$arg1": "argumento1",
            "$arg2": "argumento2",
        }
        
        defaults.update(context)
        
        result = response
        for var, value in defaults.items():
            result = result.replace(var, str(value))
        
        return result
    
    @staticmethod
    def process_response(response: str, ctx, variations: List[str] = None, 
                        use_variations: bool = False) -> str:
        """Process response with real context from Discord"""
        try:
            if use_variations and variations:
                all_responses = [response] + variations
                response = random.choice(all_responses)
            
            replacements = {
                "$username": str(ctx.author.name),
                "$user": str(ctx.author.name),
                "$userid": str(ctx.author.id),
                "$mention": ctx.author.mention,
                "$displayname": str(ctx.author.display_name),
                "$avatar": str(ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url),
                "$botname": str(ctx.bot.user.name),
                "$bot": str(ctx.bot.user.name),
                "$botid": str(ctx.bot.user.id),
                "$botmention": ctx.bot.user.mention,
                "$prefix": str(ctx.prefix),
                "$time": datetime.now().strftime("%H:%M:%S"),
                "$date": datetime.now().strftime("%Y-%m-%d"),
                "$datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "$random": str(random.randint(1, 100)),
                "$coin": random.choice(["Cara", "Cruz"]),
                "$8ball": random.choice(SimpleCommandBuilder.EIGHTBALL_RESPONSES),
                "$joke": random.choice(SimpleCommandBuilder.JOKES),
            }
            
            if ctx.guild:
                replacements.update({
                    "$servername": str(ctx.guild.name),
                    "$server": str(ctx.guild.name),
                    "$serverid": str(ctx.guild.id),
                    "$membercount": str(ctx.guild.member_count),
                    "$servericon": str(ctx.guild.icon.url if ctx.guild.icon else ""),
                })
            else:
                replacements.update({
                    "$servername": "DM",
                    "$server": "DM",
                    "$serverid": "0",
                    "$membercount": "1",
                    "$servericon": "",
                })
            
            if hasattr(ctx.channel, 'name'):
                replacements.update({
                    "$channel": str(ctx.channel.name),
                    "$channelid": str(ctx.channel.id),
                    "$channelmention": ctx.channel.mention,
                })
            else:
                replacements.update({
                    "$channel": "DM",
                    "$channelid": str(ctx.channel.id),
                    "$channelmention": "DM",
                })
            
            args = ctx.message.content.split()[1:]
            replacements["$args"] = ' '.join(args)
            for i in range(10):
                replacements[f"$arg{i+1}"] = args[i] if i < len(args) else ""
            
            result = response
            for var, value in replacements.items():
                result = result.replace(var, str(value))
            
            return result
        except Exception as e:
            print(f"[SimpleCommandBuilder] Error processing response: {e}")
            return response
    
    @staticmethod
    def validate_command(trigger: str, response: str) -> Tuple[bool, str]:
        """Validate a simple command"""
        errors = []
        warnings = []
        
        if not trigger or not trigger.strip():
            errors.append("El trigger no puede estar vacio")
        
        if trigger and len(trigger) > 32:
            errors.append("El trigger no puede tener mas de 32 caracteres")
        
        if trigger and not re.match(r'^[a-zA-Z0-9_-]+$', trigger):
            errors.append("El trigger solo puede contener letras, numeros, guiones y guiones bajos")
        
        if not response or not response.strip():
            errors.append("La respuesta no puede estar vacia")
        
        if response and len(response) > 2000:
            errors.append("La respuesta no puede tener mas de 2000 caracteres")
        
        if errors:
            return False, "; ".join(errors)
        
        if warnings:
            return True, "; ".join(warnings)
        
        return True, "Comando valido"
