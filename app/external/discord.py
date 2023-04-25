import requests
import json
from typing import Dict, Any
from dataclasses import dataclass

URL_PREFIX = "http://localhost:8831"

@dataclass
class Mock:
    status_code: int
    json_params: Dict[str, Any]
    
    def json(self):
        print(self.json_params)
        return "ok"    

def hook_v1_matching(json_params: Dict[str, Any]) -> Dict[str, Any]:
    url = URL_PREFIX + "/hook/v1/matching"
    res = requests.post(url, json=json_params)
    return {
        "status_code": res.status_code,
        "content": res.json()
    }
