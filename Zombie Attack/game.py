import asyncio
from Tufts_ble import Sniff, Yell
import time
import machine

class Game:
    def __init__(self):
        self.zombie_count = [0] * 13
        self.discriminator = '!'
        self.id = 13
        self.ble_read = []
        self.threshold = -60
        self.role = "Human"
        self.buzzer = machine.PWM(machine.Pin('GPIO18', machine.Pin.OUT))
        self.buzzer.freq(440)
        self.buzzer.duty_u16(0)
        self.led1 = machine.Pin('GPIO6', machine.Pin.OUT)
        self.led2 = machine.Pin('GPIO7', machine.Pin.OUT)

    def play(self):
        if self.role == "Zombie":
            asyncio.run(self.eat_brainz())
        elif self.role == "Human":
            asyncio.run(self.hide())

    async def eat_brainz(self):
        p = Yell()
        asyncio.create_task(self.buzz()) 
        self.led1.value(1) 
        self.led2.value(0) 
        
        while True:
            p.advertise(f'{self.discriminator}{self.id}')
            print(f'advertised {self.id}')
            await asyncio.sleep(0.1) 

    async def hide(self):
        c = Sniff(self.discriminator, verbose=True)
        c.scan(0)
        self.led2.value(1) 
        while True:
            self.clear_time()
            self.clear_distance()
            self.add_counter()
            print("zombie_count: ", self.zombie_count)
            if self.check_count():
                await self.eat_brainz()
                break
            latest = c.last
            if latest:
                self.decode(latest, c.rssi)
            await asyncio.sleep(0.1) 

    def decode(self, latest, distance):
        try:
            id = int(latest[1:])
        except ValueError:
            print(f"Error: Could not convert {latest[1:]} to an integer")
            return

        print("ble_read: ", self.ble_read)
        if id != self.id:
            self.ble_read.append((id, distance, time.time()))

    def clear_time(self):
        if not self.ble_read:
            return
        current_time = time.time()
        first_entry = self.ble_read[0][2]

        if isinstance(self.ble_read[0], (list, tuple)) and len(self.ble_read[0]) > 2:
            if current_time - first_entry > 5:
                print("Removing entry older than 5 seconds.")
                removed_entry = self.ble_read.pop(0)
                print(f"Removed entry with ID {removed_entry[0]}")

        else:
            print("Unexpected structure in self.ble_read[0]")

    def clear_distance(self):
        if not self.ble_read:
            return

        if isinstance(self.ble_read[0], (list, tuple)) and len(self.ble_read[0]) > 2:
            print("true")
            latest_distance = self.ble_read[-1][1]
            latest_id = self.ble_read[-1][0]

            print("latest_distance: ", latest_distance)
            print("latest_id: ", latest_id)

            if latest_distance < self.threshold:
                print("Removing entries with the same ID that are too far away.")
                self.ble_read = [entry for entry in self.ble_read if entry[0] != latest_id]
                print(f"Removed all entries with ID {latest_id} because they were too far away.")

        else:
            print("Unexpected structure in self.ble_read[0]")

    def add_counter(self):
        if not self.ble_read:
            return

        if isinstance(self.ble_read[0], (list, tuple)) and len(self.ble_read[0]) > 2:
            latest_id = self.ble_read[-1][0]
            latest_time = self.ble_read[-1][2]
            for entry in self.ble_read:
                if entry[0] == latest_id and latest_time - entry[2] >= 3:
                    asyncio.create_task(self.blink())
                    self.zombie_count[latest_id - 1] += 1
                    print(f"Added a count to zombie {latest_id}")
                    self.ble_read = [entry for entry in self.ble_read if entry[0] != latest_id]
                    print(f"Removed all entries with ID {latest_id} because they tagged us.")
                    break

        else:
            print("Unexpected structure in self.ble_read[0]")

    def check_count(self):
        for i, count in enumerate(self.zombie_count):
            if count >= 3:
                print(f"We have been zombified by {i + 1}. We are now a zombie.")
                self.role = "Zombie"
                self.id = i + 1
                with open("id.txt", "w") as f:
                    f.write(str(self.id))
                return True

    async def buzz(self):
        while True:
            self.buzzer.duty_u16(1000)
            await asyncio.sleep(0.1) 
            
    async def blink(self):
        if self.role != "Zombie":
            self.led1.value(1)
            await asyncio.sleep(0.1) 
            self.led1.value(0)
            await asyncio.sleep(0.001)

