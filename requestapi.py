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
    for i in range(10):
        response = requests.get(url="https://api.chess.com/pub/leaderboards",headers=headers)
        player_data = response.json()
        data = player_data['live_rapid'][i]
        username = data['username']
        name = data['name']
        name = name.split()
        score = data['score']
        conn_init, cur_init = get_db_connection()
        cur_init.execute(f"INSERT INTO chess_players(vorname, name, rapid) VALUES ('{name[0]}','{name[1]}',{score})")
        conn_init.commit()
        close_db_connection(conn_init, cur_init)
        i = i + 1
        print(username, name, score)

if __name__ == "__main__":
    """name = get_player_name()
    rapid, blitz, bullet = get_player_elo()
    instert_into_table(name, rapid, blitz, bullet)"""
    get_multiple_players()