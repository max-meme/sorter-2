from tkinter.constants import S
import keyboard as kb
from commander import *

def keyb_detect(b, ui, d, v):
    s = 50
    if b == "Up":
        command("moveby " + str(s) + " " + str(0) + " " + str(0), ui, d, v)
    elif b == "Down":
        command("moveby " + str(-s) + " " + str(0) + " " + str(0), ui, d, v)
    elif b == "Left":
        command("moveby " + str(0) + " " + str(-s) + " " + str(0), ui, d, v)
    elif b == "Right":
        command("moveby " + str(0) + " " + str(s) + " " + str(0), ui, d, v)
    elif b == "Next":
        command("moveby " + str(0) + " " + str(0) + " " + str(s), ui, d, v)
    elif b == "Prior":
        command("moveby " + str(0) + " " + str(0) + " " + str(-s), ui, d, v)
    elif b == "Return":
        ui.send()