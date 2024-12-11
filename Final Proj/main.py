import machine
import time
import random
import neopixel
from now import Now

# Initialize neopixel light strips
nPin = machine.Pin(20)
n2Pin = machine.Pin(19)
n = neopixel.NeoPixel(nPin, 5)  # Game LEDs
points = neopixel.NeoPixel(n2Pin, 3)  # Points LEDs

# Button GPIO pins and mapping
button_pins = [0, 1, 2, 21, 22]  # Actual GPIO pin numbers
button_indices = {pin: idx for idx, pin in enumerate(button_pins)}  # Mapping: {GPIO pin -> Index}
buttons = [machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP) for pin in button_pins]

# Initialize servo
servo = machine.PWM(machine.Pin(16), freq=50)

# Servo angle function
def set_servo_angle(angle):
    min_duty = 1638  # 0.5 ms pulse (duty cycle value for 0 degrees)
    max_duty = 8192  # 2.5 ms pulse (duty cycle value for 180 degrees)
    duty = min_duty + int((max_duty - min_duty) * (angle / 180))
    servo.duty_u16(duty)

# Light up game LED
def light_up(pin_index, duration):
    n[pin_index] = (255, 0, 0)    
    n.write()
    time.sleep(duration)
    n[pin_index] = (0, 0, 0)
    n.write()
    time.sleep(0.2)  # Debounce delay

# Update points LEDs
def update_points(stage):
    for i in range(3):
        if i <= stage:  # Light up LEDs for completed stages
            points[i] = (0, 255, 0)
        else:
            points[i] = (0, 0, 0)
    points.write()

# Generate sequence
def generate_sequence(length):
    sequence = [random.choice(button_pins) for _ in range(length)]
    print("Generated sequence (indices):", [button_indices[pin] for pin in sequence])
    return sequence

# Check player's input
def check_sequence(sequence):

    for step in sequence:
        correct = False
        while not correct:
            for i, button in enumerate(buttons):
                if not button.value():  # Button pressed
                    print(f"Button {i} detected as pressed")  # Debugging

                    # Blink the LED for the pressed button immediately
                    light_up(i, 0.5)  # Blink the LED for 0.5 seconds

                    print(f"Button {i} detected as released")  # Debugging

                    # Verify if the button press matches the sequence
                    pin = button_pins[i]
                    index = button_indices[pin]

                    if pin == step:
                        print(f"Correct button {index} pressed!")
                        correct = True
                    else:
                        print(f"Incorrect button {index}. Game Over.")
                        return False
            time.sleep(0.1)  # Reduced debounce delay for quicker button polling
    return True



def incorrect():
    #blink n red
    i = 0
    while i < 5:
        for j in range(5):
            n[j] = (255, 0, 0)
            n.write()
            
        time.sleep(0.5)
        
        for j in range(5):
            n[j] = (0, 0, 0)
            n.write()
            
        time.sleep(0.5)
            
        i += 1
        


def win():
    #blink points
    i = 0
    while i < 3:
        for i in range(3):
            points[i] = (0, 255, 0)
            points.write()
            
        time.sleep(0.5)
        
        for i in range(3):
            points[i] = (0, 0, 0)
            points.write()
            
        time.sleep(0.5)
            
        i += 1
        
    for j in range(5):
        n[j] = (0, 0, 0)
        n.write()
    for j in range(3):
        points[j] = (0, 0, 0)
        points.write()
        

# Game logic
def play():
    
    set_servo_angle(0)
    
    max_length = 5
    current_length = 3

    while current_length <= max_length:
        print(f"Starting Stage {current_length - 2}")
        update_points(current_length - 3)  # Update points NeoPixel based on the stage
        time.sleep(1)  # Delay between stages

        while True:
            sequence = generate_sequence(current_length)
            print(f"Memorize the sequence! Round {current_length - 2}")
            
            time.sleep(0.5)
            
            # Show the sequence
            for pin in sequence:
                print("pin: ", pin)
                print("button_indices[pin]: ", button_indices[pin])
                print("here")
                index = button_indices[pin]
                light_up(index, 1)
            
            print("Input the sequence!")
            
            # Check player input
            if check_sequence(sequence):
                print("Correct! Moving to the next stage.")
                if current_length == max_length:
                    print("Congratulations! You won!")
                    win()
                    x=0
                    for i in range(2):
                        while x < 180 :
                            set_servo_angle(x)
                            time.sleep(0.1)
                            x+=1
                            
                    now.publish(b'2complete')
                    return True
                else:
                    current_length += 1
                    break  # Exit the retry loop to move to the next stage
            else:
                print("Incorrect. Generating a new sequence for this stage.")
                incorrect()
                    #turn off all lights
                for i in range(5):
                    n[i] = (0, 0, 0)
                    n.write()
                time.sleep(1)  # Optional delay before showing the new sequence
            
        

        
def receive(msg, mac):
    print("Receive")
    print(msg)
    if msg == b"1complete":
        print("play game")
        time.sleep(5)
        if play():
            print("here")
            now.publish(b'2complete')
            time.sleep(5)
            set_servo_angle(0)
            
    elif msg == b'reset':
        print("reset")
        set_servo_angle(0)
        for i in range(5):
            n[i] = (0, 0, 0)
            n.write()
        for i in range(3):
            points[i] = (0, 0, 0)
            points.write()
          
            
now = Now(receive)
now.connect()

print("connected")

try: 
    while True:
        time.sleep(1)
    
except KeyboardInterrupt:
    now.close()
    print("Connection closed")
    
finally:
    now.close()
    print("Connection closed")


