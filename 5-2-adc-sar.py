import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4  
troyka = 17
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT )
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)

def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]






def adc():
    sig=128
    delt=64
 
    for i in range(8):
        
        GPIO.output(dac, dec2bin(sig))
        time.sleep(0.005)
        if GPIO.input(comp) == 0:
            sig=sig-delt
            delt=int(delt/2)
        else:
            sig=sig+delt
            delt=int(delt/2)
    return sig




try:
    while True:
        start_time = time.time()
        value = adc()
        voltage = round(value / 255 * 3.3, 2)
        print(value,dec2bin(value),"v={:.4}".format(value/(2**8)*3.3),"time: {:.5f} sec".format(time.time() - start_time))
        #print("ADC value: {}, Voltage: {}V".format(value, voltage))
except KeyboardInterrupt:
    print("E")
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup()

    