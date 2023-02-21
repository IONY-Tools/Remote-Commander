import sqlite3

class DBConnection:
    def __init__(self, filename):
        self.db = sqlite3.connect(filename)

    def exec(self, sql, commit=False):
        result = self.db.cursor.execute(sql)
        if commit == True:
            self.db.commit()
        return result