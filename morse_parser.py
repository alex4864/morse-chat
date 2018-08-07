import re
import numpy as np
from audio_generator import generate_tone, generate_silence

CODE = {'A': '.-',     'B': '-...',   'C': '-.-.',
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
        'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',

        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.'
        }

def insert_pipe(matchObject):
	return matchObject.group(1) + '|' + matchObject.group(2)

def string_to_code(inputString):
	inputString = inputString.upper()
	code = ''
	for char in inputString:
		if (char >= 'A' and char <= 'Z') or (char >= '0' and char <= '9'):
			code += CODE[char] + '_'
		elif (char == ' '):
			code += ' '

	# python regex doesn't allow overlaps, so this is run in a loop to catch everything
	while re.search('[.-][.-]', code):
		code = re.sub('([.-])([.-])', insert_pipe, code)

	return code

def code_to_audio(inputCode, frequency, dot_length):
	DOT = generate_tone(frequency, dot_length)
	DASH = generate_tone(frequency, dot_length * 3)
	ELEMENT_PAUSE = generate_silence(dot_length)
	CHARACTER_PAUSE = generate_silence(dot_length * 3)
	WORD_PAUSE = generate_silence(dot_length * 7)

	audio = generate_silence(.1)
	for char in inputCode:
		if char == '.':
			audio = np.append(audio, DOT)
		elif char == '-':
			audio = np.append(audio, DASH)
		elif char == '|':
			audio = np.append(audio, ELEMENT_PAUSE)
		elif char == '_':
			audio = np.append(audio, CHARACTER_PAUSE)
		elif char == ' ':
			audio = np.append(audio, WORD_PAUSE)

	return audio