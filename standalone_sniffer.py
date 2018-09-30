import socket
UDP_IP = '' #listen to any address
UDP_PORT = 6454 #set Artnet port
sock = socket.socket(socket.AF_INET, # Internet
                  socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
while True:
    data, addr = sock.recvfrom(4576)
    if len(data) == 530:
        #print("received message:", data)
        values = [bytes for bytes in data[18:]]
        print(values)
