import random
from fastapi import APIRouter
import requests
from app import utils
import os

google_router = APIRouter(prefix="/google", tags=["Google API"])

google_api_key = os.getenv("GOOGLE_API_KEY")

if google_api_key is None:
    raise ValueError("API key is missing. Please set the GOOGLE_API_KEY environment variable.")

@google_router.get("/travel_time/{origin}/{destination}")
def get_travel_time(origin: str = "New York, NY", destination: str = "Philadelphia, PA", mode: str = "driving"):
    """
    Get the travel time between two locations.

    Calls Google Distance Matrix API to calculate the actual travel time based on the provided locations and mode.

    - **origin**: The starting location for the travel (default is "New York, NY").
    - **destination**: The destination location for the travel (default is "Philadelphia, PA").
    - **mode**: The mode of travel (default is "driving"). Other modes can include walking, bicycling, etc.

    Returns:
        - A JSON object containing the origin, destination, travel time in hours, and travel time in seconds.

    Example Response:
        ```json
        {
            "origin": "New York, NY",
            "destination": "Philadelphia, PA",
            "hours": 1,
            "seconds": 3600
        }
        ```
    """
    # return {"origin": origin, "destination": destination, "hours": 0.25, "seconds": 900}

    # Call the Google Distance Matrix API
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={destination}&mode={mode}&key={google_api_key}"


    print("CALLING MATRIX API!!!!")
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Extract travel time
        if "rows" in data and data["rows"]:
            duration = data["rows"][0]["elements"][0].get("duration", {})
            hours = duration.get("text", "Not available")
            seconds = duration.get("value", "Not available")
            # travel_time = duration.get("text", "Not available")

            return {"origin": origin, "destination": destination, "hours": hours, "seconds": seconds}
        else:
            return {"error": "Could not retrieve travel time"}
    else:
        return {"error": "Failed to retrieve data from Google API"}
    


@google_router.get("/coords/{address}")
def convert_to_coords(address: str = "190 Saddlebrook Drive, Bensalem, PA 19020"):
    """
    Convert a given address to geographic coordinates (latitude and longitude).

    Calls the Google Geocoding API to retrieve the actual coordinates of the address.

    - **address**: The address whose coordinates are to be determined (default is "190 Saddlebrook Drive, Bensalem, PA 19020").

    Returns:
        - A tuple containing the latitude and longitude of the address.

    Example Response:
        ```json
        [40.736254, -74.126456]
        ```
    """
    # return (random.uniform(35, 42), random.uniform(-74, -75))

    url = f"https://maps.googleapis.com/maps/api/geocode/json"
    # Set up the parameters for the request
    params = {
        'address': address,
        'key': google_api_key
     }
     
    # Make the request to the API
    print("CALLING GEOCODE API!!!!")
    response = requests.get(url, params=params)
        
    # If the request is successful, process the result
    if response.status_code == 200:
        data = response.json()
        
        # Check if the response contains any results
        if data['status'] == 'OK':
            # Get the latitude and longitude from the first result
            lat = data['results'][0]['geometry']['location']['lat']
            lon = data['results'][0]['geometry']['location']['lng']
            return (lat, lon)
        else:
            return None, None
    else:
        print("Error: Failed to connect to the Google API.")
        return None, None

# @app.get("/blah")
# def get_dropoff_coords(lat: float =40.13201011242109, long: float = -74.93605191591041, distance: int = 5):
#     """Returns the coordinates (store, destination) where destination is distance miles away from store"""










