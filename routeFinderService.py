from flask import Flask, request, jsonify
import requests
import time
import polyline  # Import the polyline library

app = Flask(__name__)

@app.route('/routeFinderService', methods=['POST'])
def route_finder_service():
    # Retrieve parameters from the request
    data = request.get_json()
    vehicle_id = data.get('vehicleId')
    source_long = data.get('sourceLocationLongitude')
    source_lat = data.get('sourceLocationLatitude')
    dest_long = data.get('destinationLocationLongitude')
    dest_lat = data.get('destinationLocationLatitude')

    # Validate parameters
    if not all([vehicle_id, source_long, source_lat, dest_long, dest_lat]):
        return jsonify({"error": "Missing required parameters"}), 400

    # Prepare OSRM URL
    osrm_url = f"http://router.project-osrm.org/trip/v1/driving/{source_long},{source_lat};{dest_long},{dest_lat}?geometries=polyline"

    try:
        # Make the request to OSRM
        response = requests.get(osrm_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the JSON response
        osrm_data = response.json()
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except ValueError as e:
        # Handle JSON decoding errors
        return jsonify({"error": "Invalid JSON response from OSRM"}), 500

    # Check if trips exist in the response
    trips = osrm_data.get('trips')
    if not trips:
        return jsonify({"error": "No trips found in the OSRM response"}), 500

    # Extract encoded polyline from the response
    encoded_polyline = trips[0].get('geometry', '')

    if not encoded_polyline:
        return jsonify({"error": "No geometry found in the OSRM response"}), 500

    # Decode the polyline to get the coordinates
    waypoints = polyline.decode(encoded_polyline)

    # Construct the response data
    response_data = []
    for waypoint in waypoints:
        response_data.append({
            "id": vehicle_id,
            "timestamp": int(time.time()),
            "location": {
                "lon": waypoint[1],
                "lat": waypoint[0]
            }
        })

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
