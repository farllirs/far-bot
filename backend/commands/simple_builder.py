from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
import re
import random


class SimpleCommandBuilder:
<<<<<<< HEAD
    """Build and manage simple response commands with advanced variable handling and variations - v2.0.0"""
=======
    """Build and manage simple response commands with advanced variable handling and variations"""
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
    
    TEMPLATES = {
        "greeting": {
            "trigger": "hola",
            "response": "Hola $mention! 👋 Bienvenido a **$servername**!",
            "variations": [
                "Hey $username! 👋 Que bueno verte por aqui!",
                "Hola $mention! 🎉 Bienvenido a **$servername**!",
                "Saludos $username! ✨ Esperamos que disfrutes tu estancia!",
<<<<<<< HEAD
            ],
            "description": "Saluda a los usuarios",
=======
                "Bienvenido $mention! 🌟 Gracias por unirte a **$servername**!",
            ],
            "description": "Saluda a los usuarios con variaciones",
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
            "category": "basicos"
        },
        "goodbye": {
            "trigger": "adios",
            "response": "Adios $username! 👋 Hasta pronto!",
            "variations": [
                "Nos vemos $username! 👋",
                "Hasta luego $mention! 🌙",
                "Chao $username! Vuelve pronto! ✨",
<<<<<<< HEAD
=======
                "Adios $mention! Que te vaya bien! 🍀",
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
            ],
            "description": "Despide a los usuarios",
            "category": "basicos"
        },
        "info": {
            "trigger": "info",
            "response": "🤖 **Info del Bot**\n\n• Bot: $botname\n• Servidor: $servername\n• Hora: $time\n• Fecha: $date",
<<<<<<< HEAD
            "description": "Muestra informacion del bot",
            "category": "utilidades"
        },
=======
            "variations": [
                "📊 **Informacion**\n• Bot: $botname\n• Server: $servername\n• Miembros: $membercount",
                "ℹ️ **$botname**\n• Servidor: $servername\n• Canal: $channel\n• Fecha: $date",
            ],
            "description": "Muestra informacion del bot",
            "category": "utilidades"
        },
        "rules": {
            "trigger": "reglas",
            "response": "📜 **Reglas del Servidor**\n\n$mention, por favor respeta las reglas:\n\n1. Respeta a todos\n2. No spam\n3. Diviertete!",
            "variations": [
                "📋 **Normas de $servername**\n\n• Se respetuoso\n• No hagas spam\n• Pasa un buen rato!",
            ],
            "description": "Muestra las reglas",
            "category": "moderacion"
        },
        "help": {
            "trigger": "ayuda",
            "response": "📚 **Comandos Disponibles**\n\n• `$prefix hola` - Saludo\n• `$prefix info` - Info del bot\n• `$prefix ayuda` - Este mensaje",
            "variations": [
                "🆘 **Centro de Ayuda**\n\nUsa `$prefix comandos` para ver todos los comandos disponibles.",
            ],
            "description": "Lista de comandos",
            "category": "basicos"
        },
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
        "ping": {
            "trigger": "ping",
            "response": "🏓 Pong! El bot esta funcionando correctamente.",
            "variations": [
                "🏓 Pong! Latencia: ~50ms",
                "✅ Bot activo y funcionando!",
<<<<<<< HEAD
=======
                "🟢 Online! Todo operativo.",
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
            ],
            "description": "Verifica el estado del bot",
            "category": "utilidades"
        },
        "server": {
            "trigger": "servidor",
            "response": "🏠 **$servername**\n\n• Miembros: $membercount\n• Canal: $channel",
<<<<<<< HEAD
            "description": "Info del servidor",
            "category": "informacion"
        },
=======
            "variations": [
                "📊 **Info de $servername**\n\n👥 Miembros: $membercount\n📝 Canal actual: $channel",
                "🌐 **$servername**\nGracias por ser parte de nuestra comunidad, $username!",
            ],
            "description": "Info del servidor",
            "category": "informacion"
        },
        "user": {
            "trigger": "usuario",
            "response": "👤 **$displayname**\n\n• ID: $userid\n• Mencion: $mention",
            "variations": [
                "📋 **Perfil de $username**\n• ID: `$userid`\n• Display: $displayname",
            ],
            "description": "Info del usuario",
            "category": "informacion"
        },
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
        "roll": {
            "trigger": "dado",
            "response": "🎲 $username ha tirado el dado y obtuvo: **$random**",
            "variations": [
                "🎲 Resultado del dado: **$random** | Tirado por $mention",
                "🎯 $username saco un **$random** en el dado!",
<<<<<<< HEAD
=======
                "✨ El dado magico dice: **$random** para $username!",
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
            ],
            "description": "Tira un dado aleatorio",
            "category": "diversion"
        },
        "coinflip": {
            "trigger": "moneda",
            "response": "🪙 $username lanzo una moneda: **$coin**!",
<<<<<<< HEAD
            "description": "Lanza una moneda",
            "category": "diversion"
        },
        "8ball": {
            "trigger": "8ball",
            "response": "🎱 La bola magica dice: **$8ball**",
=======
            "variations": [
                "🪙 Resultado: **$coin** | Lanzado por $mention",
                "✨ La moneda cayo en: **$coin**!",
            ],
            "description": "Lanza una moneda",
            "category": "diversion"
        },
        "love": {
            "trigger": "amor",
            "response": "💕 El nivel de amor de $username es: **$random%**",
            "variations": [
                "❤️ Medidor de amor para $mention: **$random%**",
                "💘 $username tiene un **$random%** de amor hoy!",
            ],
            "description": "Mide el nivel de amor",
            "category": "diversion"
        },
        "hug": {
            "trigger": "abrazo",
            "response": "🤗 $username envia un calido abrazo!",
            "variations": [
                "🫂 $mention envia un abrazo virtual!",
                "💝 Un abrazo de $username para todos!",
            ],
            "description": "Envia un abrazo virtual",
            "category": "social"
        },
        "quote": {
            "trigger": "frase",
            "response": "💭 \"La mejor forma de predecir el futuro es crearlo.\" - Peter Drucker",
            "variations": [
                "💭 \"El exito es la suma de pequeños esfuerzos repetidos dia tras dia.\" - Robert Collier",
                "💭 \"No cuentes los dias, haz que los dias cuenten.\" - Muhammad Ali",
                "💭 \"La creatividad es la inteligencia divirtiendose.\" - Albert Einstein",
                "💭 \"El unico modo de hacer un gran trabajo es amar lo que haces.\" - Steve Jobs",
            ],
            "description": "Muestra una frase motivacional aleatoria",
            "category": "diversion"
        },
        "8ball": {
            "trigger": "8ball",
            "response": "🎱 La bola magica dice: **$8ball**",
            "variations": [
                "🔮 Respuesta del oraculo: **$8ball**",
                "✨ El destino dice: **$8ball**",
            ],
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
            "description": "Pregunta a la bola 8 magica",
            "category": "diversion"
        },
        "joke": {
            "trigger": "chiste",
            "response": "😂 $joke",
<<<<<<< HEAD
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
=======
            "variations": [
                "🤣 Chiste del dia: $joke",
                "😄 Aqui va uno: $joke",
            ],
            "description": "Cuenta un chiste aleatorio",
            "category": "diversion"
        },
    }
    
    VARIABLES = {
        # User variables
        "$username": "Nombre del usuario",
        "$user": "Alias de $username",
        "$userid": "ID del usuario",
        "$usertag": "Tag completo del usuario",
        "$mention": "Mencion al usuario (@usuario)",
        "$usermention": "Alias de $mention",
        "$displayname": "Nombre mostrado del usuario",
        "$discriminator": "Discriminador (#1234)",
        "$avatar": "URL del avatar del usuario",
        "$useravatar": "Alias de $avatar",
        
        # Server variables
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
        "$servername": "Nombre del servidor",
        "$server": "Alias de $servername",
        "$serverid": "ID del servidor",
        "$membercount": "Cantidad de miembros",
<<<<<<< HEAD
        "$servericon": "URL del icono del servidor",
        "$channel": "Nombre del canal",
        "$channelid": "ID del canal",
        "$channelmention": "Mencion del canal (#canal)",
=======
        "$members": "Alias de $membercount",
        "$servericon": "URL del icono del servidor",
        "$owner": "Dueno del servidor",
        
        # Channel variables
        "$channel": "Nombre del canal",
        "$channelid": "ID del canal",
        "$channelmention": "Mencion del canal (#canal)",
        "$topic": "Tema del canal",
        
        # Bot variables
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
        "$botname": "Nombre del bot",
        "$bot": "Alias de $botname",
        "$botid": "ID del bot",
        "$botmention": "Mencion del bot",
        "$prefix": "Prefijo de comandos",
<<<<<<< HEAD
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
=======
        
        # Time variables
        "$time": "Hora actual (HH:MM:SS)",
        "$date": "Fecha actual (YYYY-MM-DD)",
        "$datetime": "Fecha y hora completa",
        "$day": "Dia de la semana",
        "$month": "Mes actual",
        "$year": "Ano actual",
        "$timestamp": "Timestamp Unix",
        
        # Random/Fun variables
        "$random": "Numero aleatorio (1-100)",
        "$random(min,max)": "Numero aleatorio en rango",
        "$coin": "Lanzar moneda (Cara/Cruz)",
        "$8ball": "Respuesta de bola 8 magica",
        "$joke": "Chiste aleatorio",
        "$choose(a,b,c)": "Elige opcion aleatoria",
        
        # Arguments
        "$args": "Todos los argumentos del comando",
        "$arg1": "Primer argumento",
        "$arg2": "Segundo argumento",
        "$arg3": "Tercer argumento",
        "$argcount": "Cantidad de argumentos",
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
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
<<<<<<< HEAD
=======
        "Las perspectivas no son buenas",
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
        "Muy dudoso",
    ]
    
    JOKES = [
        "Por que los programadores prefieren el modo oscuro? Porque la luz atrae bugs!",
        "Que le dice un bit al otro? Nos vemos en el bus!",
        "Por que el libro de matematicas esta triste? Porque tiene muchos problemas.",
        "Que hace una abeja en el gimnasio? Zum-ba!",
        "Por que los pajaros no usan Facebook? Porque ya tienen Twitter.",
<<<<<<< HEAD
=======
        "Que le dice una iguana a su hermana gemela? Iguanita!",
        "Por que el cafe llamo a la policia? Porque lo estaban asaltando!",
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
        "Que hace un pez en el agua? Nada!",
    ]
    
    @staticmethod
    def create_command(trigger: str, response: str, description: str = "", 
                       variations: List[str] = None, use_variations: bool = False) -> Dict[str, Any]:
<<<<<<< HEAD
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
=======
        """Create a simple command with metadata and optional variations"""
        return {
            "id": trigger,
            "type": "simple",
            "trigger": trigger.lower().strip(),
            "response": response,
            "variations": variations or [],
            "use_variations": use_variations,
            "description": description,
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "enabled": True,
            "usage_count": 0
        }
    
    @staticmethod
    def get_available_variables() -> Dict[str, str]:
<<<<<<< HEAD
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
=======
        """Get list of available variables with descriptions"""
        return SimpleCommandBuilder.VARIABLES
    
    @staticmethod
    def get_variables_by_category() -> Dict[str, Dict[str, str]]:
        """Get variables organized by category"""
        return {
            "usuario": {k: v for k, v in SimpleCommandBuilder.VARIABLES.items() 
                       if any(x in k for x in ['user', 'mention', 'avatar', 'display', 'discrim'])},
            "servidor": {k: v for k, v in SimpleCommandBuilder.VARIABLES.items() 
                        if any(x in k for x in ['server', 'member', 'owner'])},
            "canal": {k: v for k, v in SimpleCommandBuilder.VARIABLES.items() 
                     if 'channel' in k or 'topic' in k},
            "bot": {k: v for k, v in SimpleCommandBuilder.VARIABLES.items() 
                   if 'bot' in k or 'prefix' in k},
            "tiempo": {k: v for k, v in SimpleCommandBuilder.VARIABLES.items() 
                      if any(x in k for x in ['time', 'date', 'day', 'month', 'year', 'timestamp'])},
            "aleatorio": {k: v for k, v in SimpleCommandBuilder.VARIABLES.items() 
                         if any(x in k for x in ['random', 'coin', '8ball', 'joke', 'choose'])},
            "argumentos": {k: v for k, v in SimpleCommandBuilder.VARIABLES.items() 
                          if 'arg' in k},
        }
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
    
    @staticmethod
    def preview_command(response: str, context: Dict[str, str] = None) -> str:
        """Preview command output with sample data"""
        context = context or {}
        
<<<<<<< HEAD
=======
        # Default preview values
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
        defaults = {
            "$username": "Usuario",
            "$user": "Usuario",
            "$userid": "123456789012345678",
<<<<<<< HEAD
            "$mention": "@Usuario",
            "$displayname": "Usuario Cool",
            "$avatar": "https://cdn.discordapp.com/avatars/...",
=======
            "$usertag": "Usuario#1234",
            "$mention": "@Usuario",
            "$usermention": "@Usuario",
            "$displayname": "Usuario Cool",
            "$discriminator": "1234",
            "$avatar": "https://cdn.discordapp.com/avatars/...",
            "$useravatar": "https://cdn.discordapp.com/avatars/...",
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
            "$servername": "Mi Servidor",
            "$server": "Mi Servidor",
            "$serverid": "987654321098765432",
            "$membercount": "150",
<<<<<<< HEAD
            "$servericon": "https://cdn.discordapp.com/icons/...",
            "$channel": "general",
            "$channelid": "111222333444555666",
            "$channelmention": "#general",
=======
            "$members": "150",
            "$servericon": "https://cdn.discordapp.com/icons/...",
            "$owner": "Admin#0001",
            "$channel": "general",
            "$channelid": "111222333444555666",
            "$channelmention": "#general",
            "$topic": "Canal de chat general",
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
            "$botname": "Far-Bot",
            "$bot": "Far-Bot",
            "$botid": "999888777666555444",
            "$botmention": "@Far-Bot",
            "$prefix": "!",
            "$time": datetime.now().strftime("%H:%M:%S"),
            "$date": datetime.now().strftime("%Y-%m-%d"),
            "$datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
<<<<<<< HEAD
=======
            "$day": datetime.now().strftime("%A"),
            "$month": datetime.now().strftime("%B"),
            "$year": str(datetime.now().year),
            "$timestamp": str(int(datetime.now().timestamp())),
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
            "$random": str(random.randint(1, 100)),
            "$coin": random.choice(["Cara", "Cruz"]),
            "$8ball": random.choice(SimpleCommandBuilder.EIGHTBALL_RESPONSES),
            "$joke": random.choice(SimpleCommandBuilder.JOKES),
            "$args": "argumento1 argumento2",
            "$arg1": "argumento1",
            "$arg2": "argumento2",
<<<<<<< HEAD
        }
        
        defaults.update(context)
        
        result = response
=======
            "$arg3": "",
            "$argcount": "2",
        }
        
        # Merge with provided context
        defaults.update(context)
        
        result = response
        
        # Handle $random(min,max) pattern
        result = re.sub(r'\$random$$(\d+),(\d+)$$', 
                       lambda m: str(random.randint(int(m.group(1)), int(m.group(2)))), 
                       result)
        
        # Handle $choose(a,b,c) pattern
        def choose_replacement(match):
            options = match.group(1).split(',')
            return random.choice([o.strip() for o in options])
        result = re.sub(r'\$choose$$([^)]+)$$', choose_replacement, result)
        
        # Replace all variables
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
        for var, value in defaults.items():
            result = result.replace(var, str(value))
        
        return result
    
    @staticmethod
    def process_response(response: str, ctx, variations: List[str] = None, 
                        use_variations: bool = False) -> str:
        """Process response with real context from Discord"""
        try:
<<<<<<< HEAD
=======
            # Choose response (original or variation)
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
            if use_variations and variations:
                all_responses = [response] + variations
                response = random.choice(all_responses)
            
<<<<<<< HEAD
=======
            # Build replacements from context
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
            replacements = {
                "$username": str(ctx.author.name),
                "$user": str(ctx.author.name),
                "$userid": str(ctx.author.id),
<<<<<<< HEAD
                "$mention": ctx.author.mention,
                "$displayname": str(ctx.author.display_name),
                "$avatar": str(ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url),
=======
                "$usertag": str(ctx.author),
                "$mention": ctx.author.mention,
                "$usermention": ctx.author.mention,
                "$displayname": str(ctx.author.display_name),
                "$discriminator": str(ctx.author.discriminator),
                "$avatar": str(ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url),
                "$useravatar": str(ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url),
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
                "$botname": str(ctx.bot.user.name),
                "$bot": str(ctx.bot.user.name),
                "$botid": str(ctx.bot.user.id),
                "$botmention": ctx.bot.user.mention,
                "$prefix": str(ctx.prefix),
                "$time": datetime.now().strftime("%H:%M:%S"),
                "$date": datetime.now().strftime("%Y-%m-%d"),
                "$datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
<<<<<<< HEAD
=======
                "$day": datetime.now().strftime("%A"),
                "$month": datetime.now().strftime("%B"),
                "$year": str(datetime.now().year),
                "$timestamp": str(int(datetime.now().timestamp())),
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
                "$random": str(random.randint(1, 100)),
                "$coin": random.choice(["Cara", "Cruz"]),
                "$8ball": random.choice(SimpleCommandBuilder.EIGHTBALL_RESPONSES),
                "$joke": random.choice(SimpleCommandBuilder.JOKES),
            }
            
<<<<<<< HEAD
=======
            # Server-specific replacements
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
            if ctx.guild:
                replacements.update({
                    "$servername": str(ctx.guild.name),
                    "$server": str(ctx.guild.name),
                    "$serverid": str(ctx.guild.id),
                    "$membercount": str(ctx.guild.member_count),
<<<<<<< HEAD
                    "$servericon": str(ctx.guild.icon.url if ctx.guild.icon else ""),
=======
                    "$members": str(ctx.guild.member_count),
                    "$servericon": str(ctx.guild.icon.url if ctx.guild.icon else ""),
                    "$owner": str(ctx.guild.owner) if ctx.guild.owner else "Desconocido",
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
                })
            else:
                replacements.update({
                    "$servername": "DM",
                    "$server": "DM",
                    "$serverid": "0",
                    "$membercount": "1",
<<<<<<< HEAD
                    "$servericon": "",
                })
            
=======
                    "$members": "1",
                    "$servericon": "",
                    "$owner": "N/A",
                })
            
            # Channel replacements
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
            if hasattr(ctx.channel, 'name'):
                replacements.update({
                    "$channel": str(ctx.channel.name),
                    "$channelid": str(ctx.channel.id),
                    "$channelmention": ctx.channel.mention,
<<<<<<< HEAD
=======
                    "$topic": str(ctx.channel.topic) if hasattr(ctx.channel, 'topic') and ctx.channel.topic else "",
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
                })
            else:
                replacements.update({
                    "$channel": "DM",
                    "$channelid": str(ctx.channel.id),
                    "$channelmention": "DM",
<<<<<<< HEAD
                })
            
            args = ctx.message.content.split()[1:]
            replacements["$args"] = ' '.join(args)
=======
                    "$topic": "",
                })
            
            # Arguments
            args = ctx.message.content.split()[1:]
            replacements["$args"] = ' '.join(args)
            replacements["$argcount"] = str(len(args))
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
            for i in range(10):
                replacements[f"$arg{i+1}"] = args[i] if i < len(args) else ""
            
            result = response
<<<<<<< HEAD
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
=======
            
            # Handle $random(min,max)
            result = re.sub(r'\$random$$(\d+),(\d+)$$', 
                          lambda m: str(random.randint(int(m.group(1)), int(m.group(2)))), 
                          result)
            
            # Handle $choose(a,b,c)
            def choose_replacement(match):
                options = match.group(1).split(',')
                return random.choice([o.strip() for o in options])
            result = re.sub(r'\$choose$$([^)]+)$$', choose_replacement, result)
            
            # Replace all variables
            for var, value in replacements.items():
                result = result.replace(var, value)
            
            return result
        except Exception as e:
            return f"Error procesando respuesta: {str(e)}"
    
    @staticmethod
    def get_template(template_name: str) -> Optional[Dict[str, Any]]:
        """Get a command template by name"""
        return SimpleCommandBuilder.TEMPLATES.get(template_name)
    
    @staticmethod
    def list_templates() -> Dict[str, Dict[str, Any]]:
        """List all available templates"""
        return SimpleCommandBuilder.TEMPLATES
    
    @staticmethod
    def get_templates_by_category() -> Dict[str, List[Dict[str, Any]]]:
        """Get templates organized by category"""
        categories = {}
        for name, template in SimpleCommandBuilder.TEMPLATES.items():
            cat = template.get("category", "otros")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append({"name": name, **template})
        return categories
    
    @staticmethod
    def validate_response(response: str) -> Tuple[bool, str, List[str]]:
        """Validate command response with detailed feedback"""
        warnings = []
        
        if not response:
            return False, "La respuesta no puede estar vacia", warnings
        
        if not response.strip():
            return False, "La respuesta no puede contener solo espacios", warnings
        
        if len(response) > 2000:
            return False, f"La respuesta excede el limite de 2000 caracteres ({len(response)}/2000)", warnings
        
        # Check for unknown variables
        used_vars = re.findall(r'\$\w+(?:$$[^)]*$$)?', response)
        valid_vars = list(SimpleCommandBuilder.VARIABLES.keys())
        valid_patterns = ['$random(', '$choose(', '$arg']
        
        for var in used_vars:
            base_var = var.split('(')[0]
            if base_var not in valid_vars and not any(var.startswith(p) for p in valid_patterns):
                warnings.append(f"Variable desconocida: {var}")
        
        # Check for potential issues
        if response.count('$') > 20:
            warnings.append("Muchas variables pueden afectar el rendimiento")
        
        if '```' in response and response.count('```') % 2 != 0:
            warnings.append("Bloques de codigo no cerrados correctamente")
        
        return True, "Respuesta valida", warnings
    
    @staticmethod
    def validate_trigger(trigger: str) -> Tuple[bool, str]:
        """Validate command trigger name"""
        if not trigger:
            return False, "El nombre del comando no puede estar vacio"
        
        if not trigger.strip():
            return False, "El nombre no puede contener solo espacios"
        
        if len(trigger) > 32:
            return False, "El nombre no puede exceder 32 caracteres"
        
        if len(trigger) < 1:
            return False, "El nombre debe tener al menos 1 caracter"
        
        if ' ' in trigger:
            return False, "El nombre no puede contener espacios"
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', trigger):
            return False, "El nombre solo puede contener letras, numeros, guiones y guiones bajos"
        
        # Reserved words
        reserved = ['help', 'commands', 'bot', 'admin', 'mod', 'owner']
        if trigger.lower() in reserved:
            return True, f"Advertencia: '{trigger}' es una palabra reservada comun"
        
        return True, "Nombre valido"
    
    @staticmethod
    def generate_variations(base_response: str, count: int = 3) -> List[str]:
        """Generate variations of a response (basic implementation)"""
        variations = []
        
        # Simple variations by changing emojis and structure
        emoji_sets = [
            ["👋", "✨", "🎉", "🌟", "💫"],
            ["😊", "😄", "🙂", "😁", "☺️"],
            ["❤️", "💕", "💖", "💗", "💝"],
        ]
        
        # Find emojis in base response
        emoji_pattern = re.compile(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]+')
        
        for i in range(count):
            variation = base_response
            for emoji_set in emoji_sets:
                for emoji in emoji_set:
                    if emoji in variation and i < len(emoji_set):
                        variation = variation.replace(emoji, emoji_set[(emoji_set.index(emoji) + i + 1) % len(emoji_set)], 1)
                        break
            if variation != base_response:
                variations.append(variation)
        
        return variations[:count]
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
