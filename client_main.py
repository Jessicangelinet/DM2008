from client_utils import *
#"172.31.31.67"

host = socket.gethostname()
port = 8888

while True:
    client = initialise(host,port)
    sendData(client, get_current_gps_coordinates())
