import socket

s = socket.socket()

# verbindung definieren
port = 6969

ip = input("Enter IP Address: ")
# verbindung zum server
s.connect((ip, port))

s.send(b'MISC:LEDS:FF,00,FF,01')

s.close()
