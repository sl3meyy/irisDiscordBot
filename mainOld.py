import discord
from discord.ext import commands

# Erstelle einen Bot-Client mit Intents
intents = discord.Intents.default()
intents.messages = True  # Aktiviere die Nachrichten-Intent
intents.guilds = True    # Aktiviere die Server-Intent
bot = commands.Bot(command_prefix='!', intents=intents)

# Event, das ausgelöst wird, wenn der Bot gestartet ist
@bot.event
async def on_ready():
    print('Bot ist bereit!')

# Event, das ausgelöst wird, wenn eine Nachricht im Discord-Server gesendet wird
@bot.event
async def on_message(message):
    # Ignoriere Nachrichten des Bots selbst
    if message.author == bot.user:
        return

    # Wenn die Nachricht '!ping' enthält, antworte mit 'Pong!'
    if message.content.startswith('!ping'):
        await message.channel.send('Pong!')
f = open("token.txt", "r")
token = f.read().replace("BOT_TOKEN=", "")
# Token des Bots - Stelle sicher, dass du deinen eigenen Token hier einfügst
bot.run(token)
