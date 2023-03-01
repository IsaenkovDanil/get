import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

GPIO.setup(15,GPIO.OUT)

GPIO.setup(22,GPIO.IN)

GPIO.output(15,GPIO.input(22))

GPIO.cleanup()