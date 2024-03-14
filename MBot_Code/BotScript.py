import cyberpi
import time
import usocket
import socket
import network
import math

CONTENT = b"""\
Data: %d
"""


def main():
    cyberpi.audio.add_vol(1)
    cyberpi.led.on(0, 0, 0xFF)

    cyberpi.network.config_sta("htljoh-public", "joh12345")

    while True:
        b = cyberpi.network.is_connect()
        if b == False:
            cyberpi.led.on(255, 0, 0)
            time.sleep(1)
        else:
            cyberpi.led.on(0, 0xFF, 0)
            cyberpi.audio.play("ring")
            break

    ip = cyberpi.network.get_ip()
    port = 6969

    cyberpi.console.println(ip)
    time.sleep(5)

    cyberpi.console.clear()
    cyberpi.led.off()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ai = socket.getaddrinfo(ip, port)

    addr = ai[0][-1]

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind(addr)
    s.sendto(ip, ("10.10.3.255", 6969))

    cyberpi.console.println("Waiting for Connections")
    cyberpi.led.on(255, 31, 0)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind(addr)

    server_socket.listen(5)
    while True:

        client_sock, client_raddr = server_socket.accept()
        print("c_socket:", client_sock, "\nc_raddr:", client_raddr)
        print("Client Address:", client_raddr)
        print("Client Socket:", client_sock)
        cyberpi.console.println("Connected to:", client_raddr)

        while True:
            # Continuously get Commands from Client
            # cyberpi.led.on(0xFF,0xFF,0xFF)
            data = client_sock.recv(1024)
            dataframe = data.decode('utf-8')
            print("###INCOMING COMMAND###")
            print("Dataframe", dataframe)
            command, extra, data = dataframe.split(':')
            print(command, ":", extra, ":", data)
            sepData = data.split(',')
            print("Data", sepData)
            cyberpi.led.off()

            if command == "MOVE":
                # Code for handling Movement
                speed = int(sepData[0])
                angle = int(sepData[1])
                style = sepData[2]

                print("Recieved Movement Command")
                if extra == "STOP":  # Stop the Robot
                    print("STOP Commanded")
                    cyberpi.mbot2.EM_stop(port="all")
                    print("Test")
                    cyberpi.led.on(0xFF, 0x00, 0x00, id=1)
                    cyberpi.led.on(0xFF, 0x00, 0x00, id=5)
                elif extra == "FWST":  # Move Forward in a straight line
                    print("Forward Commanded")
                    print(sepData[0])
                    cyberpi.mbot2.forward(speed)
                elif extra == "BWST":  # Move Backward in a straight line
                    print("Backward Commanded")
                    print(sepData[0])
                    cyberpi.mbot2.backward(speed)
                elif extra == "TRLT":  # Turn left on the spot
                    print("Turn Left Commanded")
                    cyberpi.mbot2.turn(-angle, speed)
                elif extra == "FWLT":  # Move Forward and turn left,
                    # ratio determined by angle imput [0-90]->[0.0-1.0]
                    # RPM Ratio = factor/1
                    print("Turn Forward Left Commanded")
                    factor = angle / 90
                    ltdrv = speed * factor
                    cyberpi.mbot2.drive_power(ltdrv, -speed)

            elif command == "MISC":
                # Code for miscalanious Commands
                if extra == "LEDS":
                    red = int('0x' + sepData[0], 16)
                    green = int('0x' + sepData[1], 16)
                    blue = int('0x' + sepData[2], 16)

            elif command == "DISC":
                cyberpi.mbot2.EM_stop(port="all")
                break

        cyberpi.led.off()
        cyberpi.mbot2.EM_stop(port="all")
        cyberpi.console.clear()
        client_sock.close()
        break


main()


def moveFW(time):
    for i in range(20):
        t = i / 10.0
        base = 4.0
        limit = 100.0
        value = 1 + (limit - 1) * (base ** t - 1) / (base - 1)

    if value >= limit:
        value = limit

    cyberpi.console.println(value)
    cyberpi.console.clear()

