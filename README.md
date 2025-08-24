# Oaracle - Thames Rowing Conditions

A simple web application that fetches weather and water conditions for Thames towns using the WillyWeather UK API.

## Features

- **Town Selection**: Choose from 5 Thames towns (Chiswick, Putney, Molesey, Kingston, Walton-on-Thames)
- **Real-time Data**: Fetches fresh weather, wind, tide, and sun data from WillyWeather UK
- **Raw Data Display**: Shows all API responses so you can see exactly what data is available
- **Simple Interface**: Clean, focused interface for rowing enthusiasts

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in your project root:

```bash
# Django Secret Key
DJANGO_SECRET_KEY=your-secret-key-here

# WillyWeather UK API Key
WILLY_WEATHER_API_KEY=your-willyweather-uk-api-key-here
```

**Get your WillyWeather UK API key from**: [https://www.willyweather.co.uk/api.html](https://www.willyweather.co.uk/api.html)

### 3. Set up the Database

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py populate_thames_towns
```

### 4. Run the Application

```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

## How It Works

1. **Select a Town**: Choose from the dropdown of Thames towns
2. **Click "Get Conditions"**: This will:
   - Search for the town's location in WillyWeather UK
   - Fetch fresh data for weather, wind, tides, and sun
   - Store the data in the database
   - Display all the raw data on the frontend

## API Endpoints

- `GET /api/towns/` - List all Thames towns
- `GET /api/town/{town-slug}/` - Get current conditions for a town
- `GET /api/town/{town-slug}/fetch/` - Fetch fresh WillyWeather data for a town
- `GET /api/health/` - Health check

## Data Types

The application fetches and displays:

- **Weather**: Current weather conditions
- **Wind**: Wind speed, direction, and gusts
- **Tides**: Tide times and heights
- **Sun**: Sunrise and sunset times

## Frontend

The frontend is a simple HTML/JavaScript application that:
- Shows a dropdown of Thames towns
- Fetches data when you click "Get Conditions"
- Displays all the raw API data in expandable cards
- Uses modern CSS for a clean, responsive design

## Notes

- All data is fetched from WillyWeather UK API
- Data is cached in the database to reduce API calls
- The frontend shows raw API responses so you can see exactly what data structure is available
- This is a simplified version focused on just pulling and displaying WillyWeather data