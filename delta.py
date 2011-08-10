#!/usr/bin/env python
import time
import serial
import random
import math
import ik
import servo
import pathplanner

ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(0.9)

s1 = servo.Servo(ser, 1, 750, 1435, 2300, False)
s2 = servo.Servo(ser, 2, 810, 1495, 2350, True)
s3 = servo.Servo(ser, 3, 800, 1495, 2375, True)

ik = ik.Ik()
pp = pathplanner.PathPlanner()

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
            #time.sleep(max(s1.diff, s2.diff, s3.diff) / 2000.0)

def warpadjust(coords):
    '''adjusts a target coordinate for known warpage of surface'''
    factor = 0.18
    distance = math.sqrt(coords[0] * coords[0] + coords[1] * coords[1])
    return ([coords[0], coords[1], coords[2] + (distance * factor)])

def democircle():
    i = 0.0
    size = 100
    steps = 150
    x = 0
    y = 0
    z = 0
    while (i < 2 * math.pi * 1.00001):
        i += math.pi / steps
        moveto([math.sin(i) * size + x, math.cos(i) * size + y, -134.0 + z])

def demo6():
    for i in range(-40, 70, 3):
        moveto([0, 0, -134.0 + i])
    time.sleep(1)

def demobox():
    sleepy = 0.5
    table = -1
    size = 60
    moveto([0, 0, -137 - table])
    time.sleep(sleepy)
    moveto([size, size, -137 - table])
    time.sleep(sleepy)
    moveto([-size, size, -137 - table])
    time.sleep(sleepy)
    moveto([-size, -size, -137 - table])
    time.sleep(sleepy)
    moveto([size, -size, -137 - table])
    time.sleep(sleepy)
    moveto([size, size, -137 - table])
    time.sleep(sleepy)
    moveto([0, 0, -137 - table])
    time.sleep(sleepy)

def demo9():
    sleepy = 2
    moveto([0, 0, -137 + 70])
    time.sleep(sleepy)

democircle()
#time.sleep(1)
ser.close()



