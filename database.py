import sqlite3
import pandas as pd


# TODO close connection?

def getSong(id: int):
    db = sqlite3.connect("data/wjazzd.db")
    song_info = pd.read_sql_query(f"SELECT title, avgtempo, rhythmfeel, key FROM solo_info WHERE melid=={id};", db)
    song_basseline = pd.read_sql_query(f"SELECT bass_pitch, beatid FROM beats WHERE melid=={id};", db)
    song = pd.read_sql_query(f"SELECT chord, beatid FROM beats WHERE melid=={id} AND chord > '';", db)
    song_basseline.beatid = song_basseline.beatid - song_basseline.beatid[0]
    song.beatid = song.beatid - song.beatid[0]
    return song, song_info, song_basseline

