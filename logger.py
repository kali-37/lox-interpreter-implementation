import logging
import os
import sys
from logging import FileHandler
from logging import Formatter
from logging import LogRecord
from logging import StreamHandler


class ColorFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    colors = {
        logging.DEBUG: grey,
        logging.INFO: blue,
        logging.WARNING: yellow,
        logging.ERROR: red,
        logging.CRITICAL: bold_red,
    }

    def format(self, record: LogRecord):
        color = self.colors.get(record.levelno, self.grey)
        message = super().format(record)
        return color + message + self.reset


# intialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# formatter
fmt = "%(asctime)s - %(levelname)s - %(message)s"
datefmt = "%m/%d/%Y %I:%M:%S %p"
formatter = Formatter(fmt, datefmt)
color_formatter = ColorFormatter(fmt, datefmt)

# stream handler
stream_handler = StreamHandler(sys.stdout)
stream_handler.setFormatter(color_formatter)
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

# file handler
LOG_DIR_PATH = os.path.join("logs")
os.makedirs(LOG_DIR_PATH, exist_ok=True)
file_handler = FileHandler(os.path.join(LOG_DIR_PATH, "app.log"))
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)

