#communicator that converts text commands into things to send over I2C or GPIO

from IO import *

def command(m, UI, db, v):
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
        sendI2C(db, "ah")
    
    elif command == "moveto":
        # check if negative
        if int(args[0]) < 0 or int(args[1]) < 0 or int(args[2]) < 0:
            UI.console_addline("Error: cannot move to negative")
            return
        UI.console_addline("> moving to coords")
        UI.setxyz(int(args[0]), int(args[1]), int(args[2]))
        #TODO: make moveto with i2c

    elif command == "setmicro":
        UI.console_addline("> setting microstepping to " + args[0])
        set_microstepping(args[0])

    elif command == "setsteppers":
        UI.console_addline("> set steppers to " + args[0])
        v.ms = args[0]
        set_steppers(args[0])
    
    elif command == "moveby":
        x_in = int(args[0])
        y_in = int(args[1])
        z_in = int(args[2])

        x_dif = abs(v.x - x_in)
        y_dif = abs(v.y - y_in)
        z_dif = abs(v.z - z_in)

        v.x = v.x + x_in
        v.y = v.y + y_in
        v.z = v.z + z_in

        UI.setxyz(v.x, v.y, v.z)

        
