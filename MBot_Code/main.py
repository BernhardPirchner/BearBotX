import socket
import time

s = socket.socket()

# verbindung definieren
ip = input("Enter IP Address: ")
port = 6969

# verbindung zum server
s.connect((ip, port))
time.sleep(2)
s.send(b';DATA:0:0')
time.sleep(2)
text = s.recv(1024)
print(text)
# s.send(b';MOVE:FWST:100,000,RS')  # Forward
# time.sleep(0.2)
#
# s.send(b';MOVE:TRLT:100,000,RS')  # Turn left
# time.sleep(0.2)
#
# s.send(b';MOVE:STOP:000,000,00')  # Stop
# time.sleep(0.2)
#
# s.send(b';MOVE:FWLT:100,060,RS')  # Forward Left
# time.sleep(0.2)
#
# s.send(b';MOVE:BWST:100,000,RS')  # Backwards
# time.sleep(0.2)
#
# s.send(b';MOVE:STOP:000,000,00')  # Stop
# time.sleep(0.2)
#
# s.send(b';MOVE:STOP:000,000,00')  # Stop
# time.sleep(0.2)
#
# s.send(b';MISC:LEDS:FF,00,FF,01')
# time.sleep(1)
# s.send(b';MISC:LEDS:FF,00,FF,02')
# time.sleep(1)
# s.send(b';MISC:LEDS:FF,00,FF,03')
# time.sleep(1)
# s.send(b';MISC:LEDS:FF,00,FF,04')
# time.sleep(1)
# s.send(b';MISC:LEDS:FF,00,FF,05')
# time.sleep(1)
#
# s.send(b';MISC:LEDS:FF,FF,FF,00')
# time.sleep(2)
#

s.send(b';DISC:DISC:000,000,00')

s.close()
