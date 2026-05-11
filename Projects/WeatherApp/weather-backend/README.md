# Weather Backend Service

A Flask-based REST API microservice that fetches real-time weather data from OpenWeatherMap API.

## Features

- REST API endpoint to fetch weather data for 4 supported cities
- Integration with OpenWeatherMap API
- Health check endpoint
- Supported locations: New York, Sydney, Cape Town, Bangkok
- Containerized with Docker
- Environment variable configuration

## Getting Started

### Prerequisites

- Python 3.11+
- OpenWeatherMap API Key (get it from https://openweathermap.org/api)
- Docker (optional, for containerization)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd weather-backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create .env file**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your OpenWeatherMap API key:
   ```
   OPENWEATHER_API_KEY=your_api_key_here
   ```

### Running Locally (Python)

```bash
python app.py
```

The server will start on `http://localhost:5000`

### API Endpoints

#### 1. Health Check
```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "healthy"
}
```

#### 2. Get Weather Data
```bash
curl http://localhost:5000/weather/newyork
```

**Supported location keys:**
- `newyork` - New York
- `sydney` - Sydney
- `capetown` - Cape Town
- `bangkok` - Bangkok

Response Example:
```json
{
  "city": "New York",
  "temperature": 21.5,
  "description": "broken clouds",
  "humidity": 70,
  "wind_speed": 4.5
}
```

#### 3. Get Supported Locations
```bash
curl http://localhost:5000/locations
```

Response:
```json
{
  "supported_locations": ["newyork", "sydney", "capetown", "bangkok"],
  "location_names": {
    "newyork": "New York",
    "sydney": "Sydney",
    "capetown": "Cape Town",
    "bangkok": "Bangkok"
  }
}
```

### Building Docker Image

```bash
docker build -t weather-backend:latest .
```

### Running Docker Container

#### Method 1: With environment variable
```bash
docker run -p 5000:5000 -e OPENWEATHER_API_KEY=your_api_key_here weather-backend:latest
```

#### Method 2: Using .env file
```bash
docker run -p 5000:5000 --env-file .env weather-backend:latest
```

### Docker Compose (with frontend)

See the root project README for docker-compose configuration.

## Project Structure

```
weather-backend/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── .env.example       # Environment variables template
└── README.md          # This file
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK` - Successful request
- `400 Bad Request` - Invalid location
- `401 Unauthorized` - Invalid API key
- `404 Not Found` - City not found
- `504 Gateway Timeout` - OpenWeatherMap API timeout
- `500 Internal Server Error` - Server error

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key | `default_key` |
| `FLASK_ENV` | Flask environment | `development` |

## Troubleshooting

### "Invalid API key" error
- Ensure you've set the correct API key in `.env` or as an environment variable
- Verify the API key is active on OpenWeatherMap website

### "City not found" error
- Ensure you're using one of the supported location keys: newyork, sydney, capetown, bangkok

### Connection refused (container to container)
- When running with Docker Compose, use service name: `http://backend:5000`

## Dependencies

- **Flask** - Web framework
- **requests** - HTTP client library
- **python-dotenv** - Environment variable management

## Author

DevOps Course Team

## License

MIT License
