"""
This file contains all the models used by search and storage service
"""
from LogHelper import Log

class RoomInfo:

    TAG = "RoomInfo"

    def __init__(self, roomId=0, personCapacity=0, city=None, beds=0, neighbourhood=None, price=0, pic=None, query=None):
        self.roomId = int(roomId)
        self.personCapacity = int(personCapacity)
        self.city = city
        self.beds = int(beds)
        self.neighbourhood = neighbourhood
        self.price = int(price)
        self.pic = pic
        self.query = query

    @staticmethod
    def parseFromDict(dictFromNet, query):
        ret = RoomInfo()
        try:
            listing = dictFromNet["listing"]
            ret.roomId = int(listing["id"])
            ret.personCapacity = int(listing["person_capacity"])
            ret.neighbourhood = listing.get("neighborhood")
            ret.city = RoomInfo.getCityFromQuery(query, listing.get("city"))
            ret.beds = int(listing["beds"])
            ret.query = query
            ret.pic = listing.get("picture_url")
            pricingQuote = dictFromNet["pricing_quote"]
            ret.price = RoomInfo.getPrice(pricingQuote)
        except BaseException as e:
            Log.w(RoomInfo.TAG, "parseFromDict() failed, ", e)
            ret = None
        return ret

    @staticmethod
    def getPrice(pricingQuote):
        ret = 0
        try:
            ret = int(pricingQuote["price"]["total"]["amount"])
        except BaseException as e:
            pass
        return ret

    @staticmethod
    def getCityFromQuery(query, default):
        splited = query.split(",")
        if len(splited) > 0:
            return splited[0]
        else:
            return default

    def toString(self):
        return "id:{0}, location:{1}, city:{2}, beds:{3}, neighbourhood:{4}, price:{5}, pic:{6}, query{7}".format(self.roomId, self.location, self.city, self.beds, self.neighbourhood, self.price, self.pic, self.query)