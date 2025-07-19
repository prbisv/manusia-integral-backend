import requests
import json

API_URL = "http://localhost:8000/ask"

with open("sample_user_points.json") as f:
    base_payload = json.load(f)

# Example user questions
user_messages = [
    "Melihat destiny matrix saya, Apa kelebihan dari diri saya?",
    "Melihat destiny matrix saya, Apa kelemahan dari diri saya?",
    "Melihat destiny matrix saya, apa hal yang ada di masa lalu saya yang perlu saya perbaiki untuk masa depan?",
    "Dengan mencocokkan destiny matrix, apa karir yang cocok untuk saya?",
    "Bagaimana kriteria yang cocok untuk saya dalam memilih pasangan hidup dengan melihat destiny matrix saya?"
]

for user_message in user_messages:
    payload = base_payload.copy()
    payload["message"] = user_message

    response = requests.post(API_URL, json=payload)
    # print("Status:", response.status_code)
    print("Pertanyaan:", user_message)
    try:
        print("Response:", response.json().get('response', response.text))
    except Exception as e:
        print("Response error:", response.text)
    print()
