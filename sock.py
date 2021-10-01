import socket

UDP_IP_ADDRESS = "192.168.0.121"
UDP_PORT_NO = 21324

def update_esp8266(i,r,g,b):

    v = [
    1, # UDP Protocol 1 = WARLS, leave as is
    60, # Timeout in seconds for WLED before returning to normal mode, Use 255 to stay on the UDP data without a timeout until a request is requested via another method.
    i, # LED Index
    r, # Red colour value
    g, # Green colur value
    b  # Blue colour value
    ]
    #v = [1, 5, 0, 255, 0, 0]
    #v = [2, 10, 255, 0, 0, 0, 255, 0, 0, 0, 255]
    Message = bytearray(v)
    
    clientSock = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
    clientSock.sendto (Message, (UDP_IP_ADDRESS, UDP_PORT_NO))
    
update_esp8266(0,255,0,0)