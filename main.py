import os
import json

import discord
from discord import Intents, Client, Message, Role

# Lese den Token aus der Datei
with open("token.txt", "r") as f:
    token = f.read().strip()

# Lese die Konfiguration aus der JSON-Datei
with open("iris.json", "r") as f:
    config = json.load(f)

# Extrahiere die Konfigurationsdaten
orga_kasse = config.get("orgaKasse", 100)
team_members = config.get("teamMembers", [])

# Erstelle den Discord-Client
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

# Definiere die ID des Channels
channel_id = 123456789012345678  # Hier die tatsächliche Channel-ID eintragen

# Antwortnachricht für /test
response_message_test = "Everything is fine"
# Antwortnachricht für /clear
response_message_clear = "Channel cleared!"
# Antwortnachricht für /balance
response_message_balance = f"OrgaKasse: {orga_kasse}"

# Rollen IDs
role_ids = [123456789012345678,  # Hier die tatsächlichen Rollen-IDs eintragen
            234567890123456789,
            345678901234567890]

# Mapping von Befehlen zu erlaubten Rollen
command_roles = {
    '/clear': [role_ids[0]],
    '/balance': role_ids
}

# Event für den Bot-Start
@client.event
async def on_ready():
    print(f'{client.user} is now running!')

# Event für eingehende Nachrichten
@client.event
async def on_message(message: Message):
    # Überprüfe, ob die Nachricht im gewünschten Channel ist
    if message.channel.id == channel_id:
        if message.content.startswith('/test'):
            await message.channel.send(response_message_test)
        elif message.content.startswith('/clear'):
            await clear_channel(message.channel, message.author.roles)
        elif message.content.startswith('/balance'):
            await message.channel.send(response_message_balance)
    # Überprüfe, ob die Nachricht eine private Nachricht an den Bot ist
    elif isinstance(message.channel, discord.DMChannel):
        if message.content.startswith('/test'):
            await message.author.send(response_message_test)

# Funktion zum Löschen des Channels
async def clear_channel(channel, user_roles):
    allowed_roles = command_roles['/clear']
    if any(role.id in allowed_roles for role in user_roles):
        await channel.purge()
        await channel.send(response_message_clear)
    else:
        await channel.send("You do not have permission to execute this command.")

# Main-Funktion

if __name__ == '__main__':
    client.run(token)
