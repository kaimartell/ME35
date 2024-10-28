import time
from BLE_CEEO import Yell
import machine
import asyncio
    
# MIDI message types
NoteOn = 0x90
NoteOff = 0x80
EQ = 0xB0

timestamp_ms = time.ticks_ms()
tsM = (timestamp_ms >> 7 & 0b111111) | 0x80
tsL = 0x80 | (timestamp_ms & 0b1111111)

notechannel = 0  # MIDI channel 0
basschannel = 1
hichannel = 2
velocity = 60  # Max velocity

#potentiometer
bassknob = machine.Pin(28, machine.Pin.IN, machine.Pin.PULL_UP)
adc1 = machine.ADC(bassknob)

hiknob = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)
adc2 = machine.ADC(hiknob)

midknob = machine.Pin(26, machine.Pin.IN, machine.Pin.PULL_UP)
adc3 = machine.ADC(midknob)

#capacitorsensor
capsensor1 = machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_UP)
#capsensor2 = machine.Pin(7, machine.Pin.IN, machine.Pin.PULL_UP)
#capsensor3 = machine.Pin(8, machine.Pin.IN, machine.Pin.PULL_UP)   
#capsensor4 = machine.Pin(9, machine.Pin.IN, machine.Pin.PULL_UP)
#capsensor5 = machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_UP)
#capsensor6 = machine.Pin(11, machine.Pin.IN, machine.Pin.PULL_UP)
#capsensor7 = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
#capsensor8 = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
#capsensor9 = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
#capsensor10 = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
#capsensor11 = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)

p = Yell('kmart', verbose=True, type='midi')
p.connect_up()

async def send_note(command, note, velocity):
    """Send a basic MIDI message."""
    cmd = command | (notechannel & 0x0F)
    payload = bytes([tsM, tsL, cmd, note & 0x7F, velocity & 0x7F])
    p.send(payload)
    await asyncio.sleep(0.1)


async def send_eq(command, channel, freq, gain):
    #print('cmd:', command)
    cmd = command | (channel & 0x0F)  # Make sure channel is within 0-15
    payload = bytes([tsM, tsL, cmd, freq & 0x7F, gain & 0x7F])
    #print('sending payload:', payload)
    p.send(payload)
    #print('sent payload:', payload)
        
async def main():
    try:
        while True:
            
            if capsensor1.value() == 1:
                await asyncio.create_task(send_note(NoteOn, 1, velocity))
            #if capsensor2.value() == 1:
               # await asyncio.create_task(send_note(NoteOn, 2, velocity))
            #if capsensor3.value() == 1:
                #await asyncio.create_task(send_note(NoteOn, 3, velocity))
            #if capsensor4.value() == 1:
                #await asyncio.create_task(send_note(NoteOn, 4, velocity))
            #if capsensor5.value() == 1:
               # await asyncio.create_task(send_note(NoteOn, 5, velocity))
            #if capsensor6.value() == 1:
                #await asyncio.create_task(send_note(NoteOn, 6, velocity))
            #if capsensor7.value() == 1:
               # await asyncio.create_task(send_note(NoteOn, 7, velocity))
            #if capsensor8.value() == 1:
                #await asyncio.create_task(send_note(NoteOn, 8, velocity))
            #if capsensor9.value() == 1:
                #await asyncio.create_task(send_note(NoteOn, 9, velocity))
            #if capsensor10.value() == 1:
                #await asyncio.create_task(send_note(NoteOn, 10, velocity))
            print('cap1s:', capsensor1.value())
                
            asyncio.create_task(send_eq(EQ, basschannel, 1, adc1.read_u16() >> 9))
            #asyncio.create_task(send_eq(EQ, hichannel, 2, adc2.read_u16() >> 9))
            #asyncio.create_task(send_notes(NoteOn, 60, velocity))
            await asyncio.sleep(0.01)   
            
    finally:
        p.disconnect()
        print("Disconnected.")

        
if __name__ == "__main__":
    asyncio.run(main())