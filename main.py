import sqlite3
import numpy
from datatypes import Chord, Notes, Numerals, CHORD_REGEX, MINOR_THIRD_SYMBOLS, Intervals, AddInterval
from database import getMelody

twofiveone = [7, 7]

chords = list[Chord]
key_index = 1 # TODO: determine key from database

for row in getMelody(1):
    fundamental = None
    third = None
    fifth = None
    seventh = None

    chordString = row[0]
    re_results = CHORD_REGEX.search(chordString)
    if re_results:
        # print(g.group(1), g.group(2), g.group(3), g.group(4), g.group(5), g.group(6), g.group(7), g.group(8))
        chroma = re_results.group(1)
        accidental = re_results.group(2)
        polarity = re_results.group(3)
        seventh = re_results.group(4)
        fifth = re_results.group(5)
        ninth = re_results.group(6)
        eleventh = re_results.group(7)
        thirteenth = re_results.group(8)

        fundamental = Notes[chroma+accidental if accidental else chroma]
        print(polarity)
        third = None
        if (polarity):
            if (polarity in MINOR_THIRD_SYMBOLS):
                third = AddInterval(fundamental, Intervals.MinorThird)
        else:
            third = AddInterval(fundamental, Intervals.MajorThird)
            seventh = AddInterval(fundamental, Intervals.MinorSeventh)

        # print(chroma, accidental, polarity)
        # print(fundamental, third, fifth, seventh)


    # number = Notes[fundamental].value - key_index
    # if chordString[1] == 'b':
    #     number -= 1
    # elif chordString[1] == '#':
    #     number += 1
    # chroma_numbers.append(number % 12)
    # if (len(chord) > 0):
    #     chords.append(chord)

chroma_numbers = []


for chord in chords:
    number = Notes[chord[0]].value - key_index
    if chord[1] == 'b':
        number -= 1
    elif chord[1] == '#':
        number += 1
    chroma_numbers.append(number % 12)

intervals = [0]
for i in range(len(chroma_numbers) - 1):
    intervals.append((12 - chroma_numbers[i+1] + chroma_numbers[i]) % 12)

twofiveone_occurences = []

for i in range(len(intervals)):
    if intervals[i:i+len(twofiveone)] == twofiveone:
        twofiveone_occurences.append((i-1, i+len(twofiveone)-1))

print(twofiveone_occurences)

chord_numerals = [Numerals(i).name for i in chroma_numbers]
for idx, chord in enumerate(chords):
    print(chord, chord_numerals[idx])