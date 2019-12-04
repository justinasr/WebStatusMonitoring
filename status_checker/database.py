import sqlite3
import time
import os.path
import logging


CREATE_TABLE_QUERY = """
    CREATE TABLE check_log (
        target_id VARCHAR(127),
        name VARCHAR(127),
        url VARCHAR(255),
        code INTEGER,
        timestamp INTEGER,
        response_title TEXT
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
        self.logger = logging.getLogger('logger')

    def create_database(self):
        self.logger.info('Database %s not found. Will create new.')
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute(CREATE_TABLE_QUERY)
        conn.commit()
        conn.close()

    def get_connection(self):
        if not os.path.isfile(self.filename):
            self.create_database()

        conn = sqlite3.connect(self.filename)
        conn.row_factory = dict_factory
        return conn

    def get_entries(self, target_id=None, limit=20):
        conn = self.get_connection()
        c = conn.cursor()
        query = 'SELECT target_id, name, code, timestamp, response_title FROM check_log '
        if target_id is None:
            t = (limit,)
            query += 'ORDER BY timestamp DESC LIMIT ?'
        else:
            t = (target_id, limit)
            query += 'WHERE target_id=? ORDER BY timestamp DESC LIMIT ?'

        c.execute(query, t)
        result = c.fetchall()
        conn.close()
        return result

    def add_entry_for_target(self, target_dict):
        conn = self.get_connection()
        c = conn.cursor()
        t = (target_dict['target_id'],
             target_dict['name'],
             target_dict['url'],
             target_dict['code'],
             int(time.time()),
             target_dict['response_title'])
        query = 'INSERT INTO check_log VALUES (?, ?, ?, ?, ?, ?)'
        c.execute(query, t)
        conn.commit()
        conn.close()
