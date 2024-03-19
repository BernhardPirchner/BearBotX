import socket
import time

s = socket.socket()

# verbindung definieren
ip = input("Enter IP Address: ")
port = 6969

# verbindung zum server
s.connect((ip, port))

s.send(b'MOVE:FWST:100,000,RS')  # Forward
time.sleep(0.2)

s.send(b'MOVE:TRLT:100,045,RS')  # Turn left on the spot
time.sleep(0.2)

s.send(b'MOVE:FWLT:100,000,RS')  # Forward Left, 000 on second part means turn on outer wheel
time.sleep(0.2)

s.send(b'MOVE:BWST:100,000,RS')  # Backwards
time.sleep(0.2)

s.send(b'MOVE:STOP:000,000,00')  # Stop
time.sleep(0.2)

s.send(b'MISC:LEDS:FF,00,FF,03')
time.sleep(10)
s.send(b'DISC:DISC:000,000,00')

s.close()
