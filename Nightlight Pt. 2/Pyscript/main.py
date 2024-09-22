from pyscript import document, window, when
from pyscript.js_modules import mqtt_library
import asyncio


pico = document.getElementById("info")
pub_topic = "ME35-24/Kaisnightlight"
sub_topic = "ME35-24/Kaisnightlight"
mqtt_connected = document.getElementById("mqtt_connected")

def received_mqtt_msg(message):
    message = myClient.read().split('\t')
    document.getElementById("answer").innerHTML = 'topic: %s, message: %s' % (message[0], message[1])

async def init_mqtt():
    global myClient, old_topic
    try:
        mqtt_connected.innerHTML = 'Initializing MQTT client...'
        window.console.log('Initializing MQTT client...')
        
        if mqtt_library.myClient is None:
            raise Exception("mqtt_library.myClient is None")
        
        myClient = mqtt_library.myClient
        window.console.log('myClient initialized')
        
        old_topic = sub_topic
        window.console.log(f'Old topic set to {old_topic}')
        
        myClient.init()
        
        mqtt_connected.innerHTML = 'MQTT client initialized, waiting for connection...'
        
        attempt = 0
        while not myClient.connected:
            await asyncio.sleep(0.1)
            attempt += 1
            if attempt % 10 == 0: 
                window.console.log(f'Waiting for MQTT connection... Attempt {attempt / 10}')
        
        window.console.log('MQTT client connected!')
        mqtt_connected.innerHTML = 'connected!'
        myClient.subscribe(sub_topic)
        myClient.callback = received_mqtt_msg
    except Exception as e:
        window.console.log(f'Error initializing MQTT client: {e}')
        mqtt_connected.innerHTML = f'Error: {e}'

@when("click", "#send_pico")
def send_pico(event):
    if pico is not None:
        message = pico.value
        if myClient.connected:
            try:
                window.console.log(f"Publishing to {pub_topic}: {message}")
                myClient.publish(pub_topic, message)
                
            except Exception as e:
                window.console.log(f"Error publishing message: {e}")
        else:
            window.console.log("Error: MQTT client is not connected.")
    else:
        window.console.log("Error: 'pico' element not found.")

@when("click", "#on_button")
def turn_on(event):
    message = "on"
    if myClient.connected:
        try:
            window.console.log(f"Publishing to {pub_topic}: {message}")
            myClient.publish(pub_topic, message)
        except Exception as e:
            window.console.log(f"Error publishing message: {e}")
    else:
        window.console.log("Error: MQTT client is not connected.")

@when("click", "#off_button")
def turn_off(event):
    message = "off"
    if myClient.connected:
        try:
            window.console.log(f"Publishing to {pub_topic}: {message}")
            myClient.publish(pub_topic, message)
        except Exception as e:
            window.console.log(f"Error publishing message: {e}")
    else:
        window.console.log("Error: MQTT client is not connected.")

@when("click", "#sync_button")
def toggle_sync(event):
    sync_button = document.getElementById("sync_button")
    current_text = sync_button.innerHTML

    if "Off" in current_text:
        sync_button.innerHTML = "Sync: On"
        myClient.publish(pub_topic, "sync on")
    else:
        sync_button.innerHTML = "Sync: Off"
        myClient.publish(pub_topic, "sync off")



"""@when("change", "#s_topic")
def new_subscribe(event):
    global old_topic
    window.console.log(f'Changing subscription from {old_topic} to {sub_topic}')
    myClient.unsubscribe(old_topic)
    myClient.subscribe(sub_topic)
    old_topic = sub_topic"""



asyncio.create_task(init_mqtt())
