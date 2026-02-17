### Basic Libraries for e-kagaku's RasPi Course ###
#------------------------------------------------------------------------------------------#
### File name	:	l293d.py
### Version		:	ver.0.1
### Created by	:	e-kagaku Supporter, Kazuki Mineta

### Purpose		:	
### Datasheet 	:	
#------------------------------------------------------------------------------------------#

import RPi.GPIO as GPIO
import time

MotorPin1   = 17
MotorPin2   = 27
MotorEnable = 22

def setup():
    global p_M1,p_M2
    # Set the GPIO modes to BCM Numbering
    GPIO.setmode(GPIO.BCM)
    # Set pins to output
    GPIO.setup(MotorPin1, GPIO.OUT)
    GPIO.setup(MotorPin2, GPIO.OUT)
    p_M1=GPIO.PWM(MotorPin1,2000)
    p_M2=GPIO.PWM(MotorPin2,2000)
    p_M1.start(0)
    p_M2.start(0)
    GPIO.setup(MotorEnable, GPIO.OUT, initial=GPIO.LOW)

# Define a motor function to spin the motor
# direction should be 
# 1(clockwise), 0(stop), -1(counterclockwise)
def move(direction,speed):
    # Clockwise
    if direction == 1:
        # Set direction
        #GPIO.output(MotorPin1, GPIO.HIGH)
        GPIO.output(MotorPin2, GPIO.LOW)
        # Enable the motor
        GPIO.output(MotorEnable, GPIO.HIGH)
        #p_M2.stop()
        p_M1.ChangeDutyCycle(speed)
    # Counterclockwise
    if direction == -1:
        # Set direction
        GPIO.output(MotorPin1, GPIO.LOW)
        #GPIO.output(MotorPin2, GPIO.HIGH)
        # Enable the motor
        GPIO.output(MotorEnable, GPIO.HIGH)
        #p_M1.stop()
        p_M2.ChangeDutyCycle(speed)
    # Stop
    if direction == 0:
        # Disable the motor
        GPIO.output(MotorEnable, GPIO.LOW)
        p_M1.ChangeDutyCycle(0)
        p_M2.ChangeDutyCycle(0)
        
def clear():
    # Stop the motor
    GPIO.output(MotorEnable, GPIO.LOW)
    p_M1.stop()
    p_M2.stop()
    # Release resource
    GPIO.cleanup()

#------------------------------------------------------------------------------------------#
### Update history:
# 2026/02/17	ver.0.1		Renamed l293d.py
#------------------------------------------------------------------------------------------#