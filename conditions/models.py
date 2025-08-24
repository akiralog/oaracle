from django.db import models


class ThamesTown(models.Model):
    """Model that matches your working SQLite structure exactly"""
    town_name = models.CharField(max_length=255, unique=True)
    location_id = models.IntegerField(unique=True)  # WillyWeather location ID
    is_tidal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['town_name']

    def __str__(self):
        return self.town_name
