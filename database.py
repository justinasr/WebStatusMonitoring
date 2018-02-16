import sqlite3
import datetime

"""
Create table
CREATE TABLE check_log (
    target_id VARCHAR(64),
    url VARCHAR(255),
    code INTEGER,
    date DATETIME
);
"""


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Database:
    def __init__(self, filename='Database.db'):
        self.filename = filename

    def get_connection(self):
        conn = sqlite3.connect(self.filename)
        return conn

    def get_entries_for_target(self, target_id):
        conn = self.get_connection()
        conn.row_factory = dict_factory
        c = conn.cursor()
        t = (target_id,)
        c.execute('SELECT * FROM check_log WHERE target_id=? ORDER BY date DESC', t)
        result = c.fetchall()
        conn.close()
        return result

    def get_all_targets_entries(self, limit=20):
        conn = self.get_connection()
        conn.row_factory = dict_factory
        c = conn.cursor()
        t = (limit,)
        c.execute('SELECT * FROM check_log ORDER BY date DESC LIMIT ?', t)
        result = c.fetchall()
        conn.close()
        return result

    def add_entry_for_target(self, target):
        conn = self.get_connection()
        c = conn.cursor()
        t = (target['target_id'], target['url'], target['code'], datetime.datetime.now())
        c.execute('INSERT INTO check_log VALUES (?, ?, ?, ?)', t)
        conn.commit()
        conn.close()
