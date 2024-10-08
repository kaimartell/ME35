import sensor
import time
import math
import machine
import bluetooth
from micropython import const
import struct

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
        handles = self._ble.gatts_register_services((_MOTOR_SERVICE,))
        self._handle = handles[0][0]  # Correct way to get the first handle
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
        print(f"Notify speed called with speed: {speed}")  # Debug line
        for conn_handle in self._connections:
            try:
                msg = str(speed)
                #print(f"Attempting to notify speed: {speed_str}")  # Debug line before notifying
                self._ble.gatts_notify(conn_handle, self._handle, msg)
            except Exception as e:
                print(f"Error notifying speed: {e}")  # Catch and print errors
   
    
def advertising_payload(limited_disc=False, br_edr=False, name=None, services=None):
    payload = bytearray()

    def _append(adv_type, value):
        nonlocal payload
        payload += bytes((len(value) + 1, adv_type)) + value

    # Flags
    flags = (0x02 if limited_disc else 0x06) + (0x00 if br_edr else 0x04)
    _append(0x01, struct.pack("B", flags))

    # Name
    if name:
        _append(0x09, name.encode())

    # Services (UUIDs)
    if services:
        for uuid in services:
            if isinstance(uuid, bluetooth.UUID):
                uuid_bytes = bytes(uuid)
                if len(uuid_bytes) == 2:  # 16-bit UUID
                    _append(0x03, uuid_bytes)
                elif len(uuid_bytes) == 16:  # 128-bit UUID
                    _append(0x07, uuid_bytes)

    return payload
    
   

    
    
def degrees(radians):
    return (180 * radians) / math.pi

sensor.reset()  # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)  # Set frame size to QQVGA (160x120)
sensor.skip_frames(time=2000)  # Wait for settings take effect.
clock = time.clock()  # Create a clock object to track the FPS.

k_p = 0.1
k_d = 0.05
error = 0
prev = 0

f_x = (2.8 / 3.984) * 160  # find_apriltags defaults to this if not set
f_y = (2.8 / 2.952) * 120  # find_apriltags defaults to this if not set
c_x = 160 * 0.5  # find_apriltags defaults to this if not set (the image.w * 0.5)
c_y = 120 * 0.5  # find_apriltags defaults to this if not set (the image.h * 0.5)

ble = bluetooth.BLE()
motor_ble = BLEMotor(ble)



while True:
    #print("in first while")
    clock.tick() 
    img = sensor.snapshot()

    currentTag = ''
        
    while True:
        #print("in second while")
        clock.tick()
        img = sensor.snapshot()
    
        # Check the img object
        #print(f"Image object: {img}")  
        #print(f"find_apriltags callable: {callable(img.find_apriltags)}")  # Check if it's callable
    
        for tag in img.find_apriltags(fx=f_x, fy=f_y, cx=c_x, cy=c_y):
            #print(f"Found tag: {tag}")  # Inspect the tag object
            #print(f"tag.rect type: {type(tag.rect)}")  # Debug statement
            #print(f"tag.cx type: {type(tag.cx)}")  # Debug statement
            img.draw_rectangle(tag.rect, color=(255, 0, 0))  # Access tuple directly
            img.draw_cross(tag.cx, tag.cy, color=(0, 255, 0))  # Access integers directly
    
            prev = error
            error = tag.cx - (img.width() // 2)
    
            speed = int(k_p * error + k_d * (error - prev))
            
            if error > 0:
                direction = 'left'
            elif error < 0:
                direction = 'right'
            elif error == 0:
                direction = 'straight'
            
            print("Notified")
            #motor_ble.notify_speed("Test")
            motor_ble.notify_speed(speed)  # Test with actual speed and direction values