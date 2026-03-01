from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import httpx
import json

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.get("/")
def home():
    return {"message": "Moodify API is running"}

@app.post("/recommend")
async def recommend_songs(mood: str):
    prompt = f"""
    The user is feeling: {mood}
    Suggest 5 real songs that match this mood.
    Return ONLY a JSON array like this, nothing else:
    [
        {{"title": "Song Name", "artist": "Artist Name"}},
        {{"title": "Song Name", "artist": "Artist Name"}}
    ]
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            },
            timeout=30.0
        )
    result = response.json()
    print("GROQ RESPONSE:", result)
    text = result["choices"][0]["message"]["content"]
    songs = json.loads(text)
    return {"recommendations": songs}