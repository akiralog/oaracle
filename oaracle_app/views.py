from django.shortcuts import render
from django.http import JsonResponse
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / 'locations.db'

def index(request):
    return render(request, "index.html")

def get_towns(req):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
                   SELECT town_name FROM locations
                   ''')
    towns = [{"name": row[1], "location_id": row[2]} for row in cursor.fetchall()]
    conn.close()
    return JsonResponse({"towns": towns})
    
