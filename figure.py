#!/usr/bin/env python
import math

class Figure:
    '''describes a 2d figure made from lines'''

    def __init__(self):
        self.lines = []

    def clear(self):
        self.lines = []

    def pointstolines(self, points):
        for i in range(len(points) - 1):
            self.lines.append([points[i][0], points[i][1],
                               points[i + 1][0], points[i + 1][1]]) #make lines

    def addline(self, x, y, x2, y2):
        self.lines.append([x, y, x2, y2])

    def addpoint(self, x, y):
        self.lines.append([x, y, x, y])

    def addbox(self, x, y, x2, y2):
        self.lines.append([x, y, x2, y])
        self.lines.append([x2, y, x2, y2])
        self.lines.append([x2, y2, x, y2])
        self.lines.append([x, y2, x, y])
  
    def addcircle(self, x, y, diameter, steps):
        i = 0.0
        points = []

        while (i < 2 * math.pi):
            points.append([math.sin(i) * diameter + x,
                           math.cos(i) * diameter + y]) #make points
            i += math.pi / steps

        points.append([x, y + diameter])
        self.pointstolines(points)

    def addspiral(self, x, y, diameter, steps, windings = 2):
        i = 0.0
        steps = steps / (windings * 2)
        points = []
        target =  2 * math.pi * windings

        while (i < target):
            points.append([(i/target) * math.sin(i) * diameter + x,
                           (i/target) * math.cos(i) * diameter + y]) #make points
            i += math.pi / steps
        self.pointstolines(points)

if __name__ == '__main__':
    fig = Figure()
    fig.addspiral(0, 0, 60, 180, 7)
