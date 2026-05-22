from dotenv import load_dotenv
import os
import base64
import requests
import json

import pandas as pd
import numpy as np


load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


def get_token():

    url = "https://accounts.spotify.com/api/token"

    auth = CLIENT_ID + ":" + CLIENT_SECRET
    auth = base64.b64encode(auth.encode("utf-8")).decode("utf-8")

    headers = {
        "Authorization" : "Basic " + auth
    }

    data = {"grant_type":"client_credentials"}

    r = requests.post(url = url, headers = headers, data = data)



    with open("output.txt", "w") as f:
        f.write(json.dumps(r.json(), indent = 4))

    return

def get_auth_header(token):

    headers = {
        "Authorization": "Bearer " + token
    }

    return headers
