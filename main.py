from debug import Debug
from varman import Varman
from UI import UI

d = Debug(open("debug.txt", "w"), True)
v = Varman(500, 500, 100)
d.log("Starting Sorter :D")
d.log("Creating UI")
ui = UI(v, d, "Sorter", False)