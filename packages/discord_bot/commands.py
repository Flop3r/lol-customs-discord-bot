import re
from .embed_responses import *
from ..game_handler.game import *
from .player_riot_api_handler import *

async def handle_command(message, command):
    try:
        main_command, command_args = parse_command_args(command)

        if main_command == "hello":
            await handle_hello_command(message)
        elif main_command == "ping":
            await handle_ping_command(message)
        elif main_command == "get":
            await handle_get_command(message, command_args)
        elif main_command == "set":
            await handle_set_command(message, command_args)

    except Exception as e:
        await message.reply(embedded_response(ERROR_RESPONSE.format(str(e))), mention_author=False)

def parse_command_args(command):
    matches = re.findall(r'\"(.*?)\"|(\S+)', command)
    command_args = [match[0] if match[0] else match[1] for match in matches]

    return command_args[0].lower(), command_args[1:]

async def handle_hello_command(message):
    await embed_reply(message, HELLO_RESPONSE)

async def handle_ping_command(message):
    await embed_reply(message, PONG_RESPONSE)

async def handle_set_command(message, args):
    try:
        if len(args) < 2:
            raise ValueError(MISSING_ARGUMENTS_RESPONSE.format("set <argument> <wartość>"))

        argument = args[0]

        if argument == 'riot_id':
            riot_id = args[1].strip('"')

            puuid, game_name, tag_line = decode_riot_id(riot_id)
            if puuid:
                user_id = str(message.author.id)
                response = set_riot_id(user_id, puuid, game_name, tag_line)
            else:
                response = SET_RIOT_ID_RESPONSE
        else:
            response = INVALID_ARGUMENT_RESPONSE.format(argument)

        await embed_reply(message, response)

    except ValueError as ve:
        await embed_reply(message, embedded_response(ERROR_RESPONSE.format(str(ve))))

async def handle_get_command(message, args):
    try:
        if len(args) < 1:
            raise ValueError(MISSING_ARGUMENTS_RESPONSE.format("get <argument>"))

        argument = args[0]

        if argument == 'players_status':
            response = get_players_status()
        elif argument == 'riot_id':
            user_id = str(message.author.id)
            response = get_riot_id(user_id)
            response = RIOT_ID_RESPONSE_TEMPLATE.format(response)

        else:
            response = INVALID_ARGUMENT_RESPONSE.format(argument)

        await embed_reply(message, response)

    except ValueError as ve:
        await message.reply(embedded_response(ERROR_RESPONSE.format(str(ve))), mention_author=False)

def decode_riot_id(riot_id):
    try:
        riot_id = riot_id.strip('"')
        game_name, tag_line = riot_id.split('#')

        if is_valid_riot_id(game_name, tag_line):
            puuid = get_puuid(game_name, tag_line)
            return puuid, game_name, tag_line
        else:
            return None, None, None

    except ValueError:
        return None, None, None
