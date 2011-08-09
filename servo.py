class Servo:
    def __init__(self, ser, number, minms = 600, centerms = 1500, maxms = 2400, reverse = False):
        self.ser = ser
        self.number = number
        self.ms = 0
        self.diff = 0
        self.minms = minms
        self.maxms = maxms
        self.centerms = centerms
        self.reverse = reverse
        self.movems(self.centerms)

    def movems(self, ms):
        if (ms > self.maxms):
            ms = self.maxms
        if (ms < self.minms):
            ms = self.minms
        
        self.ser.write(chr(255))
        self.ser.write(chr(self.number))
        if (self.reverse):
            self.reversedms = self.centerms + (self.centerms - ms)
            #print "servo:", self.number, " got ms:", ms, " reversing to:", self.reversedms
            self.ser.write(chr(self.reversedms / 256))
            self.ser.write(chr(self.reversedms % 256))
        else:
            #print "servo:", self.number, " got ms:", ms
            self.ser.write(chr(ms / 256))
            self.ser.write(chr(ms % 256))
        self.diff = abs(self.ms - ms)
        self.ms = ms

    def movepct(self, pct):
        self.movems(self.minms + (self.maxms - self.minms) / 100 * pct)

    def movea(self, theta):
        if (theta < -60):
            theta = -60
        if (theta > 80):
            theta = 80
        if (theta >= 0):
            self.movems(int(self.centerms + ((self.maxms - self.centerms) / 80.0 * theta)))
        else:
            self.movems(int(self.centerms + ((self.centerms - self.minms) / 60.0 * theta)))
