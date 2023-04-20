import requests
from uuid import uuid4
from random import randint

url = "http://localhost:8080/matching/entries"

def entry(name, point):
    return {"players": [{"id": str(uuid4()), "name": name, "point": point}]}

for i in range(20):
    e = entry(str(i), randint(5, 20))
    res = requests.post(url, json=e)
    print(res.text)
