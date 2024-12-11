import machine
import time
import neopixel

# Initialize NeoPixel strip
n = neopixel.NeoPixel(machine.Pin(20), 5)  # Pin 20, 18 LEDs
p = neopixel.NeoPixel(machine.Pin(19), 3)

while True:
    for i in range(5):
        n[i] = (255, 0, 0)
        n.write()
        print(f'LED {i} is on')
        time.sleep(0.5)
        n[i] = (0, 0, 0)
        n.write()
        time.sleep(0.5)
