from server_utils import *

host = socket.gethostname() #Obtain the host name of the server
port = 8888 #Port number specified

####Note: Ensure Firewall is enabled so that Port 8888 is allowed!####

server = initialise(port) #Establish connections with the client side
is_outside = False #Toggle to ensure SMS is sent only once the moment pet is within/outside of the circle

"""
This program is the main program for our GPS, where we connect to client to receive messages, calculate distances, send to adafruit, and send to AWS IoT through MQTT functions
-We initialise a host IP number and port number. Then we start listening for incoming connections on that host (throught the initialise() function)
-Once we received lat longs from the client, we will pass the values to update the map in Adafruit
-We will conduct checks to see if our gps is within the predefined circle or not, and send the data to adafruit and AWS IoT respectively.
"""
while True:
    try:
        center_lat = 0
        center_long = 0
        location = receiveCoor(server) #Receive lat long values from the client side (python server client)
        
        #Preprocess to obtain lat long values 
        lat_long = location.split() 
        lat = lat_long[0][1:len(lat_long[0])-1]
        long = lat_long[1][0: len(lat_long[1])-1]

        latitude = float(lat)
        longitude = float(long)

        updateMap(client, key,  mapfeed, latitude, longitude) #update the Adafruit Map
        toggle_chk = receiveData(client, key, togglefeed) #Check if Adafruit Dashboard wants to reset Center point or not

        if toggle_chk == "1" or (center_lat == 0 and center_long == 0): #toggle_chk == 1 (user wants to reset center point)
            center_lat = latitude
            center_long = longitude
            circle_radius_meters = int(receiveData(client, key, radiusfeed)) *100  #Receive circle radius value set by user in dahsboard
            print(circle_radius_meters)

        if is_within_circle(latitude, longitude, center_lat, center_long, circle_radius_meters): #if pet is within circle
            sendData(client, key, indicatorfeed,"0") #send data to Adafruit (lat long)
            if is_outside == False: #Once pet is within circle, execute notification() with a boolean toggle, as we do not want sms to keep spamming
                notification(f"The input coordinates are within the {circle_radius_meters/100} meter circle.") #Function to send data to AWS IoT using MQTT protocol
                is_outside = True
           
        else: #if pet is out of the circle
            sendData(client, key, indicatorfeed,"1") #send data to Adafruit (lat long)
            if is_outside == True:  #Once pet is outside circle, execute notification() with a boolean toggle, as we do not want sms to keep spamming
                notification(f"😡😡😡The input coordinates are outside the {circle_radius_meters} meter circle.") #Function to send data to AWS IoT using MQTT protocol
                is_outside = False

    except KeyboardInterrupt:
        break