# WillyWeather API Setup Guide

## Overview
This application now uses the WillyWeather API to fetch weather and water conditions for Thames towns. The old OpenWeatherMap and Environment Agency APIs have been replaced.

## Setup Steps

### 1. Get a WillyWeather API Key
- Visit [WillyWeather UK API](https://www.willyweather.co.uk/api.html)
- Sign up for an account
- Generate an API key

### 2. Configure Environment Variables
Create a `.env` file in your project root with:

```bash
# Django Secret Key
DJANGO_SECRET_KEY=your-secret-key-here

# WillyWeather API
WILLY_WEATHER_API_KEY=your-willyweather-api-key-here
```

### 3. Populate Database
The database has been set up with the 5 Thames towns:
- Chiswick
- Putney  
- Molesey
- Kingston
- Walton-on-Thames

Run this command to populate the database:
```bash
python manage.py populate_thames_towns
```

### 4. Fetch WillyWeather Data
To fetch all available data for all towns, call:
```
GET /api/willy-weather/fetch-all/
```

This will:
- Search for WillyWeather locations near each town
- Fetch weather, wind, tides, rainfall, and sunrise/sunset data
- Store all data in the database

### 5. Get Conditions for a Specific Town
To get conditions for a specific town:
```
GET /api/town/{town-slug}/
```

Example: `/api/town/chiswick/`

## Data Structure

The application stores:
- **ThamesTown**: Basic town information and coordinates
- **WillyWeatherData**: Raw API responses for each data type
- **Processed data**: Cleaned and formatted data for display

## API Endpoints

- `GET /api/willy-weather/fetch-all/` - Fetch all data for all towns
- `GET /api/town/{town-slug}/` - Get conditions for a specific town
- `GET /api/health/` - Health check

## Testing

1. Start the Django server: `python manage.py runserver`
2. Visit `/api/willy-weather/fetch-all/` to populate data
3. Test individual towns: `/api/town/chiswick/`

## Notes

- WillyWeather UK service covers UK locations
- Data is cached in the database to reduce API calls
- The frontend dropdown now uses the database instead of hardcoded coordinates
- All old API calls (OpenWeatherMap, Environment Agency) have been removed
