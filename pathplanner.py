#!/usr/bin/env python
import math

class PathPlanner:
    '''calculates linear path between two points, with chosen resolution'''
    def __init__(self):
        self.oldcoords = [0, 0, -134]
        
    def distance(self, c1, c2):
        return math.sqrt((c1[0]-c2[0])*(c1[0]-c2[0])
                         +(c1[1]-c2[1])*(c1[1]-c2[1])
                         +(c1[2]-c2[2])*(c1[2]-c2[2]))
    
    def plan(self, coords, stepsize):
        if coords == self.oldcoords:
            return [coords]
        
        distance = self.distance(self.oldcoords, coords)
        numpoints = distance / stepsize
        xdiff = self.oldcoords[0] - coords[0]
        ydiff = self.oldcoords[1] - coords[1]
        zdiff = self.oldcoords[2] - coords[2]
        xstep = xdiff / numpoints
        ystep = ydiff / numpoints
        zstep = zdiff / numpoints
        path = []
        step = 0

        while (step < numpoints - 1):
            path.append([(self.oldcoords[0] - xstep * step)
                        , (self.oldcoords[1] - ystep * step)
                        , (self.oldcoords[2] - zstep * step)])
            step += 1

        path.append(coords)
        self.oldcoords = coords            
        return path

if __name__ == '__main__':
    pp = PathPlanner()
    c = 1
    for p in pp.plan([11, 1, -134], 1):
        print c, p
        c+=1
