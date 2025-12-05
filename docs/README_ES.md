# Documentacion de Far-Bot v2.0.0 (Español)

## Tabla de Contenidos

1. [Introduccion](#introduccion)
2. [Instalacion](#instalacion)
3. [Panel Web](#panel-web)
4. [Constructor de Comandos](#constructor-de-comandos)
5. [Sistema AutoMod](#sistema-automod)
6. [Slash Commands](#slash-commands)
7. [Referencia de Variables](#referencia-de-variables)
8. [Referencia de API](#referencia-de-api)
9. [Solucion de Problemas](#solucion-de-problemas)

---

## Introduccion

Far-Bot v2.0.0 es una plataforma completa de gestion de bots de Discord. Incluye constructor visual de comandos, sistema de mensajes automaticos (bienvenida/despedida), soporte para slash commands y mucho mas.

### Repositorio

- GitHub: [https://github.com/farllirs/farllirs-bots](https://github.com/farllirs/farllirs-bots)

---

## Instalacion

```bash
# 1. Clonar repositorio
git clone https://github.com/farllirs/farllirs-bots.git
cd farllirs-bots

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Lanzar
python launcher.py
```

---

## Panel Web

### Dashboard Principal

- **Bots**: Ver y gestionar todos tus bots
- **Comandos**: Crear, editar y eliminar comandos
- **AutoMod**: Configurar mensajes automaticos por servidor
- **Editor**: Editor avanzado de comandos Python

### Acceso

Abre tu navegador en `http://localhost:5000`

---

## Constructor de Comandos

### Modo Simple

Ideal para respuestas de texto con variables:

```
Trigger: hola
Respuesta: Hola $mention! Bienvenido a $servername!
```

### Modo Avanzado

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

---

## Referencia de Variables

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

---

## Referencia de API

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

---

## Solucion de Problemas

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
