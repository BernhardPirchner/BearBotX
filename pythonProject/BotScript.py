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
        cyberpi.console.clear()
        client_sock, client_raddr = server_socket.accept()
        print("c_socket:", client_sock, "\nc_raddr:", client_raddr)
        print("Client Address:", client_raddr)
        print("Client Socket:", client_sock)

        cyberpi.led.on(0xFF, 0xFF, 0xFF)
        data = client_sock.recv(1024)
        # print(data.decode('utf-8'))
        dataframe = data.decode('utf-8')
        command, extra, data = dataframe.split(':')
        sepData = data.split(',')
        print("Data", sepData)
        cyberpi.led.off()
        red = '0x' + sepData[0]
        green = '0x' + sepData[1]
        blue = '0x' + sepData[2]
        print(red, green, blue, sep=':')
        cyberpi.led_on(red.decode('utf-8'), green.decode('utf-8'), blue.decode('utf-8'))
        # cyberpi.console.println("Data from Client:",data.decode('utf-8'))

        if data == b'STOP':
            break

        # for i in range(0,10):
        #     distance = cyberpi.ultrasonic2.get(index=1)
        #     client_sock.send(CONTENT % distance)
        #     time.sleep(0.05)
        cyberpi.led.on(0x00, 0xFF, 0xFF)
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

