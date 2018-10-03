import bpy
import socket

watt = 100
UDP_IP = '' #listen to any address
UDP_PORT = 6454 #set Artnet port
sock = socket.socket(socket.AF_INET, # Internet
                  socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
for x in range(10):
    data, addr = sock.recvfrom(4576)
    if len(data) == 530:
        #print("received message:", data)
        values = [bytes for bytes in data[18:]]
        #print(values)
        for i in range(len(values)):
            try:
                obj = bpy.data.objects["%03d" % (i+1)].children[0]
                """REPLACE THIS LINE"""
                print(obj, values[i], obj.data.energy)
            except KeyError:
                pass

"""
WITH EITHER:

For Dimmer lamps
obj.data.energy = watt * 10 * (values[i] / 255)

For 3-channel LEDs
obj.data.energy = watt * 10
obj.data.color = ((values[i] / 255),(values[i+1] / 255),(values[i+2] / 255))

For RGB-Dimmer LEDs
obj.data.energy = watt * 10 * (values[i+3] / 255)
obj.data.color = ((values[i] / 255),(values[i+1] / 255),(values[i+2] / 255))

For Dimmer-RGB LEDs
obj.data.energy = watt * 10 * (values[i] / 255)
obj.data.color = ((values[i+1] / 255),(values[i+2] / 255),(values[i+3] / 255))
"""