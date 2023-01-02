from IO import read_songcsv
import argparse
from classes import Song
from utils import Voicings, full_chord_regex

def main(song_path: str, repeats: int, voicing: int, **kwargs):
    print('analyzing: ', song_path)
    songdf = read_songcsv(song_path)
    print('song dataframe:', songdf)
    songdf.reset_index()
    song = Song(songdf, list(Voicings)[voicing])
    song.export_to_midi(song_path, instruments=['chords', 'bass'], repeats=repeats)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--song_path', type=str, required=True)
    parser.add_argument('--repeats', type=int, default=1)
    parser.add_argument('--voicing', type=int, choices=range(len(list(Voicings))), default=0)
    args = parser.parse_args()
    conf = vars(args)
    main(**conf)