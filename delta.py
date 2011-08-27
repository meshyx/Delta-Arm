#!/usr/bin/env python
import time
import serial
import random
import math
import ik
import servo
import pathplanner
import figure

ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(0.9)

s1 = servo.Servo(ser, 1, 750, 1435, 2300, False)
s2 = servo.Servo(ser, 2, 810, 1495, 2350, True)
s3 = servo.Servo(ser, 3, 800, 1495, 2375, True)

ik = ik.Ik()
pp = pathplanner.PathPlanner()
fig = figure.Figure()

def moveto(target):
    '''moves the arm to a target coordinate'''
    pathresolution = 2
    path = pp.plan(target, pathresolution)
    anglesbuffer = []
    for coords in path:
        angles = ik.calcInverse(coords)
        anglesbuffer.append(angles)
    for angles in anglesbuffer:
        if angles:
            s1.movea(angles[0])
            s2.movea(angles[1])
            s3.movea(angles[2])
            time.sleep(max(s1.diff, s2.diff, s3.diff) / 3000.0)

def drawfig(fig):
    table = -163
    lift = 10
    pathresolution = 0.5
    lines = fig.lines
    targets = []
    paths = []
    anglesbuffer = []
    
    targets.append([lines[0][0], lines[0][1], table + lift])

    for i in range(len(lines) - 1):
        targets.append([lines[i][0], lines[i][1], table])
        targets.append([lines[i][2], lines[i][3], table])

        if lines[i + 1][0] != lines[i][2] or lines[i + 1][1] != lines[i][3]:
            targets.append([lines[i][2], lines[i][3], table + lift])
            targets.append([lines[i + 1][0], lines[i + 1][1], table + lift])

    targets.append([lines[len(lines) - 1][0], lines[len(lines) - 1][1], table])
    targets.append([lines[len(lines) - 1][2], lines[len(lines) - 1][3], table])

    targets.append([lines[len(lines) - 1][2], lines[len(lines) - 1][3], table + lift * 2])

    for target in targets:
        paths.append(pp.plan(target, pathresolution))
    for path in paths:
        for coords in path:
            angles = ik.calcInverse(coords)
            anglesbuffer.append(angles)
    for angles in anglesbuffer:
        if angles:
            s1.movea(angles[0])
            s2.movea(angles[1])
            s3.movea(angles[2])
            time.sleep(max(s1.diff, s2.diff, s3.diff) / 2000.0)
        else:
            print "invalid angle"
    
def demobox():
    fig.addbox(-20, -20, 20, 20)
    drawfig(fig)

def democircle():
    for i in range(10, 41, 10):
        fig.addcircle(0, 0, i, 40)
    drawfig(fig)

def demospiral():
    fig.addspiral(0, 0, 60, 100, 4)
    drawfig(fig)

def demogrid():
    size = 60
    steps = 4
    xofs = 0
    yofs = 0
    for i in range(-size/2, size/2 + 1, size/steps):
        fig.addline(-size/2+xofs, i+yofs, size/2+xofs, i+yofs)
    for i in range(-size/2, size/2 + 1, size/steps):
        fig.addline(i+xofs, -size/2+yofs, i+xofs, size/2+yofs)
    drawfig(fig)

def setup1():
    s3.movea(90)
    time.sleep(10)

def saftlabel():
    scale = 0.3
    spacing = 5
    curr = -20
    s = [[[20,40], [0,40], [0,20], [20,20], [20,0], [0,0]]]
    a = [[[0,0], [0,40], [20,40], [20,0]], [[0,20], [20,20]]]
    f = [[[0,0], [0,40], [20,40]], [[0,20], [20,20]]]
    t = [[[10,0], [10,40]], [[-10,40], [30,40]]]
    space = [[[0,0], [0,0]]]
    to = [[[0,040], [20,40], [20,20], [0,20], [0,0], [20,0]]]
    null = [[[0,0], [0,40], [20,40], [20,0], [0,0]]]
    en = [[[5,30], [10,40], [10,0]]]

    label = [[s, a, f, t], [to, null, en, en]]
    for word in label:
        for let in word:
            for l in let:
                for i in range(len(l) - 1):
                    print l[i][0], l[i][1], l[i+1][0], l[i+1][1]
                    fig.addline(-l[i][0]*scale-curr, -l[i][1]*scale
                                , -l[i+1][0]*scale-curr, -l[i+1][1]*scale)
            drawfig(fig)
            fig.clear()
            curr = curr + spacing + 20*scale
        time.sleep(2)
        curr = -20

try:
    saftlabel()
    #setup1()
    #demogrid()
    #fig.clear()
    #demobox()
    #fig.clear()
    #democircle()
    #fig.clear()
    #demospiral()

    ser.close()
except:
    ser.close()
    print "ser closed"
    raise



