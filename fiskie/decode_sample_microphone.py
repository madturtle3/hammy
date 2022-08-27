#!/usr/bin/python3
import sys
import scipy.io
import scipy
import scipy.fftpack
import matplotlib.pyplot
import numpy
import wave
import pyaudio
from dit_time import dit_time, freq0, freq1




def get_bin(freq):
    """
    returns the bin of the frequency provided
    """
    frequencies_per_bin = bandwidth / BINS
    binned = int(freq // frequencies_per_bin)
    return binned + 1

def write_label(sample_count, time_on, value, labels):
    end_time = sample_count / rate
    start_time = end_time - time_on

    labels.write(f"{start_time}\t{end_time}\t{value}\n")



RATE = 44100
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
rate = RATE
bandwidth = rate//2
bin_time = dit_time / 2
BINS = bandwidth
bin_samples = int(rate * bin_time)
stream = pyaudio.PyAudio().open(RATE, CHANNELS, FORMAT, True)
result_vales = []
times = []
on_data=[[],[],[]]
total_data = []
NOISE_FLOOR = 25000
on = False
on1 = False
off = False
time_on = 0
sample_count = 0
TIME_OVERLAP = int(bin_samples * 0)
word = ""
full_text = ""
log: wave.Wave_write = wave.open("log.wav", "wb")
log.setnchannels(1)
log.setframerate(44100)
log.setsampwidth(2)
labels = open("label.txt", "w")
print("Ready!")
try:
    while True:
        data = stream.read(bin_samples, exception_on_overflow=False)
        log.writeframes(data)
        data = numpy.frombuffer(data, numpy.int16)
        fft_data = scipy.fftpack.fft(data, n=BINS)
        final_data = abs(fft_data[get_bin(freq0)])
        final_data1 = abs(fft_data[get_bin(freq1)])
        if not on:
            total_data.append(final_data)
        
        time_on += bin_samples / rate
        time_on = time_on
        if final_data > NOISE_FLOOR:
            if on:
                if abs(time_on - dit_time) < dit_time / 2: # if time passed
                    word += "0"
                    time_on = 0
            else: # 0 sig has just turned on
                print(0)
                time_on = 0
                on = True
                on1 = False
                off = False

        if final_data1 > NOISE_FLOOR:
            print("DAT1")
            if on1:
                if abs(time_on - dit_time) < dit_time / 2: # if time passed
                    word += "1"
                    time_on = 0
            else: # 1 sig has just turned on
                print(1)
                time_on = 0
                on1 = True
                on = False
                off = False
        if final_data < NOISE_FLOOR and final_data1 < NOISE_FLOOR:  # if pause
            if off:
                if abs(time_on - dit_time) < dit_time / 2:
                    if len(word) > 0:
                        print(chr(int(word,2)), end="", flush=True)
            else: # if sig just off
                off = True
                on1 = False
                on2 = False
        
        #NOISE_FLOOR = (sum(total_data) // len(total_data)) * 1.5
        result_vales.append(final_data)
        on_data[0].append(NOISE_FLOOR * on)
        on_data[1].append(NOISE_FLOOR * on1)
        on_data[2].append(NOISE_FLOOR * off)
        sample_count += bin_samples

except KeyboardInterrupt:
    labels.flush()
    matplotlib.pyplot.plot(result_vales)
    matplotlib.pyplot.plot(on_data[0], "red")
    matplotlib.pyplot.plot(on_data[1], "green")
    matplotlib.pyplot.plot(on_data[2], "purple")
    matplotlib.pyplot.show()
    log.close()
    labels.close()
    print("DONE")
