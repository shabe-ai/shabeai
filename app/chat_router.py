import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI, OpenAIError
import asyncio

router = APIRouter()

# Pull your key from the environment. (Safer than hard-coding!)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    message: str
    # Optional: include previous turns so you can pass them later
    history: list[dict] | None = None

@router.post("/chat")
async def chat(req: ChatRequest):
    """
    POST /chat
    {
      "message": "hello",
      "history": [
        {"role": "system", "content": "..."},
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "Hello!"}
      ]
    }
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4",          # or gpt-4, gpt-3.5-turbo, etc.
            messages=(req.history or [])  # prior turns, if any
                     + [{"role": "user", "content": req.message}],
            temperature=0.7,
            max_tokens=512,
        )
        return {"reply": completion.choices[0].message.content}
    except OpenAIError as e:
        # Surface model errors cleanly to your front-end
        raise HTTPException(status_code=502, detail=str(e))

@router.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    """
    POST /chat/stream  { "message": "...", "history": [...] }
    Responds as a text stream (chunked transfer-encoding).
    """
    async def token_generator():
        # OpenAI stream=True returns an iterator of chunks
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=(req.history or [])
                   + [{"role": "user", "content": req.message}],
            temperature=0.7,
            max_tokens=512,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta.encode("utf-8")
            # Tiny sleep yields control so FastAPI can flush chunks promptly
            await asyncio.sleep(0)         

        # Optional sentinel if you want to signal "done"
        # yield b"[DONE]"

    return StreamingResponse(token_generator(),
                             media_type="text/plain")   # keep it simple 