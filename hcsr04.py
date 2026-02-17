### Basic Libraries for e-kagaku's RasPi Course ###
#------------------------------------------------------------------------------------------#
### File name	:	hcsr04.py
### Version		:	ver.0.2
### Created by	:	e-kagaku Supporter, Kazuki Mineta

### Purpose		:	This file is a library containing functions useful for the ultrasonic sensor module (HC-SR04).
### Datasheet 	:	https://cdn.sparkfun.com/datasheets/Sensors/Proximity/HCSR04.pdf
#------------------------------------------------------------------------------------------#

import RPi.GPIO as GPIO
import time

def setup(TRIG,ECHO):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(TRIG, GPIO.OUT)
	GPIO.setup(ECHO, GPIO.IN)

def getDistance(TRIG,ECHO):
	GPIO.output(TRIG, 0)
	time.sleep(0.000002)

	GPIO.output(TRIG, 1)
	time.sleep(0.00001)
	GPIO.output(TRIG, 0)

	
	while GPIO.input(ECHO) == 0:
		a = 0
	time1 = time.time()
	while GPIO.input(ECHO) == 1:
		a = 1
	time2 = time.time()

	during = time2 - time1
	return during * 340 / 2 * 100

def clear():
	GPIO.cleanup()

#------------------------------------------------------------------------------------------#
### Update history:
# 2025/08/19    ver.0.1     Added Ultrasonic.py
# 2026/02/17	ver.0.2		Renamed hcsr04.py
#------------------------------------------------------------------------------------------#