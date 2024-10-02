import machine
import time
import asyncio

class Motor:
    def __init__(self):
        """self.motor = machine.PWM(machine.Pin(17))
        self.motor.freq(20000)
        self.motor.duty_u16(0)"""
        
        self.motor = machine.Pin('GPIO17', machine.Pin.OUT)
        
        

        
    def forward(self):
        """print("forward")
        while True: 
            print("driving")
            self.motor.duty_u16(1000)"""
        print("motor on")
        self.motor.on()
            
    
    def stop(self):
        """self.motor.duty_u16(0) """
        self.motor.off()