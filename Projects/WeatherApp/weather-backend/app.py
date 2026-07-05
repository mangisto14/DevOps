from flask import Flask, jsonify, request
import requests
import os
import json
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
CACHE_TTL = int(os.getenv('CACHE_TTL', 300))

# --- Redis cache (optional) ---
REDIS_URL = os.getenv('REDIS_URL')
redis_client = None

if REDIS_URL:
    try:
        import redis as redis_lib
        redis_client = redis_lib.from_url(
            REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=2,
            socket_timeout=2
        )
        redis_client.ping()
        logger.info("Redis connected")
    except Exception as exc:
        logger.warning("Redis unavailable, caching disabled: %s", exc)
        redis_client = None

# --- PostgreSQL history (optional) ---
DATABASE_URL = os.getenv('DATABASE_URL')
db_pool = None

if DATABASE_URL:
    try:
        import psycopg2
        from psycopg2 import pool as pg_pool

        db_pool = pg_pool.SimpleConnectionPool(1, 5, DATABASE_URL)
        _init_conn = db_pool.getconn()
        with _init_conn.cursor() as _cur:
            _cur.execute("""
                CREATE TABLE IF NOT EXISTS weather_history (
                    id           SERIAL PRIMARY KEY,
                    location_key VARCHAR(50)  NOT NULL,
                    city_name    VARCHAR(100) NOT NULL,
                    temperature  FLOAT,
                    description  VARCHAR(200),
                    humidity     INTEGER,
                    wind_speed   FLOAT,
                    queried_at   TIMESTAMPTZ DEFAULT NOW()
                );
                CREATE INDEX IF NOT EXISTS idx_wh_location
                    ON weather_history(location_key);
                CREATE INDEX IF NOT EXISTS idx_wh_time
                    ON weather_history(queried_at DESC);
            """)
            _init_conn.commit()
        db_pool.putconn(_init_conn)
        logger.info("PostgreSQL connected and schema initialized")
    except Exception as exc:
        logger.warning("PostgreSQL unavailable, history disabled: %s", exc)
        db_pool = None


def _get_db_conn():
    if db_pool is None:
        return None
    try:
        return db_pool.getconn()
    except Exception as exc:
        logger.warning("DB pool.getconn() failed: %s", exc)
        return None


def _release_db_conn(conn):
    if db_pool is not None and conn is not None:
        try:
            db_pool.putconn(conn)
        except Exception:
            pass


# --- API Docs ---

OPENAPI_SPEC = {
    "openapi": "3.0.0",
    "info": {
        "title": "WeatherApp API",
        "description": "Weather data API backed by OpenWeatherMap. Supports Redis caching and PostgreSQL history.",
        "version": "2.0.0"
    },
    "paths": {
        "/health": {
            "get": {
                "tags": ["Health"],
                "summary": "Health check",
                "responses": {
                    "200": {
                        "description": "Service is healthy",
                        "content": {"application/json": {"schema": {
                            "type": "object",
                            "properties": {"status": {"type": "string", "example": "healthy"}}
                        }}}
                    }
                }
            }
        },
        "/locations": {
            "get": {
                "tags": ["Locations"],
                "summary": "List supported locations",
                "responses": {
                    "200": {
                        "description": "Supported location keys and display names"
                    }
                }
            }
        },
        "/weather/{location_key}": {
            "get": {
                "tags": ["Weather"],
                "summary": "Get current weather for a location",
                "parameters": [{
                    "name": "location_key",
                    "in": "path",
                    "required": True,
                    "schema": {
                        "type": "string",
                        "enum": ["newyork", "sydney", "capetown", "bangkok"]
                    }
                }],
                "responses": {
                    "200": {
                        "description": "Current weather data",
                        "content": {"application/json": {"schema": {
                            "type": "object",
                            "properties": {
                                "city": {"type": "string"},
                                "temperature": {"type": "number"},
                                "description": {"type": "string"},
                                "humidity": {"type": "integer"},
                                "wind_speed": {"type": "number"}
                            }
                        }}}
                    },
                    "400": {"description": "Invalid location key"},
                    "504": {"description": "OpenWeatherMap API timeout"}
                }
            }
        },
        "/history": {
            "get": {
                "tags": ["History"],
                "summary": "Get weather query history",
                "parameters": [
                    {"name": "limit", "in": "query", "schema": {"type": "integer", "default": 20, "maximum": 100}},
                    {"name": "location", "in": "query", "schema": {"type": "string"}}
                ],
                "responses": {
                    "200": {"description": "Query history (empty list if DB not configured)"}
                }
            }
        }
    }
}


@app.route('/openapi.json')
def openapi_spec():
    return jsonify(OPENAPI_SPEC)


@app.route('/apidocs')
def swagger_ui():
    return """<!DOCTYPE html>
<html>
<head>
  <title>WeatherApp API Docs</title>
  <meta charset="utf-8"/>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
</head>
<body>
<div id="swagger-ui"></div>
<script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
<script>
  SwaggerUIBundle({ url: "/openapi.json", dom_id: "#swagger-ui" });
</script>
</body>
</html>"""


# --- Routes ---

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route('/weather/<location_key>', methods=['GET'])
def get_weather(location_key):
    if location_key.lower() not in locations:
        return jsonify({
            "error": "Invalid location",
            "supported_locations": list(locations.keys())
        }), 400

    city_name = locations[location_key.lower()]

    # Cache read
    cache_key = f"weather:{location_key}"
    if redis_client:
        try:
            cached = redis_client.get(cache_key)
            if cached:
                return jsonify(json.loads(cached)), 200
        except Exception as exc:
            logger.warning("Cache read failed: %s", exc)

    try:
        params = {
            "q": city_name,
            "appid": API_KEY,
            "units": "metric"
        }

        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()

        data = response.json()

        weather_response = {
            "city": data.get("name"),
            "temperature": data.get("main", {}).get("temp"),
            "description": data.get("weather", [{}])[0].get("description", "N/A"),
            "humidity": data.get("main", {}).get("humidity"),
            "wind_speed": data.get("wind", {}).get("speed")
        }

        # Cache write
        if redis_client:
            try:
                redis_client.setex(cache_key, CACHE_TTL, json.dumps(weather_response))
            except Exception as exc:
                logger.warning("Cache write failed: %s", exc)

        # DB history write
        conn = _get_db_conn()
        if conn:
            try:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO weather_history
                            (location_key, city_name, temperature, description, humidity, wind_speed)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        location_key,
                        weather_response["city"],
                        weather_response["temperature"],
                        weather_response["description"],
                        weather_response["humidity"],
                        weather_response["wind_speed"]
                    ))
                    conn.commit()
            except Exception as exc:
                logger.warning("Failed to write history: %s", exc)
                conn.rollback()
            finally:
                _release_db_conn(conn)

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
    return jsonify({
        "supported_locations": list(locations.keys()),
        "location_names": locations
    }), 200


@app.route('/history', methods=['GET'])
def get_history():
    if db_pool is None:
        return jsonify({
            "history": [],
            "count": 0,
            "message": "History not available (database not configured)"
        }), 200

    conn = _get_db_conn()
    if conn is None:
        return jsonify({
            "history": [],
            "count": 0,
            "message": "History not available (database connection failed)"
        }), 200

    try:
        limit = min(int(request.args.get('limit', 20)), 100)
        location_filter = request.args.get('location')

        with conn.cursor() as cur:
            if location_filter:
                cur.execute("""
                    SELECT id, location_key, city_name, temperature, description,
                           humidity, wind_speed, queried_at
                    FROM weather_history
                    WHERE location_key = %s
                    ORDER BY queried_at DESC
                    LIMIT %s
                """, (location_filter, limit))
            else:
                cur.execute("""
                    SELECT id, location_key, city_name, temperature, description,
                           humidity, wind_speed, queried_at
                    FROM weather_history
                    ORDER BY queried_at DESC
                    LIMIT %s
                """, (limit,))

            rows = cur.fetchall()

        history = [
            {
                "id": r[0],
                "location_key": r[1],
                "city_name": r[2],
                "temperature": r[3],
                "description": r[4],
                "humidity": r[5],
                "wind_speed": r[6],
                "queried_at": r[7].isoformat() if r[7] else None
            }
            for r in rows
        ]
        return jsonify({"history": history, "count": len(history)}), 200

    except Exception as exc:
        logger.error("History query failed: %s", exc)
        return jsonify({"history": [], "count": 0, "error": "Query failed"}), 500
    finally:
        _release_db_conn(conn)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
