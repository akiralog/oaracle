from django.shortcuts import render
from django.http import JsonResponse
import sqlite3
from pathlib import Path
from .weather import WeatherManager
import os

API_KEY = os.getenv('WILLY_WEATHER_API_KEY')
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / 'locations.db'

wm = WeatherManager(API_KEY)

def index(request):
    return render(request, "index.html")

def get_towns(req):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
                   SELECT town_name, location_id, is_tidal FROM locations
                   ''')
    towns = [
        {
            "name": row[0], 
            "location_id": row[1], 
            "is_tidal": bool(row[2])
            } 
        for row in cursor.fetchall()]
    conn.close()
    return JsonResponse({"towns": towns})
    
def fetch_data(request):
    location_id = int(request.GET.get("location_id"))
    is_tidal = request.GET.get("is_tidal") == "true"

    wm = WeatherManager(API_KEY)
    weather_data = wm.get_weather_data(location_id, days=1)
    tide_data = wm.get_tide_data(location_id, days=1) if is_tidal else None
    obs_data = wm.get_observational_data(location_id)  # get current gust

    return JsonResponse({
        "weather": weather_data,
        "tides": tide_data,
        "currentGust": obs_data.get("gustSpeed") if obs_data else None
    })

