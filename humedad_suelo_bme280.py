import machine, network, urequests
from machine import Pin, I2C, ADC
import time
import bme280_float as bme280
from ssd1306 import SSD1306_I2C

ssid = 'turedwifi'
password = 'tucontraseña'
url = "https://api.thingspeak.com/update?api_key=tuapi"

red = network.WLAN(network.STA_IF)

red.active(True)
red.connect(ssid, password)

while red.isconnected() == False:
  pass

print('Conexión correcta')
print(red.ifconfig())

ultima_peticion = 0
intervalo_peticiones = 30

def reconectar():
    print('Fallo de conexión. Reconectando...')
    time.sleep(10)
    machine.reset()

sensor = ADC(Pin(26))

minima_humedad = Valorminobtenido
maxima_humedad = Valormaxobtenido

i2c=I2C(0,sda=Pin(4), scl=Pin(5), freq=400000)

bme = bme280.BME280(i2c=i2c)

temp = bme.values[0]       #desechar primeros valores
pres = bme.values[1]
hum = bme.values[2]

oled = SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.text("Computadoras", 20, 20)
oled.text("y", 60, 35)
oled.text("Sensores", 35, 50)
oled.show()
time.sleep(2)

while (True):
    try:
            if (time.time() - ultima_peticion) > intervalo_peticiones:
                temperatura, presion, humedad = bme.read_compensated_data()
                temp = round(temperatura, 1)
                hum = round(humedad, 1)
                pres = round(presion/100, 1)
                porcentaje = (minima_humedad-sensor.read_u16())*100/(minima_humedad-maxima_humedad)
                porcentaje = round(porcentaje, 1)
                respuesta = urequests.get(url + "&field1=" + str(temp) + "&field2=" + str(hum) + "&field3=" + str(pres) + "&field4=" + str(porcentaje))
                print ("Respuesta: " + str(respuesta.status_code))
                respuesta.close()
                ultima_peticion = time.time()
    except OSError as e:
        reconectar()


    temp = bme.values[0]
    pres = bme.values[1]
    hum = bme.values[2]
    porcentaje = (minima_humedad-sensor.read_u16())*100/(minima_humedad-maxima_humedad)
    porcentaje = round(porcentaje, 1)
    
    oled.fill(0)
    #print(bme.values)
    oled.text("Ambiente y suelo", 0, 0)
    oled.text("Temp: " + temp, 0, 16)
    oled.text("Hum:  " + hum, 0, 30)
    oled.text("Pres: " + pres, 0, 44)
    oled.text("Suelo: " + str(porcentaje) + "%", 0, 57)
    oled.show()
    time.sleep(2)
