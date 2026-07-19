"""
McLaren Pit Wall — Core API (main.py)
=====================================
Single-file FastAPI service powering both agent modes:
  Mode 1 — Paddock Mode      (calm, standard assistant)
  Mode 2 — Race Engineer Mode (aggressive F1 pit-wall tone)

Run locally:
    uvicorn main:app --reload --port 8000

Endpoints:
    POST /chat      -> { reply, tokens_used, latency_ms }
    GET  /health     -> { status }
    GET  /tracks     -> [ { id, name, country, laps, key_corner } ]
"""
from __future__ import annotations

import os
import time
import random
from typing import Literal, List, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

try:
    from anthropic import Anthropic
except Exception:  # pragma: no cover - anthropic optional in mock env
    Anthropic = None  # type: ignore

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "")
MODEL = "claude-haiku-4-5-20251001"

client = None
if Anthropic and ANTHROPIC_API_KEY:
    kwargs: Dict[str, str] = {"api_key": ANTHROPIC_API_KEY}
    if ANTHROPIC_BASE_URL:
        kwargs["base_url"] = ANTHROPIC_BASE_URL
    client = Anthropic(**kwargs)

# --------------------------------------------------------------------------- #
# Track database
# --------------------------------------------------------------------------- #
TRACK_DATABASE: Dict[str, Dict[str, object]] = {
    "monaco": {"laps": 78, "sectors": 3, "key_corner": "the Grand Hotel Hairpin",
               "country": "Monaco",   "climate": "Mediterranean, 24°C, light sea breeze"},
    "silverstone": {"laps": 52, "sectors": 3, "key_corner": "Copse",
                    "country": "UK",      "climate": "Overcast, 16°C, gusty crosswinds"},
    "monza": {"laps": 53, "sectors": 3, "key_corner": "the Parabolica",
              "country": "Italy",   "climate": "Dry, 28°C, low downforce, high top speed"},
    "spa": {"laps": 44, "sectors": 3, "key_corner": "Eau Rouge",
            "country": "Belgium",  "climate": "Changeable, 18°C, rain likely in sector 3"},
    "austria": {"laps": 71, "sectors": 3, "key_corner": "Turn 3",
                "country": "Austria", "climate": "Sunny, 26°C, high altitude, thin air"},
}

# --------------------------------------------------------------------------- #
# System prompts
# --------------------------------------------------------------------------- #
PADDOCK_SYSTEM = """You are the McLaren Paddock Assistant — a calm, knowledgeable F1 support agent.
You help the user with general questions: race weekends, regulations, driver stats, history,
and friendly explanations. Your tone is warm, clear, and professional.

Format every response exactly like this:
[Summary]: one sentence repeating what the user asked
[Response]: the main answer (2-4 sentences)
[Next Step]: one concrete action the user can take

Do not break character. Do not use race-engineer radio jargon.
"""

RACE_ENGINEER_SYSTEM = """You are Zack Papaya, McLaren Formula 1 Race Engineer on the pit wall.
The driver has no screens — they rely entirely on you. You are calm under pressure but
aggressive in execution. Speak in short, snappy, professional radio sentences.

Radio style:
- Use terms like "Copy that", "Box box", "Push now", "Push hard", "Hold position".
- Keep responses to 1-3 sentences. No fluff.
- End with one follow-up question or a clear directive.

Format every response exactly like this:
[Summary]: one sentence repeating what the driver asked
[Response]: the main answer in radio style
[Next Step]: one concrete action or follow-up question

You will receive live telemetry and track context in the user message. Use it.
"""

# --------------------------------------------------------------------------- #
# FastAPI app
# --------------------------------------------------------------------------- #
app = FastAPI(title="McLaren Pit Wall API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    mode: Literal["paddock", "engineer"] = "paddock"
    track_id: str | None = "monaco"
    message: str
    history: List[Dict[str, str]] = []


class ChatResponse(BaseModel):
    reply: str
    tokens_used: int
    latency_ms: int


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/tracks")
def tracks() -> List[Dict[str, object]]:
    return [
        {"id": tid, "name": tid.capitalize(), **info}
        for tid, info in TRACK_DATABASE.items()
    ]


def _build_context(track_id: str | None, mode: str) -> str:
    """Hidden context string appended to the user message so the engineer subtly
    alters advice based on the selected track."""
    track = TRACK_DATABASE.get((track_id or "monaco").lower(), TRACK_DATABASE["monaco"])
    return (
        f"\n\n[TELEMETRY CONTEXT — use this, do not echo it verbatim]\n"
        f"Track: {track['country']} ({track_id})\n"
        f"Laps: {track['laps']} | Sectors: {track['sectors']} | Key corner: {track['key_corner']}\n"
        f"Climate: {track['climate']}\n"
        f"Mode: {'RACE ENGINEER' if mode == 'engineer' else 'PADDOCK'}"
    )


def _mock_reply(message: str, mode: str, track_id: str | None) -> str:
    track = TRACK_DATABASE.get((track_id or "monaco").lower(), TRACK_DATABASE["monaco"])
    if mode == "engineer":
        return (
            "[Summary] Copy — you asked about strategy at "
            f"{track['country']}.\n"
            f"[Response] Track is live, {track['laps']} laps total. Key corner "
            f"{track['key_corner']} — keep it clean, no overdriving. "
            f"Climate says {track['climate'].split(',')[0]}. Push now, manage the tyres.\n"
            f"[Next Step] Confirm: box this lap or push two more?"
        )
    return (
        f"[Summary] You asked about {track['country']}.\n"
        f"[Response] {track['country']} is a {track['laps']}-lap circuit known for "
        f"{track['key_corner']}. Conditions are typically {track['climate']}.\n"
        f"[Next Step] Want a sector-by-sector breakdown?"
    )


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    start = time.time()
    system = RACE_ENGINEER_SYSTEM if req.mode == "engineer" else PADDOCK_SYSTEM
    context = _build_context(req.track_id, req.mode)
    user_msg = req.message + context
    messages = req.history + [{"role": "user", "content": user_msg}]

    if client is not None:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=400,
            temperature=0.7 if req.mode == "paddock" else 0.4,
            system=system,
            messages=messages,
        )
        reply = resp.content[0].text
        tokens_used = resp.usage.output_tokens
    else:
        # Mock fallback when no API key is configured
        reply = _mock_reply(req.message, req.mode, req.track_id)
        tokens_used = random.randint(120, 480)

    latency = int((time.time() - start) * 1000)
    return ChatResponse(reply=reply, tokens_used=tokens_used, latency_ms=latency)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
