#main.py
import asyncio
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

async def setup_drive(topic):
    mqtt_broker = 'broker.hivemq.com' 
    port = 1883
    topic_sub = f'ME35-24/{topic}'
    
    def callback(topic, msg):
        recent_msg = ""
        print('Received: Topic: %s, Message: %s' % (topic, msg))
        if topic.decode() == topic_sub:
            recent_msg = msg.decode()
            if recent_msg == 'left':
                print("left")
                stepper.left()
            elif recent_msg == 'right':
                print("right")
                stepper.right() 
            elif recent_msg == 'start':
                print("start")
                left_motor.forward()
            elif recent_msg == 'stop':
                print("stop")
                left_motor.stop()
    
    client = MQTTClient('Kai', mqtt_broker , port, keepalive=0)
    client.connect()
    print('Connected to %s MQTT broker' % (mqtt_broker))
    client.set_callback(callback)         
    print("callback set")
    client.subscribe(topic_sub.encode()) 
    print("subscribed")
    
    while True:
        client.check_msg()
        await asyncio.sleep(0.01)

#setup
recent_msg = ""
setup_wifi('Tufts_Robot', '') 
stepper = Steering(6, 7, 8, 9)
left_motor = Motor()

async def main():
    
    asyncio.create_task(setup_drive('drive'))
    
    while True:
        await asyncio.sleep(1)
    
    
asyncio.run(main())
    
    
    