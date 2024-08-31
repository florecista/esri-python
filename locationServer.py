from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import json
import time

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes and origins

# Load waypoints from the JSON file
try:
    with open('waypoints.json', 'r') as f:
        waypoints = json.load(f)
except Exception as e:
    print(f"Error loading waypoints: {e}")
    waypoints = []

# Index to keep track of the current waypoint
waypoint_index = 0
direction = 1  # 1 for forward, -1 for backward

@app.route('/locationService')
def location_service():
    global waypoint_index, direction

    if not isinstance(waypoint_index, int):
        return jsonify({'error': 'Index is not an integer'}), 500

    if not waypoints:
        return jsonify({'error': 'No waypoints available'}), 500

    try:
        waypoint = waypoints[waypoint_index]
    except IndexError:
        return jsonify({'error': 'Index out of range'}), 500

    waypoint_index += direction
    if waypoint_index >= len(waypoints) or waypoint_index < 0:
        direction *= -1
        waypoint_index += direction

    # Return data in the original format
    response_data = {
        "id": "985CC5EC1D3FC176E053DD4D1FAC4E39",  # Hardcoded vehicle ID
        "timestamp": int(time.time()),  # Current timestamp
        "location": {
            "lon": waypoint[1],
            "lat": waypoint[0]
        }
    }

    return jsonify(response_data)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('static/images', filename)

if __name__ == '__main__':
    app.run(port=3000)
