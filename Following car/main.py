import sensor
import time
import math
import machine
import bluetooth
from ble_advertising import advertising_payload
from micropython import const

# Constants for BLE events
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_FLAG_READ = const(0x0002)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)
_FLAG_INDICATE = const(0x0020)

# BLE Service and Characteristic UUIDs
_SERVICE_UUID = bluetooth.UUID(0x1523)
_MOTOR_SPEED_CHAR_UUID = (bluetooth.UUID(0x1525), _FLAG_NOTIFY | _FLAG_READ)
_MOTOR_SERVICE = (_SERVICE_UUID, (_MOTOR_SPEED_CHAR_UUID,))

class BLEMotor:
    def __init__(self, ble, name="MotorController"):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle,),) = self._ble.gatts_register_services((_MOTOR_SERVICE,))
        self._connections = set()
        self._payload = advertising_payload(name=name, services=[_SERVICE_UUID])
        self._advertise()

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            self._advertise()
        elif event == _IRQ_GATTS_WRITE:
            pass  # Handle any incoming writes if needed

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

    def notify_speed(self, speed):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._handle, str(speed))



sensor.reset()  # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)  # Set frame size to QQVGA (160x120)
sensor.skip_frames(time=2000)  # Wait for settings take effect.
clock = time.clock()  # Create a clock object to track the FPS.

k_p = 0.1
k_d = 0.05
error = 0
prev = 0

ble = bluetooth.BLE()
motor_ble = BLEMotor(ble)

left_motor = machine.PWM(machine.Pin(9))
right_motor = machine.PWM(machine.Pin(10))
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
            
            speed = abs(int(k_p * error + k_d * (error - prev)))
            
            motor_ble.notify_speed(f"S:{speed}, D:{direction}")