import os
import json
from datetime import datetime, timezone
import requests
from dotenv import load_dotenv


today = datetime.now(timezone.utc).date()
today_str = today.strftime("%Y-%m-%d")

load_dotenv()
TELRAAM_API_KEY = os.getenv("TELRAAM_API_KEY")

url = "https://telraam-api.net/v1/reports/traffic"

body = {
    "id": "9000001463",
    "time_start": f"{today_str} 00:00:00Z",
    "time_end": f"{today_str} 23:59:59Z",
    "level": "segments",
    "format": "per-hour"
}
headers = {"X-Api-Key": TELRAAM_API_KEY}

response = requests.post(url, headers=headers, json=body)
response.raise_for_status()
data = response.json()

os.makedirs("raw", exist_ok=True)
filename = f"raw/telraam_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
with open(filename, "w") as f:
    json.dump(data, f)

print(f"Saved {len(data['report'])} records to {filename}")