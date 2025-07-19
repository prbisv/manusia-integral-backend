# Destiny Matrix Backend

This repository provides a FastAPI backend for analyzing Destiny Matrix numerology data using OpenAI's API and a custom vector store. It is designed to receive a user's numerology data, process it with a specialized prompt, and return insights in Bahasa Indonesia.

## Features
- Accepts detailed Destiny Matrix data (points, chartHeart, purposes, years, etc.)
- Integrates with OpenAI Assistants API and a vector store for context-aware answers
- Returns answers in Bahasa Indonesia
- Dockerized for easy deployment
- Includes test scripts for local and production endpoints

## Requirements
- Python 3.11+
- Docker (for containerized deployment)
- OpenAI API key and vector store ID

## Setup

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd manusia-integral-backend
   ```

2. **Configure environment variables:**
   - Copy `example.env` to `.env` and fill in your values:
     ```sh
     cp example.env .env
     # Edit .env and set OPENAI_API_KEY, VECTOR_STORE_ID, ASSISTANT_ID, PROMPT, APP_ID
     ```

3. **Install dependencies (for local development):**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run locally:**
   ```sh
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000/ask`.

5. **Run with Docker:**
   ```sh
   docker-compose up --build
   ```
   Or build and run manually:
   ```sh
   docker build -t destiny-matrix-backend .
   docker run --env-file .env -p 8000:8000 destiny-matrix-backend
   ```


## API Usage (for Frontend Developers)

### Endpoint
**POST** `/ask`

### Request Headers
- `Content-Type: application/json`

### Request Body Example
Send a JSON object with the following structure (see `sample_user_points.json` for a full example):

```json
{
  "name": "sad",
  "gender": "laki-laki",
  "date": "03.07.2025",
  "points": { /* ...matrix points... */ },
  "chartHeart": { /* ...heart chart values... */ },
  "purposes": { /* ...purpose values... */ },
  "years": { /* ...year values... */ },
  "message": "Apa kelebihan dari diri saya?"
}
```

**All fields are required except `thread_id` (optional, for conversation context).**

### Response Example
```json
{
  "response": "...jawaban dalam Bahasa Indonesia...",
  "thread_id": "..."
}
```

### Example: JavaScript/TypeScript (fetch)
```js
fetch('https://your-backend-url/ask', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(payload)
})
  .then(res => res.json())
  .then(data => {
    console.log('Jawaban:', data.response);
    // Save data.thread_id for follow-up questions if needed
  });
```

### Example: cURL
```sh
curl -X POST https://your-backend-url/ask \
  -H "Content-Type: application/json" \
  -d @sample_user_points.json
```

### Conversation Support
To maintain context for follow-up questions, include the `thread_id` from the previous response in your next request:
```json
{
  ...otherFields,
  "message": "Pertanyaan lanjutan...",
  "thread_id": "<previous_thread_id>"
}
```

### Error Handling
- If the backend cannot process your request, it will return an error message in the `response` field.
- Always check for the presence of the `response` key in the returned JSON.

## Testing

- Use `test_api.py` to test locally against `localhost:8000/ask`.
- Use `test_prod.py` to test against your deployed endpoint (set `APP_ID` in `.env`).

## Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `VECTOR_STORE_ID`: Your vector store ID
- `ASSISTANT_ID`: Your OpenAI Assistant ID
- `PROMPT`: The system prompt for the assistant (escaped as a single line)
- `APP_ID`: (Optional) Your deployed API base URL (e.g., `https://your-app-url/`)

## License
MIT
