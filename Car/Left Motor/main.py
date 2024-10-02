#main.py for first pico - steering and left motor
import asyncio
import machine
import time
import network
from steering import Steering
from motor import Motor
from mqtt import MQTTClient

def setup_wifi(SSID, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, password)

    while wlan.ifconfig()[0] == '0.0.0.0':
            print('.', end=' ')
            time.sleep(1)
        
    print('wifi connected') 
    return wlan.ifconfig()

def callback(topic, msg):
    recent_msg = ""
    print('Received: Topic: %s, Message: %s' % (topic, msg))
    if topic.decode() == 'ME35-24/kai':
        recent_msg = msg.decode()
        try:
            recent_msg_float = float(recent_msg)
            if recent_msg_float > 90:
                if (recent_msg_float - 90) / 10 > 1:
                    print("right")
                    stepper.right((recent_msg_float - 90))
            elif recent_msg_float < 90:
                if (90 - recent_msg_float) / 10 > 1:
                    print("left")
                    stepper.left((90 - recent_msg_float))
        except ValueError:
            if recent_msg == 'start':
                print("start")
                left_motor.forward()
            elif recent_msg == 'stop':
                print("stop")
                left_motor.stop()

async def setup_drive(topic):
    mqtt_broker = 'broker.hivemq.com' 
    port = 1883
    topic_sub = f'ME35-24/{topic}'
    
    client = MQTTClient('Kai', mqtt_broker , port, keepalive=0)
    client.connect()
    print('Connected to %s MQTT broker' % (mqtt_broker))
    client.set_callback(callback)         
    print("callback set")
    client.subscribe(topic_sub.encode()) 
    print("subscribed")
    #blink()
    
    while True:
        client.check_msg()
        await asyncio.sleep(0.01)
        
def blink():
    led = machine.Pin('GPIO1', machine.Pin.OUT)
    for i in range(5):
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)
    led.on()

#setup
recent_msg = ""
setup_wifi('Tufts_Robot', '') 
stepper = Steering(6, 7, 8, 9)
left_motor = Motor()

async def main():
    
    asyncio.create_task(setup_drive('kai'))
    
    while True:
        await asyncio.sleep(0.01)
    
    
asyncio.run(main())
    
    
    