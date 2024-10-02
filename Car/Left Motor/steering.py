import machine
import time
import asyncio

class Steering:
    def __init__(self, pin1, pin2, pin3, pin4):
        
        self.pins = [machine.Pin(pin, machine.Pin.OUT) for pin in [pin1, pin2, pin3, pin4]]
        print("init motor")
        self.left_hard_limit = -6
        self.right_hard_limit = 8
        self.counter = 0
        
        #loop goes m2a, m1a, m2b, m1b
        #pin 6 is m2b, pin 7 is m2a, pin 8 is m1b, pin 9 is m1a
        self.right_steps = [
            [1, 0, 0, 0], #m2a
            [0, 0, 1, 0], #m1a
            [0, 1, 0, 0], #m1b
            [0, 0, 0, 1] #m2b
            ]
        
        self.left_steps = [
            [0, 0, 0, 1], 
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [1, 0, 0, 0]
        ]
        
    def left(self):
        if self.counter == self.left_hard_limit:
            return
        else:
            for step in self.left_steps:
                for i in range(4):
                    self.pins[i].value(step[i])
                time.sleep(0.01)
            self.counter -= 1
            
        
        
    def right(self):
        if self.counter == self.right_hard_limit:
            return
        else: 
            for step in self.right_steps: 
                for i in range(4):
                    self.pins[i].value(step[i])
                time.sleep(0.01)
            self.counter += 1
            
        if self.counter == 0:
            for step in self.left_steps:
                for i in range(4):
                    self.pins[i].value(step[i])
                time.sleep(0.01)
    
            

            
        

