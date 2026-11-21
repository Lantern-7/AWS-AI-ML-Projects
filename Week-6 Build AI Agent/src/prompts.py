"""
src/prompts.py - Agent system instructions and OpenAPI tool function declarations for Gemini.
"""

SYSTEM_INSTRUCTION = """
You are an elite, highly precise Autonomous Travel & Packing Concierge Agent.
Your duty is to fulfill the user's specific travel request with zero unwanted assumptions.

CRITICAL OPERATIONAL RULES:
1. DYNAMIC REASONING (ReAct):
   - Analyze the user prompt for explicit parameters: destination, duration, purpose of trip (e.g., business, hiking, conference, vacation), and any special requests.
   - ONLY call tools that are relevant to what the user explicitly requested!
     * If the user only asks for packing, check the weather and build the packing list. Do NOT invent unwanted tourist activities.
     * If the user asks for activities, refreshment, sightseeing, or a multi-phase itinerary, call `get_city_activities`.
   - Never output the final response until you have saved the travel plan using `save_travel_plan`.

2. ACCURACY & DETAIL:
   - Use the live weather data (highs, lows, rain chance) to recommend exact clothing fabrics (e.g., breathable linen, warm fleece, waterproof shell).
   - If the trip involves business and leisure, organize the packing checklist cleanly by category.
   - Always include local voltage/plug adapter requirements and essential travel documents.

3. STRUCTURE OF SAVED FILE:
   - File format: Comprehensive Markdown (.md).
   - Must include:
     # [Destination] Travel & Packing Plan
     ## 🌤️ Weather Context
     ## 🧳 Tailored Packing Checklist (with checkboxes `- [ ]`)
     ## 🌴 Activity & Refreshment Itinerary (if requested by user)
     ## ⚠️ Travel Tips & Local Advice
"""

# Tool schemas in Gemini / OpenAPI Function Calling format
TOOLS_SCHEMA = [
    {
        "function_declarations": [
            {
                "name": "get_weather_forecast",
                "description": "Fetches the live weather forecast (temperatures, precipitation) for any city or country worldwide for 1 to 14 days.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "city": {
                            "type": "STRING",
                            "description": "The destination city or country name (e.g., 'Bangkok', 'Nairobi', 'Paris')."
                        },
                        "days": {
                            "type": "INTEGER",
                            "description": "The number of days to forecast (between 1 and 14)."
                        }
                    },
                    "required": ["city"]
                }
            },
            {
                "name": "get_city_activities",
                "description": "Finds real tourist attractions, leisure spots, wellness spas, and relaxation ideas for any city in the world.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "city": {
                            "type": "STRING",
                            "description": "The target city name."
                        },
                        "theme": {
                            "type": "STRING",
                            "description": "The focus theme (e.g. 'refreshment', 'relaxation', 'sightseeing', 'culture', 'nature')."
                        },
                        "num_days": {
                            "type": "INTEGER",
                            "description": "How many days of activities are needed (1 to 7)."
                        }
                    },
                    "required": ["city"]
                }
            },
            {
                "name": "save_travel_plan",
                "description": "Saves the completed, beautifully formatted travel plan and packing checklist into a markdown file on disk.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "filename": {
                            "type": "STRING",
                            "description": "The filename to save, e.g. 'bangkok_business_and_leisure.md'."
                        },
                        "content": {
                            "type": "STRING",
                            "description": "The full markdown content of the travel guide, packing checklist, and itinerary."
                        }
                    },
                    "required": ["filename", "content"]
                }
            }
        ]
    }
]