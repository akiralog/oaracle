from django.shortcuts import render
from django.http import JsonResponse
import sqlite3
from pathlib import Path
from .db import DatabaseManager
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
    towns = [{"name": row[0], "location_id": row[1], "is_tidal": row[2]} for row in cursor.fetchall()]
    conn.close()
    return JsonResponse({"towns": towns})
    
def fetch_data(request):
    location_id = request.GET.get("location_id")
    is_tidal = request.GET.get("is_tidal") == "true"
    
    if not location_id:
        return JsonResponse({"error": "Missing location_id"}, status=400)
    
    location_id = int(location_id)
    
    weather_data = wm.get_weather_data(location_id, days=1)
    tide_data = None
    if is_tidal:
        tide_data = wm.get_tide_data(location_id, days=1)
        
    return JsonResponse({
        "weather": weather_data,
        "tides": tide_data
    })