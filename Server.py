from Nav import Nav
from Drive import *

if __name__ == "__main__":
    d = DriveServer()
    # d = DrivePWM()
    n = Nav(d)
    n.setGoal(44.958305, -93.342473) # Left corner of football field
    while(1):
        n.navToGoal()
