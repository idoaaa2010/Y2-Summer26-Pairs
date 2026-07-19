"""
app2.py — Race Strategy & Telemetry Analyst Agent
=================================================
Backup / previous iteration of the Strategy Agent (Agent 2, "Zack Papaya").
This file is kept for reference and as a fallback if the unified
main.py service is unavailable.

Run standalone:
    python app2.py
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


def run_strategy_agent() -> None:
    """Interactive terminal loop for the Strategy Agent."""
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", "")) if Anthropic else None

    print("--- McLaren Pit Wall Radio Link Online ---")
    print('[RADIO] Zack Papaya: "Driver, radio check. Confirm which country we are racing in today?"\n')
    country_input = input("Driver (You) >> ").strip().lower()
    track_info = TRACK_DATABASE.get(
        country_input, {"laps": 56, "sectors": 3, "key_corner": "Turn 4"}
    )
    track_name = country_input.capitalize() if country_input in TRACK_DATABASE else "the circuit"
    print(f'\n[RADIO] Zack Papaya: "Copy that. Syncing data for {track_name}. Total laps today: {track_info["laps"]}. We are live."\n')

    live_telemetry = (
        f"CURRENT LIVE RACE SITUATION:\n"
        f"- Location: {track_name}\n"
        f"- Current Position: P2 (Team McLaren)\n"
        f"- Car Ahead: Max Verstappen (Red Bull) | Gap Ahead: -0.50 seconds\n"
        f"- Car Behind: Lewis Hamilton (Ferrari) | Gap Behind: +0.45 seconds\n"
        f"- Track Position: Lap 24 of {track_info['laps']}, Sector 2, approaching {track_info['key_corner']}\n"
        f"- DRS Status: DRS is AVAILABLE\n"
        f"- Your Tyres: Medium Compounds | 14 laps old\n"
        f"- Fuel Status: 22.4kg remaining (Safe to the end)\n"
        f"- Track Status: Green Flag\n"
        f"- Pit Window: OPEN\n"
    )

    system_message = (
        "You are Zack Papaya, a Formula One Race Situation Agent for Team McLaren. "
        "Your job is to track everything happening around the driver and answer like a "
        "professional race engineer. The driver has no screens — they rely entirely on you.\n\n"
        f"{live_telemetry}\n\n"
        "Format every response exactly like this:\n"
        "[Summary]: one sentence repeating what the driver asked\n"
        "[Response]: the main answer in radio style (1-2 sentences)\n"
        "[Next Step]: one concrete action or follow-up question\n\n"
        "Use radio terms like 'Copy that', 'Box box', 'Push now'. Keep it short."
    )

    history: list = []
    while True:
        user_input = input("Driver (You) >> ")
        if user_input.lower() == "exit":
            print("\nRadio off. Box this lap.")
            break

        history.append({"role": "user", "content": user_input})

        if client is not None:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=150,
                temperature=0.3,
                system=system_message,
                messages=history,
            )
            reply = response.content[0].text
        else:
            reply = (
                "[Summary] Copy — you asked about strategy.\n"
                f"[Response] P2, gap -0.50 to Max. DRS available into {track_info['key_corner']}. "
                "Push now, box in 3 laps.\n"
                "[Next Step] Confirm: box lap 27?"
            )

        print(f'\n[RADIO] Zack Papaya: "{reply}"\n')
        history.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    run_strategy_agent()
