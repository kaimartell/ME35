import machine
import time

servo = machine.PWM(machine.Pin(16), freq=50)

def set_servo_angle(angle):
    print("turning servo")
    print("angle: ", angle) 
    min_duty = 1638  # 0.5 ms pulse (duty cycle value for 0 degrees)
    max_duty = 8192  # 2.5 ms pulse (duty cycle value for 180 degrees)
    duty = min_duty + int((max_duty - min_duty) * (angle / 180))
    servo.duty_u16(duty)
    

def main():
    set_servo_angle(160)
    time.sleep(2)
    set_servo_angle(0)
    time.sleep(2)
    #set_servo_angle(160)
    i=0
    while i < 360 :
        set_servo_angle(i)
        time.sleep(0.2)
        i+=1
     
main()
#set_servo_angle(160)