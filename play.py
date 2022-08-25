import numpy
import sys
import math
import simpleaudio
from dit_time import dit_time, frequency

def gen_signal(size: int):
    """
    generate a sine wave list of length SIZE.
    """
    data = bytes(0)
    omega = math.pi * 2 * frequency
    current_step = 0
    for index in numpy.arange(0, size, 1/rate):
        wave = math.sin(index * omega) # generate waveform
        wave *= 2 ** 15 - 1
        wave = int(wave)
        data += wave.to_bytes(2, sys.byteorder, signed=True)
        current_step += 1/rate

    return data


MORSE_CODE_DICT = {'A': '.-', 'B': '-...',
                   'C': '-.-.', 'D': '-..', 'E': '.',
                   'F': '..-.', 'G': '--.', 'H': '....',
                   'I': '..', 'J': '.---', 'K': '-.-',
                   'L': '.-..', 'M': '--', 'N': '-.',
                   'O': '---', 'P': '.--.', 'Q': '--.-',
                   'R': '.-.', 'S': '...', 'T': '-',
                   'U': '..-', 'V': '...-', 'W': '.--',
                   'X': '-..-', 'Y': '-.--', 'Z': '--..',
                   '1': '.----', '2': '..---', '3': '...--',
                   '4': '....-', '5': '.....', '6': '-....',
                   '7': '--...', '8': '---..', '9': '----.',
                   '0': '-----', ', ': '--..--', '.': '.-.-.-',
                   '?': '..--..', '/': '-..-.', '-': '-....-',
                   '(': '-.--.', ')': '-.--.-', " ": " "}
rate = 8000
CODE_REVERSED = {value: key for key, value in MORSE_CODE_DICT.items()}
long = gen_signal(3 * dit_time)
short = gen_signal(dit_time)
empty_dit = bytes(int(dit_time * rate * 2))
print(len(empty_dit))
recording = bytes(0)
for char in sys.argv[1]:
    char = MORSE_CODE_DICT[char.upper()]
    for indicator in char:
        print(indicator)
        if indicator == "-":
            recording += long
        if indicator == ".":
            recording += short
        if indicator == " ":
            recording += empty_dit * 1  # space
        recording += empty_dit  # space between dits
    recording += empty_dit * 2  # space between letter
print(len(recording))
audio = simpleaudio.play_buffer(recording, 1, 2, rate)
audio.wait_done()