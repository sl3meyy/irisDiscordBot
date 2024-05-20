import json
from dotenv import load_dotenv
import os
import discord
from discord import Intents, Client, Message, Role
import subprocess
import requests

# Lese den Token aus der Datei
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

# Lese die Konfiguration aus der JSON-Datei
with open("iris.json", "r") as f:
    config = json.load(f)

# Extrahiere die Konfigurationsdaten
orga_kasse = config.get("orgaKasse")
team_members = config.get("teamMembers")

# Erstelle den Discord-Client
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

# Definiere die ID des Channels
channel_id = 1238985131448864861

# Antwortnachrichten
response_message_test = "Everything is fine"
response_message_clear = "Channel cleared!"
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
    # Überprüfe, ob die Nachricht im gewünschten Channel oder eine DM ist
    if message.channel.id == channel_id or isinstance(message.channel, discord.DMChannel):
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
                await client.close()  # Bot nach dem Update beenden
            elif command == "/version":
                version = config.get("version")
                await message.channel.send(f"Bot is on Version: {version}")
            return  # Befehl wurde ausgeführt, Schleife verlassen
    await message.channel.send("You do not have permission to execute this command.")

# Funktion zum Löschen des Channels
async def clear_channel(channel):
    await channel.purge()
    await channel.send(response_message_clear)

# Funktion zum Aktualisieren des Bots
def update():
    repo_owner = "sl3meyy"
    repo_name = "irisDiscordBot"

    # Hole das neueste Release von GitHub
    releases_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    response = requests.get(releases_url)

    if response.status_code == 200:
        release_data = response.json()
        tag_name = release_data["tag_name"]
        assets = release_data.get("assets", [])  # Sichere Methode, um Assets abzurufen

        if assets:  # Überprüfen, ob Assets vorhanden sind
            asset_url = assets[0]["browser_download_url"]

            # Stoppe den aktuellen Bot-Prozess
            client.close()  # Korrigiert: Asynchrone Funktion await client.close() verwenden

            # Downloade das neueste Release
            subprocess.run(["curl", "-L", asset_url, "-o", "irisDiscordBot.zip"])

            # Entpacke das Release
            subprocess.run(["tar", "-xf", "irisDiscordBot.zip"])

            # Starte den Bot neu
            subprocess.Popen(["python", "irisDiscordBot/main.py"])

        else:
            print(f"Keine Assets im Release {tag_name} gefunden.")

    else:
        print(f"Fehler beim Abrufen des neuesten Releases: {response.status_code}")


# Main-Funktion
if __name__ == '__main__':
    client.change_presence(status="dnd")
    client.run(token)
