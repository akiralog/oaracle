import json
import requests
from typing import Optional, List, Dict, Any

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
        
    def get_observational_data(self, location_id: int) -> Optional[Dict[str, Any]]:
        endpoint = f"https://api.willyweather.co.uk/v2/{self.api_key}/locations/{location_id}/weather.json"
        payload = {"observational": True, "days": 1}
        headers = {"Content-Type": "application/json", "x-payload": json.dumps(payload)}

        print(f"Fetching observational data for location ID: {location_id}")

        try:
            response = requests.get(endpoint, headers=headers)
            print(f"Response Status: {response.status_code}")
            response.raise_for_status()
            data = response.json()

            gust = None
            try:
                gust = data["observational"]["observations"]["wind"]["gustSpeed"]
            except KeyError:
                gust = None

            return {"gustSpeed": gust}
        except requests.exceptions.RequestException as e:
            print(f"Error fetching observational data: {e}")
            return None
