import machine
from machine import Pin
import time
import random
#from networking import Networking
from now import Now

pins = [0, 1, 2]

led_buttons = [Pin(pin, Pin.OUT) for pin in pins]

servo = machine.PWM(Pin(20), freq=50)



def light_up(pin, duration=1):
    pin.value(1)
    print(f"Lighting up pin {pin}")
    time.sleep(duration)
    pin.value(0)
    time.sleep(0.2)

def generate_sequence(length):
    sequence = [random.choice(led_buttons) for _ in range(length)]
    print(f"Generated sequence: {[pins[led_buttons.index(pin)] for pin in sequence]}")
    return sequence

def check_sequence(sequence):
    for idx, expected_pin in enumerate(sequence):
        # Switch all pins to input mode
        for pin in led_buttons:
            pin.init(Pin.IN, Pin.PULL_DOWN)

        pressed_pin = None

        print(f"Waiting for input for step {idx + 1}/{len(sequence)}...")

        while pressed_pin is None:
            for pin in led_buttons:
                if pin.value() == 1: 
                    pressed_pin = pin
                    pressed_pin_number = pins[led_buttons.index(pressed_pin)]
                    print(f"Button pressed: Button {pressed_pin_number}")
                    time.sleep(0.2) 
                    break

        expected_pin_number = pins[led_buttons.index(expected_pin)]
        print(f"Expected Button: {expected_pin_number}, Pressed Button: {pressed_pin_number}")

        if pressed_pin_number != expected_pin_number:
            print(f"Error: Expected Button {expected_pin_number}, but got Button {pressed_pin_number}")
            for pin in led_buttons:
                pin.init(Pin.OUT)
            return False  

    for pin in led_buttons:
        pin.init(Pin.OUT)
    return True 

def set_servo_angle(angle):
        # Set the servo motor to a specific angle
        min_duty = 1638  # 0.5 ms pulse (duty cycle value for 0 degrees)
        max_duty = 8192  # 2.5 ms pulse (duty cycle value for 180 degrees)
        duty = min_duty + int((max_duty - min_duty) * (angle / 180))
        servo.duty_u16(duty)

def play_game():
    #sequence_length = 3
    print("Game Start!")

    #sequence = generate_sequence(sequence_length)
    sequence = [led_buttons[2], led_buttons[1], led_buttons[2]]
    print("Watch the sequence!")
    for pin in sequence:
        light_up(pin)

    print("Now repeat the sequence!")
    if check_sequence(sequence):
        print("here")
        #move servo 180 degrees
        set_servo_angle(180)
        
            
    return True
            
      
def receive(msg, mac):
    print("Receive")
    print(msg)
    if msg == b"1complete":
        print("play game")
        time.sleep(5)
        if play_game():
            n.publish(b'2complete')
            time.sleep(5)
            set_servo_angle(0)
          
            
n = Now(receive)
n.connect()

try: 
    while True:
        time.sleep(1)
    
except KeyboardInterrupt:
    n.close()
    print("Connection closed")
    
finally:
    n.close()
    print("Connection closed")


"""networking = Networking()

recipient_mac = b'\xFF\xFF\xFF\xFF\xFF\xFF' #This mac sends to all

def receive():
    global msg
    print("Receive")
    for mac, message, rtime in networking.aen.return_messages(): #You can directly iterate over the function
        msg = message
        print(mac, message, rtime)
"""

