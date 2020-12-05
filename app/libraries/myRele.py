#!/usr/bin/python3                                                                                   

import RPi.GPIO as GPIO
import time
import sys

class MyRele(object):


    def __init__(self,rele):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.rele = rele

    def on(self):
        channel = self.rele
        GPIO.setup(channel, GPIO.OUT)
        GPIO.output(channel,GPIO.LOW)

    def off(self):
        channel = self.rele
        GPIO.setup(channel, GPIO.OUT)
        GPIO.output(channel,GPIO.HIGH)

    def check(self):
        GPIO.setup(self.rele, GPIO.OUT)
        return GPIO.input(self.rele)

if __name__ == '__main__':
    try:
        c = MyRele(14)
        print(c.check())
        if 'liga' in sys.argv:
            c.on()
            print("ligado")
        else:
            c.off()
            print("desligado")
        print(c.check())
    except KeyboardInterrupt:
        pass
    finally:
        pass
        #GPIO.cleanup()
        print("Finally rele")
