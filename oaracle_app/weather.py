import json
import requests
from typing import Optional, List, Dict, Any
from datetime import datetime

class WeatherManager:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def search_location(self, query: str = "Chiswick") -> Optional[List[Dict[str, Any]]]:
        endpoint = f"https://api.willyweather.co.uk/v2/{self.api_key}/search.json"
        payload = {"query": query, "limit": 10}
        headers = {"Content-Type": "application/json", "x-payload": json.dumps(payload)}

        print(f"Searching for: {query}")

        try:
            response = requests.get(endpoint, headers=headers)
            print(f"Response Status: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            print(f"Response received: {len(data) if isinstance(data, list) else 1} location(s) found")
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error searching for location: {e}")
            return None

    def get_weather_data(self, location_id: int, days: int = 1) -> Optional[Dict[str, Any]]:
        endpoint = f"https://api.willyweather.co.uk/v2/{self.api_key}/locations/{location_id}/weather.json"
        weather_types = ["weather", "wind", "temperature"]
        params = {"forecasts": ",".join(weather_types), "days": days}

        print(f"Fetching weather data for location ID: {location_id}")
        try:
            response = requests.get(endpoint, params=params)
            print(f"Response Status: {response.status_code}")

            if response.status_code == 400:
                params = {"forecasts": "weather", "days": 3}
                response = requests.get(endpoint, params=params)

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def get_tide_data(self, location_id: int, days: int = 1) -> Optional[Dict[str, Any]]:
        endpoint = f"https://api.willyweather.co.uk/v2/{self.api_key}/locations/{location_id}/weather.json"
        params = {"forecasts": "tides", "days": days}

        print(f"Fetching tide data for location ID: {location_id}")
        try:
            response = requests.get(endpoint, params=params)
            print(f"Response Status: {response.status_code}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching tide data: {e}")
            return None

    def display_weather_forecast(self, weather_data: Dict[str, Any]) -> None:
        """Display weather forecast in a human-readable format"""
        if not weather_data:
            print("No weather data available")
            return

        location = weather_data.get('location', {})
        forecasts = weather_data.get('forecasts', {})
        
        print("\n" + "="*80)
        print(f"WEATHER FORECAST")
        print("="*80)
        print(f"Location: {location.get('name', 'Unknown')}")
        print(f"Region: {location.get('region', 'Unknown')}, {location.get('state', 'Unknown')}")
        print(f"Coordinates: {location.get('lat', 'N/A')}°, {location.get('lng', 'N/A')}°")
        print(f"Timezone: {location.get('timeZone', 'Unknown')}")
        
        # Weather forecast
        weather_forecast = forecasts.get('weather', {})
        if weather_forecast:
            print(f"\nForecast issued: {weather_forecast.get('issueDateTime', 'Unknown')}")
            print("-" * 80)
            
            days = weather_forecast.get('days', [])
            for day_data in days:
                date_str = day_data.get('dateTime', '')
                if date_str:
                    try:
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                        formatted_date = date_obj.strftime('%A, %B %d, %Y')
                    except:
                        formatted_date = date_str
                
                entries = day_data.get('entries', [])
                if entries:
                    entry = entries[0]  # Take first entry for the day
                    
                    print(f"\n{formatted_date}")
                    print(f"   Conditions: {entry.get('precis', 'Unknown')}")
                    print(f"   Temperature: {entry.get('min', 'N/A')}° - {entry.get('max', 'N/A')}°C")
        
        # Wind data
        wind_data = forecasts.get('wind', {})
        
        if wind_data:
            print(f"\nWIND FORECAST")
            print("-" * 40)
            
            wind_days = wind_data.get('days', [])
            
            for day_data in wind_days:  # Show all requested days
                date_str = day_data.get('dateTime', '')
                if date_str:
                    try:
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                        formatted_date = date_obj.strftime('%A, %B %d')
                    except:
                        formatted_date = date_str
                
                entries = day_data.get('entries', [])
                
                if entries:
                    # Show wind at different times of day
                    morning = next((e for e in entries if '08:00:00' in e.get('dateTime', '')), None)
                    afternoon = next((e for e in entries if '14:00:00' in e.get('dateTime', '')), None)
                    evening = next((e for e in entries if '20:00:00' in e.get('dateTime', '')), None)
                    
                    print(f"\n{formatted_date}")
                    
                    if morning:
                        speed = morning.get('speed', 'N/A')
                        direction = morning.get('directionText', 'N/A')
                        gust_speed = morning.get('gustSpeed')
                        gust_str = f" (gusts {gust_speed} mph)" if gust_speed else ""
                        print(f"   Morning: {speed} mph {direction}{gust_str}")
                    
                    if afternoon:
                        speed = afternoon.get('speed', 'N/A')
                        direction = afternoon.get('directionText', 'N/A')
                        gust_speed = afternoon.get('gustSpeed')
                        gust_str = f" (gusts {gust_speed} mph)" if gust_speed else ""
                        print(f"   Afternoon: {speed} mph {direction}{gust_str}")
                    
                    if evening:
                        speed = evening.get('speed', 'N/A')
                        direction = evening.get('directionText', 'N/A')
                        gust_speed = evening.get('gustSpeed')
                        gust_str = f" (gusts {gust_speed} mph)" if gust_speed else ""
                        print(f"   Evening: {speed} mph {direction}{gust_str}")

        # Temperature details
        temp_data = forecasts.get('temperature', {})
        if temp_data:
            print(f"\nDETAILED TEMPERATURE FORECAST")
            print("-" * 40)
            
            temp_days = temp_data.get('days', [])
            for day_data in temp_days:  # Show all requested days
                date_str = day_data.get('dateTime', '')
                if date_str:
                    try:
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                        formatted_date = date_obj.strftime('%A, %B %d')
                    except:
                        formatted_date = date_str
                
                entries = day_data.get('entries', [])
                if entries:
                    print(f"\n{formatted_date}")
                    for entry in entries:
                        time_str = entry.get('dateTime', '')
                        if time_str:
                            try:
                                time_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                                formatted_time = time_obj.strftime('%H:%M')
                            except:
                                formatted_time = time_str
                        
                        temp = entry.get('temperature', 'N/A')
                        print(f"   {formatted_time}: {temp}°C")

        print("\n" + "="*80)

    def display_tide_forecast(self, tide_data: Dict[str, Any]) -> None:
        """Display tide forecast in a human-readable format"""
        if not tide_data:
            print("No tide data available")
            return

        location = tide_data.get('location', {})
        forecasts = tide_data.get('forecasts', {})
        
        print("\n" + "="*80)
        print(f"TIDE FORECAST")
        print("="*80)
        print(f"Location: {location.get('name', 'Unknown')}")
        
        tides = forecasts.get('tides', {})
        if tides:
            print(f"Forecast issued: {tides.get('issueDateTime', 'Unknown')}")
            print("-" * 80)
            
            days = tides.get('days', [])
            for day_data in days:
                date_str = day_data.get('dateTime', '')
                if date_str:
                    try:
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                        formatted_date = date_obj.strftime('%A, %B %d, %Y')
                    except:
                        formatted_date = date_str
                
                entries = day_data.get('entries', [])
                if entries:
                    print(f"\n{formatted_date}")
                    for entry in entries:
                        time_str = entry.get('dateTime', '')
                        if time_str:
                            try:
                                time_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                                formatted_time = time_obj.strftime('%H:%M')
                            except:
                                formatted_time = time_str
                        
                        tide_type = "High" if entry.get('type') == 'high' else "Low"
                        height = entry.get('height', 'N/A')
                        print(f"   {formatted_time} - {tide_type} tide: {height}m")

        print("="*80)

    @staticmethod
    def has_tides(location: Dict[str, Any]) -> bool:
        tide_type_ids = list(range(2, 17)) + [19]
        return location.get("typeId") in tide_type_ids

    @staticmethod
    def display_locations(locations: List[Dict[str, Any]]) -> None:
        if not locations:
            print("No locations to display")
            return

        print(f"\nFound {len(locations)} location(s):")
        print("=" * 60)

        for i, location in enumerate(locations, 1):
            print(f"\n{i}. {location.get('name', 'Unknown')}")
            print(f"   Region: {location.get('region', 'Unknown')}")
            print(f"   State: {location.get('state', 'Unknown')}")
            print(f"   Postcode: {location.get('postcode', 'Unknown')}")
            print(f"   Timezone: {location.get('timeZone', 'Unknown')}")
            print(f"   Coordinates: {location.get('lat', 'N/A')}, {location.get('lng', 'N/A')}")
            print(f"   Location ID: {location.get('id', 'N/A')}")
            print(f"   Type ID: {location.get('typeId', 'N/A')}")
            print(f"   Has Tides: {'Yes' if WeatherManager.has_tides(location) else 'No'}")