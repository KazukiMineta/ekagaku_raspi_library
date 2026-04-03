import RPi.GPIO as GPIO

class KY040:
    def __init__(self, clkPin=17, dtPin=18, swPin=27):
        self.clkPin = clkPin
        self.dtPin = dtPin
        self.swPin = swPin

        self.globalCounter = 0
        self.flag = 0
        self.Last_dt_Status = 0
        self.Current_dt_Status = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.clkPin, GPIO.IN)
        GPIO.setup(self.dtPin, GPIO.IN)
        GPIO.setup(self.swPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.swPin, GPIO.FALLING, callback=self._swISR)

    def _swISR(self, channel):
        pass
        self.globalCounter = 0

    def rotaryDeal(self):
        self.Last_dt_Status = GPIO.input(self.dtPin)

        while not GPIO.input(self.clkPin):
            self.Current_dt_Status = GPIO.input(self.dtPin)
            self.flag = 1

        if self.flag == 1:
            self.flag = 0
            if (self.Last_dt_Status == 0) and (self.Current_dt_Status == 1):
                self.globalCounter -= 1
            elif (self.Last_dt_Status == 1) and (self.Current_dt_Status == 0):
                self.globalCounter += 1

        return self.globalCounter

    def cleanup(self):
        GPIO.cleanup()