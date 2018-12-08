from os import popen
from bsmLib import vector

class GPS:
    def __init__ (self, device = "/dev/serial0"):
        self.device = device
        self._rawReading = ""
        self.reading = vector()

    def msgUpdate(self):
        self._rawReading = popen("cat " + self.device).read()

    def read(self):
        charPosX = 0
        charPosY = 0
        xPos = 1
        yPos = 1

        self.msgUpdate()
        x = self._rawReading[self._rawReading.find("A,"):self._rawReading.find(",N")]
        y = self._rawReading[self._rawReading.find("N,"):self._rawReading.find(",W")]
        x = x.replace("A,", '')
        y = y.replace("N,", '')
        x = x.split('.')
        y = y.split('.')

        if(x[0][:1] == '0'):
            charPosX += 1
            xPos *= -1
        if(y[0][:1] == '0'):
            charPosY += 1
            yPos *= -1

        x = xPos*(int(x[0][0+charPosX:2+charPosX])+(float(x[0][2+charPosX:4+charPosX])+float('.'+x[1]))/60)
        y = yPos*(int(y[0][0+charPosY:2+charPosY])+(float(y[0][2+charPosY:4+charPosY])+float('.'+y[1]))/60)

        self.reading.set(x, y)
        return self.reading
