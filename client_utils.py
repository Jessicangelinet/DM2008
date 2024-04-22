import geocoder
import requests
import socket
from time import sleep
import json
import datetime
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

awsiot_endpoint = "a2cxs9th318s6p-ats.iot.ap-southeast-2.amazonaws.com" 
root_ca_path = "publish_cred/AmazonRootCA1.pem"
private_key_path = "publish_cred/67afd4ef929b22d569c9f23c49a9b28615b8282a29077187214e5fc757569330-private.pem.key"
certificate_path = "publish_cred/67afd4ef929b22d569c9f23c49a9b28615b8282a29077187214e5fc757569330-certificate.pem.crt"
client_id = "Laptop"

# Connect to AWS IoT Core
myMQTTClient = AWSIoTMQTTClient(client_id)
myMQTTClient.configureEndpoint(awsiot_endpoint, 8883)
myMQTTClient.configureCredentials(root_ca_path, private_key_path, certificate_path)

myMQTTClient.connect()

def get_current_gps_coordinates():
    g = geocoder.ip('me')#this function is used to find the current information using our IP Add
    if g.latlng is not None: #g.latlng tells if the coordiates are found or not
        return g.latlng
    else:
        return None

def get_user_location():
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        print(data['loc'])
        return data['loc']
    except:
        print("Error: Unable to detect your location.")
        return None

def initialise(host,port):
    client = socket.socket()
    client.connect((host,port))
    return client

def sendData(client, data):
    client.send(str(data).encode())
    sleep(1)
    client.close()

def sendCoor(data):
    # Publish data to a topic
    topic = "lat/long"
    data = {"id": client_id, "lat/long": data, "timestamp": str(datetime.datetime.now())}
    myMQTTClient.publish(topic, json.dumps(data), 0)
