#potentiometer
import machine
import time

#potentiometer
#analog read
p = machine.Pin(28, machine.Pin.IN, machine.Pin.PULL_UP)
adc = machine.ADC(p)

while True:
    print(adc.read_u16())
    time.sleep(0.1) 