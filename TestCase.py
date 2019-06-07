"""
Test cases for storage and search services
"""
from StorageService import StorageService
from Models import RoomInfo
from Utils import *
from LogHelper import Log
import os
from SearchService import SearchService
import sys
from Server import parseConfigFile

def assertTrue(cond):
    if cond:
        print("pass")
    else:
        print("---------- failed ---------")

def assertEqual(left, right):
    if left == right:
        print("pass")
    else:
        print("--------- failed ---------")

def testSaveRoomInfo():
    storage = StorageService("/Users/wiizhang/downloads/test.db")
    roomInfo = RoomInfo(123, 6, "Shanghai", 3, "People's Square", 30.0, "https://z1.muscache.cn/im/pictures/6147f910-b7b4-4e8a-a25f-eed2a30be8a7.jpg?aki_policy=large", getQueryStr(("上海", "徐汇区", "中国")))
    storage.saveOrUpdateSingleRoom(roomInfo)
    ret = storage.getRoomById(123)
    assertEqual(ret.roomId, roomInfo.roomId)
    assertEqual(ret.personCapacity, roomInfo.personCapacity)
    assertEqual(ret.city, roomInfo.city)
    assertEqual(ret.price, roomInfo.price)
    assertEqual(ret.beds, roomInfo.beds)
    assertEqual(ret.neighbourhood, roomInfo.neighbourhood)
    assertEqual(ret.pic, roomInfo.pic)
    assertEqual(ret.query, roomInfo.query)

    roomInfo.neighbourhood = "Nanjing Street"
    roomInfo.price = 55
    queryStr = getQueryStr(("上海", "黄浦区", "中国"))
    roomInfo.query = queryStr
    storage.saveOrUpdateSingleRoom(roomInfo)
    ret = storage.getRoomById(123)
    assertEqual(ret.roomId, roomInfo.roomId)
    assertEqual(ret.personCapacity, roomInfo.personCapacity)
    assertEqual(ret.city, roomInfo.city)
    assertEqual(ret.price, 55)
    assertEqual(ret.beds, roomInfo.beds)
    assertEqual(ret.neighbourhood, "Nanjing Street")
    assertEqual(ret.pic, roomInfo.pic)
    assertEqual(ret.query, queryStr)

    assertTrue(storage.countRoomsForRecentDays(None, "上海", 30) >= 1)

    storage.close()

def testSaveReservation():
    storage = StorageService("/Users/wiizhang/downloads/test.db")
    storage.saveReservationInfo(123)
    assertTrue(storage.isAvailable(123, getDateStr()))
    storage.close()

def testServer():
    configPath = "config_exapmle.json"
    parentPath = os.environ.get('HOME')
    if not parentPath:
        print('can not fetch $HOME')
        parentPath = "."
    parentPath += "/airbnb"
    if not os.path.exists(parentPath):
        os.mkdir(parentPath, mode=0o755)

    logPath = parentPath + "/all_logs.log"
    storagePath = parentPath + "/rooms.db"
    config = parseConfigFile(configPath)
    if not config:
        sys.exit(0)
    config.localStoragePath = storagePath
    # 配置日志模块
    Log.config(logPath, echo=True)
    service = SearchService(config)
    service.doQuery()


if __name__ == "__main__":
    # Log.config("/users/wiizhang/downloads/airbnb_python_logs.log")
    # testSaveRoomInfo()
    # testSaveReservation()
    testServer()
