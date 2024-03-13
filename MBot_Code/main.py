import socket

s = socket.socket()

# verbindung definieren
port = 6969

ip = input("Enter IP Address: ")
# verbindung zum server
s.connect((ip, port))

#s.send(b'MISC:LEDS:FF,00,FF,01')
#s.send(b'MOVE:STOP:000,000,RS')
#s.send(b'MOVE:FWST:100,000,RS')
#s.send(b'MOVE:TRLT:100,045,RS')
# s.send(b'MOVE:FWLT:100,045,RS')
s.send(b'MOVE:BWST:100,000,RS')



s.close()
