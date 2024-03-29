from midiutil import MIDIFile
from typing import List

class MidiWriter():
    # creates the number of specified instruments
    # chord and bass track id are 0 and 1 by default
    def __init__(self, tempo, instruments: List[str]):
        self.instruments = instruments
        self.MidiFile = MIDIFile(numTracks=len(instruments))
        for idx, instrument in enumerate(instruments):
            self.MidiFile.addTrackName(idx, 0, instrument)
            self.MidiFile.addTempo(idx, 0, tempo)
        self.chord_track = 0
        self.bass_track = 1
        self.channel = 0
        self.volume = 100

    # write notes to chord track
    def write_chord(self, chord: List[int], beat: float, duration: float):
        for note in chord:
            self.MidiFile.addNote(
                track=self.chord_track,
                channel=self.channel,
                pitch=note,
                time=beat,
                duration=duration,
                volume=self.volume
            )
    
    # write bass notes to bass track (sequentially)
    def write_bass(self, bass_line, start_beat: float, duration: float):
        if 'bass' not in self.instruments:
            print('Warning: no bass track specified')
            return
        
        for note in bass_line:
            self.MidiFile.addNote(
                track=self.bass_track,
                channel=self.channel,
                pitch=note[0],
                time=start_beat + note[1],
                duration=duration,
                volume=self.volume
            )

    def export_midi(self, title: str):
        with open(f"{title}.mid", "wb") as output_file:
            self.MidiFile.writeFile(output_file)