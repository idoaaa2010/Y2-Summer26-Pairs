import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Track Database holding unique circuit geometry
TRACK_DATABASE = {
    "monaco": {"laps": 78, "sectors": 3, "key_corner": "the Grand Hotel Hairpin"},
    "silverstone": {"laps": 52, "sectors": 3, "key_corner": "Copse"},
    "monza": {"laps": 53, "sectors": 3, "key_corner": "the Parabolica"},
    "spa": {"laps": 44, "sectors": 3, "key_corner": "Eau Rouge"},
    "austria": {"laps": 71, "sectors": 3, "key_corner": "Turn 3"}
}

def run_chat():
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

run_chat()