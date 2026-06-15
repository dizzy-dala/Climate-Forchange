document.addEventListener('DOMContentLoaded', function () {
    const locationButton = document.getElementById('use-location-btn');
    const weatherError = document.getElementById('weather-error');
    const weatherCard = document.getElementById('weather-card');
    const cityInput = document.getElementById('city');

    locationButton.addEventListener('click', function () {
        if (!navigator.geolocation) {
            showError('Geolocation is not supported by your browser.');
            return;
        }

        showError('Finding your location...');

        navigator.geolocation.getCurrentPosition(
            function (position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                fetchWeather(lat, lon);
            },
            function () {
                showError('Unable to retrieve your location. Please allow location access and try again.');
            }
        );
    });

    function showError(message) {
        weatherError.textContent = message;
        if (weatherCard) {
            weatherCard.style.display = 'none';
        }
    }

    function fetchWeather(lat, lon) {
        const url = `/api/weather/?lat=${encodeURIComponent(lat)}&lon=${encodeURIComponent(lon)}`;
        fetch(url)
            .then(function (response) {
                if (!response.ok) {
                    return response.json().then(function (data) {
                        throw new Error(data.error || 'Unable to fetch weather.');
                    });
                }
                return response.json();
            })
            .then(function (data) {
                if (data.error) {
                    showError(data.error);
                    return;
                }
                weatherError.textContent = '';
                updateWeatherCard(data);
            })
            .catch(function (error) {
                showError(error.message);
            });
    }

    function updateWeatherCard(data) {
        if (!weatherCard) {
            return;
        }

        weatherCard.style.display = 'block';
        document.getElementById('weather-city').textContent = `🌡 Current weather in ${data.city}`;
        document.getElementById('weather-temperature').textContent = `${data.temperature} °C`;
        document.getElementById('weather-humidity').textContent = `${data.humidity}%`;
        document.getElementById('weather-wind').textContent = `${data.wind_speed} m/s`;
        document.getElementById('weather-rain').textContent = `${data.rainfall} mm`;
        document.getElementById('weather-description').textContent = data.description;
        document.getElementById('weather-advice').textContent = data.advice || 'No additional advice available.';
        const forecastLink = document.getElementById('weather-forecast-link');
        forecastLink.href = data.forecast_link;
        forecastLink.textContent = 'View extended forecast';
        cityInput.value = data.city;
    }
});