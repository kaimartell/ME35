import time
from BLE_CEEO import Yell
import machine
import asyncio
import network
from mqtt import MQTTClient
from pyscript.js_modules import teach


#global isOn variable
on = False

#setup mqtt
def connect_wifi(self, index=2):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect("Tufts_Robot", "")
        while wlan.ifconfig()[0] == '0.0.0.0':
            print('.', end=' ')
            time.sleep(1)
        print('wifi connected')
        return wlan.ifconfig()
    
def start_mqtt(self):
    mqtt_broker = 'broker.hivemq.com' 
    port = 1883
    topic_sub = 'ME35-24/Kai'

    def callback(topic, msg):
        
        global on
        
        if topic.decode() == topic_sub:
            if msg.decode() == 'on':
                on = True
            if msg.decode() == 'off':
                on = False

    self.client = MQTTClient('Kmart', mqtt_broker , port, keepalive=0)
    self.client.connect()
    print('Connected to %s MQTT broker' % (mqtt_broker))
    self.client.set_callback(callback)          # set the callback if anything is read
    self.client.subscribe(topic_sub.encode())   # subscribe to a bunch of topics

async def run_model(URL):
    model = teach.s
    model.URL2 = URL
    await model.init()
    
async def predict(classes):
    predictions = []
    for i in range (0, classes):
        divElement = document.getElementById('class' + str(i))
        if divElement:
            divValue = divElement.innerHTML
            predictions.append(divValue)
            

# MIDI message types
NoteOn = 0x90
NoteOff = 0x80
EQ = 0xB0

timestamp_ms = time.ticks_ms()
tsM = (timestamp_ms >> 7 & 0b111111) | 0x80
tsL = 0x80 | (timestamp_ms & 0b1111111)

notechannel = 0 
basschannel = 1
midchannel = 2
hichannel = 3
volumechannel = 4

velocity = 60 

#potentiometer
bassknob = machine.Pin(28, machine.Pin.IN, machine.Pin.PULL_UP)
adc1 = machine.ADC(bassknob)

hiknob = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)
adc2 = machine.ADC(hiknob)

midknob = machine.Pin(26, machine.Pin.IN, machine.Pin.PULL_UP)
adc3 = machine.ADC(midknob)

#capacitorsensor
capsensor1 = machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_UP)
capsensor2 = machine.Pin(7, machine.Pin.IN, machine.Pin.PULL_UP)
capsensor3 = machine.Pin(8, machine.Pin.IN, machine.Pin.PULL_UP)   
capsensor4 = machine.Pin(9, machine.Pin.IN, machine.Pin.PULL_UP)
capsensor5 = machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_UP)
capsensor6 = machine.Pin(11, machine.Pin.IN, machine.Pin.PULL_UP)
capsensor7 = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)
capsensor8 = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP)
capsensor9 = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)
capsensor10 = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
capsensor11 = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)

p = Yell('kmart', verbose=True, type='midi')
p.connect_up()

async def send_note(command, note, velocity):
    cmd = command | (notechannel & 0x0F)
    payload = bytes([tsM, tsL, cmd, note & 0x7F, velocity & 0x7F])
    p.send(payload)
    await asyncio.sleep(0.1)


async def send_eq(command, channel, freq, gain):
    cmd = command | (channel & 0x0F) 
    payload = bytes([tsM, tsL, cmd, freq & 0x7F, gain & 0x7F])
    p.send(payload)
        
async def main():
    
    if on:
        try:
            
            asyncio.create_task(run_model('https://teachablemachine.withgoogle.com/models/1J9Z2Z2Z/'))
            
            while True:
                
                predictions = predict(3)
                
                if predictions[0] == '3':
                    asyncio.create_task(send_eq(EQ, volumechannel, 1, 127))
                if predictions[0] == '2':
                    asyncio.create_task(send_eq(EQ, volumechannel, 1, 64))
                if predictions[0] == '1':
                    asyncio.create_task(send_eq(EQ, volumechannel, 1, 0))    
            
                if capsensor1.value() == 1:
                    await asyncio.create_task(send_note(NoteOn, 1, velocity))
                if capsensor2.value() == 1:
                    await asyncio.create_task(send_note(NoteOn, 2, velocity))
                if capsensor3.value() == 1:
                    await asyncio.create_task(send_note(NoteOn, 3, velocity))
                if capsensor4.value() == 1:
                    await asyncio.create_task(send_note(NoteOn, 4, velocity))
                if capsensor5.value() == 1:
                    await asyncio.create_task(send_note(NoteOn, 5, velocity))
                if capsensor6.value() == 1:
                    await asyncio.create_task(send_note(NoteOn, 6, velocity))
                if capsensor7.value() == 1:
                    await asyncio.create_task(send_note(NoteOn, 7, velocity))
                if capsensor8.value() == 1:
                    await asyncio.create_task(send_note(NoteOn, 8, velocity))
                if capsensor9.value() == 1:
                    await asyncio.create_task(send_note(NoteOn, 9, velocity))
                if capsensor10.value() == 1:
                    await asyncio.create_task(send_note(NoteOn, 10, velocity))
                print('cap1s:', capsensor1.value())
                    
                asyncio.create_task(send_eq(EQ, basschannel, 1, adc1.read_u16() >> 9))
                asyncio.create_task(send_eq(EQ, midchannel, 1, adc2.read_u16() >> 9))
                asyncio.create_task(send_eq(EQ, hichannel, 1, adc3.read_u16() >> 9))
                await asyncio.sleep(0.01)   
            
        finally:
            p.disconnect()
            print("Disconnected.")

    else:
        print('off')
        await asyncio.sleep(0.1)
        await main()
        
        
if __name__ == "__main__":
    connect_wifi()
    start_mqtt()
    
    asyncio.run(main())