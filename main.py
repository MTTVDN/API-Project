from utils import SongChord, Voicings, RhythmicFigures, BassFigures
from IO import read_songcsv
from midiwriter import MidiWriter
import argparse
from classes import Song

def main(song_path: str, **kwargs):
    # TODO: determine key
    print(song_path)
    songdf = read_songcsv(song_path)
    print(songdf)
    songdf.reset_index()
    song = Song(songdf)

    exit()

    mw = MidiWriter(tempo=song_info.avgtempo)

    for index, row in songdf.iterrows():
        chordString = row.chord
        newChord = ParseChord(chordString)
        newSongChord = SongChord(chord=newChord, beat=row.beatid, duration=row.duration)
        song.AddChord(newSongChord)
        song.AddBass(newSongChord, BassFigures.Standard4, chromatic=chromatic_bassline)

    mw.WriteChords(song, Voicings.Standard, RhythmicFigures.Swing8)
    mw.WriteBass(song)

    mw.ExportMidi(song_info.title.values[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--song_path', type=str, required=True)
    parser.add_argument('--chromatic_bassline', type=bool, default=False)
    parser.add_argument('--repeats', type=int)
    # parser.add_argument('--bassfigure', choices=['standard2', 'standard4', 'random'], required=True)
    args = parser.parse_args()
    conf = vars(args)
    main(**conf)