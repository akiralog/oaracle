from rest_framework import serializers
from .models import Location, WeatherCondition, WaterCondition, RowabilityScore, Forecast


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'latitude', 'longitude', 'waterway_type', 'nearest_town', 'created_at']


class WeatherConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherCondition
        fields = [
            'id', 'location', 'timestamp', 'temperature', 'wind_speed', 'wind_gust',
            'wind_direction', 'precipitation', 'humidity', 'pressure', 'visibility',
            'weather_description', 'icon_code', 'created_at'
        ]


class WaterConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterCondition
        fields = [
            'id', 'location', 'timestamp', 'water_level', 'flow_rate', 'tide_height',
            'tide_type', 'water_temperature', 'created_at'
        ]


class RowabilityScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = RowabilityScore
        fields = [
            'id', 'location', 'timestamp', 'score', 'score_value', 'factors',
            'recommendations', 'created_at'
        ]


class ForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forecast
        fields = [
            'id', 'location', 'forecast_date', 'forecast_time', 'temperature_min',
            'temperature_max', 'wind_speed', 'wind_gust', 'wind_direction',
            'precipitation_probability', 'weather_description', 'icon_code', 'created_at'
        ]


class LocationDetailSerializer(serializers.ModelSerializer):
    """Serializer for location with related data"""
    weather_conditions = WeatherConditionSerializer(many=True, read_only=True)
    water_conditions = WaterConditionSerializer(many=True, read_only=True)
    rowability_scores = RowabilityScoreSerializer(many=True, read_only=True)
    forecasts = ForecastSerializer(many=True, read_only=True)
    
    class Meta:
        model = Location
        fields = [
            'id', 'name', 'latitude', 'longitude', 'waterway_type', 'nearest_town',
            'weather_conditions', 'water_conditions', 'rowability_scores', 'forecasts',
            'created_at'
        ]


class ConditionsRequestSerializer(serializers.Serializer):
    """Serializer for requesting conditions data"""
    latitude = serializers.DecimalField(max_digits=12, decimal_places=8)
    longitude = serializers.DecimalField(max_digits=12, decimal_places=8)
    include_weather = serializers.BooleanField(default=True)
    include_water = serializers.BooleanField(default=True)
    include_forecast = serializers.BooleanField(default=True)
    days_ahead = serializers.IntegerField(min_value=1, max_value=7, default=7)


class RowabilityCalculationSerializer(serializers.Serializer):
    """Serializer for rowability score calculation"""
    wind_speed = serializers.DecimalField(max_digits=4, decimal_places=1)
    wind_gust = serializers.DecimalField(max_digits=4, decimal_places=1, required=False)
    temperature = serializers.DecimalField(max_digits=4, decimal_places=1)
    precipitation = serializers.DecimalField(max_digits=4, decimal_places=1, default=0)
    visibility = serializers.DecimalField(max_digits=5, decimal_places=1, required=False)
    water_level = serializers.DecimalField(max_digits=6, decimal_places=2, required=False)
    flow_rate = serializers.DecimalField(max_digits=8, decimal_places=2, required=False)
