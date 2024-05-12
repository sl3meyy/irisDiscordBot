from typing import Final
import os
from discord.app_commands import commands
from discord import Intents, Client, Message
from random import choice, randint
from functions import *
f = open("token.txt", "r")
token = f.read().replace("BOT_TOKEN=", "")
#print(token)

#Setting up Bot

intents: Intents = Intents.default()
intents.message_content = True # NOQA
client: Client = Client(intents=intents)
bot = commands.Bot(command_prefix='$', intents=intents)
#Message functions

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('Messages was empty because intents were not enabled probably')
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

#Startup
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

#Handle incomming messages

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = str(message.content)
    channel: str = str(message.channel)
    print(f'[{channel}] {username}: ' +user_message)
    await send_message(message, user_message)


#main entry point

def main() -> None:
    client.run(token=token)

if __name__ == '__main__':
    main()




