from django.urls import path
from . import views

app_name = 'conditions'

urlpatterns = [
    path('conditions/', views.get_rowing_conditions, name='get_rowing_conditions'),
    path('town/<str:town_name>/', views.get_conditions_by_town, name='get_conditions_by_town'),
    path('score/', views.calculate_rowability_score_api, name='calculate_score'),
    path('location/<int:location_id>/', views.location_detail, name='location_detail'),
    path('health/', views.health_check, name='health_check'),
]

