import json
def add_player(discord_id, puuid, game_name, tag_line):
    try:
        with open(f'Data/Players.json', 'r') as json_file:
            players_data = json.load(json_file)
    except FileNotFoundError:
        players_data = {}

    players_data[discord_id] = {
        'puuid' : puuid,
        'game_name' : game_name,
        'tag_line' : tag_line,
        'wins' : 0,
        'loses': 0
    }

    with open(f'Data/Players.json', 'w') as json_file:
        json.dump(players_data, json_file, indent=2)

def get_players_data():
    with open('Data/Players.json', 'r') as file:
        return json.load(file)

def reset_players_data():
    with open(f'Data/Players.json', 'w') as json_file:
        json.dump({}, json_file, indent=2)