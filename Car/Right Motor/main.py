#main.py for second pico - right motor
import asyncio
import machine
import network
import time
from mqtt import MQTTClient
from motor import Motor

# Wifi connection
def setup_wifi(SSID, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, password)

    while wlan.ifconfig()[0] == '0.0.0.0':
            print('.', end=' ')
            time.sleep(1)
        
    print('wifi connected') 
    return wlan.ifconfig()


async def setup_drive(topic):
    mqtt_broker = 'broker.hivemq.com' 
    port = 1883
    topic_sub = f'ME35-24/{topic}'
    
    def callback(topic, msg):
        recent_msg = ""
        print('Received: Topic: %s, Message: %s' % (topic, msg))
        if topic.decode() == topic_sub:
            recent_msg = msg.decode()
            if recent_msg == 'start':
                print("start")
                right_motor.forward()
            elif recent_msg == 'stop':
                print("stop")
                right_motor.stop()
    
    client = MQTTClient('alsoKai', mqtt_broker , port, keepalive=0)
    client.connect()
    print('Connected to %s MQTT broker' % (mqtt_broker))
    client.set_callback(callback)         
    print("callback set")
    client.subscribe(topic_sub.encode()) 
    print("subscribed")
    blink()
    
    
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
        
setup_wifi('Tufts_Robot', '')
right_motor = Motor()

async def main():
    asyncio.create_task(setup_drive('kai'))
    
    while True:
        await asyncio.sleep(0.01)


asyncio.run(main())
