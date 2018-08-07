import numpy as np
import matplotlib.pyplot as plt

SAMPLE_RATE = 44100
RECORD_TIME = .5

x = np.arange(0.0, RECORD_TIME, 1.0/SAMPLE_RATE, np.float32)
test_data = np.sin(880.0 * 2.0*np.pi*x) + np.sin(500.0 * 2.0*np.pi*x)


def fft_frequencies(data):
    fft_result = np.fft.rfft(data, n=SAMPLE_RATE//100)
    frq_magnitudes = np.abs(fft_result)

    max_val = np.max(frq_magnitudes)
    peaks = []
    #for i in range(1, SAMPLE_RATE - 2):
    #    if frq_magnitudes[i] > max_val / 2 and frq_magnitudes[i] > frq_magnitudes[i - 1] and frq_magnitudes[i] > frq_magnitudes[i + 1]:
    #        peaks.append(i)

    #or p in peaks:
    #    print('Peak: {}, Value: {}'.format(p, frq_magnitudes[p]))

    plt.plot(frq_magnitudes[0:2000])
    plt.show()

    return peaks

if __name__ == '__main__':
    fft_frequencies(test_data)