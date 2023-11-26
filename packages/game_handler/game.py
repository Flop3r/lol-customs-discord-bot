import json
from packages.discord_bot.responses import *

# Function to check if a player exists in players_data
def if_player_exist(user_id, players_data) -> bool:
    return user_id in players_data

# SETTERS - functions

def set_riot_id(user_id, puuid, game_name, tag_line) -> str:
    try:
        with open('Data/Players.json', 'r', encoding='utf-8') as json_file:
            players_data = json.load(json_file)
    except Exception as e:
        print(FILE_ERROR_RESPONSE.format(str(e)))
        players_data = {}

    if not if_player_exist(user_id, players_data):
        # Add the player if they don't exist
        players_data[user_id] = {'puuid': puuid, 'game_name': game_name, 'tag_line': tag_line}
    else:
        # Update the existing player data
        players_data[user_id]['puuid'] = puuid
        players_data[user_id]['game_name'] = game_name
        players_data[user_id]['tag_line'] = tag_line

    try:
        with open('Data/Players.json', 'w', encoding='utf-8') as json_file:
            json.dump(players_data, json_file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(FILE_ERROR_RESPONSE.format(str(e)))
        return SAVING_FILE_ERROR_RESPONSE

    return RIOT_ID_CHANGED_RESPONSE.format(game_name, tag_line)

# GETTERS - functions

def get_players_status() -> dict:
    try:
        with open('Data/Players.json', 'r', encoding='utf-8') as json_file:
            players_data = json.load(json_file)
    except Exception as e:
        print(FILE_ERROR_RESPONSE.format(str(e)))
        players_data = {}

    return players_data

def get_riot_ids() -> list:
    try:
        with open('Data/Players.json', 'r') as file:
            data = json.load(file)

        riot_ids = []

        for key, value in data.items():
            game_name = value.get('game_name', '')
            tag_line = value.get('tag_line', '')
            riot_ids.append(f"{game_name}#{tag_line}")

        return riot_ids

    except FileNotFoundError as e:
        print(f"Plik Players.json nie istnieje.")
        return []


def get_riot_id(user_id) -> str:
    try:
        with open('Data/Players.json', 'r', encoding='utf-8') as json_file:
            players_data = json.load(json_file)
    except Exception as e:
        print(FILE_ERROR_RESPONSE.format(str(e)))
        players_data = {}

    if if_player_exist(user_id, players_data):
        game_name = players_data[user_id]['game_name']
        tag_line = players_data[user_id]['tag_line']

        return f"{game_name}#{tag_line.upper()}"
    return INVALID_PLAYER_RESPONSE
