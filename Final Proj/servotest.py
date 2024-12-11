import machine
import time

servo = machine.PWM(machine.Pin(20), freq=50)



def set_servo_angle(angle):
        # Set the servo motor to a specific angle
        min_duty = 1638  # 0.5 ms pulse (duty cycle value for 0 degrees)
        max_duty = 8192  # 2.5 ms pulse (duty cycle value for 180 degrees)
        duty = min_duty + int((max_duty - min_duty) * (angle / 180))
        servo.duty_u16(duty)



    
    
while True:
    set_servo_angle(0)
    time.sleep(1)
    set_servo_angle(180)
    time.sleep(1)
        
        