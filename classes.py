from typing import List
from utils import CHORD_REGEX, add_interval, Notes, MINOR_THIRD_SYMBOLS, MAJOR_THIRD_SYMBOLS, Intervals, Voicings, GLOBAL_TUNING, Accents, Durations, Chord_Types
from midiwriter import MidiWriter
import pandas as pd
import random
import math

class Chord:
    def __init__(self, chord_string: str, voicing: Voicings = Voicings.Standard, octave: int = 3):
        self.name = chord_string
        self.root, self.notes, self.chord_class = self.parse_chord(chord_string)
        self.voicing = voicing
        self.reference_pitch = GLOBAL_TUNING + octave * 12
        self.function = None
        return

    def parse_chord(self, chord_string: str):
        chord_notes = {'root': None, 'third': None, 'fifth': None, 'seventh': None}
        chord_class = None

        if (chord_string == 'NC'):
            return 0, chord_notes, chord_class

        re_results = CHORD_REGEX.search(chord_string)
        if re_results:
            chroma = re_results.group(1)
            accidental = re_results.group(2)
            polarity = re_results.group(3)
            seventh_symbol = re_results.group(4)
            fifth_symbol = re_results.group(5)
            sixth_symbol = re_results.group(6)
            ninth_symbol = re_results.group(7)
            eleventh_symbol = re_results.group(8)
            thirteenth_symbol = re_results.group(9)

            chord_notes['root'] = Intervals.Unison

            if (accidental):
                root = Notes[chroma+accidental] if accidental == 'b' else add_interval(Notes[chroma], Intervals.MinorSecond)
            else:
                root = Notes[chroma]

            third_interval = None
            if (polarity):
                if (polarity in MINOR_THIRD_SYMBOLS):
                    third_interval = Intervals.MinorThird
                    chord_class = Chord_Types.Minor
                if (polarity in MAJOR_THIRD_SYMBOLS):
                    third_interval = Intervals.MajorThird
                    chord_class = Chord_Types.Major
                if (polarity == 'sus'):
                    third_interval = Intervals.PerfectFourth
                    chord_class = Chord_Types.Dominant
            else:
                third_interval = Intervals.MajorThird
            chord_notes['third'] = third_interval


            seventh_interval = None
            if seventh_symbol:
                if (not polarity):
                    seventh_interval = Intervals(third_interval + Intervals.Tritone.value)
                    chord_class = Chord_Types.Dominant
                elif(polarity == 'sus'):
                    seventh_interval = Intervals.MinorSeventh
                elif(polarity == 'o'):
                    seventh_interval = Intervals.MajorSixth
                    chord_class = Chord_Types.Diminished
                elif(seventh_symbol == 'j7'):
                    seventh_interval = Intervals.MajorSeventh
                else:
                    seventh_interval = Intervals(third_interval + Intervals.PerfectFifth.value)
            chord_notes['seventh'] = seventh_interval

            if sixth_symbol:
                chord_notes['seventh'] = Intervals.MajorSixth

            fifth_interval = None
            if fifth_symbol:
                fifth_interval = Intervals.Tritone
                chord_class = Chord_Types.Half_Diminished
            else:
                if (polarity == '+'):
                    fifth_interval = Intervals.MinorSixth
                elif (polarity == 'o'):
                    fifth_interval = Intervals.Tritone
                else: 
                    fifth_interval = Intervals.PerfectFifth
            chord_notes['fifth'] = fifth_interval

            ninth_interval = None
            if ninth_symbol:
                if (ninth_symbol == '9b'):
                    ninth_interval = Intervals.MinorSecond
                elif (ninth_symbol == '9#'):
                    ninth_interval = Intervals.MinorThird
                elif (ninth_symbol == '9'):
                    ninth_interval = Intervals.MajorSecond
            chord_notes['ninth'] = ninth_interval

            eleventh_interval = None
            if eleventh_symbol:
                if (eleventh_symbol == '11#'):
                    eleventh_interval = Intervals.Tritone
                elif (eleventh_symbol == '11'):
                    eleventh_interval == Intervals.PerfectFourth
            chord_notes['eleventh'] = eleventh_interval

            thirteenth_interval = None
            if thirteenth_symbol:
                if (thirteenth_symbol == '13b'):
                    thirteenth_interval = Intervals.MinorSixth
                elif (thirteenth_symbol == '13'):
                    thirteenth_interval == Intervals.MajorSixth
            chord_notes['thirteenth'] = thirteenth_interval

            return root, chord_notes

    def set_voicing(self, voicing: Voicings):
        self.voicing = voicing

    def midi_notes(self) -> List[int]:
        midi_root = self.reference_pitch + self.root.value
        notes = []
        for function, interval in self.notes.items():
            if self.voicing.value[function] != None and interval != None:
                notes.append(midi_root + interval.value + self.voicing.value[function] * 12)
        return notes

    def print_info(self):
        print('name: ', self.name)
        print('notes: ', self.notes)
        print('type: ', self.chord_class)
        print('midi: ', self.midi_notes())

    def preview_chord(self):
        raise NotImplementedError

class Bar:
    def __init__(self, beats: int, tempo: int, swing: bool = False, swing_percentage: float = 0.65):
        self.beat_chords = [Chord('NC')] * beats
        self.swing_percentage = swing_percentage
        self.beats = beats
        self.accents = []
    
    def set_accent(self, eight: int, swing: bool = False):
        position = eight/2 + swing * self.swing_percentage/2 * int(eight % 2)
        self.accents.append(position)
        return

    def set_accents(self, eights: List[int], swing: bool = False):
        for eight in eights:
            self.set_accent(eight, swing)

    def set_accent_freely(self, beat: float):
        if (beat < len(self.beat_chords)):
            self.accents.append(beat)

    def set_chord(self, chord: Chord, beat: int):
        self.beat_chords[beat] = chord

    def set_chords(self, chords: List[Chord], beats: List[int]):
        ratio = len(beats) // len(chords)
        for idx, beat in enumerate(beats):
            self.set_chord(chords[idx // ratio], beat)

class Song:
    def __init__(self, songdf: pd.DataFrame):
        self.bars = [None] * (songdf.bar.max() + 1)
        self.tempo = songdf['tempo'].iloc[0]
        song_bars = songdf.groupby('bar')
        for name, bar_group in song_bars:
            bar_beats = bar_group.beats.iloc[0]
            bar_tempo = bar_group.tempo.iloc[0]
            bar_swing = bar_group.feel.iloc[0] == 'swing'
            new_bar = Bar(beats=bar_beats, tempo=bar_tempo, swing=bar_swing)

            chords = []
            for index, bar_row in bar_group.iterrows():
                chord_string = bar_row.chord
                print(chord_string)
                chords.append(Chord(chord_string))

            new_bar.set_chords(chords, beats=range(bar_beats))
            accent = random.choice(list(Accents)).value
            # accent = Accents.Swing4_1.value
            new_bar.set_accents(accent, swing=bar_swing)
            self.bars[name] = new_bar

    # Add instruments?
    def export_to_midi(self, target: str, instruments: List[str], repeats: int = 1):
        mw = MidiWriter(tempo=self.tempo, instruments=instruments)
        current_bar = 0
        for bar in (self.bars * repeats):
            for accent in bar.accents:
                chord = bar.beat_chords[math.floor(accent)]
                chord.print_info()
                midi_chord = chord.midi_notes()
                mw.write_chord(chord=midi_chord, beat=current_bar + accent, duration=Durations.Eight.value)
            current_bar += bar.beats
        
        mw.export_midi(target)
