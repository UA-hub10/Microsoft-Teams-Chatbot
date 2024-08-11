import json
import requests

def monitor(query, api):
    url = "https://united-db-api-teams-default-rtdb.firebaseio.com/apis.json"
    payload = {"api":api, "query":query}
    req = requests.post(url,data=json.dumps(payload))

