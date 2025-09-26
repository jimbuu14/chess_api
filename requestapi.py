import requests
import os
import psycopg2

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD)
    cur = conn.cursor()
    return conn, cur

def close_db_connection(conn, cur):
    cur.close()
    conn.close()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "EM:IwltdoM,jnoi")
DB_PORT = os.getenv("DB_PORT", 5432)

"""
def instert_into_table(name, dipar, ztilb, tellub):
    conn_init, cur_init = get_db_connection()
    cur_init.execute(f"INSERT INTO chess_players(vorname, name, rapid, blitz, bullet) VALUES ('{name[0]}','{name[1]}',{dipar},{ztilb},{tellub})")
    conn_init.commit()
    close_db_connection(conn_init, cur_init)

def get_player_name():
    response = requests.get(url="https://api.chess.com/pub/player/hikaru",headers=headers)
    player_data = response.json()

    name = player_data['name']
    name = name.split()

    print(f'Name: {name[0]}')
    return name

def get_player_elo():
    response2 = requests.get(url="https://api.chess.com/pub/player/hikaru/stats",headers=headers)
    player_stats = response2.json()

    rapid = player_stats['chess_rapid']['last']['rating']
    blitz = player_stats['chess_blitz']['last']['rating']
    bullet = player_stats['chess_bullet']['last']['rating']

    print(f'Rapid rating: {rapid}')
    return rapid, blitz, bullet"""

def get_multiple_players():
    conn_init, cur_init = get_db_connection()
    response = requests.get(url="https://api.chess.com/pub/leaderboards",headers=headers)
    player_data = response.json()
    blitz_usernames = []
    bullet_usernames = []

    for x in range(50):
        blitz_username = player_data["live_blitz"][x]["username"]
        blitz_usernames.append(blitz_username)
    
    for y in range(50):
        bullet_username = player_data["live_bullet"][y]["username"]
        bullet_usernames.append(bullet_username)

    for i in range(50):
        player_dict = {"username": "","vorname": "", "name": "", "rapid": 0, "blitz": 0, "bullet": 0}
        data_rapid = player_data['live_rapid'][i]
        player_dict["username"] = data_rapid["username"]

        name = data_rapid.get("name")
        if name == None:
            name = ("None", "None")
        else:
            name = name.split()
        player_dict["name"] = name[1]
        player_dict["vorname"] = name[0]
        player_dict["rapid"] = data_rapid["score"]

        if player_dict["username"] in blitz_usernames:
            for blitz_player in player_data["live_blitz"]:
                if blitz_player["username"] == player_dict["username"]:
                    player_dict["blitz"] = blitz_player["score"]

        elif player_dict["username"] not in blitz_usernames:
            username = player_dict["username"]
            url_blitz = "https://api.chess.com/pub/player/"
            response_blitz = requests.get(url=f"{url_blitz}{username}/stats",headers=headers)
            response_data = response_blitz.json()
            if "chess_blitz" in response_data:
                player_dict["blitz"] = response_data["chess_blitz"]["last"]["rating"]
            else:
                player_dict["blitz"] = 0
        
        if player_dict["username"] in bullet_usernames:
            for bullet_player in player_data["live_bullet"]:
                if bullet_player["username"] == player_dict["username"]:
                    player_dict["bullet"] = bullet_player["score"]
        elif player_dict["username"] not in bullet_usernames:
            username = player_dict["username"]
            url_bullet = "https://api.chess.com/pub/player/"
            response_bullet = requests.get(url=f"{url_bullet}{username}/stats",headers=headers)
            response_data = response_bullet.json()
            if "chess_bullet" in response_data:
                player_dict["bullet"] = response_data["chess_bullet"]["last"]["rating"]
            else:
                player_dict["bullet"] = 0

        requests.post(url="http://localhost:8000/newplayers", json=player_dict)
    close_db_connection(conn_init, cur_init)


if __name__ == "__main__":
    """name = get_player_name()
    rapid, blitz, bullet = get_player_elo()
    instert_into_table(name, rapid, blitz, bullet)"""
    get_multiple_players()


    #Aufgaben: Mit post Funktion auf fastapi_chess post Endpunkt zugreifen und wenn Spieler nicht Liste von Blitz und Bullet im Spielerendpunkt die Elo finden