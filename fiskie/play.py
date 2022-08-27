import numpy
import sys
import math
import simpleaudio
import wave
from dit_time import dit_time, freq0, freq1

def gen_signal(size: int, frequency):
    """
    generate a sine wave list of length SIZE.
    """
    data = bytes(0)
    omega = math.pi * 2 * frequency
    current_step = 0
    for index in numpy.arange(0, size, 1/rate):
        wave = 0
        wave += math.sin(index * omega) # generate waveform
        wave *= 2 ** 15 - 1
        wave = int(wave)
        data += wave.to_bytes(2, sys.byteorder, signed=True)
        current_step += 1/rate
    omega = math.pi * 2 * frequency * 2

    return data


rate = 44100
one = gen_signal(dit_time, freq0)
zero = gen_signal(dit_time, freq1)
off = gen_signal(dit_time, 0)
recording = bytes(0)
for char in sys.argv[1]:
    char = bin(ord(char))
    for indicator in char:
        if indicator == "1":
            recording += one
        if indicator == "0":
            recording += zero
    recording += off # end of letter
audio = simpleaudio.play_buffer(recording, 1, 2, rate)
audio.wait_done()
wav = wave.open("test.wav", "w")
wav.setframerate(rate)
wav.setnchannels(1)
wav.setsampwidth(2)
wav.writeframes(recording)