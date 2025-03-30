import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Cargar el token del archivo .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Configurar el bot con el prefijo 'E!'
intents = discord.Intents.default()
intents.message_content = True  # Habilitar el contenido de los mensajes
bot = commands.Bot(command_prefix='E!', intents=intents)

# Base de datos en memoria
pokemon_registry = {}

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')

@bot.command(name="registrar")
async def registrar(ctx, nombre: str, nivel: int, ps: int, ataque: int, defensa: int, atq_esp: int, def_esp: int, velocidad: int):
    usuario = ctx.author.id

    if usuario not in pokemon_registry:
        pokemon_registry[usuario] = []

    pokemon_registry[usuario].append({
        "nombre": nombre.capitalize(),
        "nivel": nivel,
        "ps": ps,
        "ataque": ataque,
        "defensa": defensa,
        "atq_esp": atq_esp,
        "def_esp": def_esp,
        "velocidad": velocidad
    })

    await ctx.send(f'✅ {ctx.author.mention} ha registrado a **{nombre.capitalize()}** (Nivel {nivel}) correctamente.')

@bot.command(name="perfil")
async def perfil(ctx):
    usuario = ctx.author.id

    if usuario not in pokemon_registry or len(pokemon_registry[usuario]) == 0:
        await ctx.send(f'❌ {ctx.author.mention}, no tienes Pokémon registrados.')
        return

    mensaje = f'📜 **Pokémon de {ctx.author.name}:**\n'
    for i, poke in enumerate(pokemon_registry[usuario], start=1):
        mensaje += (
            f'**{i}. {poke["nombre"]}** (Nivel {poke["nivel"]})\n'
            f'PS: {poke["ps"]} | Ataque: {poke["ataque"]} | Defensa: {poke["defensa"]}\n'
            f'Ataque Esp.: {poke["atq_esp"]} | Defensa Esp.: {poke["def_esp"]} | Velocidad: {poke["velocidad"]}\n\n'
        )

    await ctx.send(mensaje)

@bot.command(name="edit")
async def edit(ctx, nombre: str, nuevo_nivel: int, ps: int, ataque: int, defensa: int, atq_esp: int, def_esp: int, velocidad: int):
    usuario = ctx.author.id

    if usuario not in pokemon_registry:
        await ctx.send(f'❌ {ctx.author.mention}, no tienes Pokémon registrados.')
        return

    for poke in pokemon_registry[usuario]:
        if poke["nombre"].lower() == nombre.lower():
            poke["nivel"] = nuevo_nivel
            poke["ps"] = ps
            poke["ataque"] = ataque
            poke["defensa"] = defensa
            poke["atq_esp"] = atq_esp
            poke["def_esp"] = def_esp
            poke["velocidad"] = velocidad
            await ctx.send(f'✅ {ctx.author.mention}, **{nombre.capitalize()}** ha sido actualizado a Nivel {nuevo_nivel}.')
            return

    await ctx.send(f'❌ {ctx.author.mention}, no se encontró a **{nombre.capitalize()}** en tu registro.')

@bot.command(name="delete")
async def delete(ctx, nombre: str):
    usuario = ctx.author.id

    if usuario not in pokemon_registry:
        await ctx.send(f'❌ {ctx.author.mention}, no tienes Pokémon registrados.')
        return

    for poke in pokemon_registry[usuario]:
        if poke["nombre"].lower() == nombre.lower():
            pokemon_registry[usuario].remove(poke)
            await ctx.send(f'🗑️ {ctx.author.mention}, **{nombre.capitalize()}** ha sido eliminado de tu registro.')
            return

    await ctx.send(f'❌ {ctx.author.mention}, no se encontró a **{nombre.capitalize()}** en tu registro.')

bot.run(TOKEN)





