#cap sensor
import machine
import time

capacitorSensor = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    print(capacitorSensor.value())
    time.sleep(0.1)