from dataclasses import dataclass
from enum import Enum, auto
import re
from typing import List

GLOBAL_TUNING = 21 # corresponds to midi A0

class Voicings(Enum):
    Rootless = {'root': None, 'third': 0, 'fifth': None, 'seventh': 0}
    Standard = {'root': 0, 'third': 0, 'fifth': 0, 'seventh': 0}
    Classic10 = {'root': -1, 'third': 0, 'fifth': None, 'seventh': 0}
    Inversion1 = {'root': 1, 'third': 0, 'fifth': 0, 'seventh': 0}
    Inversion2 = {'root': 1, 'third': 1, 'fifth': 0, 'seventh': 0}
    Inversion3 = {'root': 1, 'third': 1, 'fifth': 1, 'seventh': 0}

class Accents(Enum):
    Swing4_1 = [1,4]
    Swing4_2 = [0,3]

class Bass_Targets(Enum):
    ToFifth = ['root', 'fifth']
    ToThird = ['root', 'third']

class Scales(Enum):
    GREGORIAN = [0,2,4,5,7,9,11]
    HARMONIC = [0,2,3,5,7,8,11]
    MELODIC = [0,2,3,5,7,9,11]
    DIMINISHED = [0,2,3,5,6,8,9,11]
    WHOLE = [0,2,4,6,8,10]

twofiveoneintervals = [7, 7]

MINOR_THIRD_SYMBOLS = '-om'
MAJOR_THIRD_SYMBOLS = '+j'

# TODO add altered chords

chroma = '([A-G])'
accidental = '(b|#)?'
polarity = '(-|\+|o|j|sus|m)?'
seventh = '(j7|7)?'
fifth = '(b5)?'
sixth = '(6)?'
ninth = '(9b|9#|9)?'
eleventh = '(11#|11)?'
thirteenth = '(13b|13)?'
tensions = seventh+fifth+sixth+ninth+eleventh+thirteenth
CHORD_REGEX = re.compile(chroma+accidental+polarity+tensions)

class Chord_Types(Enum):
    Major = 0
    Minor = 1
    Diminished = 2
    Half_Diminished = 3
    Dominant = 4

class Durations(Enum):
    Whole = 4.
    Half = 2.
    Quarter = 1.
    Eight = 0.5
    Sixteenth = 0.25

class Intervals(Enum):
    Unison = 0
    MinorSecond = 1
    MajorSecond = 2
    MinorThird = 3
    MajorThird = 4
    PerfectFourth = 5
    Tritone = 6
    PerfectFifth = 7
    MinorSixth = 8
    MajorSixth = 9
    MinorSeventh = 10
    MajorSeventh = 11
    Octave = 12

class Notations(Enum):
    MAJOR = 'j'
    MINOR = '-'
    AUG = '+'
    NINE = '9'
    SNINE = '9#'
    FNINE = '9b'
    SELEVEN = '11#'
    SIX = '6'
    DIM = 'o'

class Notes(Enum):
    A = 0
    Bb = 1
    B = 2
    C = 3
    Db = 4
    D = 5
    Eb = 6
    E = 7
    F = 8
    Gb = 9
    G = 10
    Ab = 11
    
class Numerals(Enum):
    I = 0
    IIb = 1
    II = 2
    IIIb = 3
    III = 4
    IV = 5
    Vb = 6
    V = 7
    VIb = 8
    VI = 9
    VIIb = 10
    VII = 11

def add_interval(note: Notes, interval: Intervals)-> Notes:
    return Notes((note.value + interval.value) % 11)

def sub_interval(note: Notes, interval: Intervals)-> Notes:
    return Notes((note.value - interval.value) % 11)

def midi_leading_tones(midi_note: int) -> List[int]:
    return [midi_note + 1, midi_note + 2, midi_note - 1, midi_note - 2]