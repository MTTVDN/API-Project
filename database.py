import sqlite3

# TODO close connection?

def getMelody(id: int):
    db = sqlite3.connect("data/wjazzd.db")
    cursor = db.cursor()
    return cursor.execute(f'SELECT chord, bar FROM beats WHERE melid=={id};')

