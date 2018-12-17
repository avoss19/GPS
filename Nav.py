from time import time
from math import pi
from bsmLib import vector
from GPS import GPS
from Drive import Drive
from Drive import DrivePWM

class Nav:
    def __init__(self, drive=Drive(), gps="/dev/serial0", init_time = 10):
        self.DRIVE = drive
        self.GPS = GPS(gps)
        self.INIT_TIME = init_time
        self.TURN_TIME = 3
        self.GOAL_POS = vector()
        self.CURRENT_POS = vector()
        self.LAST_POS = vector()

    def setGoalVec(self, goal):
        # Set goal w/ vec
        self.GOAL_POS = goal

    def setGoal(self, x, y):
        # Set goal w/ x, y
        self.GOAL_POS.set(x, y)

    def setTurnTime(self, sec):
        # Set turn time
        self.TURN_TIME = sec

    def setInitTime(self, sec):
        # Set time
        self.INIT_TIME = sec

    def getCurrentPos(self):
        # Get GPS current reading
        self.LAST_POS = self.CURRENT_POS
        self.CURRENT_POS = self.GPS.read()
        return self.CURRENT_POS

    def navToGoal(self):
        # Get init reading to calc theta
        self.getCurrentPos()
        setTime = time() + self.INIT_TIME
        while(1):
            if time() < setTime:
                self.DRIVE.forward(1)
            else:
                self.DRIVE.forward(0)
                break
        self.getCurrentPos()
        goal_vec = self.GOAL_POS - (self.CURRENT_POS - self.LAST_POS)
        setTime = time() + self.TURN_TIME
        while(1):
            if time() < setTime:
                if goal_vec.heading() > pi:
                    this.DRIVE.turnRight()
                else:
                    this.DRIVE.turnLeft()
            else:
                break
