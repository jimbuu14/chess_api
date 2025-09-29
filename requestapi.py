import requests

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def get_best_player_and_post_in_db():
    url_single_player = "https://api.chess.com/pub/player/"
    url_leaderboards = "https://api.chess.com/pub/leaderboards"

    response = requests.get(url=url_leaderboards,headers=headers)
    player_data = response.json()

    post_best_players_in_db(url_single_player, player_data)

   
def post_best_players_in_db(url_single_player, player_data):   
    for rapid_player in player_data["live_rapid"]:
        player_dict = {"username": "","vorname": "", "name": "", "rapid": 0, "blitz": 0, "bullet": 0}
        player_dict["username"] = rapid_player["username"]

        name = rapid_player.get("name")
        if name == None:
            name = ("None", "None")
        else:
            name = name.split()

        player_dict["name"] = name[1]
        player_dict["vorname"] = name[0]
        player_dict["rapid"] = rapid_player["score"]

        for blitz_player in player_data["live_blitz"]:
            if blitz_player["username"] == player_dict["username"]:
                player_dict["blitz"] = blitz_player["score"]

        if player_dict["blitz"] == 0:
            username = player_dict["username"]
            response_blitz = requests.get(url=f"{url_single_player}{username}/stats",headers=headers)
            response_data = response_blitz.json()

            if "chess_blitz" in response_data:
                player_dict["blitz"] = response_data["chess_blitz"]["last"]["rating"]
            else:
                player_dict["blitz"] = 0
        
        for bullet_player in player_data["live_bullet"]:
            if bullet_player["username"] == player_dict["username"]:
                player_dict["bullet"] = bullet_player["score"]

        if player_dict["bullet"] == 0:
            username = player_dict["username"]
            response_bullet = requests.get(url=f"{url_single_player}{username}/stats",headers=headers)
            response_data = response_bullet.json()

            if "chess_bullet" in response_data:
                player_dict["bullet"] = response_data["chess_bullet"]["last"]["rating"]
            else:
                player_dict["bullet"] = 0

        requests.post(url="http://localhost:8000/newplayers", json=player_dict)


if __name__ == "__main__":
    get_best_player_and_post_in_db()


# Funktionen in Teilfunktionen unterteilen und eine mögliche Eingabe einbauen ob top 50 in rapid, blitz oder bullet in DB eingetragen werden sollen