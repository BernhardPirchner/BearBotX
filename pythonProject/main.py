import socket

s = socket.socket()

# verbindung definieren
port = 6969

ip = input("Enter IP Address: ")
# verbindung zum server
s.connect((ip, port))

s.send(b'Hello')

#packet empfangen vom server
for i in range(0,10):
    print(s.recv(4096))

s.send(b"STOP")

s.close()