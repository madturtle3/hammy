import sys
import scipy.io
import scipy
import scipy.fftpack
import matplotlib.pyplot
import numpy
import dit_time

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
CODE_REVERSED = {value:key for key, value in MORSE_CODE_DICT.items()}

def get_bin(freq):
    frequencies_per_bin = bandwidth / BINS
    binned = int(freq // frequencies_per_bin)
    return binned + 1


full_data: numpy.ndarray
rate, full_data = scipy.io.wavfile.read(sys.argv[1])
bandwidth = rate//2
bin_time = dit_time.dit_time
BINS = 500
bin_time = int(rate * bin_time)
if len(full_data.shape) > 1:
    full_data = full_data.transpose()[0]
result_vales = []
times = []
NOISE_FLOOR = 16000
on = False
time_on = 0
full_data = full_data[rate * 2:]
TIME_OVERLAP= int(bin_time * 0)
word = ""
full_text = ""
for index in range(TIME_OVERLAP, full_data.size, bin_time):
    data = full_data[index - TIME_OVERLAP: index + bin_time]

    final_data = scipy.fftpack.fft(data, n=BINS)[get_bin(1000)] * 100
    final_data = int(abs(final_data)) / 100

    time_on += bin_time / rate
    time_on = round(time_on, 2)
    if final_data > NOISE_FLOOR:
        if not on:
            on = True
            print("space for",time_on)
            if abs(time_on - .01) < .2:
                print("END DIT")
            elif abs(time_on - .25) < .2:
                print("END LETTER")
                if word != '' and word in CODE_REVERSED.keys():
                    full_text += CODE_REVERSED[word]
                    print(full_text)
                word = ""
            else:
                print("SPACE")
                if word != '' and word in CODE_REVERSED.keys():
                    full_text += CODE_REVERSED[word]
                    print(full_text)
                word = ""
                full_text += " "
            time_on = 0
    else: # if pause
        if on == True:
            print("on for", time_on)
            if time_on > .2:
                print("LONG")
                word += "-"
            elif time_on > .05:
                print("SHORT")
                word += "."
            on = False
            time_on = 0


    result_vales.append(final_data)
if word != '' and word in CODE_REVERSED.keys():
    full_text += CODE_REVERSED[word]
    word = ""
print(full_text)
matplotlib.pyplot.plot(result_vales, "r")
matplotlib.pyplot.show()
