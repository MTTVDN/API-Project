from datatypes import ParseChord, Song, SongChord, Voicings, RhythmicFigures, BassFigures
from database import getSong
from midiwriter import MidiWriter
import argparse

def main(songid: int, **kwargs):
    song = Song([])
    key_index = 1 # TODO: determine key from database


    songdf, song_info, song_bassline = getSong(songid)
    songdf['duration'] = songdf['beatid'].diff().shift(-1).fillna(8).astype(int)
    songdf.reset_index()
    song_bassline.reset_index()

    mw = MidiWriter(tempo=song_info.avgtempo)

    for index, row in songdf.iterrows():
        chordString = row.chord
        newChord = ParseChord(chordString)
        newSongChord = SongChord(chord=newChord, beat=row.beatid, duration=row.duration)
        song.structure.append(newSongChord)

    for index, songChord in enumerate(song.structure):
        mw.AddChord(songChord.chord, songChord.beat, songChord.duration, Voicings.Inversion2, RhythmicFigures.Swing1)
        if (index + 1 < len(song.structure)):
            mw.AddWalkingBass(songChord.chord, song.structure[index + 1].chord, songChord.beat, songChord.duration)
        else:
            mw.AddWalkingBass(songChord.chord, songChord.chord, songChord.beat, songChord.duration)

    # for index, row in song_bassline.iterrows():
    #     mw.AddBassNote(row.bass_pitch, row.beatid, 1)

    mw.ExportMidi(song_info.title.values[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--songid', type=int, required=True)
    args = parser.parse_args()
    main(args.songid)