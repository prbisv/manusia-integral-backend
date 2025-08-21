import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

API_URL = os.getenv("APP_ID")

if not API_URL:
    print("API_URL environment variable is not set.")
    exit()

# Sample payload for couple compatibility analysis
payload = {
    "person1": {
        "name": "namaorangpertama",
        "date": "2025-07-01"
    },
    "person2": {
        "name": "namaorangkedua",
        "date": "2025-07-02"
    },
    "points": {
        "apoint": 1,
        "bpoint": 7,
        "cpoint": 9,
        "dpoint": 17,
        "epoint": 7,
        "fpoint": 8,
        "gpoint": 16,
        "hpoint": 18,
        "ipoint": 8,
        "jpoint": 6,
        "kpoint": 10,
        "lpoint": 22,
        "mpoint": 11,
        "npoint": 16,
        "opoint": 9,
        "ppoint": 21,
        "qpoint": 7,
        "rpoint": 5,
        "spoint": 8,
        "tpoint": 14,
        "upoint": 5,
        "vpoint": 12,
    },
    "message": "Bagaimana kecocokan kami sebagai pasangan berdasarkan destiny matrix?"
}

# Send the request to the API
response = requests.post(f"{API_URL}askcouple", json=payload)
print(f"Status code: {response.status_code}")

try:
    result = response.json()
    print("\nResponse:")
    print(f"Thread ID: {result.get('thread_id')}")
    print(f"Analysis: {result.get('response')}")
except Exception as e:
    print(f"Error parsing response: {e}")
    print(f"Raw response: {response.text}")
