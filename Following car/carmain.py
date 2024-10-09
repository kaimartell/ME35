import machine
import time
import bluetooth
import asyncio
from micropython import const
import struct

left_motor = machine.PWM(machine.Pin(0), freq=1000)
right_motor = machine.PWM(machine.Pin(1), freq=1000)

# Constants for BLE events
_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_COMPLETE = const(6)
_IRQ_PERIPHERAL_CONNECT = const(7)
_IRQ_PERIPHERAL_DISCONNECT = const(8)
_IRQ_GATTC_NOTIFY = const(18)
_IRQ_GATTC_WRITE_DONE = const(20)
_IRQ_GATTC_SERVICE_DISCOVER = const(21)

# BLE UUIDs
_SERVICE_UUID = 0x1523  # 16-bit UUID as integer
_MOTOR_SPEED_CHAR_UUID = 0x1525  # 16-bit UUID as integer

class BLECentral:
    def __init__(self):
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self._irq)
        self._conn_handle = None
        self._motor_speed_handle = None
        self._last_notification = None  # Variable to store the most recent notification

    def _irq(self, event, data):
        if event == _IRQ_SCAN_RESULT:
            addr_type, addr, adv_type, rssi, adv_data = data
            # Manually check the advertisement data for the service UUID
            if self._find_service_in_advertisement(adv_data, _SERVICE_UUID):
                print("Found Motor Controller!")
                self._ble.gap_scan(None)  # Stop scanning
                self._ble.gap_connect(addr_type, addr)  # Connect to the peripheral
        elif event == _IRQ_SCAN_COMPLETE:
            print("Scan complete")
        elif event == _IRQ_PERIPHERAL_CONNECT:
            conn_handle, addr_type, addr = data
            print("Connected")
            self._conn_handle = conn_handle
            self._ble.gattc_discover_services(conn_handle)
        elif event == _IRQ_PERIPHERAL_DISCONNECT:
            conn_handle, _, _ = data
            print("Disconnected")
            self._conn_handle = None
            self._motor_speed_handle = None
            # Re-start scanning
            self.start_scan()
        elif event == _IRQ_GATTC_NOTIFY:
            #print("new notif")
            conn_handle, value_handle, notify_data = data
            #print("data: ", value_handle)
            #print("motor_speed_handle: ", self._motor_speed_handle)
            #print("conn_handle: ", conn_handle)
            #print("notify_data: ", notify_data)
            decoded_data = bytes(notify_data).decode()
            #print("decoded_data: ", decoded_data)
            if value_handle == _IRQ_GATTC_SERVICE_DISCOVER:
                # Store the most recent notification
                self._last_notification = decoded_data
                #print(f"Motor Speed: {self._last_notification}")
        elif event == _IRQ_GATTC_WRITE_DONE:
            conn_handle, value_handle, status = data
            print("Write complete")
        elif event == _IRQ_GATTC_SERVICE_DISCOVER:
            conn_handle, char_handle, char_uuid = data
            if char_uuid == _MOTOR_SPEED_CHAR_UUID:
                print(f"Found Motor Speed Characteristic: {char_handle}")
                self.subscribe_to_motor_speed(conn_handle, char_handle)


    def discover_characteristics(self, conn_handle):
        # Discover characteristics for the motor speed service
        print("Discovering characteristics...")
        self._ble.gattc_discover_characteristics(conn_handle)

    def start_scan(self):
        print("Scanning for BLE devices...")
        self._ble.gap_scan(2000, 30000, 30000)

    def _find_service_in_advertisement(self, adv_data, service_uuid):
        # Check the advertisement data to see if the service UUID is present
        i = 0
        while i < len(adv_data):
            length = adv_data[i]
            if length == 0:
                break
            ad_type = adv_data[i + 1]
            if ad_type == 0x03:  # Complete list of 16-bit UUIDs
                uuid16 = struct.unpack("<H", adv_data[i + 2 : i + length + 1])[0]
                if uuid16 == service_uuid:
                    return True
            i += length + 1
        return False

    def subscribe_to_motor_speed(self, conn_handle, char_handle):
            print("char_handle: ", char_handle)
            self._motor_speed_handle = char_handle
            self._ble.gattc_write(conn_handle, char_handle, b'\x01\x00', 1)  # Enable notifications

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

central = BLECentral()
central.start_scan()

while True:
    time.sleep(0.5)
    print("Last Notification: ", central._last_notification)
    #_last_notification returns a string with the format "speed distance"
    #split the string to get the speed and direction
    if central._last_notification:
        speed, distance = central._last_notification.split()
        
    

