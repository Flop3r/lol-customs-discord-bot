import json
import re, requests

from .responses import *
from ..game_handler.game import add_player
from .global_vars import RIOT_API

async def handle_command(message, message_content):
    message_content = message_content.lower()

    # Splitting the message content into a command and a list of arguments
    command, *args = message_content.split(maxsplit=2)

    try:
        if command == "hello":
            await message.reply(HELLO_RESPONSE, mention_author=False)

        elif command == "add":
            response = handle_add_command(args, message.guild)
            await message.reply(response, mention_author=False)

        elif command == "json":
            with open('Data/Players.json', 'r') as file:
                data = json.load(file)
            await message.reply(data, mention_author=False)

        else:
            await message.reply(INVALID_COMMAND_RESPONSE, mention_author=False)

    except Exception as e:
        print(e)

def handle_add_command(args, guild) -> str:
    print(f"Debug: args = {args}")
    print(f"Debug: args[0] = {args[0]}")
    print(f"Debug: args[1] = {args[1]}")
    # Helper function to check if the argument has a valid format
    def is_valid_arg(arg) -> bool:
        return bool(re.match(r'<@(\d{18})>', arg))

    # Helper function to check if the argument has a valid format
    def is_valid_arg2(arg) -> bool:
        return bool(re.match(r'^.+#\w{4}$', arg))

    # Helper function to extract player ID from a valid argument
    def extract_user_id(arg) -> str:
        return re.match(r'<@(\d{18})>', arg).group(1)


    # Check if the number of arguments is correct and if the argument is valid
    if len(args) != 2:
        return INVALID_ARGUMENT_RESPONSE
    if not is_valid_arg(args[0]):
        return f"{INVALID_ARGUMENT_RESPONSE}: {args[0]}"
    if not is_valid_arg2(args[1]):
        return f"{INVALID_ARGUMENT_RESPONSE}: {args[1]}"

    user_id = extract_user_id(args[0])
    member = guild.get_member(int(user_id))

    if member and is_valid_riot_id(args[1]):
        add_player(user_id, args[1])
        return USER_ADDED_RESPONSE
    else:
        return USER_NOT_FOUND_RESPONSE



def is_valid_riot_id(riot_id):
    game_name, tag_line = riot_id.split('#')

    base_url = "https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id"
    endpoint = f"{game_name}/{tag_line}"
    url = f"{base_url}/{endpoint}?api_key={RIOT_API}"

    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        print(f"Gracz o nicku {game_name}#{tag_line} istnieje.")
        return True
    elif response.status_code == 404:
        print(f"Gracz o nicku {game_name}#{tag_line} nie istnieje.")
        return False
    else:
        print(f"Błąd podczas sprawdzania gracza. Kod odpowiedzi: {response.status_code}")
        return False