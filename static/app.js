document.addEventListener("DOMContentLoaded", () => {
    const select = document.getElementById('townSelect');
    const output = document.getElementById('output');
    const fetchBtn = document.getElementById('fetchBtn');

    // Fetch towns from backend
    fetch('/api/towns/')
        .then(response => response.json())
        .then(data => {
            data.towns.forEach(town => {
                const option = document.createElement('option');
                option.value = town.location_id;        // store location_id
                option.textContent = town.name;         // display town name
                option.dataset.isTidal = town.is_tidal; // store is_tidal 
                select.appendChild(option);
            });
        })
        .catch(error => console.error("Error fetching towns:", error));

    fetchBtn.addEventListener('click', () => {
        const selectedOption = select.options[select.selectedIndex];
        const selectedTownName = selectedOption.textContent;
        const selectedLocationId = selectedOption.value;
        const isTidal = selectedOption.dataset.isTidal === "true";

        output.textContent = `Fetching data for ${selectedTownName} (ID: ${selectedLocationId})...`;
        console.log(`Is tidal? ${isTidal}`);

        // Later: fetch weather/tide data from Django backend or WillyWeather API
    });
});
