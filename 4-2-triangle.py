import RPi.GPIO as   GPIO
import time
def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]
dac = [26, 19, 13, 6, 5 , 11, 9 , 10]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac,GPIO.OUT,initial=GPIO.LOW)
try:
    while True:
        d= int(input("input "))
        t=d/256/2
        for value in range(0,256):
           binary = dec2bin(value)
           GPIO.output(dac,binary)
           time.sleep(t)
        for value in range(255,-1,-1):
            binary = dec2bin(value)
            GPIO.output(dac,binary)
            time.sleep(t)
except KeyboardInterrupt:
    pass
finally: 
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup()
    