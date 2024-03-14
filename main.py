from MQTT_to_awsIoT import *

center_lat = 0
center_long = 0

while True:
    lat, long = read_gps_data()
    print(lat, long)

    if center_lat == 0 and center_long == 0:
        center_check = input("Are you at your center point?")
        if center_check == "yes":
            center_lat = lat
            center_long = long
            print("Center point set")
            circle_radius_meters = int(input("Enter the radius of your circle area in meters: "))

    if is_within_circle(lat, long, center_lat, center_long, circle_radius_meters):
        print(f"The input coordinates are within the {circle_radius_meters} meter circle.")
    else:
        print(f"😡😡😡The input coordinates are outside the {circle_radius_meters} meter circle.")