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

def moveto(x, y, z):
    path = pp.plan((x, y, z), 0.5)
    for coords in path:
        coords = warpadjust(coords)
        angles = ik.calcInverse(coords[0], coords[1], coords[2])
        if angles:
            s1.movea(angles[0])
            s2.movea(angles[1])
            s3.movea(angles[2])
            #time.sleep(max(s1.diff, s2.diff, s3.diff) / 2000.0)

def warpadjust(coords):
    factor = 0.18
    distance = math.sqrt(coords[0] * coords[0] + coords[1] * coords[1])
    return (coords[0], coords[1], coords[2] + (distance * factor))

def demo5():
    i = 0.0
    size = 40
    steps = 10
    x = 30
    y = 30
    z = -44
    while (i < 2 * math.pi * 1.00001):
        i += math.pi / steps
        moveto(math.sin(i) * size + x, math.cos(i) * size + y, -134.0 + z)

def demo6():
    for i in range(-80, 80, 1):
        moveto(i, i, -134.0 - 45)
    time.sleep(1)

def demo7():
    for x in range(-90, 91, 10):
        for z in range(-114, -170, -1):
            moveaw(ik.calcInverse(x, 0, z))

def demo8():
    sleepy = 0.5
    table = 41
    moveto(0, 0, -137 - table)
    time.sleep(sleepy)
    moveto(0, 0, -137 - table)
    time.sleep(sleepy)
    moveto(60, 60, -137 - table)
    time.sleep(sleepy)
    moveto(-60, 60, -137 - table)
    time.sleep(sleepy)
    moveto(60, -60, -137 - table)
    time.sleep(sleepy)
    moveto(-60, -60, -137 - table)
    time.sleep(sleepy)
    moveto(0, 0, -137 - table)
    time.sleep(sleepy)

demo8()
#time.sleep(1)
ser.close()



