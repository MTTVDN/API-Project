from typing import List
from utils import CHORD_REGEX, add_interval, Notes, MINOR_THIRD_SYMBOLS, MAJOR_THIRD_SYMBOLS, Intervals, Voicings, GLOBAL_TUNING
import pandas as pd

class Chord:
    def __init__(self, chord_string: str, voicing: Voicings = Voicings.Standard, octave: int = 3):
        self.root, self.notes = self.parse_chord(chord_string)
        self.voicing = voicing
        self.reference_pitch = GLOBAL_TUNING + octave * 12
        return

    def parse_chord(chord_string: str):
        chord_notes = {}

        if (chord_string == 'NC'):
            return chord_notes

        re_results = CHORD_REGEX.search(chord_string)
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

            chord_notes['root'] = 0

            if (accidental):
                root = Notes[chroma+accidental] if accidental == 'b' else add_interval(Notes[chroma], Intervals.MinorSecond)
            else:
                root = Notes[chroma]

            if (polarity):
                if (polarity in MINOR_THIRD_SYMBOLS):
                    chord_notes['third'] = Intervals.MinorThird
                if (polarity in MAJOR_THIRD_SYMBOLS):
                    chord_notes['third'] = Intervals.MajorThird
                if (polarity == 'sus'):
                    chord_notes['third'] = Intervals.PerfectFourth
            else:
                chord_notes['third'] = Intervals.MajorThird

            if (seventhSymbol):
                if (not polarity):
                    chord_notes['seventh'] = Intervals.Tritone
                elif(polarity == 'sus'):
                    chord_notes['seventh'] = Intervals.MinorSeventh
                elif(seventhSymbol == 'j7'):
                    chord_notes['seventh'] = Intervals.MinorSixth
                else:
                    chord_notes['seventh'] = Intervals.PerfectFifth
            
            if (sixthSymbol):
                chord_notes['seventh'] = Intervals.MajorSixth

            if (fifthSymbol):
                chord_notes['fifth'] = Intervals.Tritone
            else:
                if (polarity == '+'):
                    chord_notes['fifth'] = Intervals.MinorSixth
                else: 
                    chord_notes['fifth'] = Intervals.PerfectFifth

            return root, chord_notes

    def set_voicing(self, voicing: Voicings):
        self.voicing = voicing

    def convert_to_midi_numbers(self):
        raise NotImplementedError

    def preview_chord(self):
        raise NotImplementedError

class Bar:
    def __init__(self, beats: int, tempo: int, swing: bool = False, swing_percentage: float = 0.65):
        self.beat_chords = [None] * beats
        self.accents = []
    
    def set_accent(self, eight: int, swing: bool = False):
        position = eight/2 + swing * self.swing_percentage * int(not (eight % 2))
        self.accents.append(position)
        return

    def set_accents(self, eights: int, swing: bool = False):
        for eight in eights:
            self.set_accent(eight, swing)

    def set_accent_freely(self, beat: float):
        if (beat < len(self.beat_chords)):
            self.accents.append(beat)

    def set_chord(self, chord: Chord, beat: int):
        self.beat_chords[beat] = Chord

    def set_chords(self, chords: List[Chord], beats: List[int]):
        ratio = len(beats) // len(chords)
        for idx, beat in enumerate(beats):
            self.set_chord(chords[idx // ratio], beat)

class Song:
    def __init__(self, songdf: pd.DataFrame):
        self.bars = [None]*(songdf.bar.max() + 1)
        song_bars = songdf.groupby('bar') 
        for name, bar_group in song_bars:
            bar_beats = bar_group.beats.iloc(0)
            bar_tempo = bar_group.tempo.iloc(0)
            bar_swing = bar_group.feel.iloc(0) == 'swing'
            new_bar = Bar(beats=bar_beats, tempo=bar_tempo, swing=bar_swing)

            chords = []
            for index, bar_row in bar_group.iterrows():
                chord_string = bar_row.chord
                chords.append(Chord(chord_string))

            new_bar.set_chords(chords, beats=range(bar_beats))
            self.bars[name] = new_bar