import requests
from uuid import uuid4
from random import randint, shuffle, choice

url = "http://localhost:8080/matching/entries"

def make_entry(name, point):
    return {"players": [{"id": str(uuid4()), "name": name, "point": point}]}

players = [{"id": str(uuid4()), "name": f"player{i}", "point": randint(5, 20)} for i in range(60)]
shuffle(players)
kuji = [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3]

entries = []

while players:
    entry = []
    try:
        for _ in range(choice(kuji)):
            entry.append(players.pop())
        entries.append(entry)
        entry = []
    except IndexError:
        entries.append(entry)
        entry = []
        break
    
    
for entry in entries:
    res = requests.post(url, json={"players": entry})
    print(res.text)
