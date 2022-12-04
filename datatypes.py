from dataclasses import dataclass
from enum import Enum, auto
import re

class Voicings(Enum):
    Rootless = {'root': None, 'third': 0, 'fifth': None, 'seventh': 0}
    Standard = {'root': 0, 'third': 0, 'fifth': 0, 'seventh': 0}
    Classic10 = {'root': 0, 'third': 1, 'fifth': None, 'seventh': 0}
    Inversion1 = {'root': 1, 'third': 0, 'fifth': 0, 'seventh': 0}
    Inversion2 = {'root': 1, 'third': 1, 'fifth': 0, 'seventh': 0}
    Inversion3 = {'root': 1, 'third': 1, 'fifth': 1, 'seventh': 0}

class RhythmicFigures(Enum):
    Swing1 = [0.65, 2., 4.65, 6.]

class BassFigures(Enum):
    Standard2 = ['root']
    Standard4 = ['root', 'fifth', 'root']
    Standard8 = ['root', 'third', 'fifth', 'third', 'root', 'third', 'fifth']

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

@dataclass 
class Song:
    structure: list[SongChord]

def AddInterval(note: Notes, interval: Intervals)-> Notes:
    newNote = note.value + interval.value
    if newNote > 12:
        newNote -= 12
    return Notes(newNote)


# TODO handle NC
def ParseChord(chordString: str) -> Chord:
    root = None 
    third = None
    fifth = None
    seventh = None

    if (chordString == 'NC'):
        return Chord('NC', {'root': None, 'third': None, 'fifth': None, 'seventh': None})

    re_results = CHORD_REGEX.search(chordString)
    if re_results:
        chroma = re_results.group(1)
        accidental = re_results.group(2)
        polarity = re_results.group(3)
        seventhSymbol = re_results.group(4)
        fifthSymbol = re_results.group(5)
        sixthSymbol = re_results.group(6)
        ninthSymbol = re_results.group(7)
        eleventhSymbol = re_results.group(8)
        thirteenthSymbol = re_results.group(9)

        if (accidental):
            root = Notes[chroma+accidental] if accidental == 'b' else AddInterval(Notes[chroma], Intervals.MinorSecond)
        else:
            root = Notes[chroma]

        if (polarity):
            if (polarity in MINOR_THIRD_SYMBOLS):
                third = AddInterval(root, Intervals.MinorThird)
            if (polarity in MAJOR_THIRD_SYMBOLS):
                third = AddInterval(root, Intervals.MajorThird)
            if (polarity == 'sus'):
                third = AddInterval(root, Intervals.PerfectFourth)
        else:
            third = AddInterval(root, Intervals.MajorThird)

        if (seventhSymbol):
            if (not polarity):
                seventh = AddInterval(third, Intervals.Tritone)
            elif(polarity == 'sus'):
                seventh = AddInterval(root, Intervals.MinorSeventh)
            elif(seventhSymbol == 'j7'):
                seventh = AddInterval(third, Intervals.MinorSixth)
            else:
                seventh = AddInterval(third, Intervals.PerfectFifth)
        
        if (sixthSymbol):
            seventh = AddInterval(root, Intervals.MajorSixth)

        if (fifthSymbol):
            fifth = AddInterval(root, Intervals.Tritone)
        else:
            if (polarity == '+'):
                fifth = AddInterval(root, Intervals.MinorSixth)
            else: 
                fifth = AddInterval(root, Intervals.PerfectFifth)

        newChord = Chord(chordString, {'root': root, 'third': third, 'fifth': fifth, 'seventh': seventh})
        return newChord