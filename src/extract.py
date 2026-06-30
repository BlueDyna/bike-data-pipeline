import os

import pandas as pd
import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

TELRAAM_API_KEY = os.getenv("TELRAAM_API_KEY")
if not TELRAAM_API_KEY:
    raise RuntimeError("TELRAAM_API_KEY is not set in the environment")

url = "https://telraam-api.net/v1/reports/traffic"

body = {
    "id": "9000001463",
    "time_start": "2025-10-25 00:00:00Z",
    "time_end": "2025-10-25 23:59:59Z",
    "level": "segments",
    "format": "per-hour"
}

headers = {"X-Api-Key": TELRAAM_API_KEY}
response = requests.post(url, headers=headers, json=body)
response.raise_for_status()
response_json = response.json()
dataframe = pd.DataFrame(response_json["report"])
dataframe.to_csv("test.csv")