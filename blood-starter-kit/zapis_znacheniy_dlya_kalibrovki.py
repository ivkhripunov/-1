import matplotlib.pyplot as plt
import numpy as np
import spidev
import time

maxvoltage = 3.3
vals = []
#Массив маркеров настроишь на основании полученных данных
#markers_on = [int(i) for i in range(0,20000,100)]
def getMeanAdc(samples):
    sum = 0
    for i in range(samples):
        sum += getAdc()
    
    return int(sum / samples)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1600000

print("Введите текущее давление в мм рт ст")
pres = int(input())

def getAdc():
    adcResponse = spi.xfer2([0, 0])
    return ((adcResponse[0] & 0x1F) << 8 | adcResponse[1]) >> 1

try:
    start_time = time.time()
    timer = 0
    while timer <= 11:
        value = getMeanAdc(30)
        print(value)
        vals.append(value)
        timer = time.time() - start_time
    vals = np.array(vals)
finally:
    #Просто, чтобы сразу было видно, работает ли всё
    print(vals)
    number = len(vals)
    samplingperiod = vals[number-1] / number
    '''with open("/home/gr106/Desktop/blood-starter-kit/data/fitness.txt", "a") as f:
        f.write('- Blood Lab\n\n')
        f.write(
            '- Experiment date = {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        f.write('- Experiment duration = {:.2f} s\n'.format(vals[number-1]))
        f.write('- Number of samples in measure = {}\n'.format(30))
        f.write('- Sampling period = {:.2f} us\n'.format(samplingperiod * 1e6))
        f.write('- Sampling frequency = {} Hz\n'.format(int(1 / samplingperiod)))
        f.write('- Samples count = {}\n\n'.format(number))
        f.write('- adc12bit\n') '''
    for i in range(number):
        with open("/home/gr106/Desktop/blood-starter-kit/data/" + str(pres) +"mm rt st.txt", "a") as f:
            f.write(str(vals[i]) + "\n")
    
    spi.close()




