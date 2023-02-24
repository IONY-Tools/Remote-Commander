import sqlite3

def DBConnection(filename):
    return sqlite3.connect(filename)