from machine import Pin
from max6675 import MAX6675
from umqttsimple import MQTTClient

# ESP32 Pin assignment
so = Pin(19, Pin.IN)
sck = Pin(5, Pin.OUT)
cs = Pin(23, Pin.OUT)

max = MAX6675(sck, cs, so)

def connect():
  global client_id, mqtt_server, topic_sub2
  client = MQTTClient(client_id, mqtt_server)
  client.connect()
  return client
  
def restart_and_reconnect():
  print ('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(5)
  machine.reset()
 
try:
  client = connect()
except OSError as e:
  restart_and_reconnect()
  
  
while True:
  try:
    temp_value = max.read()
    msg = (b'{0:3.1f}'.format(temp_value))
    print(temp_value)
    client.publish(topic_sub2, msg)
    time.sleep(1)
  except OSError as e:
    restart_and_reconnect()





