import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
pin = 18
GPIO.setup(pin,GPIO.OUT)
pwn =GPIO.PWM(pin, 1000)
pwn.start(0)
try:
    while True:
        duty_cycle = int(input("0 до 100 : "))
        pwn.ChangeDutyCycle(duty_cycle)
        voltage = duty_cycle / 100 *3.3
        print(f"напряжение на /цап : {voltage} B")
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
