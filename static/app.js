document.addEventListener("DOMContentLoaded", () => {
    const select = document.getElementById('townSelect');
    const output = document.getElementById('output');
    const fetchBtn = document.getElementById('fetchBtn');

    // Temporary town list (will be replaced by backend API later)
    const towns = ["Chiswick", "Putney", "Hammersmith", "Richmond"];

    towns.forEach(town => {
        const option = document.createElement('option');
        option.value = town;
        option.textContent = town;
        select.appendChild(option);
    });

    fetchBtn.addEventListener('click', () => {
        const selectedTown = select.value;
        output.textContent = `Fetching data for ${selectedTown}...`;
        // Later: fetch from Django backend API
    });
});
