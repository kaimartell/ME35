"""
The first assignment is to get everyone up to speed on the coding.  
Your goal is to make a very simple nightlight using your Pico. 
It should stop and start with MQTT commands, one of the blue LEDs on 
the board should continually breathe (get brighter then dimmer then 
brighter...), and if someone hits the button on the board, then the neopixel 
should change color and beep.
"""
import machine
import time
import neopixel
import math
import uasyncio as asyncio

class Nightlight:
    def __init__(self, led_pin, button_pin, buzzer_pin, neopixel_pin):
        self.led = machine.PWM(machine.Pin(led_pin))
        self.led.freq(1000)
        self.button = machine.Pin(button_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.buzzer = machine.PWM(machine.Pin(buzzer_pin, machine.Pin.OUT))
        self.buzzer.freq(440)
        self.buzzer.duty_u16(0)
        self.neopixel = neopixel.NeoPixel(machine.Pin(neopixel_pin), 1)
        self.hue = 0  # Initialize hue for color wheel

    def hsv_to_rgb(self, h, s, v):
        if s == 0.0: return (v, v, v)
        i = int(h*6.0)  # Assume h is in [0, 1]
        f = (h*6.0) - i
        p, q, t = v*(1.0 - s), v*(1.0 - s*f), v*(1.0 - s*(1.0-f))
        i %= 6
        if i == 0: return (v, t, p)
        if i == 1: return (q, v, p)
        if i == 2: return (p, v, t)
        if i == 3: return (p, q, v)
        if i == 4: return (t, p, v)
        if i == 5: return (v, p, q)

    async def breathe_led(self):
        duty_cycle = 0
        direction = 1
        
        while True:
            self.led.duty_u16(duty_cycle)
            duty_cycle += direction * 1000  # Increase the duty cycle increment
            
            if duty_cycle >= 65535 or duty_cycle <= 0:
                direction *= -1
            
            await asyncio.sleep(0.01)  # Use await for non-blocking sleep

    async def handle_button(self):
        while True:
            if not self.button.value():
                print("Button pressed")
                self.buzzer.duty_u16(1000)
                self.hue = (self.hue + 0.01) % 1.0  # Increment hue
                r, g, b = self.hsv_to_rgb(self.hue, 1.0, 1.0)
                self.neopixel[0] = (int(r * 255), int(g * 255), int(b * 255))
                self.neopixel.write()
            else:
                self.buzzer.duty_u16(0)
                r, g, b = self.hsv_to_rgb(self.hue, 1.0, 1.0)
                self.neopixel[0] = (int(r * 255), int(g * 255), int(b * 255))
                self.neopixel.write()
            
            await asyncio.sleep(0.01)  # Use await for non-blocking sleep

    async def activate(self):
        print("starting nightlight()")
        await asyncio.gather(self.breathe_led(), self.handle_button())

# To run the nightlight
nightlight = Nightlight(led_pin=15, button_pin=14, buzzer_pin=13, neopixel_pin=12)
asyncio.run(nightlight.activate())