"""
Save the logs to file
"""

import logging
from logging import handlers


class Log:

    _DEFAULT_LOG_PATH = "./unnamed_log.log"
    _echo = False
    _logPath = None
    _logger = None

    @staticmethod
    def config(logPath, echo=False, maxLogSize=1000000):
        Log._echo = echo

        Log._logger = logging.getLogger("Rooms-log")

        log_file = logPath if logPath else Log._DEFAULT_LOG_PATH
        # set the log file to be truncated when reach maxLogSize
        # keep 3 log files at most
        fh = handlers.RotatingFileHandler(filename=log_file, maxBytes=maxLogSize, backupCount=3, encoding="utf-8")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                                      datefmt='%Y/%m/%d %H:%M:%S')

        fh.setFormatter(formatter)
        Log._logger.addHandler(fh)

    @staticmethod
    def d(tag, msg, e=None):
        logMsg = Log._getLogBody(tag, msg, e)
        Log._logger.debug(logMsg)
        if Log._echo:
            print("debug - " + logMsg)

    @staticmethod
    def i(tag, msg, e=None):
        logMsg = Log._getLogBody(tag, msg, e)
        Log._logger.debug(logMsg)
        Log._logger.info(logMsg)
        if Log._echo:
            print("info - " + logMsg)

    @staticmethod
    def w(tag, msg, e=None):
        logMsg = Log._getLogBody(tag, msg, e)
        Log._logger.debug(logMsg)
        Log._logger.warning(logMsg)
        if Log._echo:
            print("warning - " + logMsg)

    @staticmethod
    def e(tag, msg, e=None):
        logMsg = Log._getLogBody(tag, msg, e)
        Log._logger.debug(logMsg)
        Log._logger.error(logMsg)
        if Log._echo:
            print("error - " + logMsg)


    @staticmethod
    def _getLogBody(tag, msg, e=None):
        return "[{0}]:{1}".format(tag, msg) if not e else "[{0}]:{1} Exception: {2}".format(tag, msg, repr(e))

