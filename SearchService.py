"""
This Search service is for querying airbnb's room reservation information.
Before start it, you should first config through the config method.
The implementation of this service is airbnb's public api through api.
"""


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

import datetime
import time
from airbnb.api import Api
import json


class Config:
    def __init__(self, startHour, startMinute, cityList, reportEmail, roomLimit, localStoragePath="", logPath=""):
        """
        constructor of global config
        :param startHour: the hour to start the search service each day
        :param startMinute: the minute to start the search service, use with startHour
        :param cityList: a list of tuple, for querying room information, e.g. [("上海","中国"), ("北京","中国"), ("Lisbon","Portugal")]
        :param reportEmail: the email address to send report to
        :param roomLimit: the max number of rooms returned
        :param localStoragePath: the direct where local storage file will be located in, use ~ if not provided
        """
        self.startHour = startHour
        self.startMinute = startMinute
        self.cityList = cityList
        self.reportEmail = reportEmail
        self.roomLimit = roomLimit
        self.localStoragePath = localStoragePath
        self.logPath = logPath


class SearchService:

    def __init__(self, config):
        self._config = config
        self.totalHomes = 0
        pass

    def start(self):
        while True:
            while True:
                now = datetime.datetime.now()
                if now.hour == self._config.startHour and now.minute == self._config.startMinute:
                    self.doQuery()
                else:
                    time.sleep(50)  # in second

    def doQuery(self):
        now = datetime.datetime.now()
        tomorrow = now + datetime.timedelta(days=1)
        checkin_date = "{0}-{1}-{2}".format(now.year, now.month, now.day)
        checkout_date = "{0}-{1}-{2}".format(tomorrow.year, tomorrow.month, tomorrow.day)
        api = Api(randomize=True)
        for city in self._config.cityList:
            query = "{0}, {1}, {2}".format(city[0], city[1], city[2])
            hasNextPage = True
            startOffset = 0
            while hasNextPage:
                homes = api.get_homes(query=query, checkin=checkin_date, checkout=checkout_date, offset=startOffset, items_per_grid=10)
                pagination = self.retrieveHomeData(query, homes)
                if not pagination:
                    hasNextPage = False
                else:
                    hasNextPage = pagination["has_next_page"]
                    startOffset = pagination.get("items_offset")
        print("total homes is " + str(self.totalHomes))

    def retrieveHomeData(self, query, originReturn):
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
                        print("==> first home id " + str(real_homes[0]["listing"]["id"]))
                        self.totalHomes += len(real_homes)
                        # if not pagination["has_next_page"]:
                        #     index = 0
                        #     for jsonItem in real_homes:
                        #         formatedHomeInfo = json.dumps(jsonItem, indent=4)
                        #         print("+++" + str(index) + formatedHomeInfo)
                        #         index += 1
        else:
            print("explore_tabs is empty")
        return pagination


if __name__ == "__main__":
    cityList = [("上海", "徐汇区", "中国")]
    # config = Config(22, 1, cityList, None, 100, "./rooms.db", "./logs/")
    # service = SearchService(config)
    # service.doQuery()
    import os
    os.system("pwd")
