from django.shortcuts import render
from .models import ThamesTown


def index(request):
    """Main index view - serves the frontend"""
    towns = ThamesTown.objects.all()
    return render(request, 'index.html', {'towns': towns})
