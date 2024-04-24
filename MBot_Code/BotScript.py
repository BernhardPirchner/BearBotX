import cyberpi
import time
import usocket
import socket
import network
import math
import json as jsonlib
import _thread

safetyMode = True
acceptCommands = True
autoPilot = False


def safeFunc(active):  # Function for Safe Mode Thread
    # print("Savety Thread Started")
    global acceptCommands
    global autoPilot
    global safetyMode
    while True:
        # print("Safe:",safetyMode,",Auto:",autoPilot)
        if safetyMode:
            distance = cyberpi.ultrasonic2.get(index=1)
            if distance < 10:
                print("<<<Wall Encountered>>>")
                acceptCommands = False
                cyberpi.mbot2.EM_stop(port="all")
                cyberpi.audio.play('buzzing')
                cyberpi.mbot2.straight(-10, speed=100)
                cyberpi.mbot2.turn(180, speed=100)
                acceptCommands = True
        if autoPilot:
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
    s.sendto(ip, ("10.10.3.255", 6970))

    cyberpi.console.println("Waiting for Connections")
    cyberpi.led.on(255, 31, 0)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind(addr)

    _thread.start_new_thread(safeFunc, [safetyMode])

    server_socket.listen(5)
    while True:

        client_sock, client_raddr = server_socket.accept()
        print("c_socket:", client_sock, "\nc_raddr:", client_raddr)
        print("Client Address:", client_raddr)
        print("Client Socket:", client_sock)
        cyberpi.console.println("Connected to:", client_raddr)

        while True:
            # Continuously get Commands from Client

            data = client_sock.recv(1024)
            dataframe = data.decode('utf-8').split(';')[1]
            print("###INCOMING COMMAND###")
            # print("Dataframe", dataframe)
            command, extra, data = dataframe.split(':')
            print(command, ":", extra, ":", data)
            sepData = data.split(',')
            # print("Data", sepData)
            # cyberpi.led.off()
            # print(acceptCommands)

            if command == "MOVE" and acceptCommands == True:
                # Code for handling Movement
                speed = int(sepData[0])
                angle = int(sepData[1])
                style = sepData[2]

                # print("Recieved Movement Command")
                if extra == "STOP":  # Stop the Robot
                    print("STOP Commanded")
                    cyberpi.mbot2.EM_stop(port="all")
                    cyberpi.led.on(0xFF, 0x00, 0x00, id=1)
                    cyberpi.led.on(0xFF, 0x00, 0x00, id=5)
                elif extra == "FWST":  # Move Forward in a straight line
                    print("Forward Commanded")
                    print(sepData[0])
                    cyberpi.led.off()
                    cyberpi.mbot2.forward(speed)
                elif extra == "BWST":  # Move Backward in a straight line
                    print("Backward Commanded")
                    print(sepData[0])
                    cyberpi.led.off()
                    cyberpi.led.on(0xFF, 0xFF, 0xFF, id=2)
                    cyberpi.led.on(0xFF, 0xFF, 0xFF, id=4)
                    cyberpi.mbot2.backward(speed)
                elif extra == "TRLT":  # Turn left on the spot
                    print("Turn Left Commanded")
                    cyberpi.led.off()
                    cyberpi.mbot2.drive_power(-speed, -speed)
                elif extra == "TRRT":  # Turn right on the spot
                    print("Turn Right Commanded")
                    cyberpi.led.off()
                    cyberpi.mbot2.drive_power(speed, speed)
                elif extra == "FWLT":  # Move Forward and turn left,
                    # ratio determined by angle imput [0-90]->[0.0-1.0]
                    # RPM Ratio = factor/1
                    print("Turn Forward Left Commanded")
                    cyberpi.led.off()
                    factor = angle / 90
                    ltdrv = speed * factor
                    cyberpi.mbot2.drive_power(ltdrv, -speed)
                elif extra == "FWRT":  # Move Forward and turn right,
                    # ratio determined by angle imput [0-90]->[0.0-1.0]
                    # RPM Ratio = factor/1
                    print("Turn Forward Right Commanded")
                    cyberpi.led.off()
                    factor = angle / 90
                    rtdrv = speed * factor
                    cyberpi.mbot2.drive_power(speed, -rtdrv)
                elif extra == "BWLT":  # Move Backward and turn left,
                    # ratio determined by angle imput [0-90]->[0.0-1.0]
                    # RPM Ratio = factor/1
                    print("Turn Backward Left Commanded")
                    cyberpi.led.off()
                    cyberpi.led.on(0xFF, 0xFF, 0xFF, id=2)
                    factor = angle / 90
                    ltdrv = speed * factor
                    cyberpi.mbot2.drive_power(-ltdrv, speed)
                elif extra == "BWRT":  # Move Backward and turn right,
                    # ratio determined by angle imput [0-90]->[0.0-1.0]
                    # RPM Ratio = factor/1
                    print("Turn Backward Right Commanded")
                    cyberpi.led.off()
                    cyberpi.led.on(0xFF, 0xFF, 0xFF, id=4)
                    factor = angle / 90
                    rtdrv = speed * factor
                    cyberpi.mbot2.drive_power(-speed, rtdrv)

            elif command == "MISC":
                # Code for miscalanious Commands
                if extra == "LEDS":
                    # Changing LEDS
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
                    # cyberpi.console.print("Toggled Safetymode")
                    print("Safety toggle")
                    if safetyMode == True:
                        safetyMode = False
                    else:
                        safetyMode = True

                    autoPilot = False
                    print(safetyMode)
                    # cyberpi.console.clear()
                    # cyberpi.console.print("Safe:"+str(safetyMode)+",Pilot:"+str(autoPilot))

                elif extra == "AUTO":
                    # Toggle Autopilot
                    cyberpi.console.print("Toggled Autopilot")
                    print("Autopilot toggle")
                    autoPilot = True
                    print(autoPilot)
                    # cyberpi.console.clear()
                    # cyberpi.console.print("Safe:"+str(safetyMode)+",Pilot:"+str(autoPilot))

            elif command == "DATA":
                # Code for sending Data back to the client
                dataJson = getSensorData()
                # print(dataJson)
                client_sock.send(dataJson)
                print("Data sent to client")

            elif command == "DISC":
                cyberpi.mbot2.EM_stop(port="all")
                break

        cyberpi.led.off()
        cyberpi.mbot2.EM_stop(port="all")
        cyberpi.console.clear()
        client_sock.close()


def getSensorData():
    light = cyberpi.get_brightness()
    volume = cyberpi.get_loudness()
    pitch = cyberpi.get_pitch()
    roll = cyberpi.get_roll()
    yaw = cyberpi.get_yaw()
    distance = cyberpi.ultrasonic2.get(index=1)
    battery = cyberpi.get_battery
    gyrox = str(cyberpi.get_gyro("x"))
    gyroy = str(cyberpi.get_gyro("y"))
    gyroz = str(cyberpi.get_gyro("z"))
    RGBSensorData = cyberpi.quad_rgb_sensor.get_line_sta(index=1)
    LineS = '{0:04b}'.format(RGBSensorData)
    # print(LineS)
    L2 = LineS[0]
    L1 = LineS[1]
    R1 = LineS[2]
    R2 = LineS[3]

    json_string = jsonlib.dumps(
        {'light': light, 'battery': battery, 'volume': volume, 'gyrox': gyrox, 'gyroy': gyroy, 'gyroz': gyroz,
         'pitch': pitch, 'roll': roll, 'yaw': yaw, 'distance': distance, 'L1': L1, 'L2': L2, 'R1': R1, 'R2': R2})
    json_string = json_string + "\n"
    return json_string


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


try:
    main()
except BaseException as ex:
    cyberpi.led.off()
    print("ERROR:", ex)
    cyberpi.console.print("Error: ", ex)
    cyberpi.mbot2.EM_stop(port="all")
    # cyberpi.console.clear()

