import geocoder
import requests
import socket
from time import sleep
import json
import datetime
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

#AWS  credentials
awsiot_endpoint = "a2cxs9th318s6p-ats.iot.ap-southeast-2.amazonaws.com" 
root_ca_path = "publish_cred/AmazonRootCA1.pem"
private_key_path = "publish_cred/67afd4ef929b22d569c9f23c49a9b28615b8282a29077187214e5fc757569330-private.pem.key"
certificate_path = "publish_cred/67afd4ef929b22d569c9f23c49a9b28615b8282a29077187214e5fc757569330-certificate.pem.crt"
client_id = "Laptop"

#function to get gps coordinates
def get_current_gps_coordinates():
    #this function is used to find the current information using IP Address
    g = geocoder.ip('me')
    #g.latlng tells if the coordiates are found or not
    if g.latlng is not None:
        return g.latlng
    else:
        return None

#function to establish connection to server
def initialise(host,port):
    client = socket.socket()
    client.connect((host,port))
    return client

#function to send data to server 
def sendData(client, data):
    #send encoded data to server
    client.send(str(data).encode())
    sleep(1)
    #close connection to server
    client.close()

#function to send data to aws iot topic
def sendCoor(data):
    #connect to AWS IoT Core
    myMQTTClient = AWSIoTMQTTClient(client_id)
    myMQTTClient.configureEndpoint(awsiot_endpoint, 8883)
    myMQTTClient.configureCredentials(root_ca_path, private_key_path, certificate_path)

    myMQTTClient.connect()

    #publish data to topic
    topic = "lat/long"
    data = {"id": client_id, "lat/long": data, "timestamp": str(datetime.datetime.now())}
    myMQTTClient.publish(topic, json.dumps(data), 0)

    #disconnect from IOT Core
    myMQTTClient.disconnect()