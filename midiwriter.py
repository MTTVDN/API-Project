from midiutil import MIDIFile
from utils import Voicings, Accents, BassFigures
from typing import List

class MidiWriter():
    def __init__(self, tempo, instruments: List[str]):
        self.MidiFile = MIDIFile(numTracks=len(instruments))
        for idx, instrument in enumerate(instruments):
            self.MidiFile.addTrackName(idx, 0, instrument)
            self.MidiFile.addTempo(idx, 0, tempo)
        self.chordTrack = 0
        self.bassTrack = 1
        self.channel = 0
        self.volume = 100

    def write_chord(self, chord: List[int], beat: float, duration: float):
        for note in chord:
            self.MidiFile.addNote(
                track=self.chordTrack,
                channel=self.channel,
                pitch=note,
                time=beat,
                duration=duration,
                volume=self.volume
            )
    
    def write_bass():
        raise NotImplementedError

    def export_midi(self, title: str):
        with open(f"output/{title}.mid", "wb") as output_file:
            self.MidiFile.writeFile(output_file)