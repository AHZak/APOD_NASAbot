import requests
from config import HTTPS, PATH, SECRET_TKN, TG_REQ_URL


URL = TG_REQ_URL + "/setWebhook"
PARAMS = {
    'url'           : HTTPS + PATH,
    'secret_token'  : SECRET_TKN
}

r = requests.get(url=URL, json=PARAMS)

print(r.json())
