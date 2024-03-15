import time
import serial
import math
from Adafruit_IO import Client

gps_serial_port = 'COM5'
baud_rate = 115200

def read_gps_data():

    with serial.Serial(gps_serial_port, 115200, timeout=0.5) as ser:
        try:
            while True:
                line = ser.readline().decode('latin-1').strip()
                if line.startswith("Location:"):
                    #Extract latitude and longitude
                    location = line.split()
                    latitude = location[1].rstrip(",N")
                    longitude = location[2].rstrip("E")
                    print("Current Position: ")
                    print("Latitude: ", latitude)
                    print("Longitude: ", longitude)
        except KeyboardInterrupt:
            ser.close() # Close the serial connection when the script is interrupted


    # Alternative way around 
    # ser = serial.Serial(gps_serial_port, 115200)
    # try:
    #     while True:
    #         line = ser.readline().decode('latin-1').strip()
    #         if line.startswith('$GPGGA'): # Extract latitude and longitude from GPGGA sentence
    #             if len(line.split(",")) < 10:
    #                 continue
    #             data = line.split(',')
    #             latitude = float(data[2]) if data[2] else 0.0
    #             longitude = float(data[4]) if data[4] else 0.0

    #         elif line.startswith('$GPRMC'): # Extract latitude and longitude from GPRMC sentence
    #             data = line.split(',')
    #             latitude = float(data[3]) if data[5] else 0.0
    #             longitude = float(data[3]) if data[5] else 0.0  
    #         else:
    #             continue

'''check within circle'''

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

def sendData(user, key, feed, data):
    client = Client(user, key)
    dash = client.feeds(feed)
    client.send_data(dash.key, data)
    print("Message sent")

def receiveData(user, key, feed):
    client = Client(user, key)
    data = client.receive(feed)
    return data.value

def updateMap(user, key, feed, lat, lon):
    client = Client(user, key)
    dash = client.feeds(feed)
    data = {'lat': lat,
            'lon': lon,
            'ele': None,
            'created_at': None}
    client.send_data(dash.key, 0, data)
    print("Map updated")


