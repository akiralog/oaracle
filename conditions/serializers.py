from rest_framework import serializers
from .models import ThamesTown, WillyWeatherData


class ThamesTownSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThamesTown
        fields = ['id', 'name', 'slug', 'latitude', 'longitude', 'willy_weather_id']


class WillyWeatherDataSerializer(serializers.ModelSerializer):
    town_name = serializers.CharField(source='town.name', read_only=True)
    
    class Meta:
        model = WillyWeatherData
        fields = ['id', 'town', 'town_name', 'data_type', 'timestamp', 'raw_data', 'created_at']
