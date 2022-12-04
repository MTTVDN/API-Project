from midiutil import MIDIFile
from datatypes import Chord, Voicings, RhythmicFigures, BassFigures

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

    def AddChord(self, chord: Chord, time: int, duration: int, voicing: Voicings, rhythm: RhythmicFigures):
        for accent in rhythm.value:
            if accent < duration:
                for voice, modulation in voicing.value.items():
                    if (modulation != None and chord.notes[voice]):
                        self.MidiFile.addNote(
                            track=self.chordTrack,
                            channel=self.channel,
                            pitch=57 + chord.notes[voice].value - 1 + 12 * modulation,
                            time=time + accent,
                            duration=1,
                            volume=self.volume
                        )
        return

    def AddWalkingBass(self, chord: Chord, nextChord: Chord, time: int, duration: int):
        bassFigure = BassFigures.Standard4
        if (duration == 2):
            bassFigure = bassFigure.Standard2
        elif (duration == 4):
            bassFigure = bassFigure.Standard4
        elif (duration == 8):
            bassFigure = bassFigure.Standard8

        if (chord.name != 'NC'):
            for beat, bassnote in enumerate(bassFigure.value):
                self.MidiFile.addNote(
                    track=self.bassTrack,
                    channel=self.channel,
                    pitch=45 + chord.notes[bassnote].value - 1,
                    time=time + beat,
                    duration=1,
                    volume=self.volume
                )
            self.MidiFile.addNote(
                track=self.bassTrack,
                channel=self.channel,
                pitch=45 + nextChord.notes['root'].value - 2,
                time=time + duration - 1,
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