import sqlite3
import pandas as pd

def read_songcsv(path: str):
    song = pd.read_csv(path, header=0)
    song = song.fillna(method='ffill')
    song.bar = song.bar.astype(int)
    return song