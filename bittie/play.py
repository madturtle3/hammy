#!/Library/Frameworks/Python.framework/Versions/3.10/bin/python3.10
import numpy
import sys
import math
import pyaudio
import wave
from dit_time import dit_time, frequency, harmonics_dupe

def gen_signal(size: int):
    """
    generate a sine wave list of length SIZE.
    """
    data = bytes(0)
    omega = math.pi * 2 * frequency
    current_step = 0
    for index in numpy.arange(0, size, 1/rate):
        wave = 0
        for signal in range(harmonics_dupe):
            wave += math.sin(index * omega * (signal + 1)) # generate waveform
        wave /= harmonics_dupe
        wave *= 2 ** 15 - 1
        wave = int(wave)
        data += wave.to_bytes(2, sys.byteorder, signed=True)
        current_step += 1/rate
    omega = math.pi * 2 * frequency * 2

    return data


rate = 44100
long = gen_signal(3 * dit_time)
short = gen_signal(dit_time)
empty_dit = bytes(int(dit_time * rate * 2))
recording = bytes(0)
for char in sys.argv[1]:
    char = bin(ord(char)).replace("1","-").replace("0",".")
    for indicator in char:
        if indicator == "-":
            recording += long
        if indicator == ".":
            recording += short
        if indicator == " ":
            recording += empty_dit * 1  # space
        recording += empty_dit  # space between dits
    recording += empty_dit * 2  # space between letter
sp_stream = pyaudio.PyAudio()
speaker = sp_stream.open(rate,channels=1,format=pyaudio.paInt16,output=True)
speaker.write(recording)
""" wav = wave.open("test.wav", "w")
wav.setframerate(rate)
wav.setnchannels(1)
wav.setsampwidth(2)
wav.writeframes(recording) """