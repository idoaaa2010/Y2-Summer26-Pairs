import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

TRACK_DATABASE = {
    "monaco": {"laps": 78, "sectors": 3, "key_corner": "the Grand Hotel Hairpin"},
    "silverstone": {"laps": 52, "sectors": 3, "key_corner": "Copse"},
    "monza": {"laps": 53, "sectors": 3, "key_corner": "the Parabolica"},
    "spa": {"laps": 44, "sectors": 3, "key_corner": "Eau Rouge"},
    "austria": {"laps": 71, "sectors": 3, "key_corner": "Turn 3"}
}

def run_weather_agent():
    print('You: (type bye to quit)')
    
    # Passing the exact database parameters down into the system instructions
    system_message = f"""
    You are a veteran Formula 1 Race Engineer and Trackside Meteorologist sitting on the pit wall. 
    Your tone is razor-sharp, technical, calm under intense pressure, and highly data-driven.
    
    You have exclusive access to this circuit configuration data:
    {TRACK_DATABASE}
    
    When a user provides a circuit from this list (or asks for a weather report on it), look up its key corner, lap counts, and sectors. Use that specific data to customize your tactical report. If they don't give real weather data, simulate realistic trackside data matching that track's climate.
    
    CRITICAL FORMATTING RULE: You must organize your response using the following structure, utilizing bold headers:
    **📊 TRACK CONDITIONS:** (Air/track temp, humidity, total lap constraints, and general tire grip windows)
    **💨 WIND TELEMETRY:** (Wind speed, direction, and specific tactical impact on the track's key_corner or straights)
    **🌧️ RADAR & PRECIPITATION:** (Rain probability, cell trajectory, intensity, or simulation metrics)
    **🏁 STRATEGY & DIRECTIVE:** (The specific crossover lap estimation out of total laps, tire compound window, and a precise radio directive to the driver)
    
    Keep the language immersive, technical, and formatted with clean line breaks between blocks.
    crusial: give only the information the user asks for! for example: if he asks for the weathe rgive only the staff that are relative to the weather
    """
    
    history = []
    
    while True:
        user_input = input('\n>> ')

        if user_input.lower() == 'bye':
            break
        
        history.append({'role': 'user', 'content': user_input})
        
        response = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=500,
            temperature=0.7,
            system=system_message,
            messages=history
        )
        
        reply = response.content[0].text
        print(f'\nClaude:\n{reply}')
        history.append({'role': 'assistant', 'content': reply})

run_weather_agent()
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
try:
    from app1 import run_weather_agent  # Ido's Weather Agent
except ImportError:
    # Fallback placeholder if Ido hasn't finished his file yet
    def run_weather_agent():
        print("\n[System Alert] Agent 1 (Weather) is not connected yet.")

from app import run_strategy_agent  # Your Strategy Agent (Zack Papaya)

def main():
    print("=========================================")
    print("      🏎️  MCLAREN AI PIT WALL SYSTEM  🏎️      ")
    print("=========================================")
    
    while True:
        print("\nWhich agent do you want to use?")
        print("1. Agent 1 — Weather & Environmental Conditions")
        print("2. Agent 2 — Race Strategy & Telemetry Analyst")
        print("3. Exit Program")
        
        choice = input("\nSelect an option (1-3): ").strip()
        
        if choice == "1":
            run_weather_agent()
        elif choice == "2":
            run_strategy_agent()
        elif choice == "3":
            print("\nShutting down pit wall systems. Goodbye.")
            break
        else:
            # Handles invalid inputs cleanly without crashing as requested in the README
            print("\n[!] Invalid input. Please type 1, 2, or 3.")

if __name__ == "__main__":
    main()