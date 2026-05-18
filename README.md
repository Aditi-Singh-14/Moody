# MOODIFY 🎵
Moodify tells you what to listen to based on your mood and not your history.

An app that matches your vibe and gives song recommendations that always hit for whatever you're in the mood for.
No algorithms. no "because you listened to this." just tell it how you're feeling and it gets it.

## 🔗 Live Demo
- **App:** https://moodify2026.netlify.app
- **API:** https://moodify-ia9v.onrender.com

## Tech Stack
- **Backend:**  FastAPI (Python)
- **AI:** Groq API · LLaMA 3 (mood interpretation + song generation)
- **Music API:**  iTunes Search API (track data + 30s audio previews)
- **Frontend:**  HTML · Tailwind CSS · JavaScript · Swiper.js

## Features
- Mood-based search — type how you're feeling, hit enter or "Find My Song"
- 10 song recommendations — every search returns a fresh set matched to your vibe
- Swipeable carousel — browse through 10 recommendations in a horizontal slide view
- 3 cards visible at once — center card is active, side cards are in view
- 30s audio previews — songs play directly on the card, no redirects
- Album art display — each card shows the cover so you know the vibe before you hear it
- Click-to-center — tap any card in the carousel and it snaps to the front

## How it Works
Type your mood → LLaMA 3 reads the vibe → iTunes pulls the tracks → you get a card carousel to swipe through with previews.
built with FastAPI · Groq/LLaMA 3 · iTunes Search API · HTML/Tailwind/JS

## How to Run Locally
 
### Prerequisites
- Python 3.9+
- Groq API key → [console.groq.com](https://console.groq.com)
### Setup
 
```bash
git clone <your-repo-url>
cd moodify
pip install -r requirements.txt
```
 
Create a `.env` file in the root:
 
```
GROQ_API_KEY=your_groq_api_key_here
```
 
### Run
 
```bash
uvicorn main:app --reload
```
```bash 
python3 -m http.server 3000 
```
in a second terminal.
Then open `http://localhost:3000`
 
---
## Roadmap
 
### v2
- [ ] Stacked card UI (Tinder-style swipe)
- [ ] Mood history — see what you searched and what played
- [ ] Spotify integration — save songs directly to a playlist
- [ ] Mobile responsive layout
- [ ] Multi-language mood input
---

![Moodify Screenshot](screenshot.png)
 
 *Made with ❤️ · © 2026 Moodify*
