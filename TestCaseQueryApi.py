import datetime
from airbnb.api import Api
import time
import traceback
import random
from Models import RoomInfo


def retrieveHomeData(query, originReturn, collection):
    explore_tabs = originReturn["explore_tabs"]
    pagination = None
    roomNum = 0
    if len(explore_tabs) > 0:
        firstTab = explore_tabs[0]  # dict
        pagination = firstTab["pagination_metadata"]
        # if pagination:
        #     print("has_next_page = " + str(pagination["has_next_page"]))
        #     print("items_offset = " + str(pagination.get("items_offset")))
        #     print("section_offset = " + str(pagination.get("section_offset")))
        sections = firstTab.get("sections")
        if sections:
            for item in sections:
                if item and item["result_type"] == "listings":
                    real_homes = item["listings"]
                    for roomItem in real_homes:
                        roomInfo = RoomInfo.parseFromDict(roomItem, query)
                        collection.append(roomInfo)
                    roomNum = len(real_homes)
    return pagination, roomNum


def doQuery(query, adults):
    now = datetime.datetime.now()
    tomorrow = now + datetime.timedelta(days=1)
    checkin_date = '{:%Y-%m-%d}'.format(now)
    checkout_date = '{:%Y-%m-%d}'.format(tomorrow)
    api = Api(randomize=True)
    collection = []
    try:
        hasNextPage = True
        totalNum = 0
        startOffset = 0
        while hasNextPage:
            homes = api.get_homes(query=query, checkin=checkin_date, checkout=checkout_date, offset=startOffset,
                                  items_per_grid=200, adults=adults)
            pagination, num = retrieveHomeData(query, homes, collection)
            if not pagination:
                hasNextPage = False
            else:
                hasNextPage = pagination["has_next_page"]
                startOffset = pagination.get("items_offset")
            totalNum += num
    except BaseException as e:
        traceback.print_exc()
    time.sleep(2)
    return collection


def calcUnique(querys, adults):
    roomDict = dict()
    for singleQuery in querys:
        for i in adults:
            collection = doQuery(singleQuery, i)
            for item in collection:
                roomDict[item.roomId] = item
    return len(roomDict.keys())


if __name__ == "__main__":
    roomsForShangHai = calcUnique(["上海, 中国"], [1, 2, 3])
    roomsForParts = calcUnique(["上海, 徐汇区, 中国", "上海, 浦东新区, 中国", "上海, 虹口区, 中国", "上海, 宝山区, 中国"], [1, 2, 3])

    print("rooms for shanghai in one query: " + str(roomsForShangHai))
    print("rooms for shanghai in multiple query: " + str(roomsForParts))

    roomsForBejing = calcUnique(["北京, 中国"], [1, 2, 3])
    roomsForParts = calcUnique(["北京, 西城区, 中国", "北京, 海淀区, 中国", "北京, 朝阳区, 中国", "北京, 通州区, 中国"], [1, 2, 3])

    print("rooms for beijing in one query: " + str(roomsForBejing))
    print("rooms for beijing in multiple query: " + str(roomsForParts))
