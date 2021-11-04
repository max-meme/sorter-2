#IO handler

import RPi.GPIO as GPIO
import smbus
bus = smbus.SMBus(1)

#address setup in the Arduino Program
address = 0x8

def writeData(value):
    byteValue = StringToBytes(value)    
    bus.write_i2c_block_data(address,0x00,byteValue) #first byte is 0=command byte.. just is.
    return -1


def StringToBytes(val):
        retVal = []
        for c in val:
                retVal.append(ord(c))
        return retVal

def sendI2C(db, m):
    db.log("sending: " + m)
    writeData(m)

def readIO(db):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

def set_microstepping(res):
        resolutions = {"1": (0, 0, 0),"1/2": (1, 0, 0),"1/4": (0, 1, 0),"1/8": (1, 1, 0),"1/16": (0, 0, 1),"1/32": (1, 0, 1)}
        micros = (23, 24, 25)
        GPIO.output(micros, resolutions[res])

def set_steppers(inp):
        if(inp == True):
                GPIO.output(14, 1)
        else:
                GPIO.output(14, 0)
