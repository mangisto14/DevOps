# 🌤️ Weather Dashboard Microservices - Phase 1

A complete containerized microservices application featuring a weather dashboard built with Flask and Docker.

**This project demonstrates DevOps best practices with:**
- Microservices architecture (Backend + Frontend)
- Docker containerization
- Docker Compose orchestration
- REST API integration
- Production-ready code structure

---

## 📋 Table of Contents

1. [Features](#features)
2. [Project Architecture](#project-architecture)
3. [Prerequisites](#prerequisites)
4. [Quick Start](#quick-start)
5. [Detailed Setup](#detailed-setup)
6. [Docker Deployment](#docker-deployment)
7. [Testing](#testing)
8. [Project Structure](#project-structure)
9. [Troubleshooting](#troubleshooting)

---

## ✨ Features

✅ **Backend Weather Service**
- Fetches real-time weather data from OpenWeatherMap API
- Supports 4 major cities: New York, Sydney, Cape Town, Bangkok
- RESTful API with health check endpoint
- Proper error handling and validation
- Environment variable configuration

✅ **Frontend Weather Dashboard**
- Modern, responsive UI with gradient design
- City selection dropdown menu
- Real-time weather display (temperature, humidity, wind speed, conditions)
- Error handling and loading states
- Smooth animations and hover effects

✅ **Docker & DevOps**
- Production-ready Dockerfiles for both services
- Docker Compose orchestration
- Health checks for both services
- Network communication between containers
- Volume mounts for development

---

## 🏗️ Project Architecture

### Microservices Design

```
┌─────────────────────────────────────────────────────┐
│                 Docker Network                      │
├──────────────────────┬──────────────────────────────┤
│                      │                              │
│   Frontend Service   │   Backend Service           │
│  (Port 5000)        │  (Port 5001 external,      │
│                      │   5000 internal)            │
│  - Flask App         │  - Flask API                │
│  - HTML/CSS/JS       │  - requests library        │
│  - Dashboard UI      │  - OpenWeatherMap API      │
│                      │                              │
└──────────────────────┴──────────────────────────────┘
         ↓ HTTP (http://backend:5000)
    OpenWeatherMap API
```

### Communication Flow

1. User opens dashboard → Frontend (port 5000)
2. User selects city and clicks "Get Weather"
3. Frontend calls Backend API at `http://backend:5000/weather/<city>`
4. Backend fetches data from OpenWeatherMap
5. Backend returns JSON response
6. Frontend displays weather data on dashboard

---

## 📦 Prerequisites

### For Local Development

- **Python 3.11+**
- **pip** (Python package manager)
- **OpenWeatherMap API Key** (free tier available at https://openweathermap.org/api)

### For Docker Deployment

- **Docker** (version 20.10+)
- **Docker Compose** (version 1.29+)
- **OpenWeatherMap API Key**

---

## 🚀 Quick Start (Docker Compose - Recommended)

### 1. Clone/Navigate to Project

```bash
cd weather-dashboard
```

### 2. Get OpenWeatherMap API Key

1. Visit https://openweathermap.org/api
2. Sign up for a free account
3. Generate an API key
4. Copy and save the API key

### 3. Create .env File

```bash
# Create .env file in project root
echo "OPENWEATHER_API_KEY=your_api_key_here" > .env
```

Or manually create `.env`:
```
OPENWEATHER_API_KEY=your_api_key_here
```

### 4. Build and Run with Docker Compose

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### 5. Access Dashboard

Open your browser and go to:
```
http://localhost:5000
```

### 6. Test the Application

- Select a city from dropdown
- Click "Get Weather" button
- View live weather data

---

## 🔧 Detailed Setup

### Option 1: Local Development (Python)

**Backend Setup:**

```bash
# Navigate to backend
cd weather-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your API key
# Then run backend
python app.py
```

Backend will be running on `http://localhost:5000`

**Frontend Setup (in new terminal):**

```bash
# Navigate to frontend
cd weather-frontend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set backend URL
# Windows:
set BACKEND_URL=http://localhost:5000
# Linux/Mac:
export BACKEND_URL=http://localhost:5000

# Run frontend
python app.py
```

Frontend will be running on `http://localhost:5000`

**Note**: If running both locally, access backend on different port or use separate terminal windows.

### Option 2: Docker Build and Run

**Build Docker Images:**

```bash
# Build backend image
docker build -t weather-backend:1.0 ./weather-backend

# Build frontend image
docker build -t weather-frontend:1.0 ./weather-frontend
```

**Run Backend Container:**

```bash
docker run -d \
  --name weather-backend \
  -p 5001:5000 \
  -e OPENWEATHER_API_KEY=your_api_key_here \
  weather-backend:1.0
```

**Run Frontend Container:**

```bash
docker run -d \
  --name weather-frontend \
  -p 5000:5000 \
  -e BACKEND_URL=http://localhost:5001 \
  weather-frontend:1.0
```

Open browser: `http://localhost:5000`

---

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# View status
docker-compose ps

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs frontend
docker-compose logs backend

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Environment Variables

Edit `docker-compose.yml` or create `.env`:

```env
OPENWEATHER_API_KEY=your_api_key_here
```

### Accessing Services

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend Dashboard | http://localhost:5000 | Weather dashboard UI |
| Backend API | http://localhost:5001 | RESTful API (external) |
| Backend Health | http://localhost:5001/health | Service health check |

---

## 🧪 Testing

### Test Backend API

**Test Health Endpoint:**
```bash
curl http://localhost:5001/health
```

**Test Weather Endpoint:**
```bash
# New York
curl http://localhost:5001/weather/newyork

# Sydney
curl http://localhost:5001/weather/sydney

# Cape Town
curl http://localhost:5001/weather/capetown

# Bangkok
curl http://localhost:5001/weather/bangkok
```

**Test Supported Locations:**
```bash
curl http://localhost:5001/locations
```

### Test Frontend

1. Open http://localhost:5000
2. Select a city from dropdown
3. Click "Get Weather" button
4. Verify weather data is displayed

### Test with Docker Compose

```bash
# Test backend from frontend container
docker-compose exec frontend curl http://backend:5000/health

# Test weather API
docker-compose exec frontend curl http://backend:5000/weather/newyork
```

---

## 📁 Project Structure

```
weather-dashboard/
│
├── docker-compose.yml              # Docker Compose configuration
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore patterns
├── README.md                       # This file
│
├── weather-backend/                # Backend microservice
│   ├── app.py                      # Flask API application
│   ├── requirements.txt            # Python dependencies
│   ├── Dockerfile                  # Docker configuration
│   ├── .env.example                # Environment template
│   └── README.md                   # Backend documentation
│
└── weather-frontend/               # Frontend microservice
    ├── app.py                      # Flask web application
    ├── requirements.txt            # Python dependencies
    ├── Dockerfile                  # Docker configuration
    ├── README.md                   # Frontend documentation
    ├── templates/
    │   └── index.html              # HTML dashboard template
    └── static/
        ├── style.css               # Dashboard styling
        └── script.js               # Frontend JavaScript logic
```

---

## 🔍 Troubleshooting

### Issue: "Connection refused" when frontend calls backend

**Solution**: Ensure both services are running and use correct backend URL:
- **Local development**: `http://localhost:5001` (different port)
- **Docker Compose**: `http://backend:5000` (service name)

### Issue: "Invalid API key" error

**Solution**: 
1. Verify API key in `.env` file
2. Ensure API key is active on OpenWeatherMap website
3. Try regenerating a new API key

### Issue: City not found

**Solution**: Ensure you're using one of these location keys:
- `newyork`
- `sydney`
- `capetown`
- `bangkok`

### Issue: Dashboard shows "Loading..." indefinitely

**Solution**:
1. Check browser console (F12) for errors
2. Ensure backend service is running
3. Verify `BACKEND_URL` environment variable
4. Check Docker logs: `docker-compose logs backend`

### Issue: Port already in use

**Solution**:
```bash
# Find process using port 5000
# Windows:
netstat -ano | findstr :5000

# Linux/Mac:
lsof -i :5000

# Kill the process (or change port in docker-compose.yml)
```

### Issue: Docker build fails

**Solution**:
```bash
# Clear Docker cache and rebuild
docker-compose build --no-cache

# Check Docker logs for more details
docker-compose logs
```

---

## 📊 API Reference

### Backend API Endpoints

#### 1. Health Check
```
GET /health
```
Returns service status.

#### 2. Get Weather
```
GET /weather/<location_key>
```
where `location_key` is one of: newyork, sydney, capetown, bangkok

Response:
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
```
GET /locations
```
Returns list of supported cities.

---

## 🛠️ Development Tips

### Hot Reload

The Docker Compose configuration includes volume mounts, enabling hot reload:
- Changes to Python files auto-reload (Flask debug mode)
- Changes to HTML/CSS/JS files are reflected immediately

### Adding More Cities

To add support for more cities:

1. **Backend** (`weather-backend/app.py`):
```python
locations = {
    "newyork": "New York",
    "sydney": "Sydney",
    "capetown": "Cape Town",
    "bangkok": "Bangkok",
    "paris": "Paris",  # New city
}
```

2. **Frontend** (`weather-frontend/templates/index.html`):
```html
<option value="paris">Paris</option>
```

### Production Deployment

For production deployment:
1. Set `FLASK_ENV=production` in `.env`
2. Use production WSGI server (Gunicorn) instead of Flask dev server
3. Add SSL/TLS certificates
4. Configure proper logging
5. Set up monitoring and alerting

---

## 📝 Example Test Commands

```bash
# Full workflow test

# 1. Build images
docker-compose build

# 2. Start services
docker-compose up -d

# 3. Test backend health
curl http://localhost:5001/health

# 4. Test weather API
curl http://localhost:5001/weather/newyork

# 5. Open frontend in browser
# http://localhost:5000

# 6. View logs
docker-compose logs -f

# 7. Stop services
docker-compose down
```

---

## 📚 Additional Resources

- [OpenWeatherMap API Documentation](https://openweathermap.org/api)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

---

## 📄 License

MIT License

---

## 👥 Author

DevOps Course Team

---

## 🎯 Next Steps (Phase 2)

- [ ] Add Kubernetes deployment manifests
- [ ] Implement CI/CD pipeline (GitHub Actions/GitLab CI)
- [ ] Add comprehensive unit tests
- [ ] Set up monitoring with Prometheus/Grafana
- [ ] Add API documentation (Swagger/OpenAPI)
- [ ] Implement caching layer (Redis)
- [ ] Add database for weather history
