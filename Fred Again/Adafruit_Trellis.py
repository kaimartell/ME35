# call this Adafruit_Trellis.py

from machine import I2C, Pin

# Constants
LED_ON = 1
LED_OFF = 0

HT16K33_BLINK_OFF = 0
HT16K33_BLINK_2HZ = 1
HT16K33_BLINK_1HZ = 2
HT16K33_BLINK_HALFHZ = 3

class AdafruitTrellis:
    """This class handles the functionality for the Adafruit Trellis with HT16K33."""

    # Mapping for button numbers to their corresponding bit positions
    BUTTON_MAPPING = {
        #6: b'\x01\x00\x00\x00\x00\x00',
        #7: b'\x02\x00\x00\x00\x00\x00',
        #2: b'\x04\x00\x00\x00\x00\x00',
        #8: b'\x08\x00\x00\x00\x00\x00',
        #1: b'\x10\x00\x00\x00\x00\x00',
        #4: b'\x20\x00\x00\x00\x00\x00',
        #5: b'\x40\x00\x00\x00\x00\x00',
        #0: b'\x80\x00\x00\x00\x00\x00',
        #9: b'\x00\x01\x00\x00\x00\x00',
        #14: b'\x00\x02\x00\x00\x00\x00',
        #13: b'\x00\x04\x00\x00\x00\x00',
        #12: b'\x00\x08\x00\x00\x00\x00',
        #11: b'\x00\x00\x02\x00\x00\x00',
        #3: b'\x00\x00\x04\x00\x00\x00',
        #10: b'\x00\x00\x00\x01\x00\x00',
        #15: b'\x00\x00\x00\x02\x00\x00'
        #0: b'\x01\x00\x00\x00\x00\x00',
        #1: b'\x02\x00\x00\x00\x00\x00',
        #2: b'\x04\x00\x00\x00\x00\x00',
        #3: b'\x08\x00\x00\x00\x00\x00',
        #4: b'\x10\x00\x00\x00\x00\x00',
        #5: b'\x20\x00\x00\x00\x00\x00',
        #6: b'\x40\x00\x00\x00\x00\x00',
        #7: b'\x80\x00\x00\x00\x00\x00',
        #8: b'\x00\x01\x00\x00\x00\x00',
        #9: b'\x00\x02\x00\x00\x00\x00',
        #10: b'\x00\x04\x00\x00\x00\x00',
        #11: b'\x00\x08\x00\x00\x00\x00',
        #12: b'\x00\x00\x02\x00\x00\x00',
        #13: b'\x00\x00\x04\x00\x00\x00',
        #14: b'\x00\x00\x00\x01\x00\x00',
        #15: b'\x00\x00\x00\x02\x00\x00'
        
        
        
        0: b'\x80\x00\x00\x00\x00\x00',
        1: b'\x10\x00\x00\x00\x00\x00',
        2: b'\x04\x00\x00\x00\x00\x00',
        3: b'\x00\x00\x04\x00\x00\x00',
        4: b'\x20\x00\x00\x00\x00\x00',
        5: b'\x40\x00\x00\x00\x00\x00',
        6: b'\x01\x00\x00\x00\x00\x00',
        7: b'\x02\x00\x00\x00\x00\x00',
        8: b'\x08\x00\x00\x00\x00\x00',
        9: b'\x00\x01\x00\x00\x00\x00',
        10: b'\x00\x00\x00\x01\x00\x00',
        11: b'\x00\x00\x02\x00\x00\x00',
        12: b'\x00\x08\x00\x00\x00\x00',
        13: b'\x00\x04\x00\x00\x00\x00',
        14: b'\x00\x02\x00\x00\x00\x00',
        15: b'\x00\x00\x00\x02\x00\x00'
        

    }
    
    def __init__(self, addr=0x70, i2c=None):
        self.i2c_addr = addr
        self.i2c = i2c
        self.displaybuffer = bytearray(16)  # 16 bytes for display buffer
        self.keys = bytearray(6)             # 6 bytes for key states
        self.lastkeys = bytearray(6)

    def begin(self):
        """Initialize the device and set it up for operation."""
        self.i2c.writeto(self.i2c_addr, bytearray([0x21]))  # Turn on oscillator
        self.set_brightness(15)  # Max brightness
        self.blink_rate(HT16K33_BLINK_OFF)  # Turn off blinking

    def set_brightness(self, b):
        """Set the brightness of the display."""
        if b > 15:
            b = 15
        self.i2c.writeto(self.i2c_addr, bytearray([0xE0 | b]))

    def blink_rate(self, b):
        """Set the blink rate of the display."""
        if b > 3:
            b = 0  # Turn off if not sure
        self.i2c.writeto(self.i2c_addr, bytearray([0x80 | 0x01 | (b << 1)]))

    def write_display(self):
        """Send the display buffer to the HT16K33 to update the display."""
        self.i2c.writeto(self.i2c_addr, bytearray([0x00]) + self.displaybuffer)

    def clear(self):
        """Clear the display buffer."""
        self.displaybuffer = bytearray(16)  # Clear display buffer

    def is_key_pressed(self, k):
        """Check if a specific key is currently pressed."""
        if k > 15:
            return False
        
        if k < 8:
            return self.keys[0] & (1 << k)
        
        if k < 12:
            return self.keys[1] & (1 << (k - 8))
        
        if k == 12 or k == 13:
            return self.keys[2] & (1 << (k - 11))
        
        if k == 14 or k == 15:
            return self.keys[3] & (1 << (k - 14))
        
        return self.keys[k % 8] & (1 << (k % 8))
        
        # Check the correct key bit based on the mapping
        # print(f'value being checked: {k}, self.keys: {self.keys}, buttonmapping for {k}: {self.BUTTON_MAPPING[k]}')
        # print(self.keys == self.BUTTON_MAPPING[k])
        # return self.keys == self.BUTTON_MAPPING[k]

    def was_key_pressed(self, k):
        """Check if a specific key was pressed in the last read."""
        if k > 15:
            return False
        
        if k < 8:
            return self.lastkeys[0] & (1 << k)
        
        if k < 12:
            return self.lastkeys[1] & (1 << (k - 8))
        
        if k == 12 or k == 13:
            return self.lastkeys[2] & (1 << (k - 11))
        
        if k == 14 or k == 15:
            return self.lastkeys[3] & (1 << (k - 14))
        
        return self.lastkeys[k % 8] & (1 << (k % 8))
        
        # Check the correct key bit based on the mapping
        # return self.lastkeys == self.BUTTON_MAPPING[k]
    
    def read_switches(self):
        """Update the key states from the HT16K33."""
        self.lastkeys[:] = self.keys[:]  # Copy current keys to lastkeys
        self.i2c.writeto(self.i2c_addr, bytearray([0x40]))  # Start reading switches
        self.keys = self.i2c.readfrom(self.i2c_addr, 6)  # Read 6 bytes
        return self.keys != self.lastkeys

    def set_led(self, x):
        """Turn on an LED at position x."""
        if x > 15:
            return
        self.displaybuffer[x >> 4] |= (1 << (x & 0x0F))

    def clr_led(self, x):
        """Turn off an LED at position x."""
        if x > 15:
            return
        self.displaybuffer[x >> 4] &= ~(1 << (x & 0x0F))

    def just_pressed(self, k):
        """Check if a key was just pressed."""
        return self.is_key_pressed(k) and not self.was_key_pressed(k)

    def just_released(self, k):
        """Check if a key was just released."""
        return not self.is_key_pressed(k) and self.was_key_pressed(k)

# Example usage
# if __name__ == "__main__":
#     i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
#     trellis = AdafruitTrellis(i2c=i2c)
#     trellis.begin()

#     while True:
#         if trellis.read_switches():
#             for i in range(16):
#                 if trellis.is_key_pressed(i):
#                     print(f"Key {i} pressed")
#                     trellis.set_led(i)  # Turn on the corresponding LED
#         trellis.write_display()