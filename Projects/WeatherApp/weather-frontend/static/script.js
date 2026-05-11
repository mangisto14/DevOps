// Configuration - Get backend URL from HTML data attribute
const BACKEND_URL = document.documentElement.getAttribute('data-backend-url') || 'http://localhost:5000';

console.log('Backend URL:', BACKEND_URL);

// DOM Elements
const citySelect = document.getElementById('city-select');
const getWeatherBtn = document.getElementById('get-weather-btn');
const loadingDiv = document.getElementById('loading');
const errorDiv = document.getElementById('error');
const errorMessage = document.getElementById('error-message');
const weatherResult = document.getElementById('weather-result');

// Event Listeners
getWeatherBtn.addEventListener('click', getWeather);
citySelect.addEventListener('change', function() {
    // Clear previous results when city changes
    weatherResult.style.display = 'none';
    errorDiv.style.display = 'none';
});

/**
 * Fetch weather data from backend
 */
async function getWeather() {
    const selectedCity = citySelect.value;

    // Validation
    if (!selectedCity) {
        showError('Please select a city');
        return;
    }

    try {
        // Show loading state
        loadingDiv.style.display = 'block';
        errorDiv.style.display = 'none';
        weatherResult.style.display = 'none';

        // Construct backend URL
        const url = `${BACKEND_URL}/weather/${selectedCity}`;
        console.log('Fetching from:', url);

        // Fetch weather data
        const response = await fetch(url);

        if (!response.ok) {
            try {
                const errorData = await response.json();
                throw new Error(errorData.error || `Error: ${response.status}`);
            } catch (parseError) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
        }

        const data = await response.json();

        // Display weather data
        displayWeather(data);
        loadingDiv.style.display = 'none';

    } catch (error) {
        loadingDiv.style.display = 'none';
        showError(`Failed to fetch weather: ${error.message}`);
        console.error('Error:', error);
    }
}

/**
 * Display weather data on the page
 */
function displayWeather(data) {
    document.getElementById('city-name').textContent = data.city || 'Unknown';
    document.getElementById('temperature').textContent = 
        data.temperature !== null ? `${data.temperature}°C` : 'N/A';
    document.getElementById('description').textContent = 
        data.description || 'N/A';
    document.getElementById('humidity').textContent = 
        data.humidity !== null ? `${data.humidity}%` : 'N/A';
    document.getElementById('wind-speed').textContent = 
        data.wind_speed !== null ? `${data.wind_speed} m/s` : 'N/A';

    weatherResult.style.display = 'block';
}

/**
 * Show error message
 */
function showError(message) {
    errorMessage.textContent = message;
    errorDiv.style.display = 'block';
    weatherResult.style.display = 'none';
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Weather Dashboard loaded');
    console.log('Backend URL:', BACKEND_URL);
});
