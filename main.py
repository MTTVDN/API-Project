import sqlite3
import numpy
from datatypes import Chord, Notes, Numerals, CHORD_REGEX, MINOR_THIRD_SYMBOLS, MAJOR_THIRD_SYMBOLS, Intervals, AddInterval
from database import getMelody
from midiwriter import MidiWriter

twofiveone = [7, 7]

chords = []
key_index = 1 # TODO: determine key from database

mw = MidiWriter(tempo=120)

for row in getMelody(2):
    fundamental = None
    third = None
    fifth = None
    seventh = None

    chordString = row[0]

    # TODO handle NC

    re_results = CHORD_REGEX.search(chordString)
    if re_results:
        # print(g.group(1), g.group(2), g.group(3), g.group(4), g.group(5), g.group(6), g.group(7), g.group(8))
        chroma = re_results.group(1)
        accidental = re_results.group(2)
        polarity = re_results.group(3)
        seventhSymbol = re_results.group(4)
        fifthSymbol = re_results.group(5)
        sixthSymbol = re_results.group(6)
        ninthSymbol = re_results.group(7)
        eleventhSymbol = re_results.group(8)
        thirteenthSymbol = re_results.group(9)

        fundamental = Notes[chroma+accidental if accidental else chroma]
        if (polarity):
            if (polarity in MINOR_THIRD_SYMBOLS):
                third = AddInterval(fundamental, Intervals.MinorThird)
            if (polarity in MAJOR_THIRD_SYMBOLS):
                third = AddInterval(fundamental, Intervals.MajorThird)
            if (polarity == 'sus'):
                third = AddInterval(fundamental, Intervals.PerfectFourth)
        else:
            third = AddInterval(fundamental, Intervals.MajorThird)

        if (seventhSymbol):
            if (not polarity):
                seventh = AddInterval(third, Intervals.Tritone)
            elif(polarity == 'sus'):
                seventh = AddInterval(fundamental, Intervals.MinorSeventh)
            elif(seventhSymbol == 'j7'):
                seventh = AddInterval(third, Intervals.MinorSixth)
            else:
                seventh = AddInterval(third, Intervals.PerfectFifth)
        
        if (sixthSymbol):
            seventh = AddInterval(fundamental, Intervals.MajorSixth)

        if (fifthSymbol):
            fifth = AddInterval(fundamental, Intervals.Tritone)
        else:
            if (polarity == '+'):
                fifth = AddInterval(fundamental, Intervals.MinorSixth)
            else: 
                fifth = AddInterval(fundamental, Intervals.PerfectFifth)
                
        newChord = Chord(chordString, [fundamental, third, fifth, seventh])
        chords.append(newChord)


chroma_numbers = []

time = 0
for chord in chords:
    mw.AddChord(chord, time, 4)
    time += 4

mw.ExportMidi()

# intervals = [0]
# for i in range(len(chroma_numbers) - 1):
#     intervals.append((12 - chroma_numbers[i+1] + chroma_numbers[i]) % 12)

# twofiveone_occurences = []

# for i in range(len(intervals)):
#     if intervals[i:i+len(twofiveone)] == twofiveone:
#         twofiveone_occurences.append((i-1, i+len(twofiveone)-1))

# print(twofiveone_occurences)

# chord_numerals = [Numerals(i).name for i in chroma_numbers]
# for idx, chord in enumerate(chords):
#     print(chord, chord_numerals[idx])