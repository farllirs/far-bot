import re
from typing import Dict, Any, Tuple, List, Optional
from datetime import datetime


class AdvancedCommandBuilder:
    """Build and manage advanced Python commands with improved validation and templates"""
    
    TEMPLATES = {
        # Basic Commands
        "echo": {
            "code": '''@bot.command(name='echo')
async def echo_command(ctx, *, texto: str = None):
    """Repite el mensaje que escribas"""
    if texto is None:
        await ctx.send("Por favor escribe algo para repetir!")
        return
    await ctx.send(texto)
''',
            "name": "Echo",
            "description": "Repite el mensaje del usuario",
            "category": "basicos"
        },
        
        "say": {
            "code": '''@bot.command(name='say')
async def say_command(ctx, *, mensaje: str = None):
    """El bot dice tu mensaje y borra el original"""
    if mensaje is None:
        await ctx.send("Escribe algo para que yo lo diga!")
        return
    try:
        await ctx.message.delete()
    except:
        pass
    await ctx.send(mensaje)
''',
            "name": "Say",
            "description": "El bot repite tu mensaje y borra el comando",
            "category": "basicos"
        },
        
        # Fun Commands
        "dice": {
            "code": '''@bot.command(name='dado', aliases=['dice', 'roll'])
async def dado_command(ctx, caras: int = 6):
    """Tira un dado con el numero de caras especificado"""
    import random
    if caras < 2:
        await ctx.send("❌ El dado debe tener al menos 2 caras!")
        return
    if caras > 1000:
        await ctx.send("❌ El dado no puede tener mas de 1000 caras!")
        return
    resultado = random.randint(1, caras)
    await ctx.send(f"🎲 Has sacado un **{resultado}** (dado de {caras} caras)")
''',
            "name": "Dado",
            "description": "Tira un dado con caras personalizables",
            "category": "diversion"
        },
        
        "coinflip": {
            "code": '''@bot.command(name='moneda', aliases=['coin', 'flip'])
async def moneda_command(ctx):
    """Lanza una moneda al aire"""
    import random
    resultado = random.choice(["🪙 **Cara!**", "🪙 **Cruz!**"])
    await ctx.send(f"{ctx.author.mention} ha lanzado una moneda: {resultado}")
''',
            "name": "Moneda",
            "description": "Lanza una moneda al aire",
            "category": "diversion"
        },
        
        "8ball": {
            "code": '''@bot.command(name='8ball', aliases=['bola8', 'pregunta'])
async def eightball_command(ctx, *, pregunta: str = None):
    """Pregunta a la bola 8 magica"""
    import random
    if pregunta is None:
        await ctx.send("❓ Debes hacer una pregunta!")
        return
    respuestas = [
        "Si, definitivamente! ✅",
        "Sin duda alguna ✅",
        "Probablemente si 🤔",
        "Las senales apuntan a si 🔮",
        "Pregunta de nuevo mas tarde ⏳",
        "Mejor no te lo digo ahora 🤐",
        "No puedo predecirlo ahora 🌫️",
        "Concentrate y pregunta de nuevo 🧘",
        "No cuentes con ello ❌",
        "Mi respuesta es no ❌",
        "Mis fuentes dicen que no 📉",
        "Muy dudoso 🤨"
    ]
    embed = discord.Embed(
        title="🎱 Bola 8 Magica",
        color=discord.Color.purple()
    )
    embed.add_field(name="Pregunta", value=pregunta, inline=False)
    embed.add_field(name="Respuesta", value=random.choice(respuestas), inline=False)
    embed.set_footer(text=f"Preguntado por {ctx.author.name}")
    await ctx.send(embed=embed)
''',
            "name": "Bola 8",
            "description": "Pregunta a la bola magica",
            "category": "diversion"
        },
        
        "rps": {
            "code": '''@bot.command(name='ppt', aliases=['rps', 'piedrapapeltijera'])
async def rps_command(ctx, eleccion: str = None):
    """Juega piedra, papel o tijera"""
    import random
    opciones = {"piedra": "🪨", "papel": "📄", "tijera": "✂️", "tijeras": "✂️"}
    
    if eleccion is None or eleccion.lower() not in opciones:
        await ctx.send("Elige: `piedra`, `papel` o `tijera`")
        return
    
    eleccion = eleccion.lower()
    if eleccion == "tijeras":
        eleccion = "tijera"
    
    bot_choice = random.choice(["piedra", "papel", "tijera"])
    
    # Determinar ganador
    if eleccion == bot_choice:
        resultado = "🤝 **Empate!**"
    elif (eleccion == "piedra" and bot_choice == "tijera") or \\
         (eleccion == "papel" and bot_choice == "piedra") or \\
         (eleccion == "tijera" and bot_choice == "papel"):
        resultado = "🎉 **Ganaste!**"
    else:
        resultado = "😢 **Perdiste!**"
    
    embed = discord.Embed(title="Piedra, Papel o Tijera", color=discord.Color.blue())
    embed.add_field(name="Tu eleccion", value=f"{opciones[eleccion]} {eleccion.title()}", inline=True)
    embed.add_field(name="Mi eleccion", value=f"{opciones[bot_choice]} {bot_choice.title()}", inline=True)
    embed.add_field(name="Resultado", value=resultado, inline=False)
    await ctx.send(embed=embed)
''',
            "name": "Piedra Papel Tijera",
            "description": "Juega piedra, papel o tijera",
            "category": "diversion"
        },
        
        "choose": {
            "code": '''@bot.command(name='elegir', aliases=['choose', 'pick'])
async def choose_command(ctx, *, opciones: str = None):
    """Elige entre varias opciones separadas por coma"""
    import random
    if opciones is None:
        await ctx.send("Escribe opciones separadas por coma: `!elegir pizza, hamburguesa, tacos`")
        return
    
    lista = [o.strip() for o in opciones.split(',') if o.strip()]
    
    if len(lista) < 2:
        await ctx.send("❌ Necesitas al menos 2 opciones!")
        return
    
    eleccion = random.choice(lista)
    await ctx.send(f"🎯 De las opciones: {', '.join(lista)}\\n\\n**Yo elijo:** {eleccion}")
''',
            "name": "Elegir",
            "description": "Elige una opcion aleatoria",
            "category": "diversion"
        },
        
        # Information Commands
        "userinfo": {
            "code": '''@bot.command(name='usuario', aliases=['userinfo', 'whois'])
async def userinfo_command(ctx, member: discord.Member = None):
    """Muestra informacion detallada de un usuario"""
    member = member or ctx.author
    
    roles = [role.mention for role in member.roles[1:]]  # Excluir @everyone
    roles_str = ", ".join(roles) if roles else "Ninguno"
    
    embed = discord.Embed(
        title=f"Informacion de {member.display_name}",
        color=member.color if member.color != discord.Color.default() else discord.Color.blue()
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="👤 Usuario", value=f"{member.name}#{member.discriminator}", inline=True)
    embed.add_field(name="🆔 ID", value=member.id, inline=True)
    embed.add_field(name="📛 Apodo", value=member.nick or "Ninguno", inline=True)
    embed.add_field(name="📅 Cuenta creada", value=member.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="📥 Se unio", value=member.joined_at.strftime("%d/%m/%Y") if member.joined_at else "Desconocido", inline=True)
    embed.add_field(name="🎭 Roles", value=roles_str[:1024] if len(roles_str) <= 1024 else f"{len(roles)} roles", inline=False)
    embed.set_footer(text=f"Solicitado por {ctx.author.name}")
    await ctx.send(embed=embed)
''',
            "name": "Info Usuario",
            "description": "Muestra informacion de un usuario",
            "category": "informacion"
        },
        
        "serverinfo": {
            "code": '''@bot.command(name='servidor', aliases=['serverinfo', 'server'])
async def serverinfo_command(ctx):
    """Muestra informacion detallada del servidor"""
    guild = ctx.guild
    
    # Contar canales por tipo
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    categories = len(guild.categories)
    
    embed = discord.Embed(
        title=f"📊 {guild.name}",
        color=discord.Color.green()
    )
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    embed.add_field(name="🆔 ID", value=guild.id, inline=True)
    embed.add_field(name="👑 Dueno", value=guild.owner.mention if guild.owner else "Desconocido", inline=True)
    embed.add_field(name="📅 Creado", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="👥 Miembros", value=guild.member_count, inline=True)
    embed.add_field(name="💬 Canales", value=f"📝 {text_channels} | 🔊 {voice_channels} | 📁 {categories}", inline=True)
    embed.add_field(name="🎭 Roles", value=len(guild.roles), inline=True)
    embed.add_field(name="😀 Emojis", value=len(guild.emojis), inline=True)
    embed.add_field(name="🔒 Nivel de verificacion", value=str(guild.verification_level).title(), inline=True)
    
    if guild.banner:
        embed.set_image(url=guild.banner.url)
    
    embed.set_footer(text=f"Solicitado por {ctx.author.name}")
    await ctx.send(embed=embed)
''',
            "name": "Info Servidor",
            "description": "Muestra informacion del servidor",
            "category": "informacion"
        },
        
        "avatar": {
            "code": '''@bot.command(name='avatar', aliases=['av', 'pfp'])
async def avatar_command(ctx, member: discord.Member = None):
    """Muestra el avatar de un usuario en tamano completo"""
    member = member or ctx.author
    
    embed = discord.Embed(
        title=f"Avatar de {member.display_name}",
        color=member.color if member.color != discord.Color.default() else discord.Color.random()
    )
    
    avatar_url = member.display_avatar.url
    embed.set_image(url=avatar_url)
    
    # Botones de descarga en diferentes formatos
    formats = []
    for fmt in ['png', 'jpg', 'webp']:
        try:
            formats.append(f"[{fmt.upper()}]({member.display_avatar.replace(format=fmt, size=1024).url})")
        except:
            pass
    
    if formats:
        embed.description = " | ".join(formats)
    
    embed.set_footer(text=f"Solicitado por {ctx.author.name}")
    await ctx.send(embed=embed)
''',
            "name": "Avatar",
            "description": "Muestra el avatar de un usuario",
            "category": "informacion"
        },
        
        # Utility Commands
        "remind": {
            "code": '''@bot.command(name='recordar', aliases=['remind', 'timer'])
async def remind_command(ctx, tiempo: str = None, *, mensaje: str = "Recordatorio!"):
    """Establece un recordatorio (ej: 10s, 5m, 1h)"""
    import asyncio
    import re
    
    if tiempo is None:
        await ctx.send("Uso: `!recordar <tiempo> <mensaje>`\\nEjemplo: `!recordar 10m Revisar el horno`")
        return
    
    # Parsear tiempo
    match = re.match(r'^(\\d+)([smh])$', tiempo.lower())
    if not match:
        await ctx.send("❌ Formato invalido. Usa: `10s`, `5m`, `1h`")
        return
    
    cantidad = int(match.group(1))
    unidad = match.group(2)
    
    multiplicadores = {'s': 1, 'm': 60, 'h': 3600}
    segundos = cantidad * multiplicadores[unidad]
    
    if segundos > 86400:  # 24 horas max
        await ctx.send("❌ El tiempo maximo es 24 horas!")
        return
    
    unidades_texto = {'s': 'segundos', 'm': 'minutos', 'h': 'horas'}
    await ctx.send(f"⏰ Te recordare en {cantidad} {unidades_texto[unidad]}!")
    
    await asyncio.sleep(segundos)
    await ctx.send(f"{ctx.author.mention} 📢 **Recordatorio:** {mensaje}")
''',
            "name": "Recordatorio",
            "description": "Establece un recordatorio",
            "category": "utilidades"
        },
        
        "poll": {
            "code": '''@bot.command(name='encuesta', aliases=['poll', 'votar'])
async def poll_command(ctx, *, pregunta: str = None):
    """Crea una encuesta simple con reacciones"""
    if pregunta is None:
        await ctx.send("❌ Debes escribir una pregunta para la encuesta!")
        return
    
    embed = discord.Embed(
        title="📊 Encuesta",
        description=pregunta,
        color=discord.Color.gold()
    )
    embed.set_footer(text=f"Encuesta creada por {ctx.author.name}")
    
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("👍")
    await msg.add_reaction("👎")
    await msg.add_reaction("🤷")
''',
            "name": "Encuesta",
            "description": "Crea una encuesta con reacciones",
            "category": "utilidades"
        },
        
        "calc": {
            "code": '''@bot.command(name='calc', aliases=['calcular', 'math'])
async def calc_command(ctx, *, expresion: str = None):
    """Calculadora basica segura"""
    import re
    
    if expresion is None:
        await ctx.send("Uso: `!calc <expresion>`\\nEjemplo: `!calc 2 + 2 * 3`")
        return
    
    # Solo permitir caracteres seguros
    if not re.match(r'^[\\d\\s\\+\\-\\*\\/\$$\$$\\.\\^]+$', expresion):
        await ctx.send("❌ Expresion no valida. Solo usa numeros y operadores: + - * / ( ) ^")
        return
    
    try:
        # Reemplazar ^ por ** para potencias
        expresion_python = expresion.replace('^', '**')
        resultado = eval(expresion_python)
        
        embed = discord.Embed(title="🔢 Calculadora", color=discord.Color.blue())
        embed.add_field(name="Expresion", value=f"`{expresion}`", inline=False)
        embed.add_field(name="Resultado", value=f"`{resultado}`", inline=False)
        await ctx.send(embed=embed)
    except ZeroDivisionError:
        await ctx.send("❌ No se puede dividir por cero!")
    except Exception as e:
        await ctx.send(f"❌ Error en la expresion: {str(e)}")
''',
            "name": "Calculadora",
            "description": "Calcula expresiones matematicas",
            "category": "utilidades"
        },
        
        # Moderation Commands
        "clear": {
            "code": '''@bot.command(name='limpiar', aliases=['clear', 'purge'])
@commands.has_permissions(manage_messages=True)
async def clear_command(ctx, cantidad: int = 10):
    """Elimina mensajes del canal (requiere permisos)"""
    import asyncio
    
    if cantidad < 1:
        await ctx.send("❌ La cantidad debe ser al menos 1")
        return
    if cantidad > 100:
        await ctx.send("❌ La cantidad maxima es 100 mensajes")
        return
    
    try:
        deleted = await ctx.channel.purge(limit=cantidad + 1)
        msg = await ctx.send(f"🧹 Se eliminaron **{len(deleted) - 1}** mensajes")
        await asyncio.sleep(3)
        await msg.delete()
    except discord.Forbidden:
        await ctx.send("❌ No tengo permisos para eliminar mensajes!")
    except Exception as e:
        await ctx.send(f"❌ Error: {str(e)}")
''',
            "name": "Limpiar",
            "description": "Elimina mensajes del canal",
            "category": "moderacion"
        },
        
        "kick": {
            "code": '''@bot.command(name='kick', aliases=['expulsar'])
@commands.has_permissions(kick_members=True)
async def kick_command(ctx, member: discord.Member = None, *, razon: str = "No especificada"):
    """Expulsa a un usuario del servidor"""
    if member is None:
        await ctx.send("❌ Debes mencionar a un usuario!")
        return
    
    if member == ctx.author:
        await ctx.send("❌ No puedes expulsarte a ti mismo!")
        return
    
    if member.top_role >= ctx.author.top_role:
        await ctx.send("❌ No puedes expulsar a alguien con un rol igual o superior!")
        return
    
    try:
        await member.kick(reason=f"{razon} | Por: {ctx.author}")
        embed = discord.Embed(
            title="👢 Usuario Expulsado",
            color=discord.Color.orange()
        )
        embed.add_field(name="Usuario", value=f"{member} ({member.id})", inline=False)
        embed.add_field(name="Razon", value=razon, inline=False)
        embed.add_field(name="Moderador", value=ctx.author.mention, inline=False)
        await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("❌ No tengo permisos para expulsar a este usuario!")
''',
            "name": "Kick",
            "description": "Expulsa a un usuario",
            "category": "moderacion"
        },
        
        "ban": {
            "code": '''@bot.command(name='ban', aliases=['banear'])
@commands.has_permissions(ban_members=True)
async def ban_command(ctx, member: discord.Member = None, *, razon: str = "No especificada"):
    """Banea a un usuario del servidor"""
    if member is None:
        await ctx.send("❌ Debes mencionar a un usuario!")
        return
    
    if member == ctx.author:
        await ctx.send("❌ No puedes banearte a ti mismo!")
        return
    
    if member.top_role >= ctx.author.top_role:
        await ctx.send("❌ No puedes banear a alguien con un rol igual o superior!")
        return
    
    try:
        await member.ban(reason=f"{razon} | Por: {ctx.author}")
        embed = discord.Embed(
            title="🔨 Usuario Baneado",
            color=discord.Color.red()
        )
        embed.add_field(name="Usuario", value=f"{member} ({member.id})", inline=False)
        embed.add_field(name="Razon", value=razon, inline=False)
        embed.add_field(name="Moderador", value=ctx.author.mention, inline=False)
        await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("❌ No tengo permisos para banear a este usuario!")
''',
            "name": "Ban",
            "description": "Banea a un usuario",
            "category": "moderacion"
        },
        
        # Social Commands
        "hug": {
            "code": '''@bot.command(name='abrazo', aliases=['hug', 'abrazar'])
async def hug_command(ctx, member: discord.Member = None):
    """Envia un abrazo a alguien"""
    import random
    
    gifs = [
        "https://media.tenor.com/images/b27882cf54f2d0e2d70c0a89b949cd1b/tenor.gif",
        "https://media.tenor.com/images/ca88f916b1d73770de3e3e5bee137336/tenor.gif",
        "https://media.tenor.com/images/749d728f932f69e7dc0a97559cc62dc7/tenor.gif",
    ]
    
    if member is None:
        await ctx.send(f"🤗 {ctx.author.mention} necesita un abrazo!")
        return
    
    if member == ctx.author:
        await ctx.send(f"🤗 {ctx.author.mention} se da un auto-abrazo!")
        return
    
    embed = discord.Embed(
        description=f"🤗 {ctx.author.mention} le da un calido abrazo a {member.mention}!",
        color=discord.Color.pink()
    )
    embed.set_image(url=random.choice(gifs))
    await ctx.send(embed=embed)
''',
            "name": "Abrazo",
            "description": "Envia un abrazo virtual",
            "category": "social"
        },
    }
    
    # Dangerous patterns to block
    DANGEROUS_PATTERNS = [
        r'__import__',
        r'eval\s*\(',
        r'exec\s*\(',
        r'compile\s*\(',
        r'open\s*\(',
        r'os\.system',
        r'os\.popen',
        r'subprocess',
        r'importlib',
        r'builtins',
        r'globals\s*$$\s*$$',
        r'locals\s*$$\s*$$',
        r'getattr\s*\(',
        r'setattr\s*\(',
        r'delattr\s*\(',
        r'__class__',
        r'__bases__',
        r'__subclasses__',
        r'__mro__',
        r'breakpoint',
        r'input\s*\(',
        r'help\s*$$\s*$$',
    ]
    
    # Allowed imports
    ALLOWED_IMPORTS = [
        'discord',
        'asyncio',
        'random',
        'datetime',
        'time',
        'math',
        'json',
        're',
        'typing',
        'collections',
    ]
    
    @staticmethod
    def create_command(code: str, description: str = "", name: str = "") -> Dict[str, Any]:
        """Create an advanced command with metadata"""
        # Extract command name from code if not provided
        if not name:
            match = re.search(r"@bot\.command\(name=['\"](\w+)['\"]", code)
            if match:
                name = match.group(1)
            else:
                # Try to find function name
                func_match = re.search(r'async\s+def\s+(\w+)', code)
                if func_match:
                    name = func_match.group(1).replace('_command', '').replace('_cmd', '')
                else:
                    name = "advanced_command"
        
        return {
            "id": name,
            "type": "advanced",
            "trigger": name,
            "code": code,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "enabled": True,
            "usage_count": 0
        }
    
    @staticmethod
    def validate_command(code: str) -> Tuple[bool, str, List[str]]:
        """Validate advanced command code with comprehensive checks"""
        warnings = []
        
        if not code:
            return False, "El codigo no puede estar vacio", warnings
        
        if not code.strip():
            return False, "El codigo no puede contener solo espacios", warnings
        
        if len(code) > 10000:
            return False, "El codigo excede el limite de 10000 caracteres", warnings
        
        # Check for bot decorator
        has_command = '@bot.command' in code
        has_event = '@bot.event' in code
        has_listener = '@bot.listen' in code
        
        if not (has_command or has_event or has_listener):
            return False, "El codigo debe incluir @bot.command, @bot.event o @bot.listen", warnings
        
        # Check for async function
        if 'async def' not in code:
            return False, "Debe definir una funcion asincrona (async def)", warnings
        
        # Check for dangerous operations
        for pattern in AdvancedCommandBuilder.DANGEROUS_PATTERNS:
            if re.search(pattern, code, re.IGNORECASE):
                clean_pattern = pattern.replace('\\s*', ' ').replace('\$$', '(').replace('\$$', ')')
                return False, f"Operacion peligrosa detectada: {clean_pattern}", warnings
        
        # Check imports
        import_matches = re.findall(r'import\s+(\w+)|from\s+(\w+)', code)
        for match in import_matches:
            module = match[0] or match[1]
            if module and module not in AdvancedCommandBuilder.ALLOWED_IMPORTS:
                if module not in ['commands', 'discord']:
                    return False, f"Modulo no permitido: {module}. Permitidos: {', '.join(AdvancedCommandBuilder.ALLOWED_IMPORTS)}", warnings
        
        # Basic syntax check
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            return False, f"Error de sintaxis en linea {e.lineno}: {e.msg}", warnings
        
        # Warnings (non-blocking)
        if 'await' not in code:
            warnings.append("No se encontro ninguna operacion await")
        
        if 'ctx.send' not in code and 'ctx.reply' not in code:
            warnings.append("El comando no parece enviar ninguna respuesta")
        
        if '@commands.cooldown' not in code:
            warnings.append("Considera agregar un cooldown para evitar spam")
        
        # Check for error handling
        if 'try:' not in code and 'except' not in code:
            warnings.append("Considera agregar manejo de errores (try/except)")
        
        return True, "Codigo valido", warnings
    
    @staticmethod
    def get_template(template_name: str) -> Optional[Dict[str, Any]]:
        """Get command template by name"""
        return AdvancedCommandBuilder.TEMPLATES.get(template_name)
    
    @staticmethod
    def get_template_code(template_name: str) -> str:
        """Get just the code from a template"""
        template = AdvancedCommandBuilder.TEMPLATES.get(template_name)
        return template.get("code", "") if template else ""
    
    @staticmethod
    def list_templates() -> Dict[str, Dict[str, Any]]:
        """List all available templates"""
        return AdvancedCommandBuilder.TEMPLATES
    
    @staticmethod
    def get_templates_by_category() -> Dict[str, List[Dict[str, Any]]]:
        """Get templates organized by category"""
        categories = {}
        for name, template in AdvancedCommandBuilder.TEMPLATES.items():
            cat = template.get("category", "otros")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append({
                "id": name,
                "name": template.get("name", name),
                "description": template.get("description", ""),
                "code": template.get("code", "")
            })
        return categories
    
    @staticmethod
    def get_template_info() -> List[Dict[str, str]]:
        """Get template information with descriptions"""
        return [
            {
                "id": name, 
                "name": t.get("name", name),
                "description": t.get("description", ""),
                "category": t.get("category", "otros"),
                "code": t.get("code", "")
            } 
            for name, t in AdvancedCommandBuilder.TEMPLATES.items()
        ]
    
    @staticmethod
    def get_documentation() -> Dict[str, Any]:
        """Get comprehensive documentation for advanced commands"""
        return {
            "decorators": {
                "@bot.command(name='nombre')": "Crea un comando de texto",
                "@bot.command(name='cmd', aliases=['c', 'alias'])": "Comando con alias",
                "@bot.event": "Maneja eventos del bot",
                "@bot.listen('evento')": "Escucha un evento especifico",
                "@commands.has_permissions(...)": "Requiere permisos",
                "@commands.has_role('rol')": "Requiere un rol especifico",
                "@commands.cooldown(uses, seconds, type)": "Agrega cooldown",
                "@commands.guild_only()": "Solo funciona en servidores",
                "@commands.dm_only()": "Solo funciona en DMs",
            },
            "context_attributes": {
                "ctx.send(content)": "Envia un mensaje al canal",
                "ctx.reply(content)": "Responde al mensaje del usuario",
                "ctx.author": "Usuario que ejecuto el comando",
                "ctx.guild": "Servidor donde se ejecuto",
                "ctx.channel": "Canal donde se ejecuto",
                "ctx.message": "Mensaje que activo el comando",
                "ctx.bot": "Instancia del bot",
                "ctx.prefix": "Prefijo usado",
            },
            "embed_methods": {
                "discord.Embed(title, description, color)": "Crea un embed",
                "embed.add_field(name, value, inline)": "Agrega un campo",
                "embed.set_thumbnail(url)": "Establece miniatura",
                "embed.set_image(url)": "Establece imagen grande",
                "embed.set_footer(text, icon_url)": "Pie de pagina",
                "embed.set_author(name, icon_url)": "Autor del embed",
            },
            "colors": {
                "discord.Color.red()": "Rojo",
                "discord.Color.green()": "Verde",
                "discord.Color.blue()": "Azul",
                "discord.Color.gold()": "Dorado",
                "discord.Color.purple()": "Morado",
                "discord.Color.random()": "Aleatorio",
            },
            "permissions": [
                "administrator", "manage_guild", "manage_roles",
                "manage_channels", "kick_members", "ban_members",
                "manage_messages", "manage_nicknames", "mute_members",
            ],
            "allowed_imports": AdvancedCommandBuilder.ALLOWED_IMPORTS,
        }
    
    @staticmethod
    def format_code(code: str) -> str:
        """Basic code formatting"""
        lines = code.split('\n')
        formatted = []
        indent_level = 0
        
        for line in lines:
            stripped = line.strip()
            
            # Decrease indent for certain keywords
            if stripped.startswith(('elif ', 'else:', 'except', 'finally:', 'except:')):
                indent_level = max(0, indent_level - 1)
            
            # Add proper indentation
            if stripped:
                formatted.append('    ' * indent_level + stripped)
            else:
                formatted.append('')
            
            # Increase indent after certain patterns
            if stripped.endswith(':') and not stripped.startswith('#'):
                indent_level += 1
        
        return '\n'.join(formatted)


class CommandTemplate:
    """Template engine for command generation"""
    
    @staticmethod
    def generate_from_template(template_type: str, template_name: str, params: Dict[str, Any] = None) -> str:
        """Generate command from template with parameter substitution"""
        params = params or {}
        
        if template_type == "simple":
            from backend.commands.simple_builder import SimpleCommandBuilder
            template = SimpleCommandBuilder.get_template(template_name)
            if template:
                response = template.get("response", "")
                for key, value in params.items():
                    response = response.replace(f"{{{key}}}", str(value))
                return response
        
        elif template_type == "advanced":
            template = AdvancedCommandBuilder.get_template(template_name)
            if template:
                code = template.get("code", "")
                for key, value in params.items():
                    code = code.replace(f"{{{key}}}", str(value))
                return code
        
        return ""
    
    @staticmethod
    def list_all_templates() -> Dict[str, Any]:
        """List all available templates from both builders"""
        from backend.commands.simple_builder import SimpleCommandBuilder
        
        return {
            "simple": SimpleCommandBuilder.list_templates(),
            "advanced": {k: v.get("code", "") for k, v in AdvancedCommandBuilder.list_templates().items()}
        }
    
    @staticmethod
    def get_template_categories() -> Dict[str, List[str]]:
        """Get templates organized by category"""
        return {
            "basicos": ["greeting", "goodbye", "help", "ping", "echo", "say"],
            "diversion": ["dice", "coinflip", "8ball", "rps", "choose", "roll", "love", "quote", "joke"],
            "informacion": ["userinfo", "serverinfo", "avatar", "info", "server", "user"],
            "utilidades": ["remind", "poll", "calc"],
            "moderacion": ["clear", "kick", "ban", "rules"],
            "social": ["hug"],
        }
