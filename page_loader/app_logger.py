import logging
import sys

_log_format = "%(asctime)s ~ [%(levelname)s] ~ \
%(filename)s:%(funcName)s(line %(lineno)d) ~ %(message)s"
_log_format_info = "[%(levelname)s]: %(message)s"


class LessThanFilter(logging.Filter):
    def __init__(self, exclusive_maximum, name=""):
        super(LessThanFilter, self).__init__(name)
        self.max_level = exclusive_maximum

    def filter(self, record):
        # non-zero return means we log this message
        return 1 if record.levelno < self.max_level else 0


def get_file_handler():
    file_handler = logging.FileHandler("important.log")
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler


def get_stream_handler_out():
    stream_handler_out = logging.StreamHandler(sys.stdout)
    stream_handler_out.setLevel(logging.INFO)
    stream_handler_out.setFormatter(logging.Formatter(_log_format_info))
    stream_handler_out.addFilter(LessThanFilter(logging.ERROR))
    return stream_handler_out


def get_stream_handler_err():
    stream_handler_err = logging.StreamHandler(sys.stderr)
    stream_handler_err.setLevel(logging.ERROR)
    stream_handler_err.setFormatter(logging.Formatter(_log_format))
    return stream_handler_err


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_stream_handler_err())
    logger.addHandler(get_stream_handler_out())
    return logger
