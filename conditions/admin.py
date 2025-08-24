from django.contrib import admin
from .models import ThamesTown


@admin.register(ThamesTown)
class ThamesTownAdmin(admin.ModelAdmin):
    list_display = ['town_name', 'location_id', 'is_tidal', 'created_at']
    list_filter = ['is_tidal']
    search_fields = ['town_name']
