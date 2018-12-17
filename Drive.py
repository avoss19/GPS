from bsmLib import RPL
from bsmLib import tcpServer
RPL.init()

class Drive:
    def __init__(self, l = [0], r = [1]):
        self._initVar()

    def _initVar(self, l = [0] , r = [1]):
        # Define motor pins, must be triple or array
        self.L = l
        self.R = r

        # Defualt motor directions
        self.L_DIR = -1
        self.R_DIR = 1

        # Max & Min speeds of each servo/motor
        self.MAX_SPEED = 2000
        self.MIN_SPEED = 1000

        # Difference in speed devided by 2 & Middle speed (stopped due to midpoint)
        self._DIF_SPEED = int((self.MAX_SPEED - self.MIN_SPEED) / 2)
        self.MID_SPEED = self.MIN_SPEED + self._DIF_SPEED

    def _convertSpeed(self, speed):
        # Convert speeds for range of -1 to 1 to values readable by servos/motors
        if((speed < -1) or (speed > 1)):
            print("Error: Out of bounds (Requires value between -1 & 1)")
            exit()
        if speed < 0:
            return int(self.MID_SPEED - (self._DIF_SPEED * speed))
        else:
            return int(self.MID_SPEED + (self._DIF_SPEED * speed))

    def setMax(self, speed):
        # Set max speed of servos/motors
        self.MAX_SPEED = speed

    def setMin(self, speed):
        # Set min speed of servos/motors
        self.MIN_SPEED = speed

    def setDirection(self, l, r):
        self.L_DIR = l
        self.R_DIR = r

    def drive(self, l_speed, r_speed):
        # Drive Left and Right servos/motors
        for i in self.L:
            RPL.servoWrite(i, _convertSpeed(l_speed * self.L_DIR))
        for i in self.R:
            RPL.servoWrite(i, _convertSpeed(r_speed * self.R_DIR))

    def forward(self, speed):
        # Drive bot forward
        self.drive(speed, speed)

    def turnLeft(self, speed):
        # Turn left
        self.drive(-speed, speed)

    def turnRight(self, speed):
        # Turn right
        self.drive(speed, -speed)

    def stop():
        # Stop servos/motors
        self.drive(self.MID_SPEED, self.MID_SPEED)

class DrivePWM(Drive):
    def __init__(self, l = [0], r = [1], freq = 3000):
        # Init Vars
        self._initVar(l, r)

        # PWM frequency
        self.FREQ = freq

        # Set pin modes
        for i in self.L + self.R:
            RPL.pinMode(i, RPL.PWM)

    def drive(self, l_speed, r_speed):
        # Drive Left and Right servo/motors
        for i in self.L:
            RPL.pwmWrite(0, _convertSpeed(l_speed * self.L_DIR), self.FREQ)
        for i in self.R:
            RPL.pwmWrite(0, _convertSpeed(r_speed * self.R_DIR), self.FREQ)

class DriveServer(Drive):
    def __init__(self, l = [0], r = [1], ip="0.0.0.0", port=10000):
        # Setup network
        self.NETWORK = tcpServer(ip, port)
        self.NETWORK.listen()

        # Init Vars
        self._initVar(l, r)

    def drive(self, l_speed, r_speed):
        self.NETWORK.send(str(_convertSpeed(l_speed * self.L_DIR)) + ':' + str(_convertSpeed(r_speed * self.R_DIR)))

class DriveClient(Drive):
    def __init__(self, l = [0], r = [1], ip="0.0.0.0", port=10000):
        # Setup network
        self.NETWORK = tcpClient(ip, port)
        self.NETWORK.connect()

        # Init Vars
        self._initVar(l, r)

    def drive(self):
        m = self.NETWORK.recv()
        m = m.split(':')
        for i in self.L:
            RPL.servoWrite(i, _convertSpeed(m[0] * self.L_DIR))
        for i in self.R:
            RPL.servoWrite(i, _convertSpeed(m[1] * self.R_DIR))

class DriveClientPWM(DriveClient):
    def __init__(self, l = [0], r = [1], freq = 3000, ip="0.0.0.0", port=10000):
        super().__init__(self, l, r, ip, port)

    def drive(self):
        m = self.NETWORK.recv()
        m = m.split(':')
        for i in self.L:
            RPL.pwmWrite(0, _convertSpeed(m[0] * self.L_DIR), self.FREQ)
        for i in self.R:
            RPL.pwmWrite(0, _convertSpeed(m[1] * self.R_DIR), self.FREQ)
