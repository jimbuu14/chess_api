import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }


def get_best_player_and_post_in_db():
    url_single_player = "https://api.chess.com/pub/player/"
    url_leaderboards = "https://api.chess.com/pub/leaderboards"

    response = requests.get(url=url_leaderboards,headers=headers)
    player_data = response.json()

    post_best_players_in_db(url_single_player, player_data, "rapid")
    post_best_players_in_db(url_single_player, player_data, "blitz")
    post_best_players_in_db(url_single_player, player_data, "bullet")


def get_player_name(player):
    name = player.get("name")
    if name == None:
        name = ("None", "None")
        return name[1], name[0]
    else:
        name = name.split()   
        if len(name) >= 2:
            return name[1], name[0]
        elif len(name) == 1:
            return "None", name[0]


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
   

def post_best_players_in_db(url_single_player, player_data, modus):
    if modus == "rapid": 
        modus_2 = "blitz"
        modus_3 = "bullet"

    elif modus == "blitz": 
        modus_2 = "rapid"
        modus_3 = "bullet"

    elif modus == "bullet": 
        modus_2 = "blitz"
        modus_3 = "rapid"

    for player in player_data[f"live_{modus}"]:
            player_dict = {
                "username": player["username"],
                "vorname": "", 
                "name": "", 
                modus: player["score"], 
                modus_2: 0, 
                modus_3: 0
                }

            player_dict["name"], player_dict["vorname"] = get_player_name(player)
            player_dict[modus_2] = get_blitz_or_bullet_elo(url_single_player, player_data, player_dict["username"], modus_2)
            player_dict[modus_3] = get_blitz_or_bullet_elo(url_single_player, player_data, player_dict["username"], modus_3)
            username = player_dict["username"]
            response = requests.get(url=f"http://localhost:8000/username/{username}")
            response = response.json()
            if response == None:
                requests.post(url="http://localhost:8000/newplayers", json=player_dict)

if __name__ == "__main__":
    get_best_player_and_post_in_db()


