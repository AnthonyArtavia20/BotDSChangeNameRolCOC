import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

intents = discord.Intents.default()
intents.members = True #Para poder detectar los miembros en el server
intents.message_content = True # PAra poder leer los comandos como los de cambio de nombre o Rol !name

bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.getenv('DISCORD_TOKEN') #Este se obtiene desde Discord Developers y ahorita está oculto para que no esté expuesto
ROL_VERIFICADO = os.getenv('ROL_VERIFICADO') #Este rol es el que creé como forma de identificar aquellos que ya se cambiaron el apodo y tienen acceso al resto de canales, no solo el de bienvenida.
ROL_PENDIENTE = os.getenv('ROL_PENDIENTE') #Como su nombre dice, este es para cuando la persona reciente entra al server y no se ha cambiado el nombre, osea pendiente de asignar rol.

@bot.event
async def on_ready():
  print(f"Own Bot {bot.user.name} is ready and online!")

@bot.command()
async def nombre(ctx, *, nickname):
  Channelmember = ctx.author
  try:
    #Cambio de apodo:
    await Channelmember.edit(nick=nickname)

    #Quitar el rol de "Sin verificar(...) para poder luego asignar el bueno"
    rol_pendiente = discord.utils.get(ctx.guild.roles, name=ROL_PENDIENTE)
    if rol_pendiente in Channelmember.roles:
      await Channelmember.remove_roles(rol_pendiente)

    #Dar el rol de verificado, "Nuevo Miembro":
    rol_nuevo = discord.utils.get(ctx.guild.roles, name=ROL_VERIFICADO)
    if rol_nuevo not in Channelmember.roles:
      await Channelmember.add_roles(rol_nuevo)

    await ctx.send(f"✅ ¡Nombre actualizado a **{nickname}** y acceso concedido! Recuerda leer el canal de reglas-del-clan")

  except discord.Forbidden:
    await ctx.send("No tengo permisos para cambiar tu apodo o rol o etc, admin revisa esto!")
  except Exception as delta:
    await ctx.send(f"Ocurrió el siguiente error: {delta}")

bot.run(TOKEN)