### Basic Libraries for e-kagaku's RasPi Course ###
#------------------------------------------------------------------------------------------#
### File name	:	servo.py
### Version		:	ver.0.1
### Created by	:	e-kagaku Supporter, Kazuki Mineta

### Purpose		:	
### Datasheet 	:	
#------------------------------------------------------------------------------------------#

import RPi.GPIO as GPIO
import time

SERVO_MIN_PULSE = 500
SERVO_MAX_PULSE = 2500

def map(value, inMin, inMax, outMin, outMax):
    return (outMax - outMin) * (value - inMin) / (inMax - inMin) + outMin

def setup(ServoPin):
    global p
    GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by BCM
    GPIO.setup(ServoPin, GPIO.OUT)   # Set ServoPin's mode is output
    GPIO.output(ServoPin, GPIO.LOW)  # Set ServoPin to low
    p = GPIO.PWM(ServoPin, 50)     # set Frequecy to 50Hz
    p.start(0)                     # Duty Cycle = 0
    
def setAngle(angle):      # make the servo rotate to specific angle (0-180 degrees) 
    angle = max(0, min(180, angle))
    pulse_width = map(angle, 0, 180, SERVO_MIN_PULSE, SERVO_MAX_PULSE)
    pwm = map(pulse_width, 0, 20000, 0, 100)
    p.ChangeDutyCycle(pwm)#map the angle to duty cycle and output it

def clear():
    p.stop()
    GPIO.cleanup()
    
#------------------------------------------------------------------------------------------#
### Update history:
# 2026/02/17	ver.0.2		Added servo.py
#------------------------------------------------------------------------------------------#