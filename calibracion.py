from machine import ADC, Pin
import time

sensor = ADC(Pin(26))

while True:
    print("Valor: " + str(sensor.read_u16()))
    time.sleep(2)