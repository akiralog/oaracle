from django.db import models
from django.utils import timezone


class Location(models.Model):
    """Model for storing rowing locations"""
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    waterway_type = models.CharField(max_length=100, blank=True)  # river, lake, sea, etc.
    nearest_town = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['latitude', 'longitude']

    def __str__(self):
        return f"{self.name} ({self.latitude}, {self.longitude})"


class WeatherCondition(models.Model):
    """Model for storing weather conditions"""
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='weather_conditions')
    timestamp = models.DateTimeField()
    temperature = models.DecimalField(max_digits=4, decimal_places=1)  # in Celsius
    wind_speed = models.DecimalField(max_digits=4, decimal_places=1)  # in m/s
    wind_gust = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)  # in m/s
    wind_direction = models.IntegerField()  # in degrees
    precipitation = models.DecimalField(max_digits=4, decimal_places=1, default=0)  # in mm
    humidity = models.IntegerField()  # percentage
    pressure = models.DecimalField(max_digits=6, decimal_places=1)  # in hPa
    visibility = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)  # in km
    weather_description = models.CharField(max_length=255)
    icon_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        unique_together = ['location', 'timestamp']

    def __str__(self):
        return f"{self.location.name} - {self.timestamp}"


class WaterCondition(models.Model):
    """Model for storing water conditions (tides, flow, etc.)"""
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='water_conditions')
    timestamp = models.DateTimeField()
    water_level = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # in meters
    flow_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  # in m³/s
    tide_height = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)  # in meters
    tide_type = models.CharField(max_length=20, blank=True)  # high, low, rising, falling
    water_temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)  # in Celsius
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        unique_together = ['location', 'timestamp']

    def __str__(self):
        return f"{self.location.name} - {self.timestamp}"


class RowabilityScore(models.Model):
    """Model for storing calculated rowability scores"""
    SCORE_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('dangerous', 'Dangerous'),
    ]

    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='rowability_scores')
    timestamp = models.DateTimeField()
    score = models.CharField(max_length=20, choices=SCORE_CHOICES)
    score_value = models.IntegerField()  # 1-10 scale
    factors = models.JSONField()  # Store factors that influenced the score
    recommendations = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        unique_together = ['location', 'timestamp']

    def __str__(self):
        return f"{self.location.name} - {self.timestamp} - {self.score}"


class Forecast(models.Model):
    """Model for storing weather forecasts"""
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='forecasts')
    forecast_date = models.DateField()
    forecast_time = models.TimeField()  # 3-hour intervals
    temperature_min = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    temperature_max = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    wind_speed = models.DecimalField(max_digits=4, decimal_places=1)
    wind_gust = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    wind_direction = models.IntegerField()
    precipitation_probability = models.IntegerField()  # percentage
    weather_description = models.CharField(max_length=255)
    icon_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['forecast_date', 'forecast_time']
        unique_together = ['location', 'forecast_date', 'forecast_time']

    def __str__(self):
        return f"{self.location.name} - {self.forecast_date} {self.forecast_time}"
