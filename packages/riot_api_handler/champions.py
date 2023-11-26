import requests
import json

from packages.discord_bot.global_vars import RIOT_API


def get_champions():
    url = 'https://ddragon.leagueoflegends.com/cdn/13.23.1/data/en_US/champion.json'
    response = requests.get(url)
    data = json.loads(response.content)

    return data['data']

def key_to_name(champion_key):
    champions = get_champions()

    for key, data in champions.items():
        if data['key'] == champion_key:
            return data['name']

    return None

def get_free_rotation():
    url = f'https://eun1.api.riotgames.com/lol/platform/v3/champion-rotations?api_key={RIOT_API}'
    response = requests.get(url)
    data = json.loads(response.content)

    rotation_keys = data['freeChampionIds']
    rotation_keys = [str(champion_key) for champion_key in rotation_keys]

    response = [key_to_name(str(champion_key)) for champion_key in rotation_keys]
    return response