from dataclasses import dataclass
from enum import Enum, auto
import re

GREGORIAN = [1,3,5,6,8,10,12]
HARMONIC = [1,3,4,6,8,9,12]
MELODIC = [1,3,4,6,8,10,12]
DIMINISHED = [1,3,4,6,7,9,10,12]
WHOLE = [1,3,5,7,9,11]

MINOR_THIRD_SYMBOLS = '-om'

chroma = '([A-G])'
accidental = '(b|#)?'
polarity = '(-|\+|o|j|sus|m)?'
tensions = '(j7|7)?(b5)?(9b|9#|9)?(11#|11)?(13b|13)?'
CHORD_REGEX = re.compile(chroma+accidental+polarity+tensions)

class Intervals(Enum):
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
    A = 1
    Bb = 2
    B = 3
    C = 4
    Db = 5
    D = 6
    Eb = 7
    E = 8
    F = 9
    Gb = 10
    G = 11
    Ab = 12
    
class Numerals(Enum):
    I = 1
    IIb = 2
    II = 3
    III = 4
    IVb = 5
    IV = 6
    Vb = 7
    V = 8
    VIv = 9
    VI = 10
    VIIb = 11
    VII = 12

@dataclass
class Chord:
    notes: list[Notes]

def AddInterval(note: Notes, interval: Intervals):
    return Notes(max((note.value + interval.value) % 13, 1))