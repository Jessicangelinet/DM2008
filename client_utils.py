import geocoder
import socket
from time import sleep

def get_current_gps_coordinates():
    g = geocoder.ip('me')#this function is used to find the current information using our IP Add
    if g.latlng is not None: #g.latlng tells if the coordiates are found or not
        return g.latlng
    else:
        return None

def initialise(host,port):
    client = socket.socket()
    client.connect((host,port))
    return client

def sendData(client, data):
    client.send(str(data).encode())
    sleep(1)
    client.close()