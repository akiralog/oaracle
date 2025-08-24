document.addEventListener("DOMContentLoaded", () => {
    const select = document.getElementById('townSelect');
    const fetchBtn = document.getElementById('fetchBtn');
    const weatherOutput = document.getElementById('weatherOutput');
    const tideOutput = document.getElementById('tideOutput');

    fetch('/api/towns/')
        .then(response => response.json())
        .then(data => {
            data.towns.forEach(town => {
                const option = document.createElement('option');
                option.value = town.location_id;
                option.textContent = town.name;
                option.dataset.isTidal = town.is_tidal;
                select.appendChild(option);
            });
        })
        .catch(err => console.error("Error fetching towns:", err));

    fetchBtn.addEventListener('click', () => {
        const selectedOption = select.options[select.selectedIndex];
        const locationId = selectedOption.value;
        const isTidal = selectedOption.dataset.isTidal === "true";

        weatherOutput.textContent = "Fetching weather...";
        tideOutput.textContent = "Fetching tides...";

        fetch(`/api/fetch_data/?location_id=${locationId}&is_tidal=${isTidal}`)
            .then(response => response.json())
            .then(data => {
                if (data.weather && data.weather.forecasts) {
                    const forecast = data.weather.forecasts;
                    let weatherHtml = "<table><tr><th>Type</th><th>Value</th></tr>";

                    for (const key in forecast) {
                        if (forecast.hasOwnProperty(key)) {
                            weatherHtml += `<tr><td>${key}</td><td>${JSON.stringify(forecast[key])}</td></tr>`;
                        }
                    }

                    weatherHtml += "</table>";
                    weatherOutput.innerHTML = weatherHtml;
                } else {
                    weatherOutput.textContent = "No weather data available";
                }

                if (isTidal && data.tides && data.tides.forecasts && data.tides.forecasts.tides) {
                    const days = data.tides.forecasts.tides.days;
                    let tideHtml = "<table><tr><th>DateTime</th><th>Height</th><th>Type</th></tr>";

                    days.forEach(day => {
                        day.entries.forEach(entry => {
                            tideHtml += `<tr><td>${entry.dateTime}</td><td>${entry.height}</td><td>${entry.type}</td></tr>`;
                        });
                    });

                    tideHtml += "</table>";
                    tideOutput.innerHTML = tideHtml;
                } else {
                    tideOutput.textContent = "No tide data available";
                }
            })
            .catch(err => {
                weatherOutput.textContent = "Error fetching weather";
                tideOutput.textContent = "Error fetching tides";
                console.error(err);
            });
    });
});
