import json
from dotenv import load_dotenv
import os
import discord
from discord import Intents, Client, Message, Role
import updater

#ToDo: /commands command should show different things based on users role (maybe dm?)
#ToDo: Bug fix, aktuell braucht man die 3er, 2er und 1er rolle wenn man einen 1er command ausführen will.
#ToDo: implement all commands -> release p-1.0
#ToDo: Rework commands completely


#ToDo: Bug fix (/test or other commands trigger updating)

# Lese den Token aus der Datei

# Lese die Konfiguration aus der JSON-Datei
with open("iris.json", "r") as f:
    config = json.load(f)

# Extrahiere die Konfigurationsdaten
orga_kasse = config.get("orgaKasse")
team_members = config.get("teamMembers")

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
# Erstelle den Discord-Client
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

# Definiere die ID des Channels
channel_id = 1238985131448864861

# Antwortnachricht für /test
response_message_test = "Everything is fine"
# Antwortnachricht für /clear
response_message_clear = "Channel cleared!"
# Antwortnachricht für /balance
response_message_balance = f"OrgaKasse: {orga_kasse}"

# Rollen IDs
role_ids = [
    config.get("devRole_id"),
    config.get("role1_id"),
    config.get("role2_id"),
    config.get("role3_id")
]

allCommands = [
    "Command: /clear -> clears all messages in current channel",
    "Command: /balance -> shows balance of orga",
    "Command: /test -> tests all Systems",
    "Command: /commands -> shows commands",
    "Command: /update -> Updates bot",
    "Command: /version -> Shows version",
]

# Mapping von Befehlen zu erlaubten Rollen
command_roles = {
    '/clear': [role_ids[0]],
    '/balance': role_ids,
    '/test': [role_ids[0]],
    '/commands': role_ids,
    '/update': [role_ids[0]],
    '/version': [role_ids[0]]
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
        for command, allowed_roles in command_roles.items():
            if message.content.startswith(command):
                await execute_command(message, command, allowed_roles)
                break
    # Überprüfe, ob die Nachricht eine private Nachricht an den Bot ist
    elif isinstance(message.channel, discord.DMChannel):
        for command, allowed_roles in command_roles.items():
            if message.content.startswith(command):
                await execute_command(message, command, allowed_roles)
                break

# Funktion zum Ausführen des Befehls
async def execute_command(message, command, allowed_roles):
    member_roles = [role.id for role in message.author.roles]
    for role_id in member_roles:
        if role_id in allowed_roles:
            if command == '/clear':
                await clear_channel(message.channel)
            elif command == '/balance':
                await message.channel.send(response_message_balance)
            elif command == '/test':
                await message.channel.send(response_message_test)
            elif command == '/commands':
                for i in allCommands:
                    await message.channel.send(i)
            elif command == "/update":
                await message.channel.send("Updating...")
                update()
                await client.close()
            elif command == "/version":
                version = config.get("version")
                await message.channel.send(f"Bot is on Version: {version}")
            elif command == "/tes2":
                await message.channel.send("tset 2 successful")
            return
    await message.channel.send("You do not have permission to execute this command.")

# Funktion zum Löschen des Channels
async def clear_channel(channel):
    await channel.purge()
    await channel.send(response_message_clear)

# Funktion zum Anzeigen der Befehle und den zugehörigen Rollen
async def display_commands(message):
    commands_list = ""
    for command, allowed_roles in command_roles.items():
        roles = [role.name for role in message.guild.roles if role.id in allowed_roles]
        commands_list += f"{command} - Allowed roles: {', '.join(roles)}\n"
    await message.channel.send(commands_list)
def update():
    updater.run()

# Main-Funktion
if __name__ == '__main__':
    client.change_presence(status=discord.Status.do_not_disturb)
    client.run(token)
    pid = os.getpid()
    with open("bot_pid.txt", "w") as f:
        f.write(str(pid))