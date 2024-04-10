from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json

# Your AWS IoT Core endpoint, certificates, and other configurations
awsiot_endpoint = "a2cxs9th318s6p-ats.iot.ap-southeast-2.amazonaws.com" 
root_ca_path = "/Users/ethan/Monash/DM2008/aws/AmazonRootCA1.pem"
private_key_path = "/Users/ethan/Monash/DM2008/aws/67afd4ef929b22d569c9f23c49a9b28615b8282a29077187214e5fc757569330-private.pem.key"
certificate_path = "/Users/ethan/Monash/DM2008/aws/67afd4ef929b22d569c9f23c49a9b28615b8282a29077187214e5fc757569330-certificate.pem.crt"
client_id = "Laptop"

# Connect to AWS IoT Core
myMQTTClient = AWSIoTMQTTClient(client_id)
myMQTTClient.configureEndpoint(awsiot_endpoint, 8883)
myMQTTClient.configureCredentials(root_ca_path, private_key_path, certificate_path)

# Connect to AWS IoT Core
myMQTTClient.connect()

# Publish data to a topic
topic = "general/inbound"
data = {"message": "Hello from my laptop!"}
myMQTTClient.publish(topic, json.dumps(data), 1)

# Disconnect from AWS IoT Core
myMQTTClient.disconnect()