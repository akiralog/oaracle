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
                option.value = town;
                option.textContent = town;
                select.appendChild(option);
            });
        })
        .catch(error => console.error("Error fetching towns:", error));

    fetchBtn.addEventListener('click', () => {
        const selectedTown = select.value;
        output.textContent = `Fetching data for ${selectedTown}...`;
        // Later: fetch from WillyWeather API
    });
});
