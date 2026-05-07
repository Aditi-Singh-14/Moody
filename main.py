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
def check_health():
    return {"message": "Moodify API is running"} # If you see this message, the API is alive and vibing on port 8000

@app.post("/recommend")
async def recommend_songs(mood: str):
    prompt = f"""
    The user is feeling: {mood}
    Suggest 10 real songs that match this mood from famous pop artists singers.
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
        text = result["choices"][0]["message"]["content"]
        songs = json.loads(text)
        for song in songs:
            try:
                clean_artist = song['artist'].split(" ft.")[0].split(" feat.")[0]
                itunes_response = await client.get(
                    "https://itunes.apple.com/search",
                    params={
                        "term": f"{song['title']} {clean_artist}",
                        "media": "music",
                        "limit": 1
                    },
                    timeout=10.0
                )
                itunes_data = itunes_response.json()
                results = itunes_data.get("results", [])
                if results:
                    song["preview_url"] = results[0]["previewUrl"]
                    song["album_art"] = results[0]["artworkUrl100"]
                else:
                    song["preview_url"] = None
                    song["album_art"] = None
            except Exception as e:
                print("ITUNES ERROR:", e)
                continue
    return {"recommendations": songs}
    