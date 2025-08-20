class OaracleApp {
    constructor() {
        this.selectedTown = null;
        this.townCoordinates = {
            'chiswick': { lat: 51.4875, lng: -0.2675, name: 'Chiswick' },
            'putney': { lat: 51.4619, lng: -0.2167, name: 'Putney' },
            'molesey': { lat: 51.3989, lng: -0.3647, name: 'Molesey' },
            'kingston': { lat: 51.4089, lng: -0.2975, name: 'Kingston' },
            'walton-on-thames': { lat: 51.3833, lng: -0.4167, name: 'Walton-on-Thames' }
        };
        this.init();
    }

    init() {
        this.bindEvents();
    }

    bindEvents() {
        const townSelect = document.getElementById('town-select');
        const getConditionsBtn = document.getElementById('get-conditions');
        const closeResultsBtn = document.getElementById('close-results');

        if (townSelect) {
            townSelect.addEventListener('change', (e) => {
                this.handleTownSelection(e.target.value);
            });
        }

        if (getConditionsBtn) {
            getConditionsBtn.addEventListener('click', () => {
                this.getRowingConditions();
            });
        }

        if (closeResultsBtn) {
            closeResultsBtn.addEventListener('click', () => {
                this.hideResultsPanel();
            });
        }
    }

    handleTownSelection(townValue) {
        const getConditionsBtn = document.getElementById('get-conditions');
        
        if (townValue && this.townCoordinates[townValue]) {
            this.selectedTown = this.townCoordinates[townValue];
            getConditionsBtn.disabled = false;
            getConditionsBtn.textContent = `Get Conditions for ${this.selectedTown.name}`;
        } else {
            this.selectedTown = null;
            getConditionsBtn.disabled = true;
            getConditionsBtn.textContent = 'Get Rowing Conditions';
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

    async getRowingConditions() {
        if (!this.selectedTown) {
            console.error('No town selected');
            return;
        }

        this.showLoading();

        try {
            const townKey = Object.keys(this.townCoordinates).find(
                key => this.townCoordinates[key].name === this.selectedTown.name
            );
            
            console.log('Sending request to:', `/api/town/${townKey}/`);
            
            // Call our Django backend API using the town endpoint
            const response = await fetch(`/api/town/${townKey}/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            console.log('Response status:', response.status);
            
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
        this.showResultsPanel();
        
        console.log('Received data:', data);
        
        // Update location info
        const resultsLocation = document.getElementById('results-location');
        if (resultsLocation) {
            resultsLocation.textContent = this.selectedTown.name;
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
        } else {
            const tideState = document.querySelector('.tide-state');
            if (tideState) {
                tideState.textContent = 'Could not fetch Environment Agency data';
            }
        }
        
        if (data.water_conditions?.next_tide_time !== undefined) {
            const tideTime = document.querySelector('.tide-time');
            if (tideTime) {
                tideTime.textContent = data.water_conditions.next_tide_time;
            }
        } else {
            const tideTime = document.querySelector('.tide-time');
            if (tideTime) {
                tideTime.textContent = 'No flow rate data available';
            }
        }
        
        if (data.water_conditions?.data_source !== undefined) {
            const tideSource = document.querySelector('.tide-source');
            if (tideSource) {
                tideSource.textContent = data.water_conditions.data_source;
            }
        } else {
            const tideSource = document.querySelector('.tide-source');
            if (tideSource) {
                tideSource.textContent = 'Environment Agency data unavailable';
            }
        }
        
        // Update tide details
        if (data.water_conditions?.measurement_time || data.water_conditions?.unit || data.water_conditions?.station_name) {
            const tideDetails = document.querySelector('.tide-details');
            if (tideDetails) {
                let details = [];
                if (data.water_conditions.station_name) {
                    details.push(`Station: ${data.water_conditions.station_name}`);
                }
                if (data.water_conditions.measurement_time) {
                    details.push(`Updated: ${data.water_conditions.measurement_time}`);
                }
                if (data.water_conditions.unit) {
                    details.push(`Unit: ${data.water_conditions.unit}`);
                }
                tideDetails.textContent = details.join(' | ');
            }
        } else {
            const tideDetails = document.querySelector('.tide-details');
            if (tideDetails) {
                tideDetails.textContent = 'No station data available';
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
        
        console.log('Conditions data:', data);
    }

    showError(message) {
        alert(`Error: ${message}`);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new OaracleApp();
});
