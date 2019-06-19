"""
Utils method
"""
import datetime


def getQueryStr(cityTuple):
    ret = ""
    length = len(cityTuple)
    for index, item in enumerate(cityTuple):
        ret += str(item)
        if index != length - 1:
            ret += ", "
    return ret


def getDateStr(date=None):
    """
    get given date's string format like 2019-06-01
    if param is not provided, result will be today
    :return:
    """
    if not date:
        date = datetime.datetime.now()
    return '{:%Y-%m-%d}'.format(date)


def getNowTimeStamp():
    """
    get the timestamp in seconds for now.
    :return:
    """
    return int(datetime.datetime.now().timestamp())


def getDeltaTimeStamp(date, deltaInDays):
    """
    calculate the seconds value of the timestamp which specified by date plus delta
    :param date:
    :param deltaInDays:
    :return:
    """
    return int(date.timestamp()) + deltaInDays * 86400


def to_str(s):
    if bytes != str:
        if type(s) == bytes:
            return s.decode('utf-8')
    return s


def to_bytes(s):
    if bytes != str:
        if type(s) == str:
            return s.encode('utf-8')
    return s