from midiutil import MIDIFile
from utils import Chord, Voicings, RhythmicFigures, BassFigures, Song

class MidiWriter():
    def __init__(self, tempo):
        self.MidiFile = MIDIFile(numTracks=2)
        self.MidiFile.addTrackName(0, 0, "Chords")
        self.MidiFile.addTrackName(1, 0, "Bass")
        self.MidiFile.addTempo(0, 0, tempo)
        self.MidiFile.addTempo(1, 0, tempo)
        self.chordTrack = 0
        self.bassTrack = 1
        self.channel = 0
        self.volume = 100

    def WriteChords(self, song: Song, voicing: Voicings, rhythm: RhythmicFigures):
        for beat, songChord in enumerate(song.structure):
            if (songChord):
                onset = rhythm.value[beat % len(rhythm.value)]
                if (onset != None):
                    for voice, modulation in voicing.value.items():
                        if (modulation != None and songChord.chord.notes[voice]):
                            self.MidiFile.addNote(
                                track=self.chordTrack,
                                channel=self.channel,
                                pitch=57 + songChord.chord.notes[voice].value - 1 + 12 * modulation,
                                time=beat + onset,
                                duration=1,
                                volume=self.volume
                            )

    def WriteBass(self, song: Song):
        for beat, bassnote in enumerate(song.bass):
            if bassnote:
                self.MidiFile.addNote(
                    track=self.bassTrack,
                    channel=self.channel,
                    pitch=bassnote,
                    time=beat,
                    duration=1,
                    volume=self.volume
                )

    def AddBassNote(self, bassNote: int, time: int, duration: int):
        self.MidiFile.addNote(
            track=self.bassTrack,
            channel=self.channel,
            pitch=bassNote,
            time=time,
            duration=duration,
            volume=self.volume
        )

    def ExportMidi(self, title: str):
        with open(f"output/{title}.mid", "wb") as output_file:
            self.MidiFile.writeFile(output_file)