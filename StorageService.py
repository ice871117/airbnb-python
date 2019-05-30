"""
This Storage service helps persistent room information given by SearchService.py
Employ a sqlite3 to implement the detail for now.

"""

import sqlite3

class StorageService:

    _DEFAULT_PATH = "./rooms.db"

    def __init__(self, path):
        dbPath = path if path else self._DEFAULT_PATH
        self.storage = self.prepareDB(dbPath)
        pass

    def prepareDB(self, path):
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute("create table if not exist user (id varchar(20) primary key, name varchar(20))")
        return cursor
