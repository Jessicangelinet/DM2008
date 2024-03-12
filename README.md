# DM2008

Download Adafruit GPS library in Arduino
Utilise `GPS_SoftwareSerial_Parsing` Library to obtain Lat Long values
Send the Lat Long values to python script

Use python script to read Lat Long Values from Arduino
Implement logic of distance calculation relative from initiation point
Implement MQTT protocol in python to send to AWS IoT

`Teacher suggestion:`
-python script can SEND to AWS IoT the pet's current location
-AWS IoT can also ASK python what is the current location of the pet

`Suggested Presentation Plan (Each person present one aspect)`
-What is the model
-Code
-Functionality
-Why is it efficient (Protocol, data format like JSON and why it is scalable)

`Sufficient enough for prototype stage`
GPS connected to Laptop => Obtain position => Good enough
Publish location into IOT => Good enough 



