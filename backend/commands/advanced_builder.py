import re
from typing import Dict, Any, Tuple, List, Optional
from datetime import datetime


class AdvancedCommandBuilder:
    """Build and manage advanced Python commands - v2.0.0"""
    
    TEMPLATES = {
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
            "description": "El bot repite tu mensaje",
            "category": "basicos"
        },
        
        "dice": {
            "code": '''@bot.command(name='dado', aliases=['dice', 'roll'])
async def dado_command(ctx, caras: int = 6):
    """Tira un dado con el numero de caras especificado"""
    import random
    if caras < 2:
        await ctx.send("El dado debe tener al menos 2 caras!")
        return
    if caras > 1000:
        await ctx.send("El dado no puede tener mas de 1000 caras!")
        return
    resultado = random.randint(1, caras)
    await ctx.send(f"🎲 Has sacado un **{resultado}** (dado de {caras} caras)")
''',
            "name": "Dado",
            "description": "Tira un dado personalizable",
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
            "description": "Lanza una moneda",
            "category": "diversion"
        },
        
        "8ball": {
            "code": '''@bot.command(name='8ball', aliases=['bola8', 'pregunta'])
async def eightball_command(ctx, *, pregunta: str = None):
    """Pregunta a la bola 8 magica"""
    import random
    if pregunta is None:
        await ctx.send("Debes hacer una pregunta!")
        return
    respuestas = [
        "Si, definitivamente!",
        "Sin duda alguna",
        "Probablemente si",
        "Pregunta de nuevo mas tarde",
        "No cuentes con ello",
        "Mi respuesta es no",
        "Muy dudoso"
    ]
    embed = discord.Embed(title="🎱 Bola 8 Magica", color=discord.Color.purple())
    embed.add_field(name="Pregunta", value=pregunta, inline=False)
    embed.add_field(name="Respuesta", value=random.choice(respuestas), inline=False)
    embed.set_footer(text=f"Preguntado por {ctx.author.name}")
    await ctx.send(embed=embed)
''',
            "name": "Bola 8",
            "description": "Pregunta a la bola magica",
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
        await ctx.send("Necesitas al menos 2 opciones!")
        return
    
    eleccion = random.choice(lista)
    await ctx.send(f"🎯 De las opciones: {', '.join(lista)}\\n\\n**Yo elijo:** {eleccion}")
''',
            "name": "Elegir",
            "description": "Elige una opcion aleatoria",
            "category": "diversion"
        },
        
        "userinfo": {
            "code": '''@bot.command(name='usuario', aliases=['userinfo', 'whois'])
async def userinfo_command(ctx, member: discord.Member = None):
    """Muestra informacion de un usuario"""
    member = member or ctx.author
    
    roles = [role.mention for role in member.roles[1:]]
    roles_str = ", ".join(roles) if roles else "Ninguno"
    
    embed = discord.Embed(
        title=f"Informacion de {member.display_name}",
        color=member.color if member.color != discord.Color.default() else discord.Color.blue()
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="Usuario", value=f"{member.name}", inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Se unio", value=member.joined_at.strftime("%d/%m/%Y") if member.joined_at else "Desconocido", inline=True)
    embed.add_field(name="Roles", value=roles_str[:1024] if len(roles_str) <= 1024 else f"{len(roles)} roles", inline=False)
    await ctx.send(embed=embed)
''',
            "name": "Info Usuario",
            "description": "Muestra info de un usuario",
            "category": "informacion"
        },
        
        "serverinfo": {
            "code": '''@bot.command(name='servidor', aliases=['serverinfo', 'server'])
async def serverinfo_command(ctx):
    """Muestra informacion del servidor"""
    guild = ctx.guild
    
    embed = discord.Embed(title=f"📊 {guild.name}", color=discord.Color.green())
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    embed.add_field(name="ID", value=guild.id, inline=True)
    embed.add_field(name="Dueno", value=guild.owner.mention if guild.owner else "Desconocido", inline=True)
    embed.add_field(name="Miembros", value=guild.member_count, inline=True)
    embed.add_field(name="Canales", value=f"📝 {len(guild.text_channels)} | 🔊 {len(guild.voice_channels)}", inline=True)
    embed.add_field(name="Roles", value=len(guild.roles), inline=True)
    embed.set_footer(text=f"Solicitado por {ctx.author.name}")
    await ctx.send(embed=embed)
''',
            "name": "Info Servidor",
            "description": "Muestra info del servidor",
            "category": "informacion"
        },
        
        "avatar": {
            "code": '''@bot.command(name='avatar', aliases=['av', 'pfp'])
async def avatar_command(ctx, member: discord.Member = None):
    """Muestra el avatar de un usuario"""
    member = member or ctx.author
    
    embed = discord.Embed(
        title=f"Avatar de {member.display_name}",
        color=discord.Color.random()
    )
    embed.set_image(url=member.display_avatar.url)
    await ctx.send(embed=embed)
''',
            "name": "Avatar",
            "description": "Muestra el avatar",
            "category": "informacion"
        },
        
        "poll": {
            "code": '''@bot.command(name='encuesta', aliases=['poll', 'votar'])
async def poll_command(ctx, *, pregunta: str = None):
    """Crea una encuesta simple"""
    if pregunta is None:
        await ctx.send("Debes escribir una pregunta!")
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
            "description": "Crea una encuesta",
            "category": "utilidades"
        },
        
        "clear": {
            "code": '''@bot.command(name='limpiar', aliases=['clear', 'purge'])
@commands.has_permissions(manage_messages=True)
async def clear_command(ctx, cantidad: int = 10):
    """Elimina mensajes del canal"""
    import asyncio
    
    if cantidad < 1 or cantidad > 100:
        await ctx.send("La cantidad debe estar entre 1 y 100")
        return
    
    try:
        deleted = await ctx.channel.purge(limit=cantidad + 1)
        msg = await ctx.send(f"🧹 Se eliminaron **{len(deleted) - 1}** mensajes")
        await asyncio.sleep(3)
        await msg.delete()
    except discord.Forbidden:
        await ctx.send("No tengo permisos para eliminar mensajes!")
''',
            "name": "Limpiar",
            "description": "Elimina mensajes",
            "category": "moderacion"
        },
        
        "kick": {
            "code": '''@bot.command(name='kick', aliases=['expulsar'])
@commands.has_permissions(kick_members=True)
async def kick_command(ctx, member: discord.Member = None, *, razon: str = "No especificada"):
    """Expulsa a un usuario"""
    if member is None:
        await ctx.send("Debes mencionar a un usuario!")
        return
    
    if member == ctx.author:
        await ctx.send("No puedes expulsarte a ti mismo!")
        return
    
    try:
        await member.kick(reason=f"{razon} | Por: {ctx.author}")
        embed = discord.Embed(title="👢 Usuario Expulsado", color=discord.Color.orange())
        embed.add_field(name="Usuario", value=f"{member}", inline=False)
        embed.add_field(name="Razon", value=razon, inline=False)
        embed.add_field(name="Moderador", value=ctx.author.mention, inline=False)
        await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("No tengo permisos para expulsar a este usuario!")
''',
            "name": "Kick",
            "description": "Expulsa a un usuario",
            "category": "moderacion"
        },
        
        "ban": {
            "code": '''@bot.command(name='ban', aliases=['banear'])
@commands.has_permissions(ban_members=True)
async def ban_command(ctx, member: discord.Member = None, *, razon: str = "No especificada"):
    """Banea a un usuario"""
    if member is None:
        await ctx.send("Debes mencionar a un usuario!")
        return
    
    if member == ctx.author:
        await ctx.send("No puedes banearte a ti mismo!")
        return
    
    try:
        await member.ban(reason=f"{razon} | Por: {ctx.author}")
        embed = discord.Embed(title="🔨 Usuario Baneado", color=discord.Color.red())
        embed.add_field(name="Usuario", value=f"{member}", inline=False)
        embed.add_field(name="Razon", value=razon, inline=False)
        embed.add_field(name="Moderador", value=ctx.author.mention, inline=False)
        await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("No tengo permisos para banear a este usuario!")
''',
            "name": "Ban",
            "description": "Banea a un usuario",
            "category": "moderacion"
        },
        
        "hug": {
            "code": '''@bot.command(name='abrazo', aliases=['hug'])
async def hug_command(ctx, member: discord.Member = None):
    """Envia un abrazo a alguien"""
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
    await ctx.send(embed=embed)
''',
            "name": "Abrazo",
            "description": "Envia un abrazo",
            "category": "social"
        },
    }
    
    SLASH_TEMPLATES = {
        "hello_slash": {
            "code": '''@bot.tree.command(name='hola', description='Saluda al usuario')
async def hola_slash(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hola {interaction.user.mention}! 👋')
''',
            "name": "Hola (Slash)",
            "description": "Comando slash de saludo",
            "category": "basicos"
        },
        
        "ping_slash": {
            "code": '''@bot.tree.command(name='ping', description='Verifica la latencia del bot')
async def ping_slash(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f'🏓 Pong! Latencia: {latency}ms')
''',
            "name": "Ping (Slash)",
            "description": "Comando slash de ping",
            "category": "utilidades"
        },
        
        "avatar_slash": {
            "code": '''@bot.tree.command(name='avatar', description='Muestra el avatar de un usuario')
@app_commands.describe(usuario='El usuario del que quieres ver el avatar')
async def avatar_slash(interaction: discord.Interaction, usuario: discord.Member = None):
    usuario = usuario or interaction.user
    embed = discord.Embed(title=f'Avatar de {usuario.display_name}', color=discord.Color.random())
    embed.set_image(url=usuario.display_avatar.url)
    await interaction.response.send_message(embed=embed)
''',
            "name": "Avatar (Slash)",
            "description": "Comando slash de avatar",
            "category": "informacion"
        },
        
        "say_slash": {
            "code": '''@bot.tree.command(name='say', description='El bot dice tu mensaje')
@app_commands.describe(mensaje='El mensaje que quieres que diga el bot')
async def say_slash(interaction: discord.Interaction, mensaje: str):
    await interaction.response.send_message(mensaje)
''',
            "name": "Say (Slash)",
            "description": "Comando slash para que el bot diga algo",
            "category": "basicos"
        },
        
        "userinfo_slash": {
            "code": '''@bot.tree.command(name='usuario', description='Muestra informacion de un usuario')
@app_commands.describe(usuario='El usuario del que quieres ver la informacion')
async def userinfo_slash(interaction: discord.Interaction, usuario: discord.Member = None):
    member = usuario or interaction.user
    embed = discord.Embed(title=f'Info de {member.display_name}', color=member.color)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name='ID', value=member.id, inline=True)
    embed.add_field(name='Se unio', value=member.joined_at.strftime('%d/%m/%Y') if member.joined_at else 'Desconocido', inline=True)
    await interaction.response.send_message(embed=embed)
''',
            "name": "Usuario (Slash)",
            "description": "Comando slash de info de usuario",
            "category": "informacion"
        },
    }
    
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
        r'breakpoint',
        r'input\s*\(',
    ]
    
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
        """Create an advanced command"""
        if not name:
            match = re.search(r"@bot\.command\(name=['\"](\w+)['\"]", code)
            if match:
                name = match.group(1)
            else:
                match = re.search(r"@bot\.tree\.command\(name=['\"](\w+)['\"]", code)
                if match:
                    name = match.group(1)
                else:
                    func_match = re.search(r'async\s+def\s+(\w+)', code)
                    if func_match:
                        name = func_match.group(1).replace('_command', '').replace('_cmd', '')
        
        is_slash = '@bot.tree.command' in code or '@app_commands' in code
        
        return {
            "id": name.lower().strip() if name else "unnamed_command",
            "type": "slash" if is_slash else "advanced",
            "trigger": name.lower().strip() if name else "unnamed",
            "code": code.strip(),
            "description": description or f"Comando {'slash ' if is_slash else ''}{name}",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "enabled": True,
            "usage_count": 0
        }
    
    @staticmethod
    def get_templates() -> Dict[str, Any]:
        """Get all command templates"""
        return AdvancedCommandBuilder.TEMPLATES
    
    @staticmethod
    def get_slash_templates() -> Dict[str, Any]:
        """Get slash command templates"""
        return AdvancedCommandBuilder.SLASH_TEMPLATES
    
    @staticmethod
    def get_all_templates() -> Dict[str, Any]:
        """Get all templates including slash"""
        all_templates = {}
        all_templates.update(AdvancedCommandBuilder.TEMPLATES)
        all_templates.update(AdvancedCommandBuilder.SLASH_TEMPLATES)
        return all_templates
    
    @staticmethod
    def get_templates_by_category() -> Dict[str, List[Dict]]:
        """Get templates organized by category"""
        categories = {}
        
        for key, template in AdvancedCommandBuilder.TEMPLATES.items():
            cat = template.get('category', 'otros')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append({
                'id': key,
                'is_slash': False,
                **template
            })
        
        for key, template in AdvancedCommandBuilder.SLASH_TEMPLATES.items():
            cat = template.get('category', 'slash')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append({
                'id': key,
                'is_slash': True,
                **template
            })
        
        return categories
    
    @staticmethod
    def validate_code(code: str) -> Tuple[bool, str]:
        """Validate Python code for safety and syntax"""
        errors = []
        warnings = []
        
        if not code or not code.strip():
            return False, "El codigo no puede estar vacio"
        
        # Check syntax
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            return False, f"Error de sintaxis en linea {e.lineno}: {e.msg}"
        
        # Check dangerous patterns
        for pattern in AdvancedCommandBuilder.DANGEROUS_PATTERNS:
            if re.search(pattern, code, re.IGNORECASE):
                return False, f"Codigo no permitido: patron peligroso detectado ({pattern})"
        
        # Check imports
        import_matches = re.findall(r'import\s+(\w+)|from\s+(\w+)', code)
        for match in import_matches:
            module = match[0] or match[1]
            if module not in AdvancedCommandBuilder.ALLOWED_IMPORTS:
                warnings.append(f"Modulo '{module}' podria no estar disponible")
        
        # Check for command decorator
        has_command = '@bot.command' in code or '@bot.tree.command' in code
        if not has_command:
            return False, "El codigo debe incluir @bot.command o @bot.tree.command"
        
        # Check for async function
        if 'async def' not in code:
            return False, "El comando debe ser una funcion asincrona (async def)"
        
        if warnings:
            return True, "; ".join(warnings)
        
        return True, "Codigo valido"
    
    @staticmethod
    def format_code(code: str) -> str:
        """Basic code formatting"""
        lines = code.split('\n')
        formatted = []
        indent = 0
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith(('else:', 'elif ', 'except:', 'except ', 'finally:', 'elif:')):
                indent = max(0, indent - 1)
            
            if stripped:
                formatted.append('    ' * indent + stripped)
            else:
                formatted.append('')
            
            if stripped.endswith(':') and not stripped.startswith('#'):
                indent += 1
        
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
