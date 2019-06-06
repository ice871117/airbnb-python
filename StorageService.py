"""
This Storage service helps persistent room information given by SearchService.py
Employ a sqlite3 to implement the detail for now.

"""

import sqlite3
from Models import RoomInfo
from LogHelper import Log
from Utils import *

class StorageService:

    _DEFAULT_PATH = "./rooms.db"
    _TAG = "StorageService"

    def __init__(self, path):
        dbPath = path if path else self._DEFAULT_PATH
        self._conn = self.prepareDB(dbPath)
        pass

    def prepareDB(self, path):
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        try:
            # table for room
            cursor.execute("CREATE TABLE IF NOT EXISTS room_info (_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                   room_id INTEGER UNIQUE, person_capacity INTEGER, city VARCHAR(20), beds INTEGER, \
                   localized_neighborhood VARCHAR(50), price INTEGER, pic VARCHAR(200), update_time INTEGER,\
                    query_str VARCHAR(100))")
            # table for reservation
            cursor.execute("CREATE TABLE IF NOT EXISTS reservation_info (_id INTEGER PRIMARY KEY AUTOINCREMENT,\
                           room_id INTEGER, date VARCHAR(20) )")
        except BaseException as e:
            Log.e(StorageService._TAG, "prepareDB() failed", e)
        finally:
            cursor.close()
            conn.commit()
        return conn

    def saveOrUpdateSingleRoom(self, singleRoom):
        """
        like saveOrUpdateRoomBatch() but only save or update one Room at a time
        :param singleRoom:
        :return:
        """
        rooms = []
        rooms.append(singleRoom)
        return self.saveOrUpdateRoomBatch(rooms)

    def saveOrUpdateRoomBatch(self, roomInfos):
        """
        save or update information for a given room
        :param roomInfos: a list of RoomInfo
        :return:
        """
        cursor = self._conn.cursor()
        success = True
        try:
            for roomInfo in roomInfos:
                cursor.execute("SELECT room_id FROM room_info WHERE room_id=?", (roomInfo.roomId,))
                if len(cursor.fetchall()) > 0:
                    # exist
                    cursor.execute("UPDATE room_info SET person_capacity=?, city=?, beds=?,\
                             localized_neighborhood=?, price=?, pic=?, update_time=?, query_str=? WHERE room_id=?", (
                                roomInfo.personCapacity, roomInfo.city, roomInfo.beds, roomInfo.neighbourhood,
                                int(roomInfo.price), roomInfo.pic, getNowTimeStamp(), roomInfo.query, roomInfo.roomId))
                else:
                    # new
                    cursor.execute("INSERT INTO room_info (room_id, person_capacity, city, beds, localized_neighborhood, \
                            price, pic, update_time, query_str) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                            roomInfo.roomId, roomInfo.personCapacity, roomInfo.city, roomInfo.beds, roomInfo.neighbourhood,
                            roomInfo.price, roomInfo.pic, getNowTimeStamp(), roomInfo.query))
                success = cursor.rowcount > 0 and success
        except BaseException as e:
            success = False
            Log.w(StorageService._TAG, "saveOrUpdateRoomBatch() failed", e)
        finally:
            cursor.close()
            self._conn.commit()
        return success

    def countRoomsForRecentDays(self, query, days):
        """
        get the number of available individual rooms for recent days
        :param query: the query string
        :param days: the number of days before now
        :return:
        """
        ret = 0
        cursor = self._conn.cursor()
        try:
            cursor.execute("SELECT DISTINCT(room_id) FROM room_info WHERE update_time>? AND query_str=?", (getDeltaTimeStamp(datetime.datetime.now(), -days), query))
            ret = len(cursor.fetchall())
        except BaseException as e:
            Log.w(StorageService._TAG, "countRoomsForRecentDays() failed", e)
        finally:
            cursor.close()
            self._conn.commit()
        return ret


    def saveReservationInfo(self, roomId):
        """
        mark a room as available for today
        :param roomId:
        :return:
        """
        cursor = self._conn.cursor()
        success = False
        try:
            now_date = getDateStr()
            cursor.execute("INSERT INTO reservation_info (room_id, date) VALUES(?, ?)", (roomId, now_date))
            success = cursor.rowcount > 0
        except BaseException as e:
            Log.w(StorageService._TAG, "saveReservationInfo() failed", e)
        finally:
            cursor.close()
            self._conn.commit()
        return success

    def getRoomById(self, roomId):
        """
        query full information for a given roomId
        :param roomId:
        :return: a RoomInfo with given roomId if found, None if not
        """
        cursor = self._conn.cursor()
        ret = None
        try:
            cursor.execute("SELECT room_id, person_capacity, city, beds, localized_neighborhood, \
                        price, pic, query_str FROM room_info WHERE room_id=?", (roomId,))
            values = cursor.fetchall()
            if len(values) > 0:
                ret = RoomInfo(values[0][0], values[0][1], values[0][2], values[0][3], values[0][4], values[0][5], values[0][6], values[0][7])
        except BaseException as e:
            Log.w(StorageService._TAG, "getRoomById() failed", e)
        finally:
            cursor.close()
            self._conn.commit()
        return ret

    def isAvailable(self, roomId, dateStr):
        """
        query whether a room specified by roomId is available on given date
        :param roomId:
        :param dateStr: like 2019-05-30, be sure to use '{:%Y-%m-%d}'.format(datetime)
        :return: True for available that day, False otherwise
        """
        cursor = self._conn.cursor()
        ret = False
        try:
            cursor.execute("SELECT * FROM reservation_info WHERE room_id=? AND date=?", (roomId, dateStr))
            ret = len(cursor.fetchall()) > 0
        except BaseException as e:
            Log.w(StorageService._TAG, "hasReservation() failed", e)
        finally:
            cursor.close()
            self._conn.commit()
        return ret

    def close(self):
        if self._conn:
            self._conn.close()
