import sqlite3
import pandas as pd
import numpy as np

datatypes = {'bar': np.int8, 'beats': np.int8, 'division': np.int8, 'tempo': np.int8, 'feel': str, 'swing_percentage': float}

def read_songcsv(path: str):
    song = pd.read_csv(path, header=0)
    song = song.fillna(method='ffill')
    song = song.astype(datatypes)
    return song