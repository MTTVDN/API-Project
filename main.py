from IO import read_songcsv
import argparse
from classes import Song

def main(song_path: str, repeats: int, **kwargs):
    print(song_path)
    songdf = read_songcsv(song_path)
    print(songdf)
    songdf.reset_index()
    song = Song(songdf)
    song.export_to_midi(song_path, instruments=['chords', 'bass'], repeats=repeats)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--song_path', type=str, required=True)
    parser.add_argument('--chromatic_bassline', type=bool, default=False)
    parser.add_argument('--repeats', type=int, default=1)
    args = parser.parse_args()
    conf = vars(args)
    main(**conf)