from machine import Pin, I2C, ADC
import ssd1306
from math import sqrt
from umqttsimple import MQTTClient

# ESP8266 Pin assignment
i2c = I2C(-1, scl=Pin(5), sda=Pin(4))
voltage_in = ADC(0)

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

def oled_print(value):
  oled.fill(0)
  oled.text('La corriente es', 0, 20)
  oled.text(str(value) + ' A', 0, 30)
  oled.show()

def connect():
  global client_id, mqtt_server, topic_sub
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
  
  
cant_muestras = 800
factor = 30/(1024/3.3)
sum_curr = 0
  
while True:
  try:
    for i in range (cant_muestras):
      voltage_value = voltage_in.read() - 542
      current_value = voltage_value*factor
      sum_curr += current_value**2
      time.sleep(1/cant_muestras)
    curr_RMS = sqrt(sum_curr/cant_muestras)
    oled_print(curr_RMS)
    msg = (b'{0:3.3f}'.format(curr_RMS))
    print(curr_RMS)
    client.publish(topic_sub, msg)
    sum_curr = 0
    
  except OSError as e:
    restart_and_reconnect()




