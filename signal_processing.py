from scipy.signal import butter, lfilter
import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import time


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def avg_amplitude(data):
    """
    pretty awful hack of a function, I'll find a better solution later
    """

    peaks = []
    for i in range(3, len(data) - 2):
        if data[i] > data[i-2] and data[i] > data[i-1] and data[i] > data[i+1] and data[i] > data[i+2]:
            peaks.append(data[i])

    return sum(peaks) / len(peaks)


def detect_frequency(data, frequency, fs):
    lowcut_frq = frequency - 20.0
    highcut_frq = frequency + 20.0

    filtered_data = butter_bandpass_filter(data, lowcut_frq, highcut_frq, fs, order=1)
    return avg_amplitude(filtered_data)
