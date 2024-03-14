import time
import serial
# from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient #remember to pip install AWSIoTPythonSDK pyserial

# AWS IoT endpoint and port
iot_endpoint = "your-iot-endpoint.iot.your-region.amazonaws.com"
iot_port = 8883

# AWS IoT Thing settings
thing_name = "your-thing-name"
root_ca_path = "path/to/root/ca.pem"
private_key_path = "path/to/private/key.pem.key"
cert_path = "path/to/cert.pem.crt"

gps_serial_port = 'COM5'
baud_rate = 115200

def read_gps_data():

    with serial.Serial(gps_serial_port, 115200, timeout=1) as ser:
        try:
            while True:
                line = ser.readline().decode('latin-1').strip()
                if line.startswith("Location:"):
                    #Extract latitude and longitude
                    location = line.split()
                    latitude = location[1].rstrip(",N")
                    longitude = location[2].rstrip("E")
                    print("Current Position: ")
                    print("Latitude: ", latitude)
                    print("Longitude: ", longitude)

                # with serial.Serial(gps_serial_port, 115200, timeout=1) as ser:
                #     line = ser.readline().decode('utf-8')
                #     print(line)
                #     if line.startswith('$GPGGA') or line.startswith('$GPRMC'):
                #         # Extract latitude and longitude from GPGGA sentence
                #         data = line.split(',')
                #         latitude = float(data[2]) if data[2] else 0.0
                #         longitude = float(data[4]) if data[4] else 0.0
                        # print(data)
                        #return latitude, longitude
                # return None, None

                    #return latitude, longitude
                                
        except KeyboardInterrupt:
            ser.close() # Close the serial connection when the script is interrupted

lat, long = read_gps_data()
print(lat, long)



'''check within circle'''
import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance (in meters) between two points
    on the Earth's surface using the Haversine formula.
    """
    R = 6371000  # Earth radius in meters
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def is_within_circle(lat_input, lon_input, lat_center, lon_center, radius_meters):
    """
    Check if the input latitude and longitude are within the specified circle.
    """
    distance_to_center = haversine(lat_input, lon_input, lat_center, lon_center)
    return distance_to_center <= radius_meters

# Example usage:
reference_latitude = 1.3521  # Example latitude of the center point
reference_longitude = 103.8198  # Example longitude of the center point
circle_radius_meters = 1  # Example radius in meters

if is_within_circle(lat, long, reference_latitude, reference_longitude, circle_radius_meters):
    print(f"The input coordinates are within the {circle_radius_meters} meter circle.")
else:
    print(f"😡😡😡The input coordinates are outside the {circle_radius_meters} meter circle.")



# Create an AWS IoT MQTT Client
# mqtt_client = AWSIoTMQTTClient(thing_name)
# mqtt_client.configureEndpoint(iot_endpoint, iot_port)
# mqtt_client.configureCredentials(root_ca_path, private_key_path, cert_path)

# # Connect to AWS IoT
# mqtt_client.connect()

# #Sending to AWS using JSON format
# try:
#     while True:
#         # Read GPS data
#         latitude, longitude = read_gps_data()

#         if latitude is not None and longitude is not None:
#             # Create a JSON payload with GPS data
#             payload = {
#                 "latitude": latitude,
#                 "longitude": longitude
#             }
            
#             # Convert payload to JSON format
#             json_payload = json.dumps(payload)

#             # Publish the JSON payload to AWS IoT topic
#             topic = "your/gps/topic"
#             mqtt_client.publish(topic, json_payload, 1)

#             print(f"Published GPS data: {json_payload}")

#         time.sleep(5)  # Adjust the delay based on your desired frequency

# # try:
# #     while True:
# #         # Read GPS data
# #         latitude, longitude = read_gps_data()

# #         if latitude is not None and longitude is not None:
# #             # Format GPS data as a JSON message
# #             message = '{{"latitude": {}, "longitude": {}}}'.format(latitude, longitude)

# #             # Publish the message to AWS IoT topic
# #             topic = "your/gps/topic"
# #             mqtt_client.publish(topic, message, 1)

# #             print(f"Published GPS data: {message}")

# #         time.sleep(5)  # Adjust the delay based on your desired frequency

# except KeyboardInterrupt:
#     print("Disconnecting...")
#     mqtt_client.disconnect()


