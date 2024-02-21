import socket

s = socket.socket()

# verbindung definieren
port = 1234

ip = input("Enter IP Address: ")
# verbindung zum server
s.connect((ip, port))

s.send(b'Hello')

#packet empfangen vom server
print(s.recv(4096))

s.close()