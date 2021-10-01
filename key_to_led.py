#!/usr/bin/env python
from __future__ import print_function
import sys
import mido
import socket
import random

UDP_IP_ADDRESS = "192.168.0.121"
UDP_PORT_NO = 21324

if len(sys.argv) > 1:
    portname = sys.argv[1]
else:
    portname = None  # Use default port

def _map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
    
def update_esp8266(i,r,g,b):

    v = [
    1, # UDP Protocol 1 = WARLS, leave as is
    10, # Timeout in seconds for WLED before returning to normal mode, Use 255 to stay on the UDP data without a timeout until a request is requested via another method.
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
    with mido.open_input(portname) as port:
        print('Using {}'.format(port))
        print('Waiting for messages...')
        for message in port:
            print('Received {}'.format(message))
            #print(message.note)
            #print(message.velocity)
            y = _map(message.note, 36, 96, 0, 60)
            if "note_on" in format(message):
                update_esp8266(y,random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)) # Random colour
                #update_esp8266(y,255,0,0) # Red
            elif "note_off" in format(message):
                update_esp8266(y,0,0,0)
            sys.stdout.flush()
except KeyboardInterrupt:
    pass