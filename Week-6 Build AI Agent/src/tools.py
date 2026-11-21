"""
src/tools.py - Dynamic, Production-Grade Tools for the Travel & Packing Concierge Agent.

Features:
1. get_weather_forecast: Dynamic Geocoding via Open-Meteo Geocoding API + Live Weather Forecast.
   Works for ANY city/country on Earth.
2. get_city_activities: Live search via Wikipedia Travel & Sights API for real attractions & relaxation spots.
3. save_travel_plan: Safe file exporter to outputs/ with path traversal protection.
"""

import os
import json
import urllib.request
import urllib.parse
from typing import Dict, Any, List


# ---------------------------------------------------------------------------
# Helper: Dynamic Geocoding API (Converts any City/Place Name -> Lat/Lon)
# ---------------------------------------------------------------------------

def geocode_location(place_name: str) -> Dict[str, Any]:
    """
    Dynamically resolves any city, region, or country name to latitude & longitude
    using Open-Meteo's official, free Geocoding API (no API key required).
    """
    query = urllib.parse.quote(place_name.strip())
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={query}&count=1&language=en&format=json"
    
    req = urllib.request.Request(url, headers={"User-Agent": "TravelAgent/1.0"})
    with urllib.request.urlopen(req, timeout=6) as response:
        data = json.loads(response.read().decode("utf-8"))
    
    results = data.get("results")
    if not results or len(results) == 0:
        raise ValueError(f"Could not locate '{place_name}'. Please verify the spelling.")
    
    top = results[0]
    return {
        "name": top.get("name"),
        "country": top.get("country", ""),
        "admin1": top.get("admin1", ""),
        "latitude": top.get("latitude"),
        "longitude": top.get("longitude"),
        "timezone": top.get("timezone", "auto")
    }


# ---------------------------------------------------------------------------
# Tool 1: Live Dynamic Weather Forecast for ANY Location on Earth
# ---------------------------------------------------------------------------

def get_weather_forecast(city: str, days: int = 3) -> Dict[str, Any]:
    """
    Fetches the live weather forecast for ANY city or country in the world for 1 to 14 days.
    Dynamically geocodes coordinates first, then fetches temperature and precipitation data.
    """
    # Guardrail: Clamp forecast days between 1 and 14
    days = max(1, min(int(days), 14))

    try:
        # Step 1: Dynamically look up latitude and longitude
        geo = geocode_location(city)
        lat = geo["latitude"]
        lon = geo["longitude"]
        resolved_name = f"{geo['name']}, {geo['country']}"

        # Step 2: Query the live weather forecast
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&"
            f"daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max&"
            f"forecast_days={days}&timezone=auto"
        )

        req = urllib.request.Request(weather_url, headers={"User-Agent": "TravelAgent/1.0"})
        with urllib.request.urlopen(req, timeout=6) as response:
            data = json.loads(response.read().decode("utf-8"))

        daily = data.get("daily", {})
        dates = daily.get("time", [])
        max_temps = daily.get("temperature_2m_max", [])
        min_temps = daily.get("temperature_2m_min", [])
        rain_probs = daily.get("precipitation_probability_max", [])

        summary = []
        for i in range(len(dates)):
            summary.append({
                "day": i + 1,
                "date": dates[i],
                "high_celsius": max_temps[i] if i < len(max_temps) else 25.0,
                "low_celsius": min_temps[i] if i < len(min_temps) else 18.0,
                "rain_probability_pct": rain_probs[i] if i < len(rain_probs) else 0
            })

        avg_high = sum(max_temps) / len(max_temps) if max_temps else 25.0
        avg_low = sum(min_temps) / len(min_temps) if min_temps else 18.0
        max_rain = max(rain_probs) if rain_probs else 0

        condition = "Hot & Sunny" if avg_high > 28 else ("Mild / Comfortable" if avg_high > 18 else "Cold / Chilly")
        if max_rain > 50:
            condition += " with frequent rain showers"

        return {
            "status": "success",
            "searched_query": city,
            "resolved_location": resolved_name,
            "coordinates": {"lat": lat, "lon": lon},
            "forecast_days": days,
            "overall_climate": condition,
            "average_high_c": round(avg_high, 1),
            "average_low_c": round(avg_low, 1),
            "max_rain_probability_pct": max_rain,
            "daily_forecast": summary
        }

    except Exception as e:
        return {
            "status": "error",
            "city": city,
            "error": f"Failed to retrieve weather for '{city}': {str(e)}",
            "fallback_advice": "Prepare clothing for standard seasonal temperatures with a light rain layer."
        }


# ---------------------------------------------------------------------------
# Tool 2: Dynamic Attractions & Activities Search (Wikipedia Knowledge API)
# ---------------------------------------------------------------------------

def get_city_activities(city: str, theme: str = "refreshment", num_days: int = 3) -> Dict[str, Any]:
    """
    Dynamically discovers real sights, parks, relaxation spots, and cultural activities
    for ANY destination in the world using the live Wikipedia Knowledge API.
    """
    num_days = max(1, min(int(num_days), 7))
    
    search_term = f"{city} tourism {theme} attractions"
    encoded_search = urllib.parse.quote(search_term)
    
    url = (
        f"https://en.wikipedia.org/w/api.php?"
        f"action=query&list=search&srsearch={encoded_search}&"
        f"utf8=&format=json&srlimit=6"
    )

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "TravelAgent/1.0 (Educational Agent)"})
        with urllib.request.urlopen(req, timeout=6) as response:
            data = json.loads(response.read().decode("utf-8"))

        search_results = data.get("query", {}).get("search", [])
        
        activities = []
        for item in search_results:
            title = item.get("title", "")
            snippet = item.get("snippet", "").replace('<span class="searchmatch">', '').replace('</span>', '')
            if len(snippet) > 200:
                snippet = snippet[:197] + "..."
            
            activities.append({
                "name": title,
                "description": snippet,
                "suggested_theme": theme.title()
            })

        if not activities:
            activities = [
                {"name": f"{city.title()} Central Park & Botanical Gardens", "description": "Serene outdoor walks and fresh air."},
                {"name": f"{city.title()} Historic Old Town", "description": "Atmospheric architecture and local cafes."},
                {"name": f"{city.title()} Waterfront / Panoramic Viewpoint", "description": "Scenic sunset views and relaxation."}
            ]

        return {
            "status": "success",
            "destination": city.title(),
            "theme": theme,
            "target_days": num_days,
            "found_attractions": activities
        }

    except Exception as e:
        return {
            "status": "fallback",
            "destination": city.title(),
            "theme": theme,
            "note": f"Live activity search encountered an issue: {str(e)}",
            "found_attractions": [
                {"name": f"Local Wellness Spa in {city.title()}", "description": "Unwind and recharge."},
                {"name": f"Cultural Museum & Artisan District in {city.title()}", "description": "Low-stress exploration."}
            ]
        }


# ---------------------------------------------------------------------------
# Tool 3: Safe File Writer (Outputs to outputs/)
# ---------------------------------------------------------------------------

def save_travel_plan(filename: str, content: str) -> Dict[str, Any]:
    """
    Saves the generated packing checklist and itinerary to the outputs/ directory.
    Guarded against path traversal vulnerabilities.
    """
    safe_filename = os.path.basename(filename.strip())
    if not safe_filename.endswith((".md", ".txt")):
        safe_filename += ".md"

    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs"))
    os.makedirs(output_dir, exist_ok=True)

    file_path = os.path.join(output_dir, safe_filename)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return {
            "status": "success",
            "saved_path": file_path,
            "filename": safe_filename,
            "file_size_bytes": len(content.encode("utf-8")),
            "message": f"Successfully exported travel plan to outputs/{safe_filename}."
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to write file: {str(e)}"
        }