from asyncio import create_task
import time
from BLE_CEEO import Yell
import machine
import asyncio

NoteOn = 0x90
NoteOff = 0x80

p = Yell('kmart', verbose=True, type='midi')
p.connect_up()

channel = 0
velocity = 60
last_press = 0

async def send_midi_message(command, note, velocity):
    cmd = command | (channel & 0x0F)
    payload = bytes([cmd, note & 0x7F, velocity & 0x7F])
    p.send(payload)

def debounce_handler(pin, note):
    global last_press
    current_time = time.ticks_ms()
    if current_time - last_press > 200:
        print(f"Button {note} pressed")
        asyncio.get_event_loop().create_task(send_midi_message(NoteOn, note, velocity))
    last_press = current_time

button1 = machine.Pin(6, machine.Pin.IN, machine.Pin.PULL_UP)
button2 = machine.Pin(7, machine.Pin.IN, machine.Pin.PULL_UP)
button3 = machine.Pin(8, machine.Pin.IN, machine.Pin.PULL_UP)
button4 = machine.Pin(9, machine.Pin.IN, machine.Pin.PULL_UP)

button1.irq(trigger=machine.Pin.IRQ_FALLING, handler=lambda pin: debounce_handler(pin, 1))
button2.irq(trigger=machine.Pin.IRQ_FALLING, handler=lambda pin: debounce_handler(pin, 2))
button3.irq(trigger=machine.Pin.IRQ_FALLING, handler=lambda pin: debounce_handler(pin, 3))
button4.irq(trigger=machine.Pin.IRQ_FALLING, handler=lambda pin: debounce_handler(pin, 4))

async def main():
    try:
        while True:
            print("Running...")
            await asyncio.sleep(2)
    finally:
        p.disconnect()
        print("Disconnected.")

if __name__ == "__main__":
    asyncio.run(main())
