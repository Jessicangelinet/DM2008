from client_utils import *

"""initialise host and port """
host = "52.90.148.84"
port = 8888

"""loop to send location continuously"""
while True:
    #establish connection to server
    client = initialise(host,port)
    #send gps coordinates to server
    sendData(client, get_current_gps_coordinates())
    #send coordinates to iot topic
    sendCoor(get_current_gps_coordinates())
    #buffer 10 seconds before rerunning the loop
    sleep(10)
