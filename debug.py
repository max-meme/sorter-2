from datetime import datetime
class Debug:
    def __init__(this, f, db):
        this.f = f
        this.db = db

    def log(this, m):
        if(this.db):
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            mn = "[" + current_time + "]: " + m
            print(mn)
            this.f.write(mn + "\n")