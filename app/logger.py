import logging
import sys
from logging import LogRecord
from logging import StreamHandler


class ColorFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    blue = "\x1b[39m"
    yellow = "\x1b[20m"
    red = "\x1b[20m"
    bold_red = "\x1b[1m"
    reset = "\x1b[0m"

    colors = {
        logging.INFO: blue,
        logging.WARNING: yellow,
        logging.ERROR: red,
    }

    def format(self, record: LogRecord):
        color = self.colors.get(record.levelno, self.grey)
        message = super().format(record)
        return color + message + self.reset


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fmt = "%(asctime)s - %(levelname)s - %(message)s"
datefmt = "%m/%d/%Y %I:%M:%S %p"
color_formatter = ColorFormatter(fmt, datefmt)

stream_handler = StreamHandler(sys.stdout)
stream_handler.setFormatter(color_formatter)
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)
