from django.contrib import admin
from .models import Location, WeatherCondition, WaterCondition, RowabilityScore, Forecast


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'latitude', 'longitude', 'waterway_type', 'nearest_town', 'created_at']
    list_filter = ['waterway_type', 'created_at']
    search_fields = ['name', 'nearest_town']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(WeatherCondition)
class WeatherConditionAdmin(admin.ModelAdmin):
    list_display = ['location', 'timestamp', 'temperature', 'wind_speed', 'wind_gust', 'weather_description']
    list_filter = ['timestamp', 'weather_description']
    search_fields = ['location__name']
    readonly_fields = ['created_at']


@admin.register(WaterCondition)
class WaterConditionAdmin(admin.ModelAdmin):
    list_display = ['location', 'timestamp', 'water_level', 'flow_rate', 'tide_height', 'tide_type']
    list_filter = ['timestamp', 'tide_type']
    search_fields = ['location__name']
    readonly_fields = ['created_at']


@admin.register(RowabilityScore)
class RowabilityScoreAdmin(admin.ModelAdmin):
    list_display = ['location', 'timestamp', 'score', 'score_value']
    list_filter = ['score', 'timestamp']
    search_fields = ['location__name']
    readonly_fields = ['created_at']


@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    list_display = ['location', 'forecast_date', 'forecast_time', 'temperature_min', 'temperature_max', 'wind_speed']
    list_filter = ['forecast_date', 'forecast_time']
    search_fields = ['location__name']
    readonly_fields = ['created_at']
