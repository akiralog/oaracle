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
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            this.hideLoading();
            this.showConditionsResult(data);
            
        } catch (error) {
            console.error('Error fetching conditions:', error);
            this.hideLoading();
            this.showError('Failed to fetch rowing conditions. Please try again.');
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
        // Display the conditions data
        console.log('Conditions data:', data);
        
        // For now, show a basic summary
        let message = `Location: ${data.location.name}\n`;
        if (data.current_conditions) {
            message += `Temperature: ${data.current_conditions.temperature}°C\n`;
            message += `Wind: ${data.current_conditions.wind_speed} m/s\n`;
            message += `Weather: ${data.current_conditions.weather_description}`;
        }
        
        if (data.rowability_score) {
            message += `\n\nRowability Score: ${data.rowability_score.score}/10 (${data.rowability_score.category})`;
            if (data.rowability_score.recommendations.length > 0) {
                message += `\n\nRecommendations:\n${data.rowability_score.recommendations.join('\n')}`;
            }
        }
        
        alert(message);
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
