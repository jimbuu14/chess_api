import requests

# Neuen Spieler als dictionary anlegen
newplayer = {
  "vorname": "Mark",
  "name": "Mustermann",
  "classical": 100,
  "rapid": 200,
  "blitz": 300
}

# Neuen Spieler einfügen
requests.post(url="http://localhost:8000/newplayers", json=newplayer)

# Spieler mit meisten rapid Elo ausgegeben
param = {"minormax": "max"}
maxrapid = requests.get(url="http://localhost:8000/maxplayer/rapid", params=param)
print(maxrapid.json())



    
