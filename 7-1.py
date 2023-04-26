import RPi.GPIO as GPIO
import time
import numpy as np
import matplotlib.pyplot as plt

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds =[21,20,16,12,7,8,25,24]
comp = 4  
troyka = 17
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(leds,GPIO.OUT)
GPIO.setup(dac, GPIO.OUT )
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.LOW)

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
def adc2():
        value = 0
        delta = 128
        while True:
            value += int(delta)

            signal = dec2bin(int (value))
            GPIO.output(dac, signal)
            time.sleep(0.001)

            compValue = GPIO.input(comp)
            if compValue == 1:
                if delta == 1:
                    return value  
                delta = int(delta/2) 
            else:
                value -= delta
                if delta == 1:
                    return value  
                delta = int(delta/2)    

data_volts=[]
data_times=[]
GPIO.output(troyka,0)
bits =len(dac)
levels=2**bits
max_voltage=3.3

try:
    while adc2() != 0:
        time.sleep(0.1)    
    start_time = time.time()
    GPIO.output(troyka,0)
    

    value=0
    while value<133:
        value = adc2()
        x=0
        for i in range(8):
            if(value>i):
                x+=2**i
        GPIO.output(leds,dec2bin(x))
        voltage = round(value / 255 * 3.3, 2)
        print(value,dec2bin(value),"volts = {:.4}".format(voltage),"time: {:.5f} sec".format(time.time() - start_time))
        #print("ADC value: {}, Voltage: {}V".format(value, voltage))
        data_volts.append(value)
        data_times.append(time.time()-start_time)
        
        
    GPIO.output(troyka,1)
    while value>64:
        value = adc2()
        x=0
        for i in range(8):
            if(value>i):
                x+=2**i
        GPIO.output(leds,dec2bin(x))
        voltage = round(value / 255 * 3.3, 2)
        print(value,dec2bin(value),"volts = {:.4}".format(voltage),"time: {:.5f} sec".format(time.time() - start_time))
        #print("ADC value: {}, Voltage: {}V".format(value, voltage))
        data_volts.append(value)
        data_times.append(time.time()-start_time)


        end_time =time.time()


        with open("settings.txt","w") as f:
            f.write(str((end_time-start_time)/len(data_volts)))
            f.write("\n")
            f.write(str(max_voltage/256))
    print(end_time-start_time," секунд\n",(end_time-start_time)/len(data_volts),"\n",len(data_volts)/(end_time-start_time),"\n",max_voltage/256)




except KeyboardInterrupt:
    print("E")
finally:
    GPIO.output(dac, GPIO.LOW)
    GPIO.output(troyka,GPIO.LOW)
    GPIO.cleanup()
data_volts_str =[str(item) for item in data_volts]
data_times_str =[str(item) for item in data_times]
with open("data_volts.txt","w") as f:
    f.write("\n".join(data_volts_str))
with open("data_times.txt","w") as f:
    f.write("\n".join(data_times_str))
plt.plot(data_times,data_volts)
plt.show()





with open('settings.txt') as f:
    R, C = map(float, f.read().split())

with open('data_volts.txt') as f:
    adc_data = np.array([int(line) for line in f])


time = np.arange(len(adc_data)) * R * C
voltage = adc_data * 5 / 2**12


fig, ax = plt.subplots()

ax.plot(time, voltage, '-o', markersize=4, markevery=10, label='V(t)')
ax.legend()

ax.set_xlim(time.min(), time.max())
ax.set_ylim(voltage.min(), voltage.max())

ax.set_xlabel('Время (s)')
ax.set_ylabel('Напряжение (V)')

ax.set_title('Vvs T for RC ', fontsize=12, wrap=True)

ax.grid(which='major', linestyle='-', linewidth=0.6)
ax.grid(which='minor', linestyle=':', linewidth=0.4)
ax.minorticks_on()

charging_time = voltage.argmax() * R * C
discharging_time = (len(voltage) - voltage.argmin()) * R * C
text_position = (time.min() + 0.1 * (time.max() - time.min()),
                 voltage.min() + 0.6 * (voltage.max() - voltage.min()))
ax.text(*text_position,
        f"Charging time: {charging_time:.2f}s\nDischarging time: {discharging_time:.2f}s",
        fontsize=10, color='red')

fig.savefig('output.svg')
