import re, requests

from .responses import *
from ..game_handler.game import *
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

        elif command == "get_players_data":
            await message.reply(get_players_data(), mention_author=False)

        elif command == "reset":
            reset_players_data()
            await message.reply(RESETED_RESPONSE, mention_author=False)

        else:
            await message.reply(INVALID_COMMAND_RESPONSE, mention_author=False)

    except Exception as e:
        print(e)

def handle_add_command(args, guild) -> str:
    def is_valid_arg_format(arg) -> bool:
        return bool(re.match(r'<@(\d{18})>', arg))

    def is_valid_arg2_format(arg) -> bool:
        return bool(re.match(r'^.+#.+$', arg))

    def extract_user_id(arg) -> str:
        return re.match(r'<@(\d{18})>', arg).group(1)

    if len(args) != 2:
        return INVALID_ARGUMENT_RESPONSE
    if not is_valid_arg_format(args[0]):
        return f"{INVALID_ARGUMENT_RESPONSE}: {args[0]}"
    if not is_valid_arg2_format(args[1]):
        return f"{INVALID_ARGUMENT_RESPONSE}: {args[1]}"

    user_id = extract_user_id(args[0])
    member = guild.get_member(int(user_id))

    game_name, tag_line = args[1].split('#')

    if not member:
        return USER_NOT_FOUND_RESPONSE
    elif not is_valid_riot_id(game_name, tag_line):
        return RIOT_USER_NOT_FOUND_RESPONSE
    else:
        puuid = get_puuid(game_name, tag_line)
        add_player(user_id, puuid, game_name, tag_line)
        return USER_ADDED_RESPONSE



def is_valid_riot_id(game_name, tag_line):
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

def get_puuid(game_name, tag_line):
    base_url = "https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id"
    endpoint = f"{game_name}/{tag_line}"
    url = f"{base_url}/{endpoint}?api_key={RIOT_API}"

    response = requests.get(url)
    data = json.loads(response.content)
    return data['puuid']
