import serial  
import io
import time


ser = serial.Serial("COM3", 115200)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser)) #initializes sio as a text stream wrapper around a read-write pair using ser


def getResponse():
    while ser.in_waiting == 0: #while loop that continues looping until there is data available for reading from the (ser)
        pass #makes the loop go untill there is data available
    t = ""
    for c in ser.read_all(): #returns all available bytes from the receive buffer.
        t += chr(c) #each byte "c" is converted to a character using chr(c) and then appended to the string "t"
    return t


def sendCommand(command):
    sio.write(command + "\r") #
    sio.flush() #flush makes sure the data is sent immedietly and through the io ser connection
    if "ok" in getResponse(): #checks if the laser respons with ok and prints 1 or 0 accordingly
        return 1
    else:
        return 0


def laserHome():
    sendCommand("G01 X0 Y0 F1000")


def laserInitialSetup():
    sendCommand("G90 G21 G49 G17 F1000")
    #G90 - abseloute positioning mode - coordinates used are abseloute positions from the refrence point (0, 0)
    #G21 - sets the units to milimeters
    #G49 - ensures that the machine does not apply any additional length offset corrections.
    #F feed rate of "x" units per minute - speed)


def laserOn():
    sendCommand("M03 S10")
    #M03 - Turn on laser
    #S10 - laser "power"


def laserOff():
    sendCommand("M05")  # laser off


def laserMove(x,y):
    command = f"G01 X{x} Y{y} F1000"
    sendCommand(command)
    #G01 - Linear movement - fastest route.
