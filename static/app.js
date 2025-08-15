class OaracleApp {
    constructor() {
        this.map = null;
        this.currentMarker = null;
        this.selectedLocation = null;
        this.init();
    }

    init() {
        this.initializeMap();
        this.bindEvents();
        this.showInstructions();
    }

    initializeMap() {
        // Initialize the map centered on the UK
        this.map = L.map('map', {
            center: [54.0, -2.0],
            zoom: 6,
            zoomControl: true,
            attributionControl: true
        });

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 18
        }).addTo(this.map);

        this.map.on('click', (e) => {
            this.handleMapClick(e);
        });
    }

    bindEvents() {
        const dismissBtn = document.getElementById('dismiss-instructions');
        if (dismissBtn) {
            dismissBtn.addEventListener('click', () => {
                this.hideInstructions();
            });
        }

        const getConditionsBtn = document.getElementById('get-conditions');
        if (getConditionsBtn) {
            getConditionsBtn.addEventListener('click', () => {
                this.getRowingConditions();
            });
        }

        const closeResultsBtn = document.getElementById('close-results');
        if (closeResultsBtn) {
            closeResultsBtn.addEventListener('click', () => {
                this.hideResultsPanel();
            });
        }
    }

    showInstructions() {
        const instructions = document.getElementById('instructions');
        if (instructions) {
            instructions.style.display = 'block';
        }
    }

    hideInstructions() {
        const instructions = document.getElementById('instructions');
        if (instructions) {
            instructions.style.display = 'none';
        }
    }

    handleMapClick(e) {
        const { lat, lng } = e.latlng;
        
        // Remove previous marker if exists
        if (this.currentMarker) {
            this.map.removeLayer(this.currentMarker);
        }
        this.currentMarker = L.marker([lat, lng], {
            icon: this.createCustomIcon()
        }).addTo(this.map);
        this.selectedLocation = { lat, lng };
        this.showLocationPanel();
        this.getLocationDetails(lat, lng);
        this.hideInstructions();
    }

    createCustomIcon() {
        return L.divIcon({
            className: 'custom-marker',
            html: '📍',
            iconSize: [32, 32],
            iconAnchor: [16, 32]
        });
    }

    showLocationPanel() {
        const locationPanel = document.getElementById('location-panel');
        if (locationPanel) {
            locationPanel.classList.remove('hidden');
        }
    }

    hideLocationPanel() {
        const locationPanel = document.getElementById('location-panel');
        if (locationPanel) {
            locationPanel.classList.add('hidden');
        }
    }

    showResultsPanel() {
        const resultsPanel = document.getElementById('results-panel');
        if (resultsPanel) {
            resultsPanel.classList.remove('hidden');
        }
    }

    hideResultsPanel() {
        const resultsPanel = document.getElementById('results-panel');
        if (resultsPanel) {
            resultsPanel.classList.add('hidden');
        }
    }

    async getLocationDetails(lat, lng) {
        try {
            // Using OpenStreetMap Nominatim API for reverse geocoding
            const response = await fetch(
                `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=10&addressdetails=1`
            );
            
            if (!response.ok) {
                throw new Error('Failed to fetch location details');
            }

            const data = await response.json();
            this.displayLocationDetails(data);
        } catch (error) {
            console.error('Error fetching location details:', error);
            this.displayLocationDetails({
                display_name: `Location at ${lat.toFixed(4)}, ${lng.toFixed(4)}`
            });
        }
    }

    displayLocationDetails(data) {
        const locationText = document.getElementById('location-text');
        if (locationText) {
            // Extract useful information from the response
            let displayText = data.display_name || 'Unknown location';
            
            // Try to get a more user-friendly description
            if (data.address) {
                const address = data.address;
                let parts = [];
                
                if (address.waterway) parts.push(address.waterway);
                if (address.river) parts.push(address.river);
                if (address.city) parts.push(address.city);
                else if (address.town) parts.push(address.town);
                else if (address.village) parts.push(address.village);
                
                if (parts.length > 0) {
                    displayText = parts.join(', ');
                }
            }
            
            locationText.textContent = displayText;
        }
    }

    async getRowingConditions() {
        if (!this.selectedLocation) {
            console.error('No location selected');
            return;
        }

        this.showLoading();

        try {
            console.log('Sending request to:', '/api/conditions/');
            console.log('Request data:', {
                latitude: this.selectedLocation.lat,
                longitude: this.selectedLocation.lng,
                include_weather: true,
                include_water: true,
                include_forecast: true,
                days_ahead: 7
            });
            
            // Call our Django backend API
            const response = await fetch('/api/conditions/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    latitude: this.selectedLocation.lat,
                    longitude: this.selectedLocation.lng,
                    include_weather: true,
                    include_water: true,
                    include_forecast: true,
                    days_ahead: 7
                })
            });
            
            console.log('Response status:', response.status);
            console.log('Response headers:', response.headers);
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('Response error text:', errorText);
                throw new Error(`HTTP error! status: ${response.status}, body: ${errorText}`);
            }
            
            const data = await response.json();
            console.log('Response data:', data);
            
            this.hideLoading();
            this.showConditionsResult(data);
            
        } catch (error) {
            console.error('Error fetching conditions:', error);
            this.hideLoading();
            this.showError(`Failed to fetch rowing conditions: ${error.message}`);
        }
    }

    showLoading() {
        const loading = document.getElementById('loading');
        if (loading) {
            loading.classList.remove('hidden');
        }
    }

    hideLoading() {
        const loading = document.getElementById('loading');
        if (loading) {
            loading.classList.add('hidden');
        }
    }

    showConditionsResult(data) {
        // Hide the location panel and show results
        this.hideLocationPanel();
        this.showResultsPanel();
        
        console.log('Received data:', data); // Debug log
        
        // Update location info
        const resultsLocation = document.getElementById('results-location');
        if (resultsLocation) {
            resultsLocation.textContent = data.location?.name || 'Selected location';
        }
        
        // Update wind data
        if (data.current_conditions?.wind_speed !== undefined) {
            const windSpeed = document.querySelector('.wind-speed');
            if (windSpeed) {
                windSpeed.textContent = `${data.current_conditions.wind_speed} m/s`;
            }
        }
        
        if (data.current_conditions?.wind_direction !== undefined) {
            const windDirection = document.querySelector('.wind-direction');
            if (windDirection) {
                windDirection.textContent = data.current_conditions.wind_direction;
            }
        }
        
        // Update tide data
        if (data.water_conditions?.tide_state !== undefined) {
            const tideState = document.querySelector('.tide-state');
            if (tideState) {
                tideState.textContent = data.water_conditions.tide_state;
            }
        }
        
        if (data.water_conditions?.next_tide_time !== undefined) {
            const tideTime = document.querySelector('.tide-time');
            if (tideTime) {
                tideTime.textContent = data.water_conditions.next_tide_time;
            }
        }
        
        // Update daylight data
        if (data.current_conditions?.sunrise !== undefined) {
            const sunrise = document.querySelector('.sunrise');
            if (sunrise) {
                sunrise.textContent = `Sunrise: ${data.current_conditions.sunrise}`;
            }
        }
        
        if (data.current_conditions?.sunset !== undefined) {
            const sunset = document.querySelector('.sunset');
            if (sunset) {
                sunset.textContent = `Sunset: ${data.current_conditions.sunset}`;
            }
        }
        
        // Log the full data for debugging
        console.log('Conditions data:', data);
    }

    showError(message) {
        alert(`Error: ${message}`);
    }

    // Utility method to get current location
    getCurrentLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const { latitude, longitude } = position.coords;
                    this.map.setView([latitude, longitude], 12);
                    
                    // Simulate a click at current location
                    this.handleMapClick({
                        latlng: { lat: latitude, lng: longitude }
                    });
                },
                (error) => {
                    console.error('Error getting current location:', error);
                }
            );
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new OaracleApp();
});
