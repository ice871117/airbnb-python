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
    def config(logPath, echo=False, maxLogSize=1_000_000):
        _echo = echo

        _logger = logging.getLogger("Rooms-log")

        log_file = logPath if logPath else Log._DEFAULT_LOG_PATH
        # set the log file to be truncated when reach maxLogSize
        # keep 3 log files at most
        fh = handlers.RotatingFileHandler(filename=log_file, maxBytes=maxLogSize, backupCount=3, encoding="utf-8")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',
                                      datefmt='%Y/%m/%d %H:%M:%S')

        fh.setFormatter(formatter)
        _logger.addHandler(fh)

    @staticmethod
    def d(msg):
        Log._logger.debug(msg)
        if Log._echo:
            print("debug - " + msg)

    @staticmethod
    def i(msg):
        Log._logger.info(msg)
        if Log._echo:
            print("info - " + msg)

    @staticmethod
    def w(msg):
        Log._logger.warning(msg)
        if Log._echo:
            print("warning - " + msg)

    @staticmethod
    def e(msg):
        Log._logger.error(msg)
        if Log._echo:
            print("error - " + msg)

