import pyaudio
import time
import numpy as np
from audio_generator import generate_tone, generate_silence
from morse_parser import string_to_code, code_to_audio
from analyze_audio import fft_frequencies
from signal_processing import detect_frequency

fs = 44100
CHUNKSIZE = 1024

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=fs, input=True, frames_per_buffer=CHUNKSIZE)

while True:
    data = stream.read(CHUNKSIZE)
    np_data = np.fromstring(data, dtype=np.int16)
    amplitude = detect_frequency(np_data, 880.0, 44100)

    print('amplitude: {}'.format(amplitude))

"""
outputCode = string_to_code('Justin has a small penis')
print(outputCode)
outputAudio = code_to_audio(outputCode, 880, .1)
stream = p.open(format=pyaudio.get_format_from_width(1),
                channels=1,
                rate=44100,
                output=True)

# play. May repeat with different volume values (if done interactively)
stream.write(outputAudio)

stream.stop_stream()
stream.close()
"""

p.terminate()