import RPi.GPIO as   GPIO

def dec2bin(value):
    return [int(bit) for bit in bin(value)[2:].zfill(8)]
dac = [26, 19, 13, 6, 5 , 11, 9 , 10]
GPIO.setmode(GPIO.BCM)
GPIO.setup(dac,GPIO.OUT,initial=GPIO.LOW)
try:
    while True:
        user_input = input("0 до 255 ")
        if user_input.lower() == "q":
            break
        try:
            value = int(user_input)
            if value < 0:
                raise ValueError("Значение  отрицательным")
            if value >255:
                raise ValueError("превышение 8 разрядов")
            binary_value = dec2bin(value)
            GPIO.output(dac,binary_value)
            voltage = round(value*3.3/255,2)
            print(f"напряжение на /цап : {voltage} B")
        except ValueError as e:
            print(f"Ошибка {e}")
except KeyboardInterrupt:
    pass
finally: 
    GPIO.output(dac, GPIO.LOW)
    GPIO.cleanup()
    