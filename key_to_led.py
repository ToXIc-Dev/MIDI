#!/usr/bin/env python
# This program gets the key from a MIDI device and send it to a WLED LED device to light up that specific LED
# It is custom for my needs but you should be able to edit it to yours
from __future__ import print_function
import sys
import mido
import socket
import random

UDP_IP_ADDRESS = "192.168.0.121"
UDP_PORT_NO = 21324

#if len(sys.argv) >= 1:
#    portname = sys.argv[0]
#else:
#    portname = None  # Use default port

def _map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def accept_notes(port):
    """Only let note_on and note_off messages through."""
    for message in port:
        if message.type in ('note_on', 'note_off'):
            yield message

def update_esp8266(i,r,g,b):

    v = [
    1, # UDP Protocol 1 = WARLS, leave as is
    10, # Timeout in secs for WLED before returning to normal mode, Use 255 to stay on the UDP data without a timeout until a request is requested via another method.
    i, # LED Index
    r, # Red colour value
    g, # Green colur value
    b  # Blue colour value
    ]
    Message = bytearray(v)
    
    clientSock = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
    clientSock.sendto (Message, (UDP_IP_ADDRESS, UDP_PORT_NO))
    # 36 - 96 on 61 key kb
try:
    #with mido.open_input(portname) as port:
    with mido.open_input('loopMIDI Port 2') as port:
        print('Using {}'.format(port))
        print('Waiting for messages...')
        for message in accept_notes(port):
            print('Received {}'.format(message))
            #print(message.note)
            #print(message.velocity)
            y = _map(message.note, 36, 96, 0, 60) # This is custom for my MIDI keyboard, I have a 61 key keyboard with a 58 LED strip, so the last 3 keys dont light up
            print('LED Index {}'.format(y))
            if "note_on" in format(message):
                #update_esp8266(y,random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)) # Random colour
                update_esp8266(y,255,0,0) # Red
            elif "note_off" in format(message):
                update_esp8266(y,0,0,0)
            sys.stdout.flush()
except KeyboardInterrupt:
    pass
