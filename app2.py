
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

TRACK_DATABASE = {
    "monaco": {"laps": 78, "sectors": 3, "key_corner": "the Grand Hotel Hairpin"},
    "silverstone": {"laps": 52, "sectors": 3, "key_corner": "Copse"},
    "monza": {"laps": 53, "sectors": 3, "key_corner": "the Parabolica"},
    "spa": {"laps": 44, "sectors": 3, "key_corner": "Eau Rouge"},
    "austria": {"laps": 71, "sectors": 3, "key_corner": "Turn 3"}
}

def run_strategy_agent():
    print("--- McLaren Pit Wall Radio Link Online ---")
    
    print("[RADIO] Zack Papaya: \"Driver, radio check. Confirm which country we are racing in today so I can sync the telemetry data?\"\n")
    country_input = input("Driver (You) >> ").strip().lower()
    track_info = TRACK_DATABASE.get(country_input, {"laps": 56, "sectors": 3, "key_corner": "Turn 4"})
    track_name = country_input.capitalize() if country_input in TRACK_DATABASE else "the circuit"

    print(f"\n[RADIO] Zack Papaya: \"Copy that. Syncing data for {track_name}. Total laps today: {track_info['laps']}. We are live.\"\n")

    # Fixed: Added the variable assignment back and aligned the indentation perfectly
    LIVE_TELEMETRY_DATA = (
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
        f"- Pit Window: OPEN\n\n"
        f"OPPONENT INTEL:\n"
        f"- Max Verstappen has high rear tyre degradation today.\n"
        f"- Red Bull's pit crew is slow today, averaging 3.5s+ pit stops."
    )

    # Fixed: Combined the system prompt instructions here inside the function so it reads the live telemetry data dynamically
    system_message = (
        "You are Zack Papaya, a Formula One Race Situation Agent for Team McLaren. "
        "Your job is to track everything happening around the driver and answer like a professional race engineer. "
        "The driver has no screens—they are relying entirely on you to tell them what's happening.\n\n"
        f"{LIVE_TELEMETRY_DATA}\n\n"
        "Radio Style guidelines:\n"
        "- Act like a real F1 pit wall engineer. Speak in short, snappy, professional sentences.\n"
        "- Answer the driver's specific questions immediately using the live data provided above.\n"
        "- Keep responses to 1-2 sentences. Use radio terms like 'Copy that', 'Box box', or 'Push now'.\n"
        "- End with one follow-up question."
    )

    history = []

    while True:
        user_input = input("Driver (You) >> ")

        if user_input.lower() == "exit":
            print("\nRadio off. Box this lap.")
            break

        history.append({
            "role": "user",
            "content": user_input
        })

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=150, 
            temperature=0.3, 
            system=system_message,
            messages=history
        )

        reply = response.content[0].text
        print(f"\n[RADIO] Zack Papaya: \"{reply}\"\n")

        history.append({
            "role": "assistant",
            "content": reply
        })

if __name__ == "__main__":
    run_strategy_agent()