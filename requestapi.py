import requests

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def get_best_player_and_post_in_db():
    url_single_player = "https://api.chess.com/pub/player/"
    url_leaderboards = "https://api.chess.com/pub/leaderboards"

    response = requests.get(url=url_leaderboards,headers=headers)
    player_data = response.json()

    post_best_players_in_db(url_single_player, player_data)


def get_player_name(rapid_player):
    name = rapid_player.get("name")
    if name == None:
        name = ("None", "None")
    else:
        name = name.split()

    return name[1], name[0]


def get_blitz_or_bullet_elo(url_single_player, player_data, username, modus):
    for player in player_data[f"live_{modus}"]:
        if player["username"] == username:
            return player["score"]

    response_player = requests.get(url=f"{url_single_player}{username}/stats",headers=headers)
    response_data = response_player.json()

    if f"chess_{modus}" in response_data:
        return response_data[f"chess_{modus}"]["last"]["rating"]
    else:
        return 0
   

def post_best_players_in_db(url_single_player, player_data):   
    for rapid_player in player_data["live_rapid"]:
        player_dict = {
            "username": rapid_player["username"],
            "vorname": "", 
            "name": "", 
            "rapid": rapid_player["score"], 
            "blitz": 0, 
            "bullet": 0
            }

        player_dict["name"], player_dict["vorname"] = get_player_name(rapid_player)
        player_dict["blitz"] = get_blitz_or_bullet_elo(url_single_player, player_data, player_dict["username"], "blitz")
        player_dict["bullet"] = get_blitz_or_bullet_elo(url_single_player, player_data, player_dict["username"], "bullet")

        requests.post(url="http://localhost:8000/newplayers", json=player_dict)


if __name__ == "__main__":
    get_best_player_and_post_in_db()


# Funktionen in Teilfunktionen unterteilen und eine mögliche Eingabe einbauen ob top 50 in rapid, blitz oder bullet in DB eingetragen werden sollen