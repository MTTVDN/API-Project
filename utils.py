from dataclasses import dataclass
from enum import Enum, auto
import re

GLOBAL_TUNING = 21 # corresponds to midi A0

class Voicings(Enum):
    Rootless = {'root': None, 'third': 0, 'fifth': None, 'seventh': 0}
    Standard = {'root': 0, 'third': 0, 'fifth': 0, 'seventh': 0}
    Classic10 = {'root': -1, 'third': 0, 'fifth': None, 'seventh': 0}
    Inversion1 = {'root': 1, 'third': 0, 'fifth': 0, 'seventh': 0}
    Inversion2 = {'root': 1, 'third': 1, 'fifth': 0, 'seventh': 0}
    Inversion3 = {'root': 1, 'third': 1, 'fifth': 1, 'seventh': 0}

class RhythmicFigures(Enum):
    Swing4 = [0.65, None, 0., None]
    Swing8 = [0.65, None, 0., None, 0., 0.65, None, None]

class BassFigures(Enum):
    Standard2 = ['root', 'fifth']
    Standard4 = ['root', 'third', 'fifth', 'third']

class Scales(Enum):
    GREGORIAN = [1,3,5,6,8,10,12]
    HARMONIC = [1,3,4,6,8,9,12]
    MELODIC = [1,3,4,6,8,10,12]
    DIMINISHED = [1,3,4,6,7,9,10,12]
    WHOLE = [1,3,5,7,9,11]

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

class Durations(Enum):
    Whole = 4.
    Half = 2.
    Quarter = 1.
    Eight = 0.5
    Sixteenth = 0.25

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
    IIIb = 4
    III = 5
    IV = 6
    Vb = 7
    V = 8
    VIv = 9
    VI = 10
    VIIb = 11
    VII = 12

# TODO: save chord notes as dict of functions (root, third, seventh etc.)
@dataclass
class Chord:
    name: str
    notes: dict[str, Notes]

@dataclass
class SongChord:
    chord: Chord
    beat: int
    duration: int

class Song:
    def __init__(self, beats):
        self.beats = beats
        self.structure: list[SongChord] = [None]*(beats+8)
        self.bass: list[int] = [None]*(beats+8)
    
    def AddChord(self, songChord: SongChord):
        self.structure[songChord.beat:songChord.beat+songChord.duration] = [songChord]*songChord.duration
    
    def AddBass(self, songChord: SongChord, figure: BassFigures, chromatic: bool = False):
        if songChord.chord.name != 'NC':
            if (chromatic):
                if (songChord.beat > 0):
                    self.bass[songChord.beat - 1] = 33 + songChord.chord.notes['root'].value - 2

            for beat in range(songChord.duration):
                function = figure.value[beat % len(figure.value)]
                self.bass[songChord.beat + beat] = 33 + songChord.chord.notes[function].value - 1


def add_interval(note: Notes, interval: Intervals)-> Notes:
    return Notes((note.value + interval.value - 1) % 12 + 1)