from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.conf import settings
from datetime import datetime, timedelta
import requests
import json

from .models import Location, WeatherCondition, WaterCondition, RowabilityScore, Forecast
from .serializers import (
    LocationSerializer, WeatherConditionSerializer, WaterConditionSerializer,
    RowabilityScoreSerializer, ForecastSerializer, LocationDetailSerializer,
    ConditionsRequestSerializer, RowabilityCalculationSerializer
)


def fetch_weather_data(lat, lng):
    """
    Fetch weather data from OpenWeatherMap API
    """
    try:
        # Check if API key is configured
        if not hasattr(settings, 'OPENWEATHERMAP_API_KEY') or settings.OPENWEATHERMAP_API_KEY == 'your_api_key_here':
            print("Warning: OpenWeatherMap API key not configured, using placeholder data")
            return None
        
        # Fetch current weather
        current_url = f"{settings.OPENWEATHERMAP_BASE_URL}/weather"
        params = {
            'lat': lat,
            'lon': lng,
            'appid': settings.OPENWEATHERMAP_API_KEY,
            'units': 'metric',  # Use Celsius and m/s
            'lang': 'en'
        }
        
        response = requests.get(current_url, params=params, timeout=10)
        if response.status_code != 200:
            print(f"OpenWeatherMap API error: {response.status_code}")
            return None
            
        weather_data = response.json()
        
        # Extract relevant data
        current_conditions = {
            'temperature': weather_data['main']['temp'],
            'wind_speed': weather_data['wind']['speed'],
            'wind_gust': weather_data['wind'].get('gust', 0),
            'wind_direction': weather_data['wind'].get('deg', 0),
            'precipitation': weather_data.get('rain', {}).get('1h', 0),
            'humidity': weather_data['main']['humidity'],
            'pressure': weather_data['main']['pressure'],
            'visibility': weather_data.get('visibility', 10000) / 1000,  # Convert to km
            'weather_description': weather_data['weather'][0]['description'],
            'icon_code': weather_data['weather'][0]['icon']
        }
        
        # Convert wind direction from degrees to cardinal
        wind_deg = current_conditions['wind_direction']
        if wind_deg is not None:
            directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                         'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
            current_conditions['wind_direction'] = directions[round(wind_deg / 22.5) % 16]
        
        # Get sunrise/sunset times
        sunrise_timestamp = weather_data['sys']['sunrise']
        sunset_timestamp = weather_data['sys']['sunset']
        
        # Convert to local time 
        sunrise_time = datetime.fromtimestamp(sunrise_timestamp).strftime('%H:%M')
        sunset_time = datetime.fromtimestamp(sunset_timestamp).strftime('%H:%M')
        
        current_conditions['sunrise'] = sunrise_time
        current_conditions['sunset'] = sunset_time
        
        return current_conditions
        
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None


@api_view(['POST'])
@permission_classes([AllowAny])
def get_rowing_conditions(request):
    """
    Get rowing conditions for a specific location
    """
    serializer = ConditionsRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    lat = data['latitude']
    lng = data['longitude']
    
    # Get or create location
    location, created = Location.objects.get_or_create(
        latitude=lat,
        longitude=lng,
        defaults={
            'name': f"Location at {lat}, {lng}",
            'waterway_type': 'unknown',
            'nearest_town': 'Unknown'
        }
    )
    
    # If location was just created, try to get better details
    if created:
        try:
            # Reverse geocoding using OpenStreetMap Nominatim
            response = requests.get(
                f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lng}&zoom=10&addressdetails=1",
                timeout=5
            )
            if response.status_code == 200:
                geo_data = response.json()
                if geo_data.get('address'):
                    address = geo_data['address']
                    
                    # Extract waterway information
                    waterway = address.get('waterway') or address.get('river') or address.get('lake')
                    if waterway:
                        location.waterway_type = waterway
                    
                    # Extract nearest town
                    town = address.get('city') or address.get('town') or address.get('village')
                    if town:
                        location.nearest_town = town
                    
                    # Update location name
                    if waterway and town:
                        location.name = f"{waterway} near {town}"
                    elif waterway:
                        location.name = waterway
                    elif town:
                        location.name = town
                    
                    location.save()
        except Exception as e:
            print(f"Error in reverse geocoding: {e}")
    
    # Initialize response data
    response_data = {
        'location': LocationSerializer(location).data,
        'current_conditions': {},
        'forecast': [],
        'rowability_score': None
    }
    
    # Get current weather conditions (placeholder for now)
    if data['include_weather']:
        # Try to fetch real weather data from OpenWeatherMap
        real_weather = fetch_weather_data(lat, lng)
        
        if real_weather:
            response_data['current_conditions'] = real_weather
        else:
            # Fallback to placeholder data if API call fails
            response_data['current_conditions'] = {
                'temperature': 15.0,
                'wind_speed': 5.0,
                'wind_gust': 8.0,
                'wind_direction': 'S',
                'precipitation': 0.0,
                'humidity': 65,
                'pressure': 1013.0,
                'visibility': 10.0,
                'weather_description': 'Partly cloudy',
                'icon_code': '02d',
                'sunrise': '06:30',
                'sunset': '18:45'
            }
    
    # Get water conditions (placeholder for now)
    if data['include_water']:
        response_data['water_conditions'] = {
            'water_level': None,
            'flow_rate': None,
            'tide_height': None,
            'tide_type': None,
            'water_temperature': None,
            'tide_state': 'Rising',  # Add tide state
            'next_tide_time': '14:30'  # Add next tide time
        }
    
    # Get forecast (placeholder for now)
    if data['include_forecast']:
        # Generate sample forecast data
        forecast_data = []
        for i in range(data['days_ahead']):
            for time_slot in ['09:00', '12:00', '15:00', '18:00']:
                forecast_data.append({
                    'date': (timezone.now().date() + timedelta(days=i)).isoformat(),
                    'time': time_slot,
                    'temperature_min': 12.0,
                    'temperature_max': 18.0,
                    'wind_speed': 5.0 + (i * 0.5),
                    'wind_gust': 8.0 + (i * 0.5),
                    'wind_direction': 180,
                    'precipitation_probability': 20,
                    'weather_description': 'Partly cloudy',
                    'icon_code': '02d'
                })
        response_data['forecast'] = forecast_data
    
    # Calculate rowability score
    if response_data['current_conditions']:
        score_data = calculate_rowability_score(response_data['current_conditions'])
        response_data['rowability_score'] = score_data
    
    return Response(response_data)


@api_view(['POST'])
@permission_classes([AllowAny])
def calculate_rowability_score_api(request):
    """
    Calculate rowability score based on conditions
    """
    serializer = RowabilityCalculationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    score_data = calculate_rowability_score(data)
    
    return Response(score_data)


def calculate_rowability_score(conditions):
    """
    Calculate rowability score based on weather and water conditions
    Returns a score from 1-10 with category and recommendations
    """
    score = 10  # Start with perfect score
    factors = []
    recommendations = []
    
    # Wind speed scoring (most important for rowing)
    wind_speed = conditions.get('wind_speed', 0)
    if wind_speed <= 3:
        factors.append({'factor': 'wind_speed', 'value': wind_speed, 'impact': 'positive', 'description': 'Light winds ideal for rowing'})
    elif wind_speed <= 6:
        score -= 1
        factors.append({'factor': 'wind_speed', 'value': wind_speed, 'impact': 'minor', 'description': 'Moderate winds, manageable'})
    elif wind_speed <= 10:
        score -= 2
        factors.append({'factor': 'wind_speed', 'value': wind_speed, 'impact': 'moderate', 'description': 'Strong winds, challenging conditions'})
        recommendations.append('Consider shorter sessions or sheltered areas')
    else:
        score -= 4
        factors.append({'factor': 'wind_speed', 'value': wind_speed, 'impact': 'major', 'description': 'Very strong winds, potentially dangerous'})
        recommendations.append('Not recommended for rowing today')
    
    # Wind gust scoring
    wind_gust = conditions.get('wind_gust')
    if wind_gust and wind_gust > wind_speed * 1.5:
        score -= 1
        factors.append({'factor': 'wind_gust', 'value': wind_gust, 'impact': 'moderate', 'description': 'Gusty conditions, unpredictable'})
        recommendations.append('Be prepared for sudden wind changes')
    
    # Temperature scoring
    temperature = conditions.get('temperature', 20)
    if 10 <= temperature <= 25:
        factors.append({'factor': 'temperature', 'value': temperature, 'impact': 'positive', 'description': 'Comfortable temperature for rowing'})
    elif 5 <= temperature < 10 or 25 < temperature <= 30:
        score -= 1
        factors.append({'factor': 'temperature', 'value': temperature, 'impact': 'minor', 'description': 'Temperature outside ideal range'})
        if temperature < 10:
            recommendations.append('Dress warmly, consider thermal gear')
        else:
            recommendations.append('Stay hydrated, consider early morning sessions')
    else:
        score -= 2
        factors.append({'factor': 'temperature', 'value': temperature, 'impact': 'moderate', 'description': 'Extreme temperature conditions'})
        if temperature < 5:
            recommendations.append('Very cold, consider indoor alternatives')
        else:
            recommendations.append('Very hot, consider early morning or evening')
    
    # Precipitation scoring
    precipitation = conditions.get('precipitation', 0)
    if precipitation > 5:
        score -= 1
        factors.append({'factor': 'precipitation', 'value': precipitation, 'impact': 'minor', 'description': 'Wet conditions'})
        recommendations.append('Bring waterproof gear')
    
    # Visibility scoring
    visibility = conditions.get('visibility')
    if visibility and visibility < 5:
        score -= 1
        factors.append({'factor': 'visibility', 'value': visibility, 'impact': 'moderate', 'description': 'Poor visibility'})
        recommendations.append('Consider postponing or choose well-lit areas')
    
    # Ensure score is within 1-10 range
    score = max(1, min(10, score))
    
    # Determine category based on score
    if score >= 8:
        category = 'excellent'
    elif score >= 6:
        category = 'good'
    elif score >= 4:
        category = 'fair'
    elif score >= 2:
        category = 'poor'
    else:
        category = 'dangerous'
    
    # Add general recommendations based on score
    if score >= 8:
        recommendations.append('Excellent conditions for rowing!')
    elif score >= 6:
        recommendations.append('Good conditions, enjoy your row!')
    elif score >= 4:
        recommendations.append('Fair conditions, proceed with caution')
    elif score >= 2:
        recommendations.append('Poor conditions, consider alternatives')
    else:
        recommendations.append('Dangerous conditions, not recommended for rowing')
    
    return {
        'score': score,
        'category': category,
        'factors': factors,
        'recommendations': recommendations
    }


@api_view(['GET'])
@permission_classes([AllowAny])
def location_detail(request, location_id):
    """
    Get detailed information about a specific location
    """
    location = get_object_or_404(Location, id=location_id)
    serializer = LocationDetailSerializer(location)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint
    """
    return Response({
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'service': 'Oaracle Conditions API'
    })
