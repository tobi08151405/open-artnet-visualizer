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
                    obj.data.energy = watt * 10 * (values[i] / 255)
                    print(obj, values[i], obj.data.energy)
                except KeyError:
                    pass