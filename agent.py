import os
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Dict, Any, Optional

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
vector_key = os.getenv("VECTOR_STORE_ID")
system_prompt = os.getenv("PROMPT")
if not api_key or not vector_key or not system_prompt:
    raise ValueError("environment variable not set.")

client = OpenAI(api_key=api_key)

assistant = client.beta.assistants.create(
  name="Destiny Matrix analysis specialist",
  instructions=system_prompt,
  model="gpt-4o",
  tools=[{"type": "file_search"}],
)

assistant = client.beta.assistants.update(
  assistant_id=assistant.id,
  tool_resources={"file_search": {"vector_store_ids": [vector_key]}},
)

app = FastAPI()

class DestinyMatrixInput(BaseModel):
    points: Dict[str, Any]
    message: str
    thread_id: Optional[str] = None

@app.post("/ask")
async def ask_destiny_matrix(input_data: DestinyMatrixInput):
    # Compose the user's message with the points
    points_str = "\n".join(f"{k}: {v}" for k, v in input_data.points.items())
    user_message = f"Data matrix:\n{points_str}\n\nPertanyaan: {input_data.message}"

    # Create or use an existing thread
    if input_data.thread_id:
        thread_id = input_data.thread_id
        thread = client.beta.threads.retrieve(thread_id)
    else:
        thread = client.beta.threads.create(messages=[{"role": "user", "content": user_message}])
        thread_id = thread.id

    # Create a run and poll for completion
    run = client.beta.threads.runs.create_and_poll(thread_id=thread_id, assistant_id=assistant.id)
    messages = list(client.beta.threads.messages.list(thread_id=thread_id, run_id=run.id))
    message_content = messages[0].content[0].text

    # Optionally, handle citations if needed (not shown here)

    return {
        "response": message_content.value,
        "thread_id": thread_id
    }