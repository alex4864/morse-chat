import numpy as np

def generate_tone(frequency, duration):
	fs = 44100  # sampling rate, Hz, must be integer

	# generate samples, note conversion to float32 array
	samples = ((np.sin(2 * np.pi * np.arange(fs * duration) * frequency / fs)) * 127 + 128).astype(np.byte)
	return samples

def generate_silence(duration):
	fs = 44100
	samples = np.full(int(fs * duration), 0).astype(np.byte)
	return samples
