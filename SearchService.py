"""
This Search service is for querying airbnb's room reservation information.
Before start it, you should first config through the config method.
The implementation of this service is airbnb's public api through api.
"""
import time
from airbnb.api import Api
from Utils import *
from Models import RoomInfo
from StorageService import StorageService
from LogHelper import Log
import os
from Report import MailReporter
import xlwt
import zipfile

"""
Typical structure of a home json

{
    "listing": {
        "badges": [],
        "bathroom_label": "2 baths",
        "bathrooms": 2.0,
        "bed_label": "3 beds",
        "bedroom_label": "2 bedrooms",
        "bedrooms": 2,
        "beds": 3,
        "city": "Shanghai",
        "guest_label": "6 guests",
        "host_languages": [
            "zh",
            "en"
        ],
        "host_thumbnail_url_small": "https://a0.muscache.com/im/pictures/278729e6-cb26-421c-a44b-822a17940b42.jpg?aki_policy=profile_small",
        "host_thumbnail_url": "https://a0.muscache.com/im/pictures/278729e6-cb26-421c-a44b-822a17940b42.jpg?aki_policy=profile_x_medium",
        "id": 22786976,
        "is_business_travel_ready": false,
        "is_fully_refundable": false,
        "is_new_listing": false,
        "is_superhost": false,
        "kicker_content": {
            "messages": [
                "Entire condominium",
                "3 beds"
            ],
            "text_color": "#231341"
        },
        "lat": 31.23334,
        "lng": 121.47625,
        "localized_city": "Shanghai",
        "localized_neighborhood": "People's Square",
        "name": "\u6b65\u884c3\u5206\u949f\u5357\u4eac\u8def\u6b65\u884c\u8857|\u4eba\u6c11\u5e7f\u573a\u5730\u94c1\u7ad9\u65c1\u5927\u7a7a\u95f4\u4e24\u5c45|\u5916\u6ee9\u591c\u666f|\u8c6b\u56ed|\u8721\u50cf\u9986",
        "neighborhood": "People's Square",
        "person_capacity": 6,
        "picture_count": 33,
        "picture_url": "https://z1.muscache.cn/im/pictures/6147f910-b7b4-4e8a-a25f-eed2a30be8a7.jpg?aki_policy=large",
        "picture_urls": [
            "https://z1.muscache.cn/im/pictures/6147f910-b7b4-4e8a-a25f-eed2a30be8a7.jpg?aki_policy=large",
            "https://z1.muscache.cn/im/pictures/41f90b6a-6528-451c-96e6-c306a24ad3ca.jpg?aki_policy=large",
            "https://z1.muscache.cn/im/pictures/effb3c44-3963-4c3d-9e87-88bfcff62bc3.jpg?aki_policy=large"
        ],
        "picture": {
            "id": 435630379,
            "dominant_saturated_color": "#6995C7",
            "large_ro": "https://z1.muscache.cn/im/pictures/6147f910-b7b4-4e8a-a25f-eed2a30be8a7.jpg?aki_policy=large_ro",
            "picture": "https://z1.muscache.cn/im/pictures/6147f910-b7b4-4e8a-a25f-eed2a30be8a7.jpg?aki_policy=large",
            "preview_encoded_png": "iVBORw0KGgoAAAANSUhEUgAAAAUAAAADCAIAAADUVFKvAAAAO0lEQVQIHQEwAM//AZCEfAQICRcaHeTe2x0UCQGRl6PKvaiJkJesnJQC+O4BaWVhKiYlKSIczM/SvMLIzBAU+rCh5dcAAAAASUVORK5CYII=",
            "saturated_a11y_dark_color": "#6995C7",
            "scrim_color": "#2F2B28"
        },
        "preview_amenities": "Wifi,Kitchen,Hair dryer,Shampoo",
        "preview_encoded_png": "iVBORw0KGgoAAAANSUhEUgAAAAUAAAADCAIAAADUVFKvAAAAO0lEQVQIHQEwAM//AZCEfAQICRcaHeTe2x0UCQGRl6PKvaiJkJesnJQC+O4BaWVhKiYlKSIczM/SvMLIzBAU+rCh5dcAAAAASUVORK5CYII=",
        "property_type_id": 37,
        "reviews_count": 52,
        "room_and_property_type": "Entire condominium",
        "room_type_category": "entire_home",
        "room_type": "Entire home/apt",
        "scrim_color": "#2F2B28",
        "show_structured_name": false,
        "space_type": "Entire condominium",
        "star_rating": 4.5,
        "tier_id": 0,
        "user": {
            "first_name": " ",
            "has_profile_pic": true,
            "id": 144984297,
            "is_superhost": false,
            "picture_url": "https://a0.muscache.com/im/pictures/278729e6-cb26-421c-a44b-822a17940b42.jpg?aki_policy=profile_x_medium",
            "smart_name": " ",
            "thumbnail_url": "https://a0.muscache.com/im/pictures/278729e6-cb26-421c-a44b-822a17940b42.jpg?aki_policy=profile_small"
        },
        "wide_kicker_content": {
            "messages": [
                "Entire condominium"
            ],
            "text_color": "#9B3143"
        },
        "public_address": "Shanghai, Shanghai Shi, China",
        "amenity_ids": [
            1,
            4,
            45,
            56,
            120
        ],
        "preview_amenity_names": [
            "Wifi",
            "Kitchen",
            "Hair dryer",
            "Shampoo"
        ],
        "reviews": [],
        "star_rating_color": "#008489",
        "preview_tags": [],
        "avg_rating": 4.65,
        "map_highlight_status": "NO_HIGHLIGHT"
    },
    "pricing_quote": {
        "can_instant_book": true,
        "monthly_price_factor": 0.95,
        "price": {
            "localized_title": "Total",
            "price_items": [],
            "total": {
                "amount": 34.0,
                "amount_formatted": "$34",
                "currency": "USD",
                "is_micros_accuracy": false
            }
        },
        "price_string": "From $30 per night",
        "rate": {
            "amount": 30.0,
            "amount_formatted": "$30",
            "currency": "USD",
            "is_micros_accuracy": false
        },
        "rate_type": "nightly",
        "rate_with_service_fee": {
            "amount": 30.0,
            "amount_formatted": "$30",
            "currency": "USD",
            "is_micros_accuracy": false
        },
        "weekly_price_factor": 0.98,
        "should_show_from_label": false
    },
    "verified": {
        "enabled": false,
        "badge_text": "Plus",
        "badge_secondary_text": "Verified",
        "kicker_badge_type": "filled"
    },
    "verified_card": false
}
"""


class Config:
    def __init__(self, startHour, startMinute, cityList, reportEmail, senderEmail, senderEmailPass, roomLimit,
                 localStoragePath="", countingDays=30):
        """
        constructor of global config
        :param startHour: the hour to start the search service each day
        :param startMinute: the minute to start the search service, use with startHour
        :param cityList: a list of tuple, for querying room information, e.g. [("上海","中国"), ("北京","中国"), ("Lisbon","Portugal")]
        :param reportEmail: the email address to send report to
        :param senderEmail: the email address for the report sender
        :param senderEmailPass the password for sender email
        :param roomLimit: the max number of rooms returned
        :param localStoragePath: the direct where local storage file will be located in, use ~ if not provided
        :param use how many days's data to analyze the ratio of reserved rooms
        """
        self.startHour = startHour
        self.startMinute = startMinute
        self.cityList = cityList
        self.reportEmail = reportEmail
        self.senderEmail = senderEmail
        self.senderEmailPasswd = senderEmailPass
        self.roomLimit = roomLimit
        self.localStoragePath = localStoragePath
        self.countingDays = countingDays


class SearchService:
    TAG = "SearchService"

    def __init__(self, config):
        self._config = config
        pass

    def start(self):
        while True:
            while True:
                now = datetime.datetime.now()
                if now.hour == self._config.startHour and now.minute == self._config.startMinute:
                    self.doQuery()
                    time.sleep(60 * 60)
                else:
                    time.sleep(50)  # in second

    def doQuery(self):
        print("===> querying on " + getDateStr())
        now = datetime.datetime.now()
        tomorrow = now + datetime.timedelta(days=1)
        checkin_date = '{:%Y-%m-%d}'.format(now)
        checkout_date = '{:%Y-%m-%d}'.format(tomorrow)
        api = Api(randomize=True)
        storageService = StorageService(self._config.localStoragePath)
        analyzeCollection = []
        forExcel = []
        try:
            for city in self._config.cityList:
                query = getQueryStr(city)
                hasNextPage = True
                startOffset = 0
                homeInfoCollection = []
                while hasNextPage:
                    homes = api.get_homes(query=query, checkin=checkin_date, checkout=checkout_date, offset=startOffset,
                                          items_per_grid=10)
                    pagination = self.retrieveHomeData(query, homes, homeInfoCollection)
                    if not pagination:
                        hasNextPage = False
                    else:
                        hasNextPage = pagination["has_next_page"]
                        startOffset = pagination.get("items_offset")
                if len(homeInfoCollection) > 0:
                    storageService.saveOrUpdateRoomBatch(homeInfoCollection)
                    analyze, excelRet = self.performAnalyze(homeInfoCollection, query, storageService)
                    analyzeCollection.append(analyze)
                    forExcel.append(excelRet)
                else:
                    Log.w(SearchService.TAG, "no data for query={0}".format(query))
        except BaseException as e:
            Log.w(SearchService.TAG, "doQuery() failed, ", e)
        finally:
            storageService.close()
        if len(analyzeCollection) > 0:
            self.reportForAnalyzeResult(analyzeCollection, forExcel)
        else:
            Log.w(SearchService.TAG, "no analyze result generated")

    def retrieveHomeData(self, query, originReturn, homeInfoCollection):
        print("analyzing " + query)
        explore_tabs = originReturn["explore_tabs"]
        pagination = None
        if len(explore_tabs) > 0:
            firstTab = explore_tabs[0]  # dict
            pagination = firstTab["pagination_metadata"]
            if pagination:
                print("has_next_page = " + str(pagination["has_next_page"]))
                print("items_offset = " + str(pagination.get("items_offset")))
                print("section_offset = " + str(pagination.get("section_offset")))
            sections = firstTab.get("sections")
            if sections:
                for item in sections:
                    if item and item["result_type"] == "listings":
                        real_homes = item["listings"]
                        print(str(len(real_homes)) + " rooms for " + query)
                        for roomItem in real_homes:
                            roomInfo = RoomInfo.parseFromDict(roomItem, query)
                            if roomInfo:
                                homeInfoCollection.append(roomInfo)

        else:
            print("explore_tabs is empty")
        return pagination

    def performAnalyze(self, homeInfoCollection, query, storageService):
        count = storageService.countRoomsForRecentDays(query, None, self._config.countingDays)
        reserved = count - len(homeInfoCollection)
        ratio = float(reserved) / float(count) if count > 0 else 0
        ratio = '{:0.2f}'.format(ratio * 100)
        excelRet = list()
        excelRet.append(query)
        excelRet.append(count)
        excelRet.append(reserved)
        excelRet.append(ratio)
        return "{0} - total:{1}, reserved:{2}, reservation ratio:{3}%".format(query, count, reserved, ratio), excelRet

    def reportForAnalyzeResult(self, analyzeCollection, forExcel):
        reporter = MailReporter(self._config.senderEmail, self._config.senderEmailPasswd)
        title = "Airbnb分析日报"
        content = ""
        excel = self.buildExcel(forExcel)
        for item in analyzeCollection:
            content += item
            content += "\r\n"
        receivers = list()
        receivers.append(self._config.reportEmail)
        reporter.send(receivers, title, content, excel)

    def buildExcel(self, value):
        tempXls = "temp/temp.xls"
        tempZip = "temp/result.zip"
        if not os.path.exists("temp"):
            os.mkdir("temp")
        if os.path.exists(tempZip):
            os.remove(tempZip)
        if os.path.exists(tempXls):
            os.remove(tempXls)
        rows = len(value)  # 获取需要写入数据的行数
        workbook = xlwt.Workbook()  # 新建一个工作簿
        sheet = workbook.add_sheet("analyze data")  # 在工作簿中新建一个表格
        # 填表头
        sheet.write(0, 0, "查询地区")
        sheet.write(0, 1, "总房间数")
        sheet.write(0, 2, "今日已预订")
        sheet.write(0, 3, "预订比例")
        for i in range(0, rows):
            for j in range(0, len(value[i])):
                sheet.write(i + 1, j, value[i][j])  # 像表格中写入数据（对应的行和列）
        workbook.save(tempXls)
        with zipfile.ZipFile(tempZip, 'w') as myZip:
            myZip.write(tempXls)
        return tempZip
