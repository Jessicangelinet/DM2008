import time
import serial
# from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient #remember to pip install AWSIoTPythonSDK pyserial

# AWS IoT endpoint and port
iot_endpoint = "your-iot-endpoint.iot.your-region.amazonaws.com"
iot_port = 8883

# AWS IoT Thing settings
thing_name = "your-thing-name"
root_ca_path = "path/to/root/ca.pem"
private_key_path = "path/to/private/key.pem.key"
cert_path = "path/to/cert.pem.crt"

gps_serial_port = 'COM5'
baud_rate = 115200

def read_gps_data():

    with serial.Serial(gps_serial_port, 115200, timeout=1) as ser:
        try:
            while True:
                line = ser.readline().decode('latin-1').strip()
                if line.startswith("Location:"):
                    #Extract latitude and longitude
                    location = line.split()
                    latitude = location[1].rstrip(",N")
                    longitude = location[2].rstrip("E")
                    print("Latitude: ", latitude)
                    print("Longitude: ", longitude)

                    return latitude, longitude
                                
        except KeyboardInterrupt:
            ser.close() # Close the serial connection when the script is interrupted


'''check within circle'''
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

center_lat = 0
center_long = 0
while True:
    lat, long = read_gps_data()
    print(lat, long)

    if center_lat == 0 and center_long == 0:
        center_check = input("Are you at your center point?")
        if center_check == "yes":
            center_lat = lat
            center_long = long
            print("Center point set")
            circle_radius_meters = int(input("Enter the radius of your circle area in meters: "))

    if is_within_circle(lat, long, center_lat, center_long, circle_radius_meters):
        print(f"The input coordinates are within the {circle_radius_meters} meter circle.")
    else:
        print(f"😡😡😡The input coordinates are outside the {circle_radius_meters} meter circle.")
