import requests
import json

API_URL = "http://localhost:8000/ask"

with open("sample_user_points.json") as f:
    points = json.load(f)

# Example user question
user_message = "Apa makna utama dari destiny matrix saya?"

payload = {
    "points": points,
    "message": user_message
}

response = requests.post(API_URL, json=payload)
print("Status:", response.status_code)
print("Response:", response.json())
