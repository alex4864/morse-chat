import pyaudio
import time
import numpy as np
from audio_generator import generate_tone, generate_silence
from morse_parser import string_to_code, code_to_audio
from analyze_audio import fft_frequencies
from signal_processing import detect_frequency

outputCode = string_to_code('So long and thanks for all the fish')
print(outputCode)
outputAudio = code_to_audio(outputCode, 880, .05)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.get_format_from_width(1),
                channels=1,
                rate=44100,
                output=True)

# play. May repeat with different volume values (if done interactively)
stream.write(outputAudio)

stream.stop_stream()
stream.close()