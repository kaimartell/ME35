import sensor
import time
import math
import machine

sensor.reset()  # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)  # Set frame size to QQVGA (160x120)
sensor.skip_frames(time=2000)  # Wait for settings take effect.
clock = time.clock()  # Create a clock object to track the FPS.

k_p = 0.1
k_d = 0.05
error = 0
prev = 0

left_motor = machine.PWM(machine.PIN(9))
right_motor = machine.PWM(machine.PIN(10))
for motor in [left_motor, right_motor]:
    motor.freq(50)


def motor_speed(speed, direction):

    if direction == 'left':
        left_motor.duty_u16(0)
        right_motor.duty_u16(speed)
    elif direction == 'right':
        left_motor.duty_u16(speed)
        right_motor.duty_u16(0)
    elif direction == 'straight':
        left_motor.duty_u16(100)
        right_motor.duty_u16(100)
    

while True:
    clock.tick() 
    img = sensor.snapshot()

    currentTag = ''
        
    while True:
        
        clock.tick()
        img = sensor.snapshot()
        
        for tag in img.find_apriltags():
            img.draw_rectangle(tag.rect(), color=(255, 0, 0))
            img.draw_cross(tag.cx(), tag.cy(), color=(0, 255, 0))

            tag_id = tag.id()
            tag_name = tag.family() 
            tag_rotation = (180 * tag.rotation()) / math.pi
            
            currentTag = f'{tag_id}, {tag_name}'
    
            prev = error
            error = tag.cx() - (img.width() // 2)
            
            if error > 0:
                direction = 'left'
            elif error < 0:
                direction = 'right'
            elif error == 0:
                direction = 'straight'
            
            motor_speed(abs(int(k_p * error + k_d * (error - prev))), direction)
    