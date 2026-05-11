# Weather Frontend Service

A Flask-based web dashboard that provides a user-friendly interface to check real-time weather data from the Weather Backend Service.

## Features

- Clean, modern UI with responsive design
- Dropdown menu to select from 4 major cities
- Real-time weather data display
- Shows temperature, weather description, humidity, and wind speed
- Error handling and loading states
- Containerized with Docker
- Easy backend service integration

## Technology Stack

- **Backend Framework**: Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Python Version**: 3.11+

## Getting Started

### Prerequisites

- Python 3.11+
- Docker (optional, for containerization)
- Weather Backend Service running (see weather-backend README)

### Installation

1. **Navigate to the project directory**
   ```bash
   cd weather-frontend
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

### Running Locally (Python)

```bash
python app.py
```

The dashboard will be available at `http://localhost:5000`

**Note**: Make sure the backend service is running on `http://localhost:5000` or set the `BACKEND_URL` environment variable.

### Running with Custom Backend URL

```bash
# Windows
set BACKEND_URL=http://backend-service:5000
python app.py

# Linux/Mac
export BACKEND_URL=http://backend-service:5000
python app.py
```

## Building Docker Image

```bash
docker build -t weather-frontend:latest .
```

## Running Docker Container

### Method 1: With localhost backend
```bash
docker run -p 5000:5000 -e BACKEND_URL=http://localhost:5000 weather-frontend:latest
```

### Method 2: With Docker Compose (Recommended)
See the root project README for docker-compose configuration.

## UI Screenshots

### Main Dashboard
The weather dashboard displays:
- City selection dropdown
- "Get Weather" button
- Real-time weather display with:
  - City name
  - Current temperature (°C)
  - Weather condition description
  - Humidity percentage
  - Wind speed (m/s)

### Supported Cities
- New York
- Sydney
- Cape Town
- Bangkok

## API Integration

The frontend communicates with the Backend Weather Service using:

**Endpoint**: `GET /weather/<location_key>`

**Example Request**:
```javascript
fetch('http://backend:5000/weather/newyork')
  .then(response => response.json())
  .then(data => console.log(data))
```

**Example Response**:
```json
{
  "city": "New York",
  "temperature": 21.5,
  "description": "broken clouds",
  "humidity": 70,
  "wind_speed": 4.5
}
```

## Project Structure

```
weather-frontend/
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── README.md          # This file
├── templates/
│   └── index.html     # Main dashboard HTML
└── static/
    ├── style.css      # Dashboard styling
    └── script.js      # Frontend logic and API calls
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `BACKEND_URL` | URL of the backend service | `http://localhost:5000` |
| `FLASK_ENV` | Flask environment | `development` |

## Features in Detail

### Responsive Design
- Works on desktop, tablet, and mobile devices
- Modern gradient background and card-based layout
- Smooth transitions and hover effects

### Error Handling
- Displays user-friendly error messages
- Handles network timeouts
- Validates input before API calls

### Loading States
- Shows loading message while fetching data
- Clear visual feedback for user actions

### Accessibility
- Semantic HTML structure
- Proper form labels and attributes
- Keyboard navigation support

## Troubleshooting

### "Failed to fetch weather" error
- Ensure the backend service is running
- Check that `BACKEND_URL` is set correctly
- Verify CORS is properly configured (if running on different domains)

### Dashboard not loading
- Ensure Flask is running (`python app.py`)
- Check that port 5000 is not in use
- Try clearing browser cache

### Backend connection refused (Docker)
- When using Docker Compose, use service name: `BACKEND_URL=http://backend:5000`
- For local testing, use `BACKEND_URL=http://localhost:5000`

## Development

### Running in Debug Mode
The Flask app runs with `debug=True` in development:
```bash
python app.py
```

Changes to `app.py`, `templates/`, or `static/` will auto-reload.

### JavaScript Console
Open browser DevTools (F12) to see console logs and debug API calls.

## Dependencies

- **Flask** - Web framework for serving the dashboard
- **Werkzeug** - WSGI toolkit (Flask dependency)

## Author

DevOps Course Team

## License

MIT License
