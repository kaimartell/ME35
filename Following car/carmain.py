import machine
import time


left_motor = machine.PWM(machine.Pin(0), freq=1000)
right_motor = machine.PWM(machine.Pin(1), freq=1000)


def motor_speed(speed, direction):

    if direction == 'left':
        print("in left")
        left_motor.duty_u16(0)
        right_motor.duty_u16(speed)
    elif direction == 'right':
        print("in right")
        left_motor.duty_u16(speed)
        right_motor.duty_u16(0)
    elif direction == 'straight':
        print("in straight")
        while True:
            left_motor.duty_u16(32768)  # 50% duty cycle
            right_motor.duty_u16(32768)  # 50% duty cycle
            
        
if __name__ == '__main__':
    while True:
        print("in main2")
        motor_speed(32768, 'straight')