import time
from BLE_CEEO import Yell

NoteOn = 0x90  # For reference, not used here
ControlChange = 0xB0  # MIDI Control Change message
StopNotes = 123
SetInstrument = 0xC0
Reset = 0xFF

# Define your payload sender
p = Yell('kmart', verbose=True, type='midi')
p.connect_up()

channel = 0  # MIDI channel 0
scene_trigger_cc = 0  # Change this to map to the correct control in GarageBand
trigger_value = 127  # Trigger the scene

# Create the timestamp
timestamp_ms = time.ticks_ms()
tsM = (timestamp_ms >> 7 & 0b111111) | 0x80
tsL = 0x80 | (timestamp_ms & 0b1111111)

# Create the MIDI message: Control Change on channel 0
cmd = ControlChange | (channel & 0x0F)  # Combine channel with CC message

# Payload for triggering a Live Loop
payload = bytes([tsM, tsL, cmd, scene_trigger_cc, trigger_value])

# Send the trigger 3 times with a pause
for i in range(128):
    print(f"Sending trigger {i + 1}")
    p.send(payload)
    scene_trigger_cc = scene_trigger_cc + 1
    time.sleep(2)

# Clean up
p.disconnect()

