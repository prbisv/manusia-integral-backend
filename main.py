from typing import Union
import os
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    # "https://manusiaintegral.com",
    # "http://localhost:8000",
    # "http://localhost:3000",
    "*"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # Allow all origins
    allow_credentials=False,           # Credentials not allowed with wildcard
    allow_methods=["*"],
    allow_headers=["*"],
)

class DestinyMatrixInput(BaseModel):
    name: str
    gender: str
    date: str
    points: Dict[str, Any]
    chartHeart: Dict[str, Any]
    purposes: Dict[str, Any]
    years: Dict[str, Any]
    message: str
    thread_id: Optional[str] = None

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
vector_key = os.getenv("VECTOR_STORE_ID")
system_prompt = os.getenv("PROMPT")
assistant_id = os.getenv("ASSISTANT_ID")

if not api_key or not vector_key or not system_prompt:
    raise ValueError("environment variable not set.")

client = OpenAI(api_key=api_key)

## to create an assistant, uncomment the following lines
## Note: This should be done only once, and the assistant_id should be stored in the
## environment variable for future use.

# assistant = client.beta.assistants.create(
#   name="Destiny Matrix analysis specialist",
#   instructions=system_prompt,
#   model="gpt-4o",
#   tools=[{"type": "file_search"}],
# )

assistant = client.beta.assistants.update(
  assistant_id=assistant_id,
  tool_resources={"file_search": {"vector_store_ids": [vector_key]}},
)

@app.post("/ask")
async def ask_destiny_matrix(input_data: DestinyMatrixInput):
    # Compose the user's message with all relevant data
    user_message = (
        f"Nama: {input_data.name}\n"
        f"Gender: {input_data.gender}\n"
        f"Tanggal Lahir: {input_data.date}\n"
        f"Points: {input_data.points}\n"
        f"ChartHeart: {input_data.chartHeart}\n"
        f"Purposes: {input_data.purposes}\n"
        f"Years: {input_data.years}\n"
        f"Pertanyaan: {input_data.message}"
    )

    # Create or use an existing thread
    if input_data.thread_id:
        thread_id = input_data.thread_id
        thread = client.beta.threads.retrieve(thread_id)
    else:
        thread = client.beta.threads.create(messages=[{"role": "user", "content": user_message}])
        thread_id = thread.id

    # Create a run and poll for completion
    run = client.beta.threads.runs.create_and_poll(thread_id=thread_id, assistant_id=assistant_id)
    messages = list(client.beta.threads.messages.list(thread_id=thread_id, run_id=run.id))
    message_content = messages[0].content[0].text

    return {
        "response": message_content.value,
        "thread_id": thread_id
    }