document.addEventListener("DOMContentLoaded", () => {
    const select = document.getElementById('townSelect');
    const fetchBtn = document.getElementById('fetchBtn');
    const weatherOutput = document.getElementById('weatherOutput');
    const tideOutput = document.getElementById('tideOutput');

    // fetch towns from backend
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
                // weather
                if (data.weather && data.weather.forecasts && data.weather.forecasts.temperature) {
                    const tempData = data.weather.forecasts.temperature.days[0].entries;
                    const windData = data.weather.forecasts.wind.days[0].entries;

                    // display current wind & gust
                    let weatherHtml = `<p>Current wind: ${data.currentWind ?? "N/A"} mph</p>`;
                    weatherHtml += `<p>Current gust: ${data.currentGust ?? "N/A"} mph</p>`;
                    weatherHtml += "<table><tr><th>Time</th><th>Temp (°C)</th><th>Wind (mph)</th><th>Direction</th></tr>";

                    tempData.forEach((tempEntry, i) => {
                        const time = tempEntry.dateTime.slice(11,16);
                        const temp = tempEntry.temperature;
                        const wind = windData[i] ? windData[i].speed : "N/A";
                        const direction = windData[i] ? windData[i].directionText : "N/A";
                        weatherHtml += `<tr><td>${time}</td><td>${temp}</td><td>${wind}</td><td>${direction}</td></tr>`;
                    });

                    weatherHtml += "</table>";
                    weatherOutput.innerHTML = weatherHtml;
                } else {
                    weatherOutput.textContent = "No weather data available";
                }

                // tides
                if (isTidal && data.tides && data.tides.forecasts && data.tides.forecasts.tides) {
                    const days = data.tides.forecasts.tides.days;
                    
                    // find next tide
                    let nextTide = null;
                    const now = new Date();
                    outer: for (const day of days) {
                        for (const entry of day.entries) {
                            const tideTime = new Date(entry.dateTime);
                            if (tideTime > now) {
                                nextTide = entry;
                                break outer;
                            }
                        }
                    }

                    let tideHtml = "";
                    if (nextTide) {
                        const tideDate = new Date(nextTide.dateTime);
                        const hours = tideDate.getHours() % 12 || 12;
                        const minutes = tideDate.getMinutes().toString().padStart(2, '0');
                        const ampm = tideDate.getHours() >= 12 ? "PM" : "AM";
                        tideHtml += `<p>Next tide: ${nextTide.type} at ${hours}:${minutes} ${ampm}</p>`;
                    }

                    tideHtml += "<table><tr><th>Time</th><th>Height (m)</th><th>Type</th></tr>";

                    days.forEach(day => {
                        day.entries.forEach(entry => {
                            const tideDate = new Date(entry.dateTime);
                            const hours = tideDate.getHours() % 12 || 12;
                            const minutes = tideDate.getMinutes().toString().padStart(2, '0');
                            const ampm = tideDate.getHours() >= 12 ? "PM" : "AM";
                            const timeStr = `${hours}:${minutes} ${ampm}`;

                            tideHtml += `<tr><td>${timeStr}</td><td>${entry.height} m</td><td>${entry.type}</td></tr>`;
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
