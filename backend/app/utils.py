from geopy.distance import geodesic


def add_distance(lat, long, distance):
    """
    Adds a specified distance in miles to a set of coordinates (latitude, longitude).

    This function calculates the new coordinates after moving a given distance
    from the starting coordinates in the northward direction (90 degrees).

    Parameters:
        - lat (float): The latitude of the starting point.
        - long (float): The longitude of the starting point.
        - distance (float): The distance to move, in miles.

    Returns:
        - (float, float): The new latitude and longitude after moving the specified distance.
    """
    new_coords = geodesic(miles=distance).destination((lat, long), 90, distance)  # 0 degrees = North
    print(new_coords.latitude, new_coords.longitude)
    return (new_coords.latitude, new_coords.longitude)