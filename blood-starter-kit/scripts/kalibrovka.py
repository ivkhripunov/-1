import matplotlib.pyplot as plt
import numpy as np
import spidev
import time

maxvoltage = 3.3
values = []
preses = []
val = 0
num = 0

#Массив маркеров настроишь на основании полученных данных
#markers_on = [int(i) for i in range(0,20000,100)]

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1600000

print("Введите калибровочное давление в мм рт ст, если ввели все, то введите 0")
pres = int(input())

def getAdc():
    adcResponse = spi.xfer2([0, 0])
    return ((adcResponse[0] & 0x1F) << 8 | adcResponse[1]) >> 1

try:
    while pres != 0:
        with open("/home/gr106/Desktop/blood-starter-kit/data/" + str(pres) +"mm rt st.txt", "r") as f:
            for line in f.readlines():
                val += int(line)
                
                num += 1
        val = val / num
        values.append(val)
        preses.append(pres)
        print("Введите калибровочное давление в мм рт ст, если ввели все, то введите 0")
        pres = int(input())
        num = 0
        val = 0
    (k, b) = np.polyfit(values, preses, 1)
    #k = -k
    vals = []
    nums = []
    pressures = []
    for i in range(1800):
        pressures.append(b + k*i)
        nums.append(i)
    fig, ax = plt.subplots(figsize=(12, 9))
    print(values)
    print(preses)
    
    ax.plot(values, preses,
            linestyle='--',
            linewidth=3,
            color='darkmagenta')
    ax.plot(nums, pressures,
            linestyle='-',
            linewidth=1,
            color='red'
            )
    ax.set_title('Задание каллибровки', style='italic')
    ax.legend(labels=("значения в точках", "аппроксимирующая"), loc="upper right")
    ax.set_xlabel('значения напряжения в у е')
    ax.set_ylabel('давление (мм рт ст)')
    ax.axes.grid(
        which="major",
        linewidth="0.4",
    )
    ax.minorticks_on()
    ax.axes.grid(
       which = "minor",
       linewidth = "0.2"
    )
    print('угловой коэффициент = ' + str(k))
    print('Свободный член = ' + str(b))
    plt.savefig('/home/gr106/Desktop/blood-starter-kit/plots/pressure-calibration.png')
finally:
    plt.show()
    spi.close()





