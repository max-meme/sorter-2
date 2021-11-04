#communicator that converts text commands into things to send over I2C or GPIO

from IO import *
resolution = {"1": (0, 0, 0),"1/2": (1, 0, 0),"1/4": (0, 1, 0),"1/8": (1, 1, 0),"1/16": (0, 0, 1),"1/32": (1, 0, 1)}

def command(m, UI, db):
    m_list = m.split()
    command = m_list[0]
    m_list.pop(0)
    args = m_list
    if command == "":
        return
    elif command == "doof":
        UI.console_addline("> ne du")
    
    elif command == "autohome":
        UI.console_addline("> autohoming")
        UI.setxyz(0, 0, 0)
        sendI2C(db, "")
    
    elif command == "moveto":
        # check if negative
        if int(args[0]) < 0 or int(args[1]) < 0 or int(args[2]) < 0:
            UI.console_addline("Error: cannot move to negative")
            return
        UI.console_addline("> moving to coords")
        UI.setxyz(int(args[0]), int(args[1]), int(args[2]))
        #TODO: make moveto with i2c

    elif command == "setmicro":
        set_microstepping(args[0])

    elif command == "setstepper":
        set_steppers(args[0])
