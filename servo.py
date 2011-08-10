#!/usr/bin/env python

class Servo:
    ''' A servo object is initialized with a Serial object to communicate via, its
    number in the Arduino "MultipleSerialServoControl" sketch, adjustment values for
    endpoints, and whether it needs to have reversed arm movement'''

    def __init__(self, ser, number, minms = 600, centerms = 1500, maxms = 2400, reverse = False):
        self.ser = ser
        self.number = number
        self.ms = 0 #current location
        self.diff = 0 #difference between old and new location
        self.minms = minms
        self.maxms = maxms
        self.centerms = centerms
        self.reverse = reverse
        self.movems(self.centerms)

    def movems(self, ms):
        '''moves servo to location denoted by ms'''
        if (ms > self.maxms):
            ms = self.maxms
            print "servo ms out of range"
        if (ms < self.minms):
            print "servo ms out of range"
            ms = self.minms
        
        self.ser.write(chr(255))
        self.ser.write(chr(self.number))
        if (self.reverse):
            self.reversedms = self.centerms + (self.centerms - ms)
            self.ser.write(chr(self.reversedms / 256))
            self.ser.write(chr(self.reversedms % 256))
        else:
            self.ser.write(chr(ms / 256))
            self.ser.write(chr(ms % 256))
        self.diff = abs(self.ms - ms)
        self.ms = ms

    def movepct(self, pct):
        '''moves servo to location denoted by percentage of movement'''
        self.movems(self.minms + (self.maxms - self.minms) / 100 * pct)

    def movea(self, theta):
        '''moves servo to location denoted by angle from -90 to 90,
        with 0 being the previously defined center. Angles will only
        be correct if endpoints are correctly set.'''
        if (theta >= 0):
            self.movems(int(self.centerms + ((self.maxms - self.centerms) / 90 * theta)))
        else:
            self.movems(int(self.centerms + ((self.centerms - self.minms) / 90 * theta)))
