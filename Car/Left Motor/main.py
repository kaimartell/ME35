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
    global counter
    
    print('Received: Topic: %s, Message: %s' % (topic, msg))
    if topic.decode() == 'ME35-24/kai':
        recent_msg = msg.decode()
        print("counter: ", counter)
        try:
            recent_msg_float = float(recent_msg)
            if 85 < recent_msg_float < 95:
                print("here1")
                if counter < 0:
                    stepper.right(0 - counter)
                elif counter > 0:
                    stepper.left(counter)
                counter = 0
                    
            elif 75 < recent_msg_float < 85:
                print("here2")
                if counter < -1: 
                    stepper.right(abs(counter + 1))
                elif counter > -1:
                    stepper.left(abs(counter - 1))
                counter = -1
                
            elif 65 < recent_msg_float < 75:
                print("here3")
                if counter < -2:
                    stepper.right(abs(counter + 2))
                elif counter > 2:
                    stepper.left(abs(counter - 2))
                counter = -2
                
            elif 55 < recent_msg_float < 65:
                print("here4")
                if counter < -3:
                    stepper.right(abs(counter + 3))
                elif counter > 3:
                    stepper.left(abs(counter - 3))
                counter = -3
                
            elif 45 < recent_msg_float < 55:
                print("here5")
                if counter < -4:
                    stepper.right(abs(counter + 4))
                elif counter > 4:
                    stepper.left(abs(counter - 4))
                counter = -4
                
            elif 35 < recent_msg_float < 45:
                print("here6")
                if counter < -5:
                    stepper.right(abs(counter + 5))
                elif counter > 5:
                    stepper.left(abs(counter - 5))
                counter = -5
                
            elif 95 < recent_msg_float < 105:
                print("here7")
                if counter < 1:
                    stepper.right(1 - counter)
                elif counter > -1:
                    stepper.left(abs(counter - 1))
                counter = 1
                
            elif 105 < recent_msg_float < 115:
                print("here8")
                if counter < 2:
                    stepper.right(2 - counter)
                elif counter > -2:
                    stepper.left(abs(counter - 2))
                counter = 2
                
            elif 115 < recent_msg_float < 125:
                print("here9")
                if counter < 3:
                    stepper.right(3 - counter)
                elif counter > -3:
                    stepper.left(abs(counter - 3))
                counter = 3
                
            elif 125 < recent_msg_float < 135:
                print("here10")
                if counter < 4:
                    stepper.right(4 - counter)
                elif counter > -4:
                    stepper.left(abs(counter - 4))
                counter = 4
                
            elif 135 < recent_msg_float < 145:
                print("here11")
                if counter < 5:
                    stepper.right(5 - counter)
                elif counter > -5:
                    stepper.left(abs(counter - 5))
                counter = 5  
                
                
            
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

#setup
recent_msg = ""
setup_wifi('Tufts_Robot', '') 
stepper = Steering(6, 7, 8, 9)
left_motor = Motor()
counter = 0

async def main():
    
    asyncio.create_task(setup_drive('kai'))
    
    while True:
        await asyncio.sleep(0.01)
    
    
asyncio.run(main())
    
    
    