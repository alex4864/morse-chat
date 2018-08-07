import logging

class Decoder:

    CODE = {'A': '.-',   'B': '-...', 'C': '-.-.',
            'D': '-..',  'E': '.',    'F': '..-.',
            'G': '--.',  'H': '....', 'I': '..',
            'J': '.---', 'K': '-.-',  'L': '.-..',
            'M': '--',   'N': '-.',   'O': '---',
            'P': '.--.', 'Q': '--.-', 'R': '.-.',
            'S': '...',  'T': '-',    'U': '..-',
            'V': '...-', 'W': '.--',  'X': '-..-',
            'Y': '-.--', 'Z': '--..',

            '0': '-----', '1': '.----', '2': '..---',
            '3': '...--', '4': '....-', '5': '.....',
            '6': '-....', '7': '--...', '8': '---..',
            '9': '----.'
            }

    def __init__(self, pace, sensitivity, output_stream, resolution):
        """
        :param pace: the 'dot' length, upon which all other lengths are based
        :param sensitivity: the amplitude above which the frame is considered to be positive
        :param output_stream: stream for decoded chars to be output to
        :param resolution: time between measurements, used for tolerance calculations
        """
        self.pace = pace
        self.sensitivity = sensitivity
        self.output_stream = output_stream
        self.resolution = resolution
        self._frames = []
        self._cursor = -1
        self._char_buffer = ''

        self.elem = {
            'DOT': 1 * self.pace,
            'DASH': 3 * self.pace,
            'ELEMENT_PAUSE': 1 * self.pace,
            'CHARACTER_PAUSE': 3 * self.pace,
            'WORD_PAUSE': 7 * self.pace,
        }

        self.logger = logging.getLogger('Decoder')
        self.logger.setLevel(logging.ERROR)


    def output(self, char):
        self.output_stream.write(char)
        self.output_stream.flush()

    def push_to_buffer(self, element):
        if element == ' ':
            if len(self._char_buffer) == 0:
                return

            try:
                self.output(self.decode_char(self._char_buffer) + ' ')
            except self.DecodingException as e:
                self.logger.warning(e)

            self._char_buffer = ''
        elif element == '_':
            try:
                self.output(self.decode_char(self._char_buffer))
            except self.DecodingException as e:
                self.logger.warning(e)

            self._char_buffer = ''
        else:
            self._char_buffer += element


    def decode_char(self, sequence):
        code = sequence.replace('|', '')
        for char in self.CODE:
            if self.CODE[char] == code:
                return char

        raise self.DecodingException('Sequence {} not understood'.format(code))


    def add_frame(self, amplitude, time):
        if len(self._frames) == 0:
            self._frames.append({'value': amplitude > self.sensitivity, 'time': time})
            self._cursor = 0
            return

        self._frames.append({'value': amplitude > self.sensitivity, 'time': time})
        if self._frames[-1]['value'] != self._frames[-2]['value']:
            try:
                element = self.decode_element(self._frames[self._cursor:-1])
                self.push_to_buffer(element)
            except self.DecodingException as e:
                self.logger.warning(e)
            self._cursor = len(self._frames) - 1

        #if self._frames[-1]['time'] - self._frames[self._cursor]['time'] > self.elem['WORD_PAUSE'] + self.pace:
        #    if self._frames[-1]['value']:
        #        raise self.DecodingException('Positive signal detected for too long, possible interference')
        #    else:
        #        self.push_to_buffer(' ')


    # TODO: Clean this up a bit, and remove hardcoding on resolution
    def decode_element(self, frames):
        positive = all( [f['value'] for f in frames] )

        duration = frames[-1]['time'] - frames[0]['time']
        tolerance = self.resolution * 4

        if positive:
            if self.elem['DOT'] - tolerance < duration < self.elem['DOT'] + tolerance:
                return '.'
            elif self.elem['DASH'] - tolerance < duration < self.elem['DASH'] + tolerance:
                return '-'
        else:
            if self.elem['ELEMENT_PAUSE'] - tolerance < duration < self.elem['ELEMENT_PAUSE'] + tolerance:
                return '|'
            elif self.elem['CHARACTER_PAUSE'] - tolerance < duration < self.elem['CHARACTER_PAUSE'] + tolerance:
                return '_'
            elif self.elem['WORD_PAUSE'] - tolerance < duration:
                return ' '

        raise self.DecodingException('Element Signature <{}, {}> not recognized'.format(positive, duration))


    class DecodingException(Exception):
        def __init__(self, *args, **kwargs):
            Exception.__init__(self, *args, **kwargs)