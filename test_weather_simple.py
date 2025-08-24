#!/usr/bin/env python3
"""
Simple test script to verify the basic setup works
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append('/c:/Users/Nikolai/Desktop/oaracle')

# Set Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oaracle_backend.settings')
django.setup()

from conditions.models import ThamesTown

def test_basic_setup():
    """Test that the basic Django setup works"""
    print("🧪 Testing basic Django setup...")
    
    # Test that we can access the model
    try:
        towns = ThamesTown.objects.all()
        print(f"✅ Database connection works! Found {towns.count()} towns")
        
        for town in towns:
            tidal_status = "🌊 Tidal" if town.is_tidal else "🏘️ Non-tidal"
            print(f"   - {town.town_name} (ID: {town.location_id}, {tidal_status})")
            
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    print("\n✅ Basic setup test completed!")
    return True

if __name__ == "__main__":
    test_basic_setup()
