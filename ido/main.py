import os
import json
import urllib.request
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

TRACK_DATABASE = {
    "monaco": {"laps": 78, "sectors": 3, "key_corner": "the Grand Hotel Hairpin", "coords": (43.7347, 7.4206)},
    "silverstone": {"laps": 52, "sectors": 3, "key_corner": "Copse", "coords": (52.0786, -1.0169)},
    "monza": {"laps": 53, "sectors": 3, "key_corner": "the Parabolica", "coords": (45.6156, 9.2811)},
    "spa": {"laps": 44, "sectors": 3, "key_corner": "Eau Rouge", "coords": (50.4372, 5.9714)},
    "austria": {"laps": 71, "sectors": 3, "key_corner": "Turn 3", "coords": (47.2197, 14.7647)}
}

# ==========================================
# CENTRAL PIT WALL MEMORY
# ==========================================
SHARED_PIT_WALL = {
    "current_track": None, # Reset to None so the agents are forced to ask you!
    "latest_weather_intel": "Track dry, ambient 24°C, track temp 38°C.",
    "latest_strategy_intel": "P2 behind Verstappen (-0.5s), tyre Mediums (14 laps old)."
}

def get_live_telemetry(track_id):
    """Generates track-specific race data based on the current circuit."""
    # Fallback to a generic track if the user types something not in the database
    if not track_id:
        track_id = "unknown circuit"
        
    track_info = TRACK_DATABASE.get(track_id, {"laps": 56, "sectors": 3, "key_corner": "Turn 4"})
    track_name = track_id.capitalize()
    
    return (
        f"CURRENT LIVE RACE SITUATION:\n"
        f"- Location: {track_name}\n"
        f"- Current Position: P2 (Team McLaren)\n"
        f"- Gap to P1 (Max Verstappen): -0.50 seconds\n"
        f"- Track Position: Lap 24 of {track_info['laps']}, approaching {track_info['key_corner']}\n"
        f"- Your Tyres: Medium Compounds | 14 laps old\n"
        f"- Pit Window: OPEN\n"
        f"OPPONENT INTEL: Verstappen has high rear tyre degradation."
    )

def fetch_real_weather(track_id):
    """Fetches real-time weather from Open-Meteo API using track coordinates."""
    if not track_id:
        track_id = "unknown"
        
    track_info = TRACK_DATABASE.get(track_id)
    if track_info and "coords" in track_info:
        lat, lon = track_info["coords"]
    else:
        # Default fallback to Silverstone
        lat, lon = (52.0786, -1.0169)
        
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,wind_speed_10m,precipitation"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            current = data.get("current", {})
            temp = current.get("temperature_2m", "N/A")
            wind = current.get("wind_speed_10m", "N/A")
            precip = current.get("precipitation", "N/A")
            return f"LIVE API WEATHER (Lat: {lat}, Lon: {lon}): Temp: {temp}°C, Wind: {wind}km/h, Rain/Precipitation: {precip}mm."
    except Exception:
        return "LIVE API WEATHER: Offline (Unable to fetch real-time data)."

# ==========================================
# BACKEND CONSULTATION FUNCTIONS
# ==========================================
def consult_weather_agent(driver_prompt: str) -> str:
    print("  [BACKEND] 📡 Strategy Agent -> Weather Agent: Fetching environmental telemetry...")
    track = SHARED_PIT_WALL["current_track"] or "the circuit"
    
    live_weather = fetch_real_weather(SHARED_PIT_WALL["current_track"])
    
    sys_prompt = f"""
    You are the Trackside Meteorologist.
    The driver at {track.capitalize()} asked: "{driver_prompt}"
    
    {live_weather}
    
    Provide a direct, technical weather & surface grip analysis relevant to their question for this specific track.
    Do NOT ask questions. Keep it under 3 sentences.
    """
    
    response = client.messages.create(
        model='claude-3-haiku-20240307',
        max_tokens=200,
        temperature=0.3,
        system=sys_prompt,
        messages=[{"role": "user", "content": driver_prompt}]
    )
    intel = response.content[0].text
    SHARED_PIT_WALL["latest_weather_intel"] = intel
    return intel

def consult_strategy_agent(driver_prompt: str) -> str:
    print("  [BACKEND] 📡 Weather Agent -> Strategy Agent: Fetching telemetry & pit strategy...")
    track = SHARED_PIT_WALL["current_track"]
    telemetry = get_live_telemetry(track)
    
    sys_prompt = f"""
    You are Zack Papaya, McLaren Lead Race Strategist.
    The driver asked: "{driver_prompt}"
    
    {telemetry}
    
    Provide immediate strategy metrics (gaps, tyre life, pit window status) relevant to their question based on the telemetry above.
    Do NOT ask questions. Keep it under 3 sentences.
    """
    
    response = client.messages.create(
        model='claude-3-haiku-20240307',
        max_tokens=200,
        temperature=0.3,
        system=sys_prompt,
        messages=[{"role": "user", "content": driver_prompt}]
    )
    intel = response.content[0].text
    SHARED_PIT_WALL["latest_strategy_intel"] = intel
    return intel


# ==========================================
# AGENT 1: WEATHER & CONDITIONS
# ==========================================
def run_weather_agent():
    print('\n--- Weather & Conditions Agent Online ---')
    print('You: (type "exit" for main menu, "switch" to change agents)')
    
    # 1. Ask for track if we don't know it yet
    if not SHARED_PIT_WALL["current_track"]:
        print("\n[METEOROLOGIST]: \"Trackside weather station online. Which circuit are we at?\"\n")
        country_input = input("Engineer (You) >> ").strip().lower()
        
        if country_input == 'exit':
            return 'menu'
        elif country_input == 'switch':
            return 'strategy'
            
        SHARED_PIT_WALL["current_track"] = country_input
        print(f"\n[METEOROLOGIST]: \"Weather radar locked on {country_input.capitalize()}. Waiting for your query.\"\n")
    else:
        print(f"\n[METEOROLOGIST]: \"Weather radar is still locked on {SHARED_PIT_WALL['current_track'].capitalize()}.\"\n")
    
    history = []
    
    while True:
        user_input = input('\nDriver (You) >> ').strip()

        if user_input.lower() == 'exit':
            return 'menu'
        elif user_input.lower() == 'switch':
            return 'strategy'
        
        # Update track if mentioned mid-conversation
        for track in TRACK_DATABASE:
            if track in user_input.lower():
                SHARED_PIT_WALL["current_track"] = track

        strategy_context = consult_strategy_agent(user_input)
        track_name = (SHARED_PIT_WALL["current_track"] or "the circuit").capitalize()
        live_weather = fetch_real_weather(SHARED_PIT_WALL["current_track"])
        
        system_message = f"""
        You are a veteran Formula 1 Trackside Meteorologist on the McLaren pit wall.
        Circuit: {track_name}
        
        {live_weather}
        
        LIVE STRATEGY & TELEMETRY FROM BACKEND:
        {strategy_context}
        
        CRITICAL INSTRUCTIONS:
        - Provide relevant track, wind, and precipitation data UPFRONT for {track_name}.
        - Integrate the Strategy Agent's backend telemetry into your advice when relevant.
        - DO NOT ask questions. Be decisive, authoritative, and clear.
        - Format with clean bold headers:
          **📊 TRACK CONDITIONS:**
          **💨 WIND TELEMETRY:**
          **🌧️ RADAR & PRECIPITATION:**
        give only the relevent answer to what the user asked for! and ask if hed like the other info!
        """
        
        history.append({'role': 'user', 'content': user_input})
        
        response = client.messages.create(
            model='claude-3-haiku-20240307',
            max_tokens=400,
            temperature=0.4,
            system=system_message,
            messages=history
        )
        
        reply = response.content[0].text
        print(f'\n[METEOROLOGIST]:\n{reply}')
        
        SHARED_PIT_WALL["latest_weather_intel"] = reply
        history.append({'role': 'assistant', 'content': reply})


# ==========================================
# AGENT 2: RACE STRATEGY & TELEMETRY
# ==========================================
def run_strategy_agent():
    print("\n--- McLaren Pit Wall Radio Link Online ---")
    print('You: (type "exit" for main menu, "switch" to change agents)')
    
    # 1. Ask for track if we don't know it yet
    if not SHARED_PIT_WALL["current_track"]:
        print("\n[RADIO] Zack Papaya: \"Driver, radio check. Confirm which country we are racing in today so I can sync the telemetry data?\"\n")
        country_input = input("Driver (You) >> ").strip().lower()
        
        if country_input == 'exit':
            return 'menu'
        elif country_input == 'switch':
            return 'weather'
            
        SHARED_PIT_WALL["current_track"] = country_input
        print(f"\n[RADIO] Zack Papaya: \"Copy that. Telemetry synced for {country_input.capitalize()}. We are live.\"\n")
    else:
        print(f"\n[RADIO] Zack Papaya: \"Driver, telemetry is still synced for {SHARED_PIT_WALL['current_track'].capitalize()}. We are live.\"\n")
    
    history = []

    while True:
        user_input = input("\nDriver (You) >> ").strip()

        if user_input.lower() == "exit":
            return 'menu'
        elif user_input.lower() == 'switch':
            return 'weather'

        # Update track if mentioned mid-conversation
        for track in TRACK_DATABASE:
            if track in user_input.lower():
                SHARED_PIT_WALL["current_track"] = track

        # Get backend weather data and local track telemetry
        weather_context = consult_weather_agent(user_input)
        live_telemetry = get_live_telemetry(SHARED_PIT_WALL["current_track"])

        system_message = f"""
        You are Zack Papaya, McLaren Lead Race Engineer on the pit wall.
        
        {live_telemetry}
        
        LIVE WEATHER & METEOROLOGY FROM BACKEND:
        {weather_context}
        
        CRITICAL INSTRUCTIONS:
        - Give the driver decisive race strategy upfront based heavily on their specific location on the track (e.g., lap number, key corner) and the opponent gaps.
        - If they ask about weather, rain, or track surface, use the Weather Agent's backend data to command them (e.g., Box for Inters).
        - Keep radio comms snappy, professional, and limited to 2-3 sentences.
        - DO NOT ask any questions back to the driver.
        """

        history.append({"role": "user", "content": user_input})

        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=200, 
            temperature=0.3, 
            system=system_message,
            messages=history
        )

        reply = response.content[0].text
        print(f"\n[RADIO] Zack Papaya: \"{reply}\"\n")
        history.append({"role": "assistant", "content": reply})


# ==========================================
# MAIN MENU SYSTEM
# ==========================================
def main():
    current_state = 'menu'
    
    while True:
        if current_state == 'menu':
            print("\n=========================================")
            print("      🏎️  MCLAREN AI PIT WALL SYSTEM  🏎️      ")
            print("=========================================")
            print("1. Agent 1 — Weather & Environmental Conditions")
            print("2. Agent 2 — Race Strategy & Telemetry Analyst")
            print("3. Exit Program")
            
            choice = input("\nSelect an option (1-3): ").strip()
            
            if choice == "1":
                current_state = 'weather'
            elif choice == "2":
                current_state = 'strategy'
            elif choice == "3":
                print("\nShutting down pit wall systems. Goodbye.")
                break
            else:
                print("\n[!] Invalid option.")
                
        elif current_state == 'weather':
            current_state = run_weather_agent()
            
        elif current_state == 'strategy':
            current_state = run_strategy_agent()


if __name__ == "__main__":
    main()