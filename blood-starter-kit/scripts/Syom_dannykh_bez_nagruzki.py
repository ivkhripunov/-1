import matplotlib.pyplot as plt
import numpy as np
import spidev
import time

maxvoltage = 3.3
vals = []
times = []
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

def getAdc():
    adcResponse = spi.xfer2([0, 0])
    return ((adcResponse[0] & 0x1F) << 8 | adcResponse[1]) >> 1

try:
    start_time = time.time()
    for i in range(360000):
        value = getAdc()
        vals.append(value)
        timer = time.time() - start_time
        times.append(timer)


    vals = np.array(vals)
    times = np.array(times)


    vals = vals * 0.104154818757622 -13.66429084810035
finally:
    #Просто, чтобы сразу было видно, работает ли всё
    # print(vals)
    print(times)

    fig, ax = plt.subplots(figsize=(12, 9))
    ax.plot(times,vals,
        linestyle = '-',
        linewidth = 1,
        #markevery=markers_on,
        color = 'darkmagenta')
    ax.set_title('Артериальное давление без нагрузки', style='italic')
    ax.legend(labels = ("Артериальное давление"), loc = "upper right")
    ax.set_ylabel('Давление (мм рт ст)')
    ax.set_xlabel('время (с)')
    #ax.figure(figsize=(10, 7))
    ax.axes.grid(
        which = "major",
        linewidth = "0.4",
    )
    ax.minorticks_on()
    ax.axes.grid(
        which = "minor",
        linewidth = "0.2"
    )

    #укажи путь к папке для сохранения графика
    plt.savefig('/home/gr106/Desktop/blood-starter-kit/plots/fitness.png')
    plt.show()
    number = len(times)
    samplingperiod = times[number - 1] / number
    with open("/home/gr106/Desktop/blood-starter-kit/data/fitness.txt", "w") as f:
        f.write('- Blood Lab\n\n')
        f.write(
            '- Experiment date = {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        f.write('- Experiment duration = {:.2f} s\n'.format(times[number - 1]))
        f.write('- Number of samples in measure = {}\n'.format(30))
        f.write('- Sampling period = {:.2f} us\n'.format(samplingperiod * 1e6))
        f.write('- Sampling frequency = {} Hz\n'.format(int(1 / samplingperiod)))
        f.write('- Samples count = {}\n\n'.format(number))
        f.write('- adc12bit\n')
    for i in range(number):
        with open("/home/gr106/Desktop/blood-starter-kit/data/fitness.txt", "a") as f:
            f.write(str(vals[i]) + " " + str(times[i]) + "\n")
    spi.close()




