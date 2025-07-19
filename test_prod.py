import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

API_URL = os.getenv("APP_ID")

if not API_URL:
    print("API_URL environment variable is not set.")
    exit()

with open("sample_user_points.json") as f:
    base_payload = json.load(f)

# Example user question
user_message = "Melihat destiny matrix saya, Apa kelebihan dari diri saya?"

payload = base_payload.copy()
payload["message"] = user_message

response = requests.post(API_URL+"ask", json=payload)
print("Pertanyaan:", user_message)
try:
    print("Response:", response.json().get('response', response.text))
except Exception as e:
    print("Response error:", response.text)