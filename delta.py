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
    pathresolution = 10
    path = pp.plan(target, pathresolution)
    anglesbuffer = []
    for coords in path:
        coords = warpadjust(coords)
        angles = ik.calcInverse(coords)
        anglesbuffer.append(angles)
    for angles in anglesbuffer:
        if angles:
            s1.movea(angles[0])
            s2.movea(angles[1])
            s3.movea(angles[2])
            #time.sleep(max(s1.diff, s2.diff, s3.diff) / 1000.0)

def warpadjust(coords):
    '''adjusts a target coordinate for known warpage of surface'''
    factor = 0.18
    distance = math.sqrt(coords[0] * coords[0] + coords[1] * coords[1])
    return ([coords[0], coords[1], coords[2] + (distance * factor)])

def drawfig(fig, table):
    lift = 20
    lines = fig.lines

    moveto([lines[0][0], lines[0][1], table + lift])

    for i in range(len(lines) - 1):
        moveto([lines[i][0], lines[i][1], table])
        moveto([lines[i][2], lines[i][3], table])

        if lines[i + 1][0] != lines[i][2] or lines[i + 1][1] != lines[i][3]:
            moveto([lines[i][2], lines[i][3], table + lift])
            moveto([lines[i + 1][0], lines[i + 1][1], table + lift])

    moveto([lines[len(lines) - 1][0], lines[len(lines) - 1][1], table])
    moveto([lines[len(lines) - 1][2], lines[len(lines) - 1][3], table])

    moveto([lines[len(lines) - 1][2], lines[len(lines) - 1][3], table + lift * 2])
    time.sleep(0.2)
    
def demobox():
    fig.addbox(-80, -80, 80, 80)
    drawfig(fig, -200)

def democircle():
    fig.addcircle(0, 0, 80, 40)
    drawfig(fig, -200)

def demospiral():
    fig.addspiral(0, 0, 80, 100, 4)
    drawfig(fig, -200)

def demogrid():
    size = 80
    step = 40
    for i in range(-size, size + 1, step):
        fig.addline(-size, i, size, i)
    for i in range(-size, size + 1, step):
        fig.addline(i, -size, i, size)

    drawfig(fig, -200)


demogrid()
fig.clear()
democircle()
fig.clear()
demospiral()
ser.close()



