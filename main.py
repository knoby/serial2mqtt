import time
from machine import UART
import network
from robust import MQTTClient


##### CONFIGURATION ######
MQTT_Server_IP = "192.168.2.60"
MQTT_ClientName = "ESP8266Test"
MQTT_Topic = 'Heizung/'

SERIAL_BAUD_RATE = 9600

##########################

uart = UART(0, baudrate=SERIAL_BAUD_RATE,
            timeout=100, timeout_char=50, rxbuf=128)

# wait for connection
wifi = network.WLAN(network.STA_IF)
while not wifi.isconnected():
    time.sleep(1)

client = MQTTClient(MQTT_Client_Name, MQTT_Server_IP)
client.connect(clean_session=True)

# Counter test
counter = 1
while 1:

    # Read from Serial
    while 1:
        line = uart.readline()
        if line == None:
            break

        # Eval the line
        line = line.strip()
        if not line.startswith("--MQTT--"):
            continue
        # Check if message contains a topic and a message
        sep = line.find(b":=")
        if sep == -1:  # No Separator found
            continue
        if len(line) <= (sep+2) or sep == 8:  # No Message or no Topic found
            continue
        topic = bytearray(Topic) + bytearray(line[8:sep])
        msg = line[sep+2:len(line)]

        client.publish(topic, msg)
