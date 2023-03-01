import sqlite3
import os

print(os.getcwd())

def DBConnection(filename):
    return sqlite3.connect(filename, check_same_thread=False)