import requests
import polyline  # Import the polyline library
import json

# Local variables
vehicle_id = "985CC5EC1D3FC176E053DD4D1FAC4E39"
source_long = 149.135440
source_lat = -35.306250
dest_long = 149.189423
dest_lat = -35.308022

# Prepare OSRM URL
osrm_url = f"http://router.project-osrm.org/trip/v1/driving/{source_long},{source_lat};{dest_long},{dest_lat}?geometries=polyline"

try:
    # Make the request to OSRM
    response = requests.get(osrm_url)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Parse the JSON response
    osrm_data = response.json()
except requests.RequestException as e:
    print(f"Error during OSRM request: {str(e)}")
    exit(1)
except ValueError as e:
    # Handle JSON decoding errors
    print(f"Error parsing OSRM response as JSON: {str(e)}")
    exit(1)

# Check if trips exist in the response
trips = osrm_data.get('trips')
if not trips:
    print("No trips found in the OSRM response.")
    exit(1)

# Extract encoded polyline from the response
encoded_polyline = trips[0].get('geometry', '')

if not encoded_polyline:
    print("No geometry found in the OSRM response.")
    exit(1)

# Decode the polyline to get the coordinates
waypoints = polyline.decode(encoded_polyline)

# Write the waypoints to a JSON file
try:
    with open('waypoints.json', 'w') as f:
        json.dump(waypoints, f)
    print("Waypoints successfully written to waypoints.json")
except IOError as e:
    print(f"Could not write to file: {str(e)}")
    exit(1)
