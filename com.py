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