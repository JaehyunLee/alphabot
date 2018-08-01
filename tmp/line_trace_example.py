#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
from AlphaBot2 import AlphaBot2
from TRSensors import TRSensor
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

maximum = 30

TR = TRSensor()
Ab = AlphaBot2()
Ab.stop()
print('Sensor Calibration..')
time.sleep(0.5)
for i in range(0, 100):
    if i < 25 or i >= 75:
        Ab.right()
        Ab.setPWMA(30)
        Ab.setPWMB(30)
    else:
        Ab.left()
        Ab.setPWMA(30)
        Ab.setPWMB(30)
    TR.calibrate()
Ab.stop()

# Ready for start
while input('Say start! ') != 'start':
    print('You say start!')
    time.sleep(0.05)

Ab.forward()

while True:
    position, Sensors = TR.readLine()
    if Sensors[0] > 900 and Sensors[1] > 900 and Sensors[2] > 900 and Sensors[3] > 900 and Sensors[4] > 900:
        time.sleep(0.05)
        Ab.setPWMA(0)
        Ab.setPWMB(0)
    else:
        proportional = position - 2000
        power_difference = proportional / 30

        if power_difference > maximum:
            power_difference = maximum
        if power_difference < - maximum:
            power_difference = - maximum
        if power_difference < 0:
            Ab.setPWMA(maximum + power_difference)
            Ab.setPWMB(maximum)
        else:
            Ab.setPWMA(maximum)
            Ab.setPWMB(maximum - power_difference)
