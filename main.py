from debug import Debug
from UI import UI

d = Debug(open("debug.txt", "w"), True)
d.log("Starting Sorter :D \nCreating UI")
ui = UI("sorter", False)

