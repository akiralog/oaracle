document.addEventListener("DOMContentLoaded", () => {
    const select = document.getElementById('townSelect');
    const fetchBtn = document.getElementById('fetchBtn');
    const weatherOutput = document.getElementById('weatherOutput');
    const tideOutput = document.getElementById('tideOutput');

    const directionArrows = {
        N: "↑",
        NNE: "↗",
        NE: "↗",
        ENE: "↗",
        E: "→",
        ESE: "↘",
        SE: "↘",
        SSE: "↘",
        S: "↓",
        SSW: "↙",
        SW: "↙",
        WSW: "↙",
        W: "←",
        WNW: "↖",
        NW: "↖",
        NNW: "↖"
    };

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

                    // display current gust separately
                    let weatherHtml = `<p>Current gust: ${data.currentGust ?? "N/A"} mph</p>`;
                    weatherHtml += "<table><tr><th>Time</th><th>Temp (°C)</th><th>Wind (mph)</th><th>Direction</th></tr>";

                    tempData.forEach((tempEntry, i) => {
                        const time = tempEntry.dateTime.slice(11,16);
                        const temp = tempEntry.temperature;
                        const wind = windData[i] ? windData[i].speed : "N/A";
                        const directionText = windData[i] ? windData[i].directionText : "N/A";
                        const directionArrow = directionArrows[directionText] ?? "";
                        weatherHtml += `<tr><td>${time}</td><td>${temp}</td><td>${wind}</td><td>${directionArrow} ${directionText}</td></tr>`;
                    });

                    weatherHtml += "</table>";
                    weatherOutput.innerHTML = weatherHtml;
                } else {
                    weatherOutput.textContent = "No weather data available";
                }

                // tides
                if (isTidal && data.tides && data.tides.forecasts && data.tides.forecasts.tides) {
                    const days = data.tides.forecasts.tides.days;
                    let tideHtml = "<table><tr><th>DateTime</th><th>Height (m)</th><th>Type</th></tr>";

                    days.forEach(day => {
                        day.entries.forEach(entry => {
                            tideHtml += `<tr><td>${entry.dateTime}</td><td>${entry.height} m</td><td>${entry.type}</td></tr>`;
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
