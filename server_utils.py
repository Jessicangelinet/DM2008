import socket
import math
from Adafruit_IO import Client
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
from time import sleep

""" Adafruit credentials """
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

""" AWS credentials """
circle_radius_meters = 1000
toggle_chk = 0
awsiot_endpoint = "a2cxs9th318s6p-ats.iot.ap-southeast-2.amazonaws.com" 
root_ca_path = "subscribe_cred/AmazonRootCA1.pem"
private_key_path = "subscribe_cred/6e546d9adf0cc8c45d62584a58590090cc8f9106523cfb28f5466ca07762095d-private.pem.key"
certificate_path = "subscribe_cred/6e546d9adf0cc8c45d62584a58590090cc8f9106523cfb28f5466ca07762095d-certificate.pem.crt"
client_id = "Server"

"""function to establish connection to server"""
def initialise(port):
    # this function is used to establish connection to the server using socket library
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    server.bind((host,port))
    server.listen()
    return server

"""function to receive data from client"""
def receiveCoor(server):
    # this function is used to receive data from the client and decode it
    client, _ = server.accept()
    msg = client.recv(1024).decode()
    return msg

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

"""function to send data to server"""
def sendData(user, key, feed, data):
    # this function is used to send data to the Adafruit IO feed
    client = Client(user, key)
    dash = client.feeds(feed)
    client.send_data(dash.key, data)
    # print("Message sent")

"""Toggle feed feature"""
def receiveData(user, key, feed):
    # this function is used to receive data from the Adafruit IO feed
    client = Client(user, key)
    data = client.receive(feed)
    # 0/1 for off/on are the possible values
    return data.value

"""function to update map"""
def updateMap(user, key, feed, lat, lon):
    # this function is used to update the map on the Adafruit IO dashboard
    client = Client(user, key)
    dash = client.feeds(feed)
    data = {'lat': lat,
            'lon': lon,
            'ele': None,
            'created_at': None}
    client.send_data(dash.key, 0, data)
    print("Map updated")

"""function to update toggle"""
def notification(message):
    # Connect to AWS IoT Core using the AWS credentials and endpoint through MQTT comunication
    myMQTTClient = AWSIoTMQTTClient(client_id)
    myMQTTClient.configureEndpoint(awsiot_endpoint, 8883)
    myMQTTClient.configureCredentials(root_ca_path, private_key_path, certificate_path)

    myMQTTClient.connect()

    # Publish data to a topic
    topic = "general/inbound"
    data = {"alert": message}
    myMQTTClient.publish(topic, json.dumps(data), 1)

    # Disconnect from AWS IoT Core
    myMQTTClient.disconnect()

"""function to retrieve data from AWS IoT Core"""
def retrieval():
    # this function is used to retrieve data from AWS IoT Core
    coor = []
    # Connect to AWS IoT Core
    myMQTTClient = AWSIoTMQTTClient(client_id)
    myMQTTClient.configureEndpoint(awsiot_endpoint, 8883)
    myMQTTClient.configureCredentials(root_ca_path, private_key_path, certificate_path)

    # Define a callback function to receive messages
    def message_callback(client, userdata, message):
        # Append the message payload to the list
        coor.append(message.payload.decode('utf-8'))

    myMQTTClient.connect()

    topic = "lat/long"
    myMQTTClient.subscribe(topic, 1, message_callback)
    # Keep the script running to receive messages
    try:
        while True:
            # Wait for messages
            if len(coor) > 0:
                myMQTTClient.disconnect()
                break
            continue
    except KeyboardInterrupt:
        # Disconnect from AWS IoT Core on KeyboardInterrupt
        myMQTTClient.disconnect()
    
    return coor.pop()