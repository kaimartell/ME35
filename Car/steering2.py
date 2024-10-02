import machine
import time

class Steering:
    def __init__(self, pin1, pin2, pin3, pin4):
        
        self.pins = [machine.Pin(pin, machine.Pin.OUT) for pin in [pin1, pin2, pin3, pin4]]
        
        #loop goes m2a, m1a, m2b, m1b
        #pin 6 is m2b, pin 7 is m2a, pin 8 is m1b, pin 9 is m1a
        self.left = [
            [1, 0, 0, 0], #m2a
            [0, 0, 1, 0], #m1a
            [0, 1, 0, 0], #m1b
            [0, 0, 0, 1] #m2b
            ]
        
        self.right = [
            [0, 0, 0, 1], 
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [1, 0, 0, 0]
        ]
        
    def drive(self):
        for step in self.left:
            for i in range(4):
                self.pins[i].value(step[i])
            time.sleep(0.01)
            

