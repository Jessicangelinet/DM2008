"""bing"""
import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance (in meters) between two points
    on the Earth's surface using the Haversine formula.
    """
    R = 6371000  # Earth radius in meters
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def is_within_circle(lat_input, lon_input, lat_center, lon_center, radius_meters):
    """
    Check if the input latitude and longitude are within the specified circle.
    """
    distance_to_center = haversine(lat_input, lon_input, lat_center, lon_center)
    return distance_to_center <= radius_meters

# Example usage:
reference_latitude = 1.3521  # Example latitude of the center point
reference_longitude = 103.8198  # Example longitude of the center point
circle_radius_meters = 1000  # Example radius in meters

input_latitude = 1.3554  # Example input latitude
input_longitude = 103.8672  # Example input longitude

if is_within_circle(input_latitude, input_longitude, reference_latitude, reference_longitude, circle_radius_meters):
    print(f"The input coordinates are within the {circle_radius_meters} meter circle.")
else:
    print(f"The input coordinates are outside the {circle_radius_meters} meter circle.")


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""phind"""
from math import radians, cos, sin, asin, sqrt

def haversine1(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

# Example usage
center_lat = -7.7940023
center_lon = 110.3656535
input_lat = -7.79457
input_lon = 110.36563
radius = 1.00 # in kilometers

distance = haversine(center_lon, center_lat, input_lon, input_lat)

if distance <= radius:
    print('The input point is within the circle.')
else:
    print('The input point is outside the circle.')
