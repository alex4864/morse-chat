import pyaudio
from time import time
import numpy as np
from signal_processing import detect_frequency
from decoder import Decoder
import sys


fs = 44100
CHUNKSIZE = 128
SENSITIVITY = 1500
PACE = .05

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=fs, input=True, frames_per_buffer=CHUNKSIZE)

d = Decoder(PACE, SENSITIVITY, sys.stdout, .003)
timestamps = []
start_time = time()
while time() - start_time < 100:
    timestamps.append(time())
    data = stream.read(CHUNKSIZE)
    np_data = np.fromstring(data, dtype=np.int16)
    amplitude = detect_frequency(np_data, 880.0, 44100)
    d.add_frame(amplitude, timestamps[-1])


    #print('amplitude: {}'.format(amplitude))

deltas = [timestamps[i] - timestamps[i-1] for i in range(1, len(timestamps))]
avg_delta = sum(deltas) / len(deltas)
print('Average Delta: {}'.format(avg_delta))