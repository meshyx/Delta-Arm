#!/usr/bin/env python
import math

class Ik:
    '''Adapted from http://forums.trossenrobotics.com/tutorials/introduction-129/delta-robot-kinematics-3276/'''

    def __init__(self, e = 75, f = 62, re = 155, rf = 88):
        self.maxangle = 90
        self.minangle = -75
        self.e = e
        self.f = f
        self.re = re
        self.rf = rf
        self.sqrt3 = math.sqrt(3.0)
        self.sin120 = self.sqrt3/2.0
        self.cos120 = -0.5
        self.tan60 = math.sqrt(3.0)
        self.sin30 = 0.5
        self.tan30 = 1.0 / self.sqrt3

    def calcAngleYZ(self, x0, y0, z0):
        '''internal helper function'''
        y1 = -0.5 * 0.57735 * self.f
        y0 = y0 - 0.5 * 0.57735 * self.e

        a = (x0 * x0 + y0 * y0 + z0 * z0 + self.rf * self.rf - self.re * self.re - y1 * y1) / (2 * z0)
        b = (y1 - y0) / z0;

        d = -(a + b * y1) * (a + b * y1) + self.rf * (b * b * self.rf + self.rf)

        if (d < 0):
            return False # non-existing point

        yj = (y1 - a * b - math.sqrt(d)) / (b * b + 1)
        zj = a + b * yj

        if yj > y1:
            magic = 180.0
        else:
            magic = 0.0

        theta = 180.0 * math.atan(-zj / (y1 - yj)) / math.pi + magic
        return theta

    def calcInverse(self, coords):
        '''coords to angles'''
        x0, y0, z0 = coords
        theta1 = theta2 = theta3 = 0
        theta1 = self.calcAngleYZ(x0, y0, z0)
        if (theta1):
            theta2 = self.calcAngleYZ(x0 * self.cos120 + y0 * self.sin120, y0 * self.cos120 - x0 * self.sin120, z0)
        if (theta2):
            theta3 = self.calcAngleYZ(x0 * self.cos120 - y0 * self.sin120, y0 * self.cos120 + x0 * self.sin120, z0)
        if (theta3):
            return self.applyLimits([theta1, theta2, theta3])
        else:
            return False

    def applyLimits(self, angles):
        for i in range(len(angles)):
            if (angles[i] < self.minangle):
                angles[i] = self.minangle
                print "servo min angle out of range"
            if (angles[i] > self.maxangle):
                angles[i] = self.maxangle
                print "servo max angle out of range"
        return angles

    def calcForward(self, angles):
        '''angles to coords'''
        theta1, theta2, theta3 = angles
        t = (self.f - self.e) * self.tan30 / 2.0
        dtr = math.pi / 180.0
        theta1 = theta1 * dtr
        theta2 = theta2 * dtr
        theta3 = theta3 * dtr

        y1 = - (t + self.rf * math.cos(theta1))
        z1 = - self.rf * math.sin(theta1)

        y2 = (t + self.rf * math.cos(theta2)) * self.sin30
        x2 = y2 * self.tan60
        z2 = - self.rf * math.sin(theta2)

        y3 = (t + self.rf * math.cos(theta3)) * self.sin30
        x3 = - y3 * self.tan60
        z3 = - self.rf * math.sin(theta3)

        dnm = (y2 - y1) * x3 - (y3 - y1) * x2

        w1 = y1 * y1 + z1 * z1
        w2 = x2 * x2 + y2 * y2 + z2 * z2
        w3 = x3 * x3 + y3 * y3 + z3 * z3

        a1 = (z2 - z1) * (y3 - y1) - (z3 - z1) * (y2 - y1)
        b1 = - ((w2 - w1) * (y3 - y1) - (w3 - w1) * (y2 - y1)) / 2.0

        a2 = - (z2 - z1) * x3 + (z3 - z1) * x2
        b2 = ((w2 - w1) * x3 - (w3 - w1) * x2) / 2.0
 
        a = a1 * a1 + a2 * a2 + dnm * dnm
        b = 2 * (a1 * b1 + a2 * (b2 - y1 * dnm) - z1 * dnm * dnm)
        c = (b2 - y1 * dnm) * (b2 - y1 * dnm) + b1 * b1 + dnm * dnm * (z1 * z1 - self.re * self.re)  

        d = b * b - 4.0 * a * c

        if (d < 0):
            return False # non-existing point
 
        z0 = -0.5 * (b + math.sqrt(d)) / a
        x0 = (a1 * z0 + b1) / dnm
        y0 = (a2 * z0 + b2) / dnm
        return ([x0, y0, z0])

if __name__ == '__main__':
    ik = Ik()
    for x in range(-12, 12):
        print x, x, ik.calcInverse([x, x, -120])
