import machine
import time

# Set up pins as PWM for the test
test_pin = machine.PWM(machine.Pin(1), freq=1000)  # GPIO8

# Vary brightness (which simulates varying motor speed)
while True:
    for duty in range(0, 65536, 1000):  # Gradually increase duty cycle
        test_pin.duty_u16(duty)
        time.sleep(0.05)
