// Oaracle - Rowing Conditions App
document.addEventListener('DOMContentLoaded', function() {
    const townSelect = document.getElementById('town-select');
    const getConditionsBtn = document.getElementById('get-conditions');
    const loading = document.getElementById('loading');
    const resultsPanel = document.getElementById('results-panel');
    const closeResultsBtn = document.getElementById('close-results');

    // Enable/disable button based on selection
    townSelect.addEventListener('change', function() {
        getConditionsBtn.disabled = !this.value;
    });

    // Get conditions button click
    getConditionsBtn.addEventListener('click', function() {
        const selectedTown = townSelect.value;
        if (selectedTown) {
            getRowingConditions(selectedTown);
        }
    });

    // Close results panel
    closeResultsBtn.addEventListener('click', function() {
        resultsPanel.classList.add('hidden');
    });

    async function getRowingConditions(townName) {
        // Show loading
        loading.classList.remove('hidden');
        resultsPanel.classList.add('hidden');

        try {
            // Call the weather API
            const response = await fetch('/api/weather/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    town_name: townName,
                    days: 1
                })
            });

            const data = await response.json();

            if (response.ok) {
                displayRowingConditions(data, townName);
            } else {
                console.error('Error fetching weather data:', data.error);
                showError('Failed to fetch weather data. Please try again.');
            }
        } catch (error) {
            console.error('Network error:', error);
            showError('Network error. Please check your connection and try again.');
        } finally {
            loading.classList.add('hidden');
        }
    }

    function displayRowingConditions(data, townName) {
        // Update location info
        document.getElementById('results-location').textContent = `${townName} - WillyWeather ID: ${data.town.location_id}`;

        // Parse and display weather data
        if (data.weather_data) {
            displayWindConditions(data.weather_data);
            displayDaylightConditions(data.weather_data);
        }

        // Parse and display tide data if available
        if (data.tide_data && data.town.is_tidal) {
            displayTideConditions(data.tide_data);
        } else {
            // Hide tide card if no tide data
            const tideCard = document.querySelector('.tide-card');
            if (tideCard) {
                tideCard.style.display = 'none';
            }
        }

        // Show results
        resultsPanel.classList.remove('hidden');
    }

    function displayWindConditions(weatherData) {
        const windCard = document.querySelector('.wind-card .condition-data');
        const forecasts = weatherData.forecasts || {};
        const windData = forecasts.wind;

        if (windData && windData.days && windData.days[0] && windData.days[0].entries) {
            const windEntry = windData.days[0].entries[0];
            const speed = windEntry.speed || 'N/A';
            const direction = windEntry.directionText || 'N/A';
            const gustSpeed = windEntry.gustSpeed;

            windCard.innerHTML = `
                <p class="wind-speed"><strong>${speed} mph</strong></p>
                <p class="wind-direction">${direction}</p>
                ${gustSpeed ? `<p class="wind-gusts">Gusts: ${gustSpeed} mph</p>` : ''}
            `;
        } else {
            windCard.innerHTML = '<p>Wind data unavailable</p>';
        }
    }

    function displayTideConditions(tideData) {
        const tideCard = document.querySelector('.tide-card .condition-data');
        const forecasts = tideData.forecasts || {};
        const tidesData = forecasts.tides;

        if (tidesData && tidesData.days && tidesData.days[0] && tidesData.days[0].entries) {
            const todayTides = tidesData.days[0].entries;
            let tideInfo = '';

            // Show next few tides
            todayTides.slice(0, 3).forEach(tide => {
                const time = new Date(tide.dateTime).toLocaleTimeString('en-GB', { 
                    hour: '2-digit', 
                    minute: '2-digit' 
                });
                const type = tide.type === 'high' ? 'High' : 'Low';
                const height = tide.height || 'N/A';
                tideInfo += `<p><strong>${time} - ${type}</strong>: ${height}m</p>`;
            });

            tideCard.innerHTML = tideInfo;
        } else {
            tideCard.innerHTML = '<p>Tide data unavailable</p>';
        }

        // Show the tide card
        const tideCardElement = document.querySelector('.tide-card');
        if (tideCardElement) {
            tideCardElement.style.display = 'block';
        }
    }

    function displayDaylightConditions(weatherData) {
        const daylightCard = document.querySelector('.daylight-card .condition-data');
        const forecasts = weatherData.forecasts || {};
        const sunData = forecasts.sun;

        if (sunData && sunData.days && sunData.days[0] && sunData.days[0].entries) {
            const sunEntries = sunData.days[0].entries;
            let sunrise = 'N/A';
            let sunset = 'N/A';

            sunEntries.forEach(entry => {
                if (entry.type === 'sunrise') {
                    sunrise = new Date(entry.dateTime).toLocaleTimeString('en-GB', { 
                        hour: '2-digit', 
                        minute: '2-digit' 
                    });
                } else if (entry.type === 'sunset') {
                    sunset = new Date(entry.dateTime).toLocaleTimeString('en-GB', { 
                        hour: '2-digit', 
                        minute: '2-digit' 
                    });
                }
            });

            daylightCard.innerHTML = `
                <p class="sunrise"><strong>Sunrise:</strong> ${sunrise}</p>
                <p class="sunset"><strong>Sunset:</strong> ${sunset}</p>
            `;
        } else {
            daylightCard.innerHTML = '<p>Daylight data unavailable</p>';
        }
    }

    function showError(message) {
        // Create a simple error display
        const errorDiv = document.createElement('div');
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #f5c6cb;
            z-index: 1000;
            max-width: 300px;
        `;
        errorDiv.textContent = message;
        
        document.body.appendChild(errorDiv);
        
        // Remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }
});
