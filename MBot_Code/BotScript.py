import cyberpi
import time
import usocket
import socket
import network
import math
import json as jsonlib
import _thread

safetyMode = False
acceptCommands = True
autoPilot = False


## Function for second Thread
def safeFunc(active):
    print("Safety Thread Started")
    global acceptCommands
    global autoPilot
    global safetyMode
    while True:
        if safetyMode:  # Safetymode
            distance = cyberpi.ultrasonic2.get(index=1)
            if distance < 10:  # Wall encountered
                acceptCommands = False  # Stop Main thread from recieving Commands
                cyberpi.mbot2.EM_stop(port="all")  # Stop
                cyberpi.audio.play('buzzing')
                cyberpi.mbot2.straight(-10, speed=100)  # Drive Back 10 cm
                cyberpi.mbot2.turn(180, speed=100)  # Turn around
                acceptCommands = True  # Continue Main thread receiving Commands
        if autoPilot:  # ----------DEPRECATED >>> NEEDS TO BE REWRITTEN DUE TO SPECIFICATIONS
            # L2 = cyberpi.quad_rgb_sensor.get_gray('l2', index = 1)
            L1 = cyberpi.quad_rgb_sensor.get_gray('l1', index=1)
            R1 = cyberpi.quad_rgb_sensor.get_gray('r1', index=1)
            # R2 = cyberpi.quad_rgb_sensor.get_gray('r2', index = 1)

            if L1 < 50 and R1 < 50:
                cyberpi.mbot2.drive_power(30, -30)  # straight ahead
                # cyberpi.led.on(255,0,0,id=2)
                # cyberpi.led.on(255,0,0,id=4)
            elif R1 > 50:
                cyberpi.mbot2.drive_power(0, -30)  # turn left
                # cyberpi.led.on(255,0,0,id=2)
            elif L1 > 50:
                cyberpi.mbot2.drive_power(30, 0)  # turn right
                # callable.led.on(255,0,0,id=4)


## Main Function
def main():
    cyberpi.audio.set_vol(1)
    cyberpi.led.on(0, 0, 0xFF)

    global acceptCommands
    global autoPilot
    global safetyMode

    cyberpi.network.config_sta("htljoh-public", "joh12345")

    while True:
        b = cyberpi.network.is_connect()
        if b == False:
            cyberpi.led.on(0xFF, 0, 0)
            time.sleep(1)
        else:
            cyberpi.led.on(0, 0xFF, 0)
            cyberpi.audio.play("ring")
            break

    ip = cyberpi.network.get_ip()  # assigned IP-Adress
    port = 6969  # Communication Port

    cyberpi.console.println(ip)
    time.sleep(5)

    # Socket for Broadcast message using UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ai = socket.getaddrinfo(ip, port)
    addr = ai[0][-1]  # formatted IP-Adress
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.sendto(ip, ("10.10.3.255", 6970))  # Broadcast

    cyberpi.console.println("Waiting for Connection")
    cyberpi.led.on(255, 64, 0)

    # Socket for Communication Server using TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(addr)

    # Start Thread for Safety Mode and Autopilot
    _thread.start_new_thread(safeFunc, [safetyMode])

    # listen for Connections
    server_socket.listen(5)
    while True:
        # Client Connection
        client_sock, client_raddr = server_socket.accept()
        cyberpi.console.clear()
        print("c_socket:", client_sock, "\nc_raddr:", client_raddr)
        print("Client Address:", client_raddr)
        print("Client Socket:", client_sock)
        test = "Connected To: " + str(client_raddr[0])
        cyberpi.console.println(test)
        print("Good to go")
        # Continuously get Commands from Client
        while True:
            data = client_sock.recv(1024)  # Data from Client
            dataframe = data.decode('utf-8').split(';')[1]  # Stacked Command Protection
            command, extra, data = dataframe.split(':')  # Extracted Command Data
            sepData = data.split(',')  # Seperated Data Values
            print(command, ":", extra, ":", data)

            if command == "MOVE" and acceptCommands == True:
                # Code for handling Movement
                speed = int(sepData[0])
                angle = int(sepData[1])
                style = sepData[2]

                if extra == "STOP":  # Stop the Robot
                    print("STOP Commanded")
                    cyberpi.mbot2.EM_stop(port="all")
                    cyberpi.led.on(0xFF, 0x00, 0x00, id=1)
                    cyberpi.led.on(0xFF, 0x00, 0x00, id=5)
                elif extra == "FWST":  # Move Forward in a straight line
                    print(sepData[0])
                    cyberpi.led.off()
                    cyberpi.mbot2.forward(speed)
                elif extra == "BWST":  # Move Backward in a straight line
                    print(sepData[0])
                    cyberpi.led.off()
                    cyberpi.led.on(0xFF, 0xFF, 0xFF, id=2)
                    cyberpi.led.on(0xFF, 0xFF, 0xFF, id=4)
                    cyberpi.mbot2.backward(speed)
                elif extra == "TRLT":  # Turn left on the spot
                    cyberpi.led.off()
                    cyberpi.mbot2.drive_power(-speed, -speed)
                elif extra == "TRRT":  # Turn right on the spot
                    cyberpi.led.off()
                    cyberpi.mbot2.drive_power(speed, speed)
                elif extra == "FWLT":  # Move Forward and turn left,
                    # ratio determined by angle imput [0-90]->[0.0-1.0]
                    # RPM Ratio = factor/1
                    cyberpi.led.off()
                    factor = angle / 90
                    ltdrv = speed * factor
                    cyberpi.mbot2.drive_power(ltdrv, -speed)
                elif extra == "FWRT":  # Move Forward and turn right,
                    # ratio determined by angle imput [0-90]->[0.0-1.0]
                    # RPM Ratio = factor/1
                    cyberpi.led.off()
                    factor = angle / 90
                    rtdrv = speed * factor
                    cyberpi.mbot2.drive_power(speed, -rtdrv)
                elif extra == "BWLT":  # Move Backward and turn left,
                    # ratio determined by angle imput [0-90]->[0.0-1.0]
                    # RPM Ratio = factor/1
                    cyberpi.led.off()
                    cyberpi.led.on(0xFF, 0xFF, 0xFF, id=2)
                    factor = angle / 90
                    ltdrv = speed * factor
                    cyberpi.mbot2.drive_power(-ltdrv, speed)
                elif extra == "BWRT":  # Move Backward and turn right,
                    # ratio determined by angle imput [0-90]->[0.0-1.0]
                    # RPM Ratio = factor/1
                    cyberpi.led.off()
                    cyberpi.led.on(0xFF, 0xFF, 0xFF, id=4)
                    factor = angle / 90
                    rtdrv = speed * factor
                    cyberpi.mbot2.drive_power(-speed, rtdrv)
            elif command == "MISC":
                # Code for miscalanious Commands
                if extra == "LEDS":  # Changing LEDS
                    r = int('0x' + sepData[0], 16)
                    g = int('0x' + sepData[1], 16)
                    b = int('0x' + sepData[2], 16)
                    if sepData[3] == '00':
                        cyberpi.led.on(r, g, b)
                    else:
                        ID = int(sepData[3])
                        cyberpi.led.on(r, g, b, id=ID)
                elif extra == "SAFE":
                    # Toggle Safety Mode
                    if safetyMode == True:
                        safetyMode = False
                    else:
                        safetyMode = True
                    autoPilot = False

                elif extra == "AUTO":
                    # Toggle Autopilot
                    if autoPilot == True:
                        autoPilot = False
                    else:
                        autoPilot = True
                    safetyMode = False

            elif command == "DATA":
                # Code for sending Data back to the client
                dataJson = getSensorData()
                client_sock.send(dataJson)
            elif command == "LINE":
                # Code for sending Line Data to client
                dataJson = getLineData()
                client_sock.send(dataJson)
            elif command == "DISC":
                cyberpi.mbot2.EM_stop(port="all")
                break

        cyberpi.led.off()
        cyberpi.mbot2.EM_stop(port="all")
        cyberpi.console.print("Waiting for Connection")
        cyberpi.led.on(0xFF, 0x40, 0x00)
        client_sock.close()


## Get Data from Sensors and return formatted JSON
def getSensorData():
    light = cyberpi.get_brightness()  # brightness
    volume = cyberpi.get_loudness()  # audio volume
    pitch = cyberpi.get_pitch()  # pitch ofset from initial position
    roll = cyberpi.get_roll()  # roll ofset from initial position
    yaw = cyberpi.get_yaw()  # yaw ofset from initial position
    distance = cyberpi.ultrasonic2.get(index=1)  # distance from ultrasonic
    battery = cyberpi.get_battery  # battery percentage
    gyrox = str(cyberpi.get_gyro("x"))  # pitch acceleration
    gyroy = str(cyberpi.get_gyro("y"))  # roll acceleration
    gyroz = str(cyberpi.get_gyro("z"))  # yaw acceleration
    accy = str(cyberpi.get_acc("y"))  # forward acceleration
    RGBSensorData = cyberpi.quad_rgb_sensor.get_line_sta(index=1)
    LineS = '{0:04b}'.format(RGBSensorData)
    L2 = LineS[0]  # outer left Sensor
    L1 = LineS[1]  # inner left Sensor
    R1 = LineS[2]  # inner right Sensor
    R2 = LineS[3]  # outer right Sensor

    # JSON string
    json_string = jsonlib.dumps(
        {'light': light, 'battery': battery, 'volume': volume, 'gyrox': gyrox, 'gyroy': gyroy, 'gyroz': gyroz,
         'pitch': pitch, 'roll': roll, 'yaw': yaw, 'accy': accy, 'distance': distance, 'L1': L1, 'L2': L2, 'R1': R1,
         'R2': R2})
    json_string = json_string + "\n"
    return json_string


def getLineData():
    RGBSensorData = cyberpi.quad_rgb_sensor.get_line_sta(index=1)
    LineS = '{0:04b}'.format(RGBSensorData)
    L2 = LineS[0]  # outer left Sensor
    L1 = LineS[1]  # inner left Sensor
    R1 = LineS[2]  # inner right Sensor
    R2 = LineS[3]  # outer right Sensor

    # JSON string
    json_string = jsonlib.dumps({'L2': L2, 'L1': L1, 'R1': R1, 'R2': R2})
    json_string = json_string + "\n"
    return json_string


## Smooth acceleration
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


### Main
try:
    main()
except BaseException as ex:  # Catch Error
    cyberpi.led.off()
    print("ERROR:", ex)
    cyberpi.console.println("Error")
    cyberpi.console.print(ex)
    cyberpi.mbot2.EM_stop(port="all")

