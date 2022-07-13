import rtmidi
import time

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
print(available_ports)

if available_ports:
    midiout.open_port(1)
else:
    midiout.open_virtual_port("My virtual output")

with midiout:
    note_on = [0x90, 33, 112] # channel 1, middle C, velocity 112
    note_off = [0x80, 33, 0]
    midiout.send_message(note_on)
    time.sleep(1)
    midiout.send_message([0XB0, 41, 5])
    time.sleep(1)
    midiout.send_message([0XB0, 41, 127])
    time.sleep(1)
    midiout.send_message([0XB0, 41, 50])
    midiout.send_message(note_off)
    time.sleep(0.1)
    print("sending midi")

del midiout