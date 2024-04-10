from MQTT_to_awsIoT import *

client = "Tiffany_"
key = "aio_zRAk54lXbvNRFOUDCkzBiNoGy0er"
mapfeed = "longitude-latitude"
togglefeed = "on-slash-off"
# data = input("Enter value: ")

def dms_to_dd(d, m, s):
    dd = d + float(m)/60 + float(s)/3600
    return dd

updateMap(client, key, mapfeed, lat=dms_to_dd(1,20,959.1), lon=dms_to_dd(103,41,70.5))
print(receiveData(client, key, togglefeed))