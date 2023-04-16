#!/Library/Frameworks/Python.framework/Versions/3.10/bin/python3.10
import scipy.io
import scipy
import scipy.fftpack
import matplotlib.pyplot
import numpy
import wave
import pyaudio
from dit_time import dit_time, frequency, harmonics_dupe

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
CODE_REVERSED = {value: key for key, value in MORSE_CODE_DICT.items()}


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

    # labels.write(f"{start_time}\t{end_time}\t{value}\n")



RATE = 44100
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
rate = RATE
bandwidth = rate//2
bin_time = dit_time / 2
BINS = 500
bin_samples = int(rate * bin_time)
stream = pyaudio.PyAudio().open(RATE, CHANNELS, FORMAT, True)
result_vales = []
times = []
on_data=[]
total_data = []
NOISE_FLOOR = 2 * (10**6) * harmonics_dupe
on = False
time_on = 0
sample_count = 0
TIME_OVERLAP = int(bin_samples * 0)
word = ""
full_text = ""
labels = ""
""" labels = open("label.txt", "w")
log: wave.Wave_write = wave.open("log.wav", "wb")
log.setnchannels(1)
log.setframerate(44100)
log.setsampwidth(2) """
print("Ready!")
try:
    while True:
        data = stream.read(bin_samples, exception_on_overflow=False)
        #log.writeframes(data)
        data = numpy.frombuffer(data, numpy.int16)
        fft_data = scipy.fftpack.fft(data, n=BINS)
        final_data = 0
        for layer in range(harmonics_dupe):
            bin_data = fft_data[get_bin(frequency * (layer + 1))] * 100
            final_data += int(abs(bin_data)) / 100
        if not on:
            total_data.append(final_data)
        time_on += bin_samples / rate
        time_on = time_on
        if final_data > NOISE_FLOOR:
            if not on:  # if signal has just turned on
                on = True
                if abs(time_on - dit_time) < dit_time:
                    write_label(sample_count, time_on, "END DIT", labels)
                elif abs(time_on - dit_time * 3) < dit_time:
                    write_label(sample_count, time_on, "END LETTER", labels)

                    if word != '' and word in CODE_REVERSED.keys():
                        full_text += CODE_REVERSED[word]
                        print(full_text[-1], end="", flush=True)
                    word = ""
                elif abs(time_on - dit_time * 7) < dit_time:
                    write_label(sample_count, time_on, "SPACE", labels)
                    if word != '' and word in CODE_REVERSED.keys():
                        full_text += CODE_REVERSED[word]
                        print(full_text[-1], end="", flush=True)
                    word = ""
                    full_text += " "
                    print(full_text[-1], end="", flush=True)
                else:
                    write_label(sample_count, time_on, "SPACE", labels)
                    if word != '' and word in CODE_REVERSED.keys():
                        full_text += CODE_REVERSED[word]
                        print(full_text[-1], end="", flush=True)
                    word = ""
                    full_text += " "
                    print(full_text[-1], end="", flush=True)


                time_on = 0
        else:  # if pause
            if on == True:  # signal has just turned off
                if time_on > dit_time * 2:
                    write_label(sample_count, time_on, "LONG", labels)
                    word += "-"
                elif time_on >= dit_time * .75:
                    write_label(sample_count, time_on, "SHORT", labels)
                    word += "."
                elif time_on < dit_time:
                    pass
                else:
                    raise Exception(
                        "everything has fallen apart at " + str(time_on))
                on = False
                time_on = 0
            else:
                if time_on > dit_time * 15:
                    write_label(sample_count, time_on, "END TRANSMISSION", labels)
                    if word != '' and word in CODE_REVERSED.keys():
                        full_text += CODE_REVERSED[word]
                        print(full_text[-1], end=" ", flush=True)
                    word = ""
                
        #NOISE_FLOOR = (sum(total_data) // len(total_data)) * 1.5
        result_vales.append(final_data)
        on_data.append(NOISE_FLOOR * on)
        sample_count += bin_samples

except KeyboardInterrupt:
    matplotlib.pyplot.plot(result_vales)
    matplotlib.pyplot.plot(on_data, "red")
    """matplotlib.pyplot.savefig("data.png")
    log.close()
    labels.flush()
    labels.close() """
    print("DONE")
