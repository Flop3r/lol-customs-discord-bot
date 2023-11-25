import discord
import responses

from global_vars import PREFIX

async def send_message(message, message_content):
    try:
        response = responses.handle_response(message)
        await message.channel.send(response)

    except Exception as e:
        print(e)


def client_run(TOKEN):
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

        if message_content[0] == PREFIX:
            message_content = message_content[1:]
            await send_message(message, message_content)


    client.run(TOKEN)