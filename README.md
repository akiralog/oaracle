# Oaracle - Rowing Conditions

An open source way to view rowing conditions in a specific area based on wind, gusts and tide.

## 🌟 Features

- **Map-First Interface**: Fullscreen interactive map using Leaflet.js
- **Pin-Drop Selection**: Simply click anywhere on the map to select your rowing location
- **Location Context**: Automatic reverse-geocoding to show nearest town and waterway
- **Django Backend**: Robust API backend with PostgreSQL-ready models
- **Weather Integration**: OpenWeatherMap API integration (coming next)
- **Tide/Flow Data**: UKHO Tides API and Environment Agency river flow API (coming next)
- **Rowability Scoring**: Smart scoring system based on multiple factors
- **7-Day Forecast**: Timeline view for planning ahead (coming next)
- **Shareable Links**: Direct links to specific locations (coming next)

## 🚀 Getting Started

### Prerequisites

- A modern web browser
- Python 3.x
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/akiralog/oaracle.git
cd oaracle
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run database migrations:
```bash
python manage.py migrate
```

5. Start the Django development server:
```bash
python manage.py runserver
```

6. Open your browser and navigate to:
```
http://localhost:8000
```

## 🗺️ How to Use

1. **Select Location**: Click anywhere on the map to drop a pin
2. **View Details**: See the location context (town, waterway)
3. **Get Conditions**: Click "Get Rowing Conditions" to fetch weather and water data
4. **Plan Ahead**: View 7-day forecast with rowability scores 

## 🔧 Technology Stack

- **Backend**: Django 4.2 with Django REST Framework
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Maps**: Leaflet.js with OpenStreetMap
- **Geocoding**: OpenStreetMap Nominatim API
- **Styling**: Modern CSS with Inter font family
- **Database**: SQLite (development), PostgreSQL ready (production)

## 📋 Development Roadmap

### Phase 1: Landing Page & Map 
- [x] Fullscreen interactive map
- [x] Pin-drop location selection
- [x] Location context display
- [x] Modern, responsive UI
- [x] Django backend with API endpoints

### Phase 2: Weather Integration 
- [ ] OpenWeatherMap API integration
- [ ] 7-day weather forecast
- [ ] Wind speed and gust data
- [ ] Temperature and precipitation

### Phase 3: Water Conditions 
- [ ] UKHO Tides API for coastal areas
- [ ] Environment Agency river flow data
- [ ] Smart tide/flow detection

### Phase 4: Rowability Scoring 
- [x] Multi-factor scoring algorithm
- [x] Score calculation API
- [ ] Timeline view for planning

### Phase 5: Sharing & Advanced Features
- [ ] Shareable location links
- [ ] Favorite locations

## 🌍 API Integrations

- **OpenStreetMap**: Free map tiles and geocoding
- **OpenWeatherMap**: Weather forecasts and current conditions
- **Environment Agency**: UK river flow and water level data

## 🚀 Quick Commands

```bash
# Start development server
python manage.py runserver

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Access admin panel
# http://localhost:8000/admin/
```