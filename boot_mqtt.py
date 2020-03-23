import time
from umqttsimple import MQTTClient
import ubinascii

import network
import machine
import micropython

import esp

esp.osdebug(None)

import gc
gc.collect()

ssid = 'VTR-0814086'
password = 'kk8vkGffqpgb'
mqtt_server = '192.168.0.12'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'current'
topic_sub2 = b'temp'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())









