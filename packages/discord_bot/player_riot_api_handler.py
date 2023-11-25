# player_riot_api_handler.py
import json
import requests
from .global_vars import RIOT_API

def is_valid_riot_id(game_name, tag_line):
    base_url = "https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id"
    endpoint = f"{game_name}/{tag_line}"
    url = f"{base_url}/{endpoint}?api_key={RIOT_API}"

    response = requests.get(url)
    if response.status_code == 200:
        return True
    elif response.status_code == 404:
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
