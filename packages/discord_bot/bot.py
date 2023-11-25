import discord

from .commands import handle_command
from .global_vars import PREFIX, TOKEN

def client_run():
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print("Im ready")

    @client.event
    async def on_message(message):

        username = str(message.author)
        message_content = message.content
        channel = str(message.channel)

        print(f"{username} said: {message_content} on {channel}")

        if message_content.startswith(PREFIX):
            message_content = message_content[1:]
            await handle_command(message, message_content)


    client.run(TOKEN)

