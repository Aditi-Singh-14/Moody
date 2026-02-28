from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import httpx

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@app.get("/")
def home():
    return {"message": "MoodTunes API is running"}

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
           f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}",
            json={
                "contents": [{"parts": [{"text": prompt}]}]
            },
            timeout=30.0
        )
    
    result = response.json()
    print("GEMINI RESPONSE:", result)
    
    if "candidates" not in result:
        return {"error": result}
    
    text = result["candidates"][0]["content"]["parts"][0]["text"]
    return {"recommendations": text}