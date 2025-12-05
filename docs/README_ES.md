<<<<<<< HEAD
# Documentacion de Far-Bot v2.0.0 (Español)
=======
# Documentacion de Far-Bot (Español)
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c

## Tabla de Contenidos

1. [Introduccion](#introduccion)
2. [Instalacion](#instalacion)
<<<<<<< HEAD
3. [Panel Web](#panel-web)
4. [Constructor de Comandos](#constructor-de-comandos)
5. [Sistema AutoMod](#sistema-automod)
6. [Slash Commands](#slash-commands)
7. [Referencia de Variables](#referencia-de-variables)
=======
3. [Configuracion](#configuracion)
4. [Panel Web](#panel-web)
5. [Constructor de Comandos](#constructor-de-comandos)
6. [Referencia de Variables](#referencia-de-variables)
7. [Comandos Avanzados](#comandos-avanzados)
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
8. [Referencia de API](#referencia-de-api)
9. [Solucion de Problemas](#solucion-de-problemas)

---

## Introduccion

<<<<<<< HEAD
Far-Bot v2.0.0 es una plataforma completa de gestion de bots de Discord. Incluye constructor visual de comandos, sistema de mensajes automaticos (bienvenida/despedida), soporte para slash commands y mucho mas.

### Repositorio

- GitHub: [https://github.com/farllirs/farllirs-bots](https://github.com/farllirs/farllirs-bots)
=======
Far-Bot es una plataforma de gestion de bots de Discord disenada para hacer la creacion de bots accesible para todos. Ya seas un principiante que quiere respuestas de texto simples o un desarrollador avanzado que necesita control total con Python, Far-Bot tiene lo que necesitas.

### Conceptos Clave

- **Bot**: Una aplicacion de Discord que se conecta a tu servidor
- **Comando**: Una accion activada por un mensaje (ej: `!hola`)
- **Trigger**: La palabra que activa un comando
- **Respuesta**: Lo que el bot envia de vuelta
- **Variable**: Marcadores dinamicos reemplazados con datos reales
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c

---

## Instalacion

<<<<<<< HEAD
```bash
# 1. Clonar repositorio
git clone https://github.com/farllirs/farllirs-bots.git
cd farllirs-bots

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Lanzar
python launcher.py
```

=======
### Prerequisitos

1. **Python 3.8+**: Descargar de [python.org](https://python.org)
2. **pip**: Usualmente incluido con Python
3. **Token de Bot de Discord**: Crear en [Portal de Desarrolladores de Discord](https://discord.com/developers/applications)

### Instalacion Paso a Paso

```bash
# 1. Descargar Far-Bot
git clone https://github.com/farllirs/far-bot.git
cd far-bot

# 2. Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 3. Instalar dependencias
python installer.py

# 4. Ejecutar el instalador para configuracion inicial
python installer.py

# 5. Lanzar Far-Bot
python launcher.py
```

### Crear un Bot de Discord

1. Ve al [Portal de Desarrolladores de Discord](https://discord.com/developers/applications)
2. Haz clic en "New Application" y dale un nombre
3. Ve a la seccion "Bot" y haz clic en "Add Bot"
4. Copia el Token (mantenlo en secreto!)
5. Habilita estos Intents:
   - Presence Intent
   - Server Members Intent
   - Message Content Intent
6. Ve a OAuth2 > URL Generator
7. Selecciona scopes: `bot`, `applications.commands`
8. Selecciona los permisos que tu bot necesita
9. Copia la URL e invita el bot a tu servidor

---

## Configuracion

### Configuracion del Bot

Cada bot puede configurarse con:

| Opcion | Descripcion | Por Defecto |
|--------|-------------|-------------|
| Token | Tu token del bot de Discord | Requerido |
| Prefijo | Prefijo de comandos | `!` |
| Nombre | Nombre mostrado en el panel | Nombre de usuario del bot |
| Auto-inicio | Iniciar cuando Far-Bot arranque | `false` |

### Configuracion del Servidor

Edita `config.json` o usa el instalador:

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

## Panel Web

<<<<<<< HEAD
### Dashboard Principal

- **Bots**: Ver y gestionar todos tus bots
- **Comandos**: Crear, editar y eliminar comandos
- **AutoMod**: Configurar mensajes automaticos por servidor
- **Editor**: Editor avanzado de comandos Python

### Acceso

Abre tu navegador en `http://localhost:5000`
=======
### Dashboard

El dashboard principal muestra:
- Bots activos y su estado
- Total de comandos en todos los bots
- Cantidad de servidores
- Actividad reciente

### Gestion de Bots

- **Agregar Bot**: Haz clic en el boton "Nuevo Bot"
- **Iniciar/Detener**: Usa los botones de play/stop
- **Editar**: Haz clic en una tarjeta de bot para modificar configuraciones
- **Eliminar**: Elimina un bot y todos sus comandos

### Gestion de Comandos

- **Ver Comandos**: Haz clic en un bot para ver sus comandos
- **Agregar Comando**: Elige modo Simple o Avanzado
- **Editar Comando**: Haz clic en un comando para modificarlo
- **Eliminar Comando**: Elimina comandos individuales
- **Importar/Exportar**: Respalda y restaura comandos
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c

---

## Constructor de Comandos

### Modo Simple

<<<<<<< HEAD
Ideal para respuestas de texto con variables:

```
Trigger: hola
Respuesta: Hola $mention! Bienvenido a $servername!
=======
El Constructor de Comandos Simple es perfecto para:
- Respuestas de texto
- Mensajes de bienvenida
- Comandos de informacion
- Respuestas de FAQ

#### Crear un Comando Simple

1. Ingresa el **Trigger** (nombre del comando sin prefijo)
2. Escribe la **Respuesta** (usa variables para contenido dinamico)
3. Agrega una **Descripcion** (opcional)
4. Haz clic en **Guardar**

#### Ejemplos de Comandos Simples

**Comando de Saludo**
```
Trigger: hola
Respuesta: Hola $username! 👋 Bienvenido a **$servername**!
```

**Info del Servidor**
```
Trigger: servidor
Respuesta: 📊 **$servername**
Miembros: $membercount
Canal: $channel
```

**Respuesta Aleatoria**
```
Trigger: dado
Respuesta: 🎲 $username saco un $random (1-100)!
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
```

### Modo Avanzado

<<<<<<< HEAD
Para comandos Python completos:

```python
@bot.command(name='dado')
async def dado_cmd(ctx, caras: int = 6):
    import random
    resultado = random.randint(1, caras)
    await ctx.send(f"🎲 Sacaste: {resultado}")
```

---

## Sistema AutoMod

### Acceso

Click en "AutoMod" en el sidebar o accede a `/automod.html`

### Funciones

1. **Mensajes de Bienvenida**
   - Mensaje cuando alguien se une
   - Opcion de embed con colores
   - Mensaje DM opcional

2. **Mensajes de Despedida**
   - Mensaje cuando alguien se va
   - Personalizable con variables

3. **Auto-Roles**
   - Asignar roles automaticamente a nuevos miembros

4. **Registro de Actividad**
   - Log de joins/leaves
   - Log de mensajes eliminados/editados

---

## Slash Commands

### Crear un Slash Command

En el editor avanzado, usa esta estructura:

```python
@bot.tree.command(name='ping', description='Muestra la latencia')
async def ping_slash(interaction: discord.Interaction):
    await interaction.response.send_message(f'Pong! {round(bot.latency * 1000)}ms')
```

### Sincronizar

Los slash commands se sincronizan automaticamente al iniciar el bot.

=======
El Constructor Avanzado permite codigo Python completo:

#### Crear un Comando Avanzado

1. Escribe tu codigo Python usando el decorador `@bot.command`
2. Usa el panel de plantillas para empezar rapido
3. Valida tu codigo antes de guardar
4. Haz clic en **Guardar**

#### Ejemplos de Comandos Avanzados

**Dado con Caras Personalizadas**
```python
@bot.command(name='dado')
async def dado_cmd(ctx, caras: int = 6):
    """Tira un dado con caras personalizadas"""
    import random
    if caras < 2:
        await ctx.send("El dado debe tener al menos 2 caras!")
        return
    resultado = random.randint(1, caras)
    await ctx.send(f"🎲 Sacaste un **{resultado}** (d{caras})")
```

**Info de Usuario con Embed**
```python
@bot.command(name='quien')
async def quien_cmd(ctx, member: discord.Member = None):
    """Muestra informacion del usuario"""
    member = member or ctx.author
    embed = discord.Embed(
        title=f"Sobre {member.name}",
        color=member.color
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Se unio", value=member.joined_at.strftime("%Y-%m-%d"))
    embed.add_field(name="Roles", value=len(member.roles))
    await ctx.send(embed=embed)
```

>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
---

## Referencia de Variables

<<<<<<< HEAD
### Usuario
| Variable | Descripcion |
|----------|-------------|
| `$username` | Nombre del usuario |
| `$mention` | Mencion @usuario |
| `$userid` | ID del usuario |
| `$avatar` | URL del avatar |

### Servidor
| Variable | Descripcion |
|----------|-------------|
| `$servername` | Nombre del servidor |
| `$membercount` | Cantidad de miembros |
| `$servericon` | URL del icono |

### Bot
| Variable | Descripcion |
|----------|-------------|
| `$botname` | Nombre del bot |
| `$prefix` | Prefijo actual |

### Tiempo
| Variable | Descripcion |
|----------|-------------|
| `$time` | Hora actual |
| `$date` | Fecha actual |

### Aleatorio
| Variable | Descripcion |
|----------|-------------|
| `$random` | Numero 1-100 |
| `$coin` | Cara/Cruz |
| `$8ball` | Respuesta magica |
=======
### Variables de Usuario

| Variable | Descripcion | Ejemplo de Salida |
|----------|-------------|-------------------|
| `$username` | Nombre del usuario | `Juan` |
| `$userid` | ID del usuario | `123456789012345678` |
| `$mention` | Menciona al usuario | `@Juan` |
| `$displayname` | Nombre mostrado | `Juanito` |
| `$discriminator` | Discriminador | `1234` |
| `$avatar` | URL del avatar | `https://cdn.discord...` |

### Variables de Servidor

| Variable | Descripcion | Ejemplo de Salida |
|----------|-------------|-------------------|
| `$servername` | Nombre del servidor | `Mi Servidor` |
| `$serverid` | ID del servidor | `987654321098765432` |
| `$membercount` | Cantidad de miembros | `150` |
| `$servericon` | URL del icono | `https://cdn.discord...` |

### Variables de Canal

| Variable | Descripcion | Ejemplo de Salida |
|----------|-------------|-------------------|
| `$channel` | Nombre del canal | `general` |
| `$channelid` | ID del canal | `111222333444555666` |
| `$channelmention` | Mencion del canal | `#general` |

### Variables del Bot

| Variable | Descripcion | Ejemplo de Salida |
|----------|-------------|-------------------|
| `$botname` | Nombre del bot | `Far-Bot` |
| `$botid` | ID del bot | `999888777666555444` |
| `$botmention` | Mencion del bot | `@Far-Bot` |
| `$prefix` | Prefijo de comandos | `!` |

### Variables de Tiempo

| Variable | Descripcion | Ejemplo de Salida |
|----------|-------------|-------------------|
| `$time` | Hora actual | `14:30:45` |
| `$date` | Fecha actual | `2025-12-04` |
| `$datetime` | Fecha y hora completa | `2025-12-04 14:30:45` |
| `$day` | Nombre del dia | `Jueves` |
| `$month` | Nombre del mes | `Diciembre` |
| `$year` | Año | `2025` |

### Variables Especiales

| Variable | Descripcion | Ejemplo de Salida |
|----------|-------------|-------------------|
| `$random` | Aleatorio 1-100 | `42` |
| `$random(min,max)` | Aleatorio en rango | `$random(1,10)` → `7` |
| `$args` | Todos los argumentos | `hola mundo` |
| `$arg1`, `$arg2`... | Argumento especifico | `hola` |

---

## Comandos Avanzados

### Imports Permitidos

Por seguridad, solo estos modulos estan permitidos:
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

### Decoradores

```python
# Comando basico
@bot.command(name='cmd')
async def mi_cmd(ctx):
    pass

# Con alias
@bot.command(name='cmd', aliases=['c', 'comando'])
async def mi_cmd(ctx):
    pass

# Requerir permisos
@bot.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban_cmd(ctx, member: discord.Member):
    pass

# Cooldown
@bot.command(name='diario')
@commands.cooldown(1, 86400, commands.BucketType.user)
async def diario_cmd(ctx):
    pass
```

### Manejo de Errores

```python
@bot.command(name='dividir')
async def dividir_cmd(ctx, a: int, b: int):
    try:
        resultado = a / b
        await ctx.send(f"Resultado: {resultado}")
    except ZeroDivisionError:
        await ctx.send("No se puede dividir por cero!")
    except Exception as e:
        await ctx.send(f"Error: {e}")
```
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c

---

## Referencia de API

<<<<<<< HEAD
### Bots
| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | `/api/bots` | Listar bots |
| POST | `/api/bots` | Crear bot |
| POST | `/api/bots/{id}/start` | Iniciar bot |
| POST | `/api/bots/{id}/stop` | Detener bot |

### Comandos
| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | `/api/bots/{id}/commands` | Listar comandos |
| POST | `/api/bots/{id}/commands` | Crear comando |
| DELETE | `/api/bots/{id}/commands/{cmd}` | Eliminar comando |

### AutoMod
| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | `/api/bots/{id}/automod/{guild}` | Obtener config |
| PUT | `/api/bots/{id}/automod/{guild}` | Actualizar config |

=======
### Endpoints

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | `/api/bots` | Listar todos los bots |
| POST | `/api/bots` | Crear nuevo bot |
| GET | `/api/bots/{id}` | Obtener detalles del bot |
| PUT | `/api/bots/{id}` | Actualizar bot |
| DELETE | `/api/bots/{id}` | Eliminar bot |
| POST | `/api/bots/{id}/start` | Iniciar bot |
| POST | `/api/bots/{id}/stop` | Detener bot |
| GET | `/api/bots/{id}/commands` | Listar comandos |
| POST | `/api/bots/{id}/commands` | Agregar comando |
| PUT | `/api/bots/{id}/commands/{cmd}` | Actualizar comando |
| DELETE | `/api/bots/{id}/commands/{cmd}` | Eliminar comando |

>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
---

## Solucion de Problemas

<<<<<<< HEAD
### El bot no responde

1. Verifica que Message Content Intent este habilitado en Discord Developer Portal
2. Verifica que el prefijo sea correcto
3. Revisa que el comando este habilitado

### Los slash commands no aparecen

1. Espera unos minutos (Discord puede tardar en sincronizar)
2. Reinicia el bot desde el panel
3. Verifica que el bot tenga el scope `applications.commands`

### Error "Response is required"

- Los comandos simples DEBEN tener una respuesta
- No dejes el campo de respuesta vacio

### Obtener Ayuda

- GitHub Issues: [https://github.com/farllirs/farllirs-bots/issues](https://github.com/farllirs/farllirs-bots/issues)
=======
### Problemas Comunes

**El bot no responde a comandos**
- Verifica que Message Content Intent este habilitado
- Verifica que el prefijo sea correcto
- Asegurate que el comando este habilitado

**Error "Token invalido"**
- Regenera tu token de bot
- Asegurate que no haya espacios extra

**Los comandos no se guardan**
- Verifica los permisos de archivos
- Verifica que el directorio de datos exista

**El panel no carga**
- Verifica que el puerto 5000 este disponible
- Intenta con un navegador diferente

### Obtener Ayuda

- Revisa [GitHub Issues](https://github.com/farllirs/far-bot/issues)
- Unete a nuestro [Servidor de Discord](https://discord.gg/farbot)
- Lee el [FAQ](docs/FAQ_ES.md)
>>>>>>> 9cf509251284ef38bf215d47a080c5df52a9b90c
