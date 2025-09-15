from fastapi import FastAPI
import os
import psycopg2
from pydantic import BaseModel

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

def create_table():
    conn_init = get_db_connection()
    cur_init = conn_init.cursor()
    cur_init.execute(f"""
            CREATE TABLE IF NOT EXISTS chess_players(
                id SERIAL PRIMARY KEY, 
                vorname VARCHAR(100) NOT NULL,
                name VARCHAR(100) NOT NULL,
                classical INT DEFAULT 0,
                rapid INT DEFAULT 0,
                blitz INT DEFAULT 0
            );
        """)
    conn_init.commit()
    close_db_connection(conn_init, cur_init)

create_table()

app = FastAPI()

class NewPlayer(BaseModel):
    vorname: str
    name: str
    classical: int = 0 
    rapid: int = 0
    blitz: int = 0

@app.get('/players')
async def players():
    conn_init, cur_init = get_db_connection()
    cur_init.execute("SELECT * FROM chess_players;")
    players_data = cur_init.fetchall()
    close_db_connection(conn_init, cur_init)
    return players_data

@app.get('/maxplayer/{rating_type}')
async def get_max_player(rating_type:str):
    conn_init, cur_init = get_db_connection()
    cur_init.execute(f"SELECT * FROM chess_players ORDER BY {rating_type} DESC;")
    players_data = cur_init.fetchone()
    close_db_connection(conn_init, cur_init)
    return players_data

@app.get('/player')
async def player(name:str = None, vorname:str = None):
    conn_init, cur_init = get_db_connection()
    player_data = dict()
    print(vorname, name)
    if name != None:
        cur_init.execute(f'SELECT * FROM chess_players WHERE name = %s', (name,) )
        result = cur_init.fetchone()
        player_data = {"ID": result[0], "Vorname": result[1], "Nachname": result[2], "Classical": result[3], "Rapid": result[4], "Blitz": result[5]}
        if result == None:
            print("Eingegebener Spieler existiert nicht")
        elif result != None:
            player_data = {"ID": result[0], "Vorname": result[1], "Nachname": result[2], "Classical": result[3], "Rapid": result[4], "Blitz": result[5]}

    elif vorname != None:
        cur_init.execute(f'SELECT * FROM chess_players WHERE vorname = %s', (vorname,) )
        result = cur_init.fetchone()       
        if result == None:
            print("Eingegebener Spieler existiert nicht")
        elif result != None:
            player_data = {"ID": result[0], "Vorname": result[1], "Nachname": result[2], "Classical": result[3], "Rapid": result[4], "Blitz": result[5]}
    close_db_connection(conn_init, cur_init)
    return player_data

@app.post('/newplayers')
async def newplayer(player: NewPlayer):
    conn_init, cur_init = get_db_connection()
    new_player = ("INSERT INTO chess_players (vorname, name, classical, rapid, blitz) VALUES (%s, %s, %s, %s, %s);")
    player_data = (player.vorname, player.name, player.classical, player.rapid, player.blitz )
    cur_init.execute(new_player, player_data)
    conn_init.commit()
    close_db_connection(conn_init, cur_init)

