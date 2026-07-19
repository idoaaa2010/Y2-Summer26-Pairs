"""
app1.py — Weather & Environmental Conditions Agent
===================================================
Backup / previous iteration of the Weather Agent (Agent 1).
This file is kept for reference and as a fallback if the unified
main.py service is unavailable.

Run standalone:
    python app1.py
"""
from __future__ import annotations

import os
from typing import Dict

try:
    from anthropic import Anthropic
except Exception:  # pragma: no cover
    Anthropic = None  # type: ignore

TRACK_DATABASE: Dict[str, Dict[str, object]] = {
    "monaco": {"laps": 78, "sectors": 3, "key_corner": "the Grand Hotel Hairpin"},
    "silverstone": {"laps": 52, "sectors": 3, "key_corner": "Copse"},
    "monza": {"laps": 53, "sectors": 3, "key_corner": "the Parabolica"},
    "spa": {"laps": 44, "sectors": 3, "key_corner": "Eau Rouge"},
    "austria": {"laps": 71, "sectors": 3, "key_corner": "Turn 3"},
}


def run_weather_agent() -> None:
    """Interactive terminal loop for the Weather Agent."""
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", "")) if Anthropic else None

    system_message = f"""
    You are a veteran Formula 1 Race Engineer and Trackside Meteorologist sitting on the pit wall.
    Your tone is razor-sharp, technical, calm under intense pressure, and highly data-driven.

    You have exclusive access to this circuit configuration data:
    {TRACK_DATABASE}

    When a user provides a circuit from this list (or asks for a weather report on it), look up
    its key corner, lap counts, and sectors. Use that specific data to customize your tactical
    report. If they don't give real weather data, simulate realistic trackside data matching that
    track's climate.

    Format every response exactly like this:
    [Summary]: one sentence repeating what the user asked
    [Response]: the main answer
    [Next Step]: one concrete action the user can take

    Crucial: give only the information the user asks for.
    """

    history: list = []
    print("Weather Agent online. (type 'bye' to quit)")

    while True:
        user_input = input("\n>> ")
        if user_input.lower() == "bye":
            break

        history.append({"role": "user", "content": user_input})

        if client is not None:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=500,
                temperature=0.7,
                system=system_message,
                messages=history,
            )
            reply = response.content[0].text
        else:
            track = TRACK_DATABASE.get(user_input.lower(), TRACK_DATABASE["monaco"])
            reply = (
                "[Summary] Weather request for "
                f"{user_input.capitalize()}.\n"
                f"[Response] {track['laps']} laps, key corner {track['key_corner']}. "
                "Simulated: 22°C air, 38°C track, 55% humidity, light wind.\n"
                "[Next Step] Request a tire compound window?"
            )

        print(f"\nClaude:\n{reply}")
        history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    run_weather_agent()
