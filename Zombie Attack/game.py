import asyncio
from Tufts_ble import Sniff, Yell
import time

class Game:
    def __init__(self):
        self.zombie_count = [0] * 13
        self.discriminator = 0
        self.id = 13
        
    def play(self):
        role = input("Zombie or Human: ")
        self.discriminator = input("Discriminator symbol: ")
        if role == "Zombie":
            asyncio.run(self.eat_brainz())
        elif role == "Human":  
            asyncio.run(self.hide())
                  
    async def eat_brainz(self):    
        p = Yell()
        while True:
            print('advertising ', f'{self.discriminator}{self.id}')
            p.advertise(f'{self.discriminator}{self.id}')
            time.sleep(0.1)
        #p.stop_advertising()
        
    async def hide(self):
        c = Sniff(self.discriminator, verbose = True)
        c.scan(0) 
        while True:
            latest = c.last
            distance = c.rssi
            if latest:
                self.decode(latest, distance)
            time.sleep(0.5)
            
    def decode(self, latest, distance):
        id = int(latest[1:])
        print(id)
        print(distance)
        if distance > -70:
            self.zombie_count[id - 1] += 1
            print(self.zombie_count)
            