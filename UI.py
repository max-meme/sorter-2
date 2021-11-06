import tkinter as tk
from commander import *
from datetime import datetime

class UI:
    def __init__(this, v, d, window_name, testing):
        root = tk.Tk()

        this.d = d
        this.v = v

        this.testing = testing
        this.window_name = window_name
        this.x_Label_text = tk.StringVar(value = "x: 0")
        this.y_Label_text = tk.StringVar(value = "y: 0")
        this.z_Label_text = tk.StringVar(value = "z: 0")
        this.stepper_Label_text = tk.StringVar(value = "OFF")
        this.light_Label_text = tk.StringVar(value = "OFF")
        this.Lb = tk.Listbox()
        this.create_UI(root)
    
    def console_addline(this, text):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        this.Lb.insert(0, "[" + current_time + "]: " + text)

    def send(this):
        text = this.inp.get()
        this.inp.delete(0, tk.END)
        this.console_addline(text)
        command(text, this, this.d, this.v)
        
    def create_UI(this, root):
        root.title(this.window_name)
        root.geometry("800x700")

        #arrow buttons
        arrow_Frame = tk.Frame(root, height = 200, width = 200)
        arrow_Frame.place(anchor="w", relx=0, rely=0.5)

        chars = ["↖", "↑", "↗", "←", "o", "→", "↙", "↓", "↘"]
        s = 50 #configure amount of steps per button press here
        command_inputs = [
            lambda: command("moveby " + str(-s) + " " + str(s) + " 0", this, this.d, this.v), lambda: command("moveby " + str(s) + " " + str(0) + " 0", this, this.d, this.v), lambda: command("moveby " + str(s) + " " + str(s) + " 0", this, this.d, this.v),
            lambda: command("moveby " + str(0) + " " + str(-s) + " 0", this, this.d, this.v), lambda: command("autohome", this, this.d, this.v), lambda: command("moveby " + str(0) + " " + str(s) + " 0", this, this.d, this.v),
            lambda: command("moveby " + str(-s) + " " + str(-s) + " 0", this, this.d, this.v), lambda: command("moveby " + str(-s) + " " + str(0) + " 0", this, this.d, this.v), lambda: command("moveby " + str(s) + " " + str(-s) + " 0", this, this.d, this.v)
        ]
        arrow_buttons = []
        posx = 0
        posy = 0
        i = 0
        for c in chars:
            temp_button = tk.Button(arrow_Frame, text = c, height = 2, width = 4, command = command_inputs[i])
            temp_button.grid(column = posx, row = posy, padx=2, pady=2)
            arrow_buttons.append(temp_button)
            posx = posx + 1
            if(posx == 3):
                posy = posy + 1
                posx = 0
            i = i + 1

        #console
        console_Frame = tk.Frame(root, background="#14a9ff")
        console_Frame.place(anchor="sw", relx=0, rely=1, relwidth=0.5, relheight=0.4)

        send_button = tk.Button(console_Frame, text="Send", command=this.send)
        send_button.pack(side="bottom", fill="x")

        inp = tk.Entry(console_Frame, background="grey")
        inp.pack(side="bottom", fill="x")
        this.inp = inp

        #console text with scrollbar
        console_text_Frame = tk.Frame(console_Frame)
        scrolly = tk.Scrollbar(console_text_Frame, orient=tk.VERTICAL)
        scollx = tk.Scrollbar(console_text_Frame, orient=tk.HORIZONTAL)
        this.Lb = tk.Listbox(console_text_Frame, yscrollcommand=scrolly.set, xscrollcommand=scollx.set, selectmode=tk.EXTENDED)

        scrolly.config(command=this.Lb.yview)
        scollx.config(command=this.Lb.xview)

        scrolly.pack(side=tk.RIGHT, fill="y")
        scollx.pack(side=tk.BOTTOM, fill="x")
        this.Lb.pack(expand=True, fill=tk.BOTH)
        console_text_Frame.pack(expand=True, fill=tk.BOTH)
        
        #x y z indicators
        indicator_Frame = tk.Frame(root, relief=tk.RIDGE, bd=3)
        indicator_Frame.place(relx=0.5, rely=1, anchor="sw", relwidth=0.06)

        x_Label = tk.Label(indicator_Frame, textvariable = this.x_Label_text, background="#1cff20", justify=tk.LEFT, anchor="w").pack(side=tk.TOP, fill="x")
        y_Label = tk.Label(indicator_Frame, textvariable = this.y_Label_text, background="#ff3c2e", justify=tk.LEFT, anchor="w").pack(side=tk.TOP, fill="x")
        z_Label = tk.Label(indicator_Frame, textvariable = this.z_Label_text, background="#2ec7ff", justify=tk.LEFT, anchor="w").pack(side=tk.TOP, fill="x")
        
        #status display

        status_Frame = tk.Frame(root, relief=tk.RIDGE, bd=3)
        status_Frame.place(relx=0.56, rely=1, anchor="sw")

        stepper_button = tk.Button(status_Frame, text="Steppers", command=this.toggle_steppers).grid(row=0, column=0, padx=2, pady=2, sticky="NESW")
        stepper_Label = tk.Label(status_Frame, textvariable=this.stepper_Label_text).grid(row=0, column=1, padx=2, pady=2, sticky="NESW")

        lights_button = tk.Button(status_Frame, text="Lights", command=this.toggle_steppers).grid(row=1, column=0, padx=2, pady=2, sticky="NESW")
        lights_Label = tk.Label(status_Frame, textvariable=this.light_Label_text).grid(row=1, column=1, padx=2, pady=2, sticky="NESW")

        root.mainloop()

    #setter for x y z
    def setxyz(this, x, y, z):
        this.x_Label_text.set("x: " + str(x))
        this.y_Label_text.set("y: " + str(y))
        this.z_Label_text.set("z: " + str(z))
    
    def toggle_steppers(this):
        if this.v.stepper_status:
            this.v.stepper_status = False
            command("setsteppers False")
            this.stepper_Label_text.set("OFF")
        else:
            this.v.stepper_status = True
            command("setsteppers True")
            this.stepper_Label_text.set("ON")
