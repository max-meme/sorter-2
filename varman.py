# Responsible for managing all variables
class Varman:
    def __init__(this, x_max, y_max, z_max):
        this.x = 0
        this.y = 0
        this.z = 0

        this.max_x = x_max
        this.max_y = y_max
        this.max_z = z_max

        this.stepper_status = False
        this.light_status = False

        this.ms = 1
