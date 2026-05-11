from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

# Backend service configuration
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:5000')

@app.route('/', methods=['GET'])
def index():
    """Render the main dashboard page"""
    return render_template('index.html', backend_url=BACKEND_URL)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
