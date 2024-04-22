from server_utils import *

# host = socket.gethostname()
# port = 8888

# server = initialise(port)

while True:
    try:
        center_lat = 0
        center_long = 0
        location = retrieval()

        lat_long = location.split()
        lat = lat_long[1][:len(lat_long[1])-1]
        long = lat_long[2]

        latitude = float(lat)
        longitude = float(long)

        updateMap(client, key,  mapfeed, latitude, longitude)
        toggle_chk = receiveData(client, key, togglefeed)

        if toggle_chk == "1" or (center_lat == 0 and center_long == 0):
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
        break