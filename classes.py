from typing import List
from utils import CHORD_REGEX, add_interval, sub_interval, midi_leading_tones, Notes, MINOR_THIRD_SYMBOLS, MAJOR_THIRD_SYMBOLS, Intervals, Voicings, GLOBAL_TUNING, Accents, Durations, Chord_Types
from midiwriter import MidiWriter
import pandas as pd
import random
import math

# holds functionality concerning chords
class Chord:
    def __init__(self, chord_string: str, voicing: Voicings = Voicings.Rootless, octave: int = 3):
        self.name = chord_string
        self.root, self.notes, self.chord_class = self.parse_chord(chord_string)
        self.voicing = voicing
        self.reference_pitch = GLOBAL_TUNING + octave * 12
        self.midi_root = self.reference_pitch + self.root.value
        self.function = None
        return

    # given a chord symbol/string, determine the notes that are part of this chord
    def parse_chord(self, chord_string: str):
        print('digesting ', chord_string)
        chord_notes = {'root': None, 'third': None, 'fifth': None, 'seventh': None}
        chord_class = None

        if (chord_string == 'NC'):
            print('warning: NC is currently not supported')
            exit()

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
                    seventh_interval = Intervals(third_interval.value + Intervals.Tritone.value)
                    chord_class = Chord_Types.Dominant
                elif(polarity == 'sus'):
                    seventh_interval = Intervals.MinorSeventh
                elif(polarity == 'o'):
                    seventh_interval = Intervals.MajorSixth
                    chord_class = Chord_Types.Diminished
                elif(seventh_symbol == 'j7'):
                    seventh_interval = Intervals.MajorSeventh
                else:
                    seventh_interval = Intervals(third_interval.value + Intervals.PerfectFifth.value)
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
            else:
                ninth_interval = Intervals.MajorSecond # implicit ninth
            chord_notes['ninth'] = ninth_interval

            eleventh_interval = None
            if eleventh_symbol:
                if (eleventh_symbol == '11#'):
                    eleventh_interval = Intervals.Tritone
                elif (eleventh_symbol == '11'):
                    eleventh_interval = Intervals.PerfectFourth
            chord_notes['eleventh'] = eleventh_interval

            thirteenth_interval = None
            if thirteenth_symbol:
                if (thirteenth_symbol == '13b'):
                    thirteenth_interval = Intervals.MinorSixth
                elif (thirteenth_symbol == '13'):
                    thirteenth_interval = Intervals.MajorSixth
            chord_notes['thirteenth'] = thirteenth_interval

            return root, chord_notes, chord_class

    # set how the chord should be voiced by an instrument
    def set_voicing(self, voicing: Voicings):
        self.voicing = voicing

    # return the midi notes of the chord voicing
    def voiced_midi_notes(self) -> List[int]:
        notes = []
        for function, interval in self.notes.items():
            if self.voicing.value.get(function, None) != None and interval != None:
                notes.append(self.midi_root + interval.value + self.voicing.value.get(function, 0) * 12)
        return notes

    # return midi notes of all notes that are part of the chord
    def midi_notes(self) -> List[int]:
        notes = []
        for interval in self.notes.values():
            if interval != None:
                notes.append(self.midi_root + interval.value)
        return notes

    # return midi notes of all notes except notes that potentially clash (avoid tones)
    def safe_midi_notes(self) -> List[int]:
        notes = []
        if self.chord_class == Chord_Types.Major:
            for function, interval in self.notes.items():
                if interval != None and function != 'seventh':
                    notes.append(self.midi_root + interval.value)
        else: 
            return self.midi_notes()

    # print chord info
    def print_info(self):
        print('name: ', self.name)
        print('root: ', self.root)
        print('notes: ', self.notes)
        print('type: ', self.chord_class)
        print('midi: ', self.voiced_midi_notes())

    # placeholder for sonic preview of a chord
    def preview_chord(self):
        raise NotImplementedError

# holds the concept of a measure
class Measure:
    def __init__(self, beats: int, tempo: int, swing: bool = False, swing_percentage: float = 0.60):
        self.beat_chords = [None] * beats
        self.swing_percentage = swing_percentage
        self.beats = beats
        self.accents = []
    
    # set the moments in the bar that need to be accentuated
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

    # set the chords present in the measure
    def set_chord(self, chord: Chord, beat: int):
        self.beat_chords[beat] = chord

    def set_chords(self, chords: List[Chord], beats: List[int]):
        ratio = len(beats) // len(chords)
        for idx, beat in enumerate(beats):
            self.set_chord(chords[idx // ratio], beat)

# holds the abstract representation of the complete song (containing measures and chords)
class Song:
    # initialize all measures and chords based on song dataframe
    def __init__(self, songdf: pd.DataFrame):
        self.bars = [None] * (songdf.bar.max() + 1)
        print(songdf)
        self.tempo = songdf['tempo'].iloc[0]
        self.beat_chords: List[Chord] = []
        song_bars = songdf.groupby('bar')
        for name, bar_group in song_bars:
            print(bar_group)
            bar_beats = bar_group.beats.iloc[0]
            bar_tempo = bar_group.tempo.iloc[0]
            bar_swing = bar_group.feel.iloc[0] == 'swing'
            new_bar = Measure(beats=bar_beats, tempo=bar_tempo, swing=bar_swing)

            chords = []
            for index, bar_row in bar_group.iterrows():
                print('chord', bar_row.chord)
                chord_string = bar_row.chord
                print('this chord: ', chord_string)
                chords.append(Chord(chord_string))

            new_bar.set_chords(chords, beats=range(bar_beats))
            self.beat_chords.extend(new_bar.beat_chords)
            accent = random.choice(list(Accents)).value
            new_bar.set_accents(accent, swing=bar_swing)
            self.bars[name] = new_bar
    
    # given a chord and a preceding chord, determine in what octave the notes should be played to create smoother transitions
    def lead_voices(self, prev_chord: List[int], chord: List[int]) -> List[int]:
        new_chord = []
        voice_leads = []
        for prev_note in prev_chord:
            voice_leads.extend((prev_note, prev_note + 1, prev_note + 2, prev_note - 1, prev_note - 2))

        for note in chord:
            if note in voice_leads:
                new_chord.append(note)
            elif (note - 12) in voice_leads:
                new_chord.append(note - 12)
            elif (note + 12) in voice_leads:
                new_chord.append(note + 12)
            else:
                new_chord.append(note)
        return new_chord
  
    # given a list of chords, create a bassline that ties these chords together
    def walking_bass_line(self, chords: List[Chord], octave = -2):
        bass_notes = [None] * (len(chords) + 1)
        bass_notes[0] = chords[0].midi_root
        bass_notes[-1] = chords[-1].midi_root
        for idx, bass_note in reversed(list(enumerate(bass_notes[0:-1]))):
            print(bass_notes)
            if chords[idx].name != chords[idx - 1].name:
                bass_notes[idx] = chords[idx].midi_root # start bass of new chord on the root for more harmonic support
            else:
                chord_tones = chords[idx].safe_midi_notes()
                # if bass_notes[idx + 1] in chord_tones: chord_tones.remove(bass_notes[idx + 1])
                leading_tones = midi_leading_tones(bass_notes[idx + 1])
                # if bass_notes[idx + 1] in leading_tones: leading_tones.remove(bass_notes[idx + 1])

                random.shuffle(chord_tones)
                random.shuffle(leading_tones)
                if not idx % 2:
                    bass_notes[idx] = chord_tones[0]
                else:
                    for note in chord_tones:
                        leads = [lead for lead in leading_tones if (lead % 11 == note % 11)]
                        if len(leads):
                            bass_notes[idx] = random.choice(leads)
                            continue
                    if bass_notes[idx] == None:
                        print('no lead found')
                        bass_notes[idx] = chord_tones[0]

        print(bass_notes)
        return [note + 12 * octave for note in bass_notes]
        

    # export the song to a collection of midi tracks using the chords and walking bassline functions
    def export_to_midi(self, target: str, instruments: List[str], repeats: int = 1, voice_leading: bool = True):
        mw = MidiWriter(tempo=self.tempo, instruments=instruments)
        current_beat = 0
        prev_chord = None
        repeated_bars = self.bars * repeats
        repeated_beat_chords = self.beat_chords * repeats

        bass_line = [(note, position) for position, note in enumerate(self.walking_bass_line(repeated_beat_chords))]
        print(bass_line)
        mw.write_bass(bass_line, 0, Durations.Eight.value)

        for bar in repeated_bars:
            for accent in bar.accents:
                chord = bar.beat_chords[math.floor(accent)]
                chord.print_info()
                midi_chord = chord.voiced_midi_notes()
                if voice_leading and prev_chord:
                    midi_chord = self.lead_voices(prev_chord, midi_chord)
                mw.write_chord(chord=midi_chord, beat=current_beat + accent, duration=Durations.Eight.value)
                prev_chord = midi_chord
            current_beat += bar.beats
        
        mw.export_midi(target)
