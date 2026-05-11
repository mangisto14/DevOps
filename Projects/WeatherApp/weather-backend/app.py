from flask import Flask, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Supported locations mapping
locations = {
    "newyork": "New York",
    "sydney": "Sydney",
    "capetown": "Cape Town",
    "bangkok": "Bangkok"
}

# OpenWeatherMap API Configuration
API_KEY = os.getenv('OPENWEATHER_API_KEY', 'default_key')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

@app.route('/weather/<location_key>', methods=['GET'])
def get_weather(location_key):
    """
    Get weather data for a specific location
    
    Args:
        location_key: lowercase location identifier (newyork, sydney, capetown, bangkok)
    
    Returns:
        JSON response with weather data or error message
    """
    # Validate location key
    if location_key.lower() not in locations:
        return jsonify({
            "error": "Invalid location",
            "supported_locations": list(locations.keys())
        }), 400
    
    city_name = locations[location_key.lower()]
    
    try:
        # Fetch data from OpenWeatherMap API
        params = {
            "q": city_name,
            "appid": API_KEY,
            "units": "metric"
        }
        
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract relevant weather information
        weather_response = {
            "city": data.get("name"),
            "temperature": data.get("main", {}).get("temp"),
            "description": data.get("weather", [{}])[0].get("description", "N/A"),
            "humidity": data.get("main", {}).get("humidity"),
            "wind_speed": data.get("wind", {}).get("speed")
        }
        
        return jsonify(weather_response), 200
    
    except requests.exceptions.Timeout:
        return jsonify({"error": "Request timeout while fetching weather data"}), 504
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            return jsonify({"error": "Invalid API key"}), 401
        elif response.status_code == 404:
            return jsonify({"error": "City not found"}), 404
        else:
            return jsonify({"error": "Error fetching weather data"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/locations', methods=['GET'])
def get_locations():
    """Get list of supported locations"""
    return jsonify({
        "supported_locations": list(locations.keys()),
        "location_names": locations
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
