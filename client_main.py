from client_utils import *
#"172.31.31.67"

host = "54.165.235.72"
port = 8888

while True:
    client = initialise(host,port)
    sendData(client, get_current_gps_coordinates())
    sendCoor(get_current_gps_coordinates())
    sleep(10)
