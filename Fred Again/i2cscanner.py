import machine
import time

def i2c_scan():
    try:
        # Try using I2C bus 0
        i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))  # Adjust pins as necessary
        devices = i2c.scan()
        
        if devices:
            print('I2C devices found on bus 0:', [hex(device) for device in devices])
        else:
            print('No I2C devices found on bus 0')
    except ValueError as e:
        print(f"Error on I2C bus 0: {e}")

    try:
        # Try using I2C bus 1 with correct pins
        i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2))  # Adjust pins as necessary
        devices = i2c.scan()
        
        if devices:
            print('I2C devices found on bus 1:', [hex(device) for device in devices])
        else:
            print('No I2C devices found on bus 1')
    except ValueError as e:
        print(f"Error on I2C bus 1: {e}")

while True:
    i2c_scan()
    time.sleep(5)