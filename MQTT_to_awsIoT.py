import time
import serial
import math
from Adafruit_IO import Client
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
from time import sleep;

gps_serial_port = 'COM5'
baud_rate = 115200
client = "Tiffany_"
key = "aio_zRAk54lXbvNRFOUDCkzBiNoGy0er"
mapfeed = "longitude-latitude"
togglefeed = "on-slash-off"
indicatorfeed = "outside"
radiusfeed = "radius"
circle_radius_meters = 1000
toggle_chk = 0

awsiot_endpoint = "a2cxs9th318s6p-ats.iot.ap-southeast-2.amazonaws.com" 
root_ca_path = "AmazonRootCA1.pem"
private_key_path = "67afd4ef929b22d569c9f23c49a9b28615b8282a29077187214e5fc757569330-private.pem.key"
certificate_path = "67afd4ef929b22d569c9f23c49a9b28615b8282a29077187214e5fc757569330-certificate.pem.crt"
client_id = "Laptop"

def read_gps_data():

    with serial.Serial(gps_serial_port, 115200, timeout=0.5) as ser:
        try:
            center_lat = 0
            center_long = 0
            while True:
                line = ser.readline().decode('latin-1').strip()
                if line.startswith("Location:"):
                    #Extract latitude and longitude
                    location = line.split()
                    latitude = float(location[1].rstrip(",N"))
                    longitude = float(location[2].rstrip("E"))

                    
                    print("Current Position: ")
                    print("Latitude: ", latitude)
                    print("Longitude: ", longitude)

                    ddLat = dms_to_dd(latitude)
                    ddLong = dms_to_dd(longitude)
                    
                    updateMap(client, key,  mapfeed, ddLat, ddLong)

                    toggle_chk = receiveData(client, key, togglefeed)
                                        
                    if toggle_chk == "1" or (center_lat == 0 and center_long == 0):
                        # print("ENTERED")
                        center_lat = latitude
                        center_long = longitude
                        circle_radius_meters = int(receiveData(client, key, radiusfeed)) *100
                        print("Center point set")
                        print(circle_radius_meters)

                    if is_within_circle(latitude, longitude, center_lat, center_long, circle_radius_meters):
                        sendData(client, key, indicatorfeed,"0")
                        notification(f"The input coordinates are within the {circle_radius_meters/100} meter circle.")
                        sleep(100)
                    else: #if out of the circle
                        sendData(client, key, indicatorfeed,"1") #Send to adafruit here
                        notification(f"😡😡😡The input coordinates are outside the {circle_radius_meters} meter circle.")
                        sleep(100)
                        



        except KeyboardInterrupt:
            ser.close() # Close the serial connection when the script is interrupted

def dms_to_dd(position):

    position = str(position)

    dotIdx = position.index(".")

    d = position[:dotIdx-2]
    m = position[dotIdx-2:dotIdx]
    s = position[dotIdx+1:]
    ms = s[:2] + "."  + position[-2:]

    dd = float(d) + float(m)/60 + float(ms)/3600
    return dd


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

    reference: https://stackoverflow.com/questions/29545704/fast-haversine-approximation-python-pandas
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

    the initial idea was to make a rectangle with the current point as one of the edges.
    However, this would not work as the distance calculated using latitude as x-axis and longitude as y-axis will make it
    pependicular to the latitude and longitude but might be diagonal in real life.

    Hence, why circle is chosen to ensure the shape anywhere on the earth is a circle. -Jessica
    """
    distance_to_center = haversine(lat_input, lon_input, lat_center, lon_center)
    return distance_to_center <= radius_meters

def sendData(user, key, feed, data):
    client = Client(user, key)
    dash = client.feeds(feed)
    client.send_data(dash.key, data)
    print("Message sent")

#Toggle feed feature
def receiveData(user, key, feed):
    client = Client(user, key)
    data = client.receive(feed)
    return data.value
    # 0/1

def updateMap(user, key, feed, lat, lon):
    client = Client(user, key)
    dash = client.feeds(feed)
    data = {'lat': lat,
            'lon': lon,
            'ele': None,
            'created_at': None}
    client.send_data(dash.key, 0, data)
    print("Map updated")

def notification(message):
    # Connect to AWS IoT Core
    myMQTTClient = AWSIoTMQTTClient(client_id)
    myMQTTClient.configureEndpoint(awsiot_endpoint, 8883)
    myMQTTClient.configureCredentials(root_ca_path, private_key_path, certificate_path)

    # Connect to AWS IoT Core
    myMQTTClient.connect()

    # Publish data to a topic
    topic = "general/inbound"
    data = {"message": message}
    myMQTTClient.publish(topic, json.dumps(data), 1)

    # Disconnect from AWS IoT Core
    myMQTTClient.disconnect()

