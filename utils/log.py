import logging
from logging.handlers import RotatingFileHandler

from utils import BASE_DIR

class ReaderLog(object):
    __instance = None
    __loggers = {}

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            logging.basicConfig(filename='%s/logs/reader.log' % BASE_DIR, level=logging.INFO)
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def get_logger(self, name, level, path, max_size, back_count):
        if name not in self.__loggers:
            logger = logging.getLogger(name)
            logger.setLevel(level)
            handler = RotatingFileHandler(path + '/%s.log' % name, maxBytes=max_size, backupCount=back_count)
            formatter = logging.Formatter('[%(levelname)s] - %(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.propagate = False
            self.__loggers[name] = logger
        return self.__loggers[name]



def get_logger(name, level=logging.INFO, path=BASE_DIR + '/logs', max_size = 1024*1024*10, back_count=0):
    if not isinstance(level, int):
        if level.isdigit():
            level = int(level)
        else:
            level = level.upper()
            assert hasattr(logging, level), '输入的日志级别不对，请输入日志的名称或者日志级别的数值'
            level = getattr(logging, level)

    rl = ReaderLog()
    return rl.get_logger(name, level, path, max_size, back_count)