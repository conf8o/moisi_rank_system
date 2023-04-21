import requests

from uuid import uuid4
from random import randint
import json

url_prefix = "http://localhost:8080/matching"

def entry(name, point):
    return {"players": [{"id": str(uuid4()), "name": name, "point": point}]}

def make_random_entry():
    url = url_prefix + "/entries"
    for i in range(20):
        e = entry(str(i), randint(5, 20))
        res = requests.post(url, json=e)
        print(res.json())

def print_entry_list():
    url = url_prefix + "/entries"
    res = requests.get(url)
    print(res.status_code)

    entries = res.json()
    if entries:
        for entry in entries:
            players = entry["players"]
            print(", ".join(f"{p['name']}({p['point']}pt)" for p in players))

def make_match():
    print("Match Making")
    url = url_prefix + "/match_making"
    res = requests.post(url)
    print(res.status_code)

    matches = res.json()
    if matches:
        matches = res.json()["matches"]
        for match in matches:
            print(match["id"])

def print_match_list():
    print("Print Match List")
    url = url_prefix + "/matches"
    res = requests.get(url)

    matches = res.json()
    if matches:
        for match in matches:
            print(match["id"])

def print_match(id):
    print("Print Match")
    url = url_prefix + "/matches/" + id
    res = requests.get(url)
    match = res.json()
    if match:
        parties = res.json()["parties"]
        for party in parties:
            players = party["players"]
            avg = sum(p["point"] for p in players) / len(players)
            print(", ".join(f"{p['name']}({p['point']}pt)" for p in players), f" 平均: {avg}")

def commit_match(id):
    print("Commit Match")
    url = url_prefix + "/match_committing/" + id
    res = requests.post(url)
    print(res.status_code)

    match = res.json()
    if match:
        parties = res.json()["parties"]
        for party in parties:
            players = party["players"]
            avg = sum(p["point"] for p in players) / len(players)
            print(", ".join(f"{p['name']}({p['point']}pt)" for p in players), f" 平均: {avg}")


def players_to_discord_vc(match_id):
    pass
