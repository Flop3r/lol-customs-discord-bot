import json
def add_player(discord_id, riot_id= "nickname"):
    try:
        with open(f'Data/Players.json', 'r') as json_file:
            players_data = json.load(json_file)
    except FileNotFoundError:
        players_data = {}

    players_data[discord_id] = {
        'riot_id' : riot_id,
        'wins' : 0,
        'loses': 0
    }

    with open(f'Data/Players.json', 'w') as json_file:
        json.dump(players_data, json_file, indent=2)