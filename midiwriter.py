from midiutil import MIDIFile
from datatypes import Chord

class MidiWriter():
    def __init__(self, tempo):
        self.MidiFile = MIDIFile(1)
        self.MidiFile.addTempo(0, 0, tempo)
        self.track = 0
        self.channel = 0
        self.volume = 100

    def AddChord(self, chord: Chord, time: int, duration: int):
        for note in chord.notes:
            self.MidiFile.addNote(
                track=self.track,
                channel=self.channel,
                pitch=57 + note.value - 1,
                time=time,
                duration=duration,
                volume=self.volume
            )
        return

    def ExportMidi(self):
        with open("output/chords.mid", "wb") as output_file:
            self.MidiFile.writeFile(output_file)