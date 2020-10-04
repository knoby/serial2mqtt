import time
from machine import UART
import network
from robust import MQTTClient
		

uart = UART(0, baudrate=9600, timeout=100, timeout_char=50, rxbuf=128)

#wait for connection
wifi = network.WLAN(network.STA_IF)
while not wifi.isconnected():
	time.sleep(1)

client = MQTTClient("ESP8266Test", "192.168.2.60")
client.connect(clean_session=True)

# Counter test
counter = 1	
while 1:

	# Read from Serial
	while 1:
		line = uart.readline();
		if line == None:
			break;

		# Eval the line
		line = line.strip();
		if not line.startswith("--MQTT--"):
			continue;
		# Check if message contains a topic and a message
		sep = line.find(b":=");
		if sep == -1: # No Separator found
			continue;
		if len(line) <= (sep+2) or sep == 8: # No Message or no Topic found
			continue;
		topic = bytearray('/Heizung') + bytearray(line[8:sep]);
		msg = line[sep+2:len(line)];
		
		client.publish(topic, msg);
		

