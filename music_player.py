import argparse
import asyncio
import math
import numpy as np
import rtmidi
import time
from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import AsyncIOOSCUDPServer

NOTE_ON = 0x90
NOTE_OFF = 0x80
CC = 0XB0

# note numbers
NOTE_C1 = 33
NOTE_CS1 = 35
NOTE_D1 = 37
NOTE_DS1 = 39
NOTE_E1 = 41
NOTE_F1 = 44
NOTE_FS1 = 46
NOTE_G1 = 49
NOTE_GS1 = 52
NOTE_A1 = 55
NOTE_AS1 = 58
NOTE_B1 = 62

# CC messages
SLIDE_TIME = 5  # slide from one note to another
EXPRESSION = 11
OCTAVE = 40
LFO_RATE = 41
LFO_INT = 42
VCO_PITCH_1 = 43
VCO_PITCH_2 = 44
VCO_PITCH_3 = 45
EG_ATTACK = 46
EQ_DEC_REL = 47
CUTOFF_EG_INT = 48
GATE_TIME = 49

# array of shapes and arc lengths
shapes = [['rectangle', 133], ['rectangle', 180], ['circle', 200], ['triangle', 144], ['circle', 12.45]]
rgb = [10, 200, 500]

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
print(available_ports)

if available_ports:
    # midiout.open_port(1)
    midiout.open_port(0)
else:
    midiout.open_virtual_port("My virtual output")


def play_note(note, length):
    midiout.send_message([NOTE_ON, note, 127])
    time.sleep(length)
    midiout.send_message([NOTE_OFF, note, 0])


def calc_time(arc_length):
    return np.interp(arc_length, [120, 1000], [0.1, 0.4])


def replace_shapes(*newshapes):
    these_shapes = []
    i = 0
    for shape in newshapes:
        if i == 0:
            i = 1
            continue

        these_shapes.append(shape)

    global shapes
    shapes = these_shapes
    print('new shapes' + str(shapes))


def replace_rgb(*rgbvals):
    temp_rgb = []

    i = 0
    for val in rgbvals:
        if i == 0:
            i = 1
            continue

        temp_rgb.append(val)

    global rgb
    rgb = temp_rgb
    print("new rgb vals: " + str(rgb))


async def play_shapes():
    with midiout:
        while True:
            global shapes
            for shape in shapes:
                print('playing shape')
                name = shape[0]
                arc = shape[1]
                print(name)
                print(arc)

                # convert rgb values to CC messages
                global rgb
                # print(str(rgb))

                midiout.send_message([CC, EXPRESSION, np.interp(rgb[0], [0, 8000], [0, 127])])
                midiout.send_message([CC, LFO_RATE, np.interp(rgb[1], [0, 8000], [0, 127])])
                midiout.send_message([CC, LFO_INT, np.interp(rgb[2], [0, 8000], [0, 127])])

                if name == 'circle':
                    midiout.send_message([CC, SLIDE_TIME, 127])
                    play_note(NOTE_C1, calc_time(arc))
                    play_note(NOTE_D1, calc_time(arc))
                    play_note(NOTE_E1, calc_time(arc))
                    play_note(NOTE_F1, calc_time(arc))
                    play_note(NOTE_G1, calc_time(arc))
                    play_note(NOTE_A1, calc_time(arc))
                    play_note(NOTE_B1, calc_time(arc))
                    play_note(NOTE_A1, calc_time(arc))
                    play_note(NOTE_G1, calc_time(arc))
                    play_note(NOTE_F1, calc_time(arc))
                    play_note(NOTE_E1, calc_time(arc))
                    play_note(NOTE_D1, calc_time(arc))
                    play_note(NOTE_C1, calc_time(arc))
                elif name == 'rectangle':
                    midiout.send_message([CC, SLIDE_TIME, 0])
                    play_note(NOTE_C1, calc_time(arc))
                    play_note(NOTE_E1, calc_time(arc))
                    play_note(NOTE_G1, calc_time(arc))
                    play_note(NOTE_C1, calc_time(arc))
                elif name == 'triangle':
                    midiout.send_message([CC, SLIDE_TIME, 75])
                    play_note(NOTE_C1, calc_time(arc))
                    play_note(NOTE_G1, calc_time(arc))
                    play_note(NOTE_C1, calc_time(arc))
                else:
                    play_note(NOTE_C1, 0.5)

            await asyncio.sleep(0)


async def init_main():
    # Create server for listening to incoming shapes and rgb values
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="The ip to listen on")
    parser.add_argument("--port", type=int, default=5005, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = Dispatcher()
    dispatcher.map("/shapes", replace_shapes)
    dispatcher.map("/rgb", replace_rgb)
    server = AsyncIOOSCUDPServer((args.ip, args.port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving

    await play_shapes()  # Enter main loop of program

    transport.close()  # Clean up serve endpoint


asyncio.run(init_main())
