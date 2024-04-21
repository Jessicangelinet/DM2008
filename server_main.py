from server_utils import *

host = socket.gethostname()
port = 8888

server = initialise(port)
while True:
    print(receiveData(server))