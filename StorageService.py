"""
This Storage service helps persistent room information given by SearchService.py
Employ a sqlite3 to implement the detail for now.

"""

import sqlite3

class StorageService:

    _DEFAULT_PATH = "./rooms.db"

    def __init__(self, path):
        dbPath = path if path else self._DEFAULT_PATH
        self.prepareDB(dbPath)
        pass

    def prepareDB(self, path):
        print()
