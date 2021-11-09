#communicator that converts text commands into things to send over I2C or GPIO

from tkinter.constants import Y
from IO import *

def command(m, UI, d, v):
    m_list = m.split()
    c = m_list[0]
    m_list.pop(0)
    args = m_list
    if c == "":
        return
    elif c == "doof":
        UI.console_addline("> ne du")
    
    elif c == "autohome":
        UI.console_addline("> autohoming")
        v.x = 0
        v.y = 0
        v.z = 0
        UI.updatexyz()
        sendI2C(d, "ah")
    
    elif c == "moveto":
        x_in = int(args[0])
        y_in = int(args[1])
        z_in = int(args[2])

        # check if negative
        if x_in < 0 or y_in < 0 or z_in < 0:
            UI.console_addline("> Error: cannot move to negative")
            return
        
        # check if higher then max
        if x_in > v.max_x or y_in > v.max_y or z_in > v.max_z:
            UI.console_addline("> Error: limit reached")
            return
        UI.console_addline("> moving to x:" + args[0] + " y:" + args[1] + " z:" + args[2])

        v.x = x_in
        v.y = y_in
        v.z = z_in
        UI.updatexyz()

        sendI2C(d, "moveto-" + args[0] + "-" + args[1] + "-" + args[2])

    elif c == "setmicro":
        UI.console_addline("> setting microstepping to " + args[0])
        v.ms = int(args[0])
        set_microstepping(args[0])

    elif c == "setsteppers":
        UI.console_addline("> set steppers to " + args[0])
        set_steppers(args[0])
    
    elif c == "moveby":
        x_in = int(args[0])
        y_in = int(args[1])
        z_in = int(args[2])

        command("moveto " + str(v.x + x_in) + " " + str(v.y + y_in) + " " + str(v.z + z_in), UI, d, v)